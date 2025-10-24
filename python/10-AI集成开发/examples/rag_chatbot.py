"""
完整的RAG聊天机器人示例
使用 LangChain + OpenAI + Qdrant

功能：
- 文档摄取和向量化
- 语义搜索
- 上下文增强回答
- 对话历史
- 流式输出

运行方式:
    uv add langchain langchain-openai langchain-community qdrant-client tiktoken
    
    export OPENAI_API_KEY="your-api-key"
    python rag_chatbot.py
"""

from langchain_openai import ChatOpenAI, OpenAIEmbeddings
from langchain.text_splitter import RecursiveCharacterTextSplitter
from langchain.prompts import ChatPromptTemplate, MessagesPlaceholder
from langchain.schema import HumanMessage, AIMessage, SystemMessage
from langchain.schema.runnable import RunnablePassthrough
from langchain_community.vectorstores import Qdrant
from qdrant_client import QdrantClient
from qdrant_client.models import Distance, VectorParams
from typing import List, Dict, Tuple
import asyncio
import os
from datetime import datetime

# ============ 配置 ============

OPENAI_API_KEY = os.getenv("OPENAI_API_KEY", "your-api-key-here")
QDRANT_URL = "http://localhost:6333"  # 本地Qdrant
COLLECTION_NAME = "knowledge_base"

# ============ RAG聊天机器人 ============

class RAGChatbot:
    """RAG聊天机器人"""
    
    def __init__(
        self,
        model_name: str = "gpt-4-turbo",
        temperature: float = 0.7,
        top_k: int = 3
    ):
        """初始化聊天机器人"""
        
        # LLM
        self.llm = ChatOpenAI(
            model=model_name,
            temperature=temperature,
            api_key=OPENAI_API_KEY,
            streaming=True
        )
        
        # 嵌入模型
        self.embeddings = OpenAIEmbeddings(
            model="text-embedding-3-large",
            api_key=OPENAI_API_KEY
        )
        
        # 向量数据库客户端
        try:
            self.qdrant_client = QdrantClient(url=QDRANT_URL)
            self._ensure_collection()
        except Exception as e:
            print(f"⚠️  Warning: Could not connect to Qdrant: {e}")
            print("   Running in-memory mode (documents will not persist)")
            self.qdrant_client = QdrantClient(":memory:")
            self._ensure_collection()
        
        # 向量存储
        self.vector_store = Qdrant(
            client=self.qdrant_client,
            collection_name=COLLECTION_NAME,
            embeddings=self.embeddings
        )
        
        # 文本分割器
        self.text_splitter = RecursiveCharacterTextSplitter(
            chunk_size=1000,
            chunk_overlap=200,
            separators=["\n\n", "\n", "。", "！", "？", ".", "!", "?", " ", ""]
        )
        
        # 对话历史
        self.conversation_history: List[Tuple[str, str]] = []
        
        # 配置
        self.top_k = top_k
        
        print("✓ RAG Chatbot initialized")
    
    def _ensure_collection(self):
        """确保集合存在"""
        try:
            self.qdrant_client.get_collection(COLLECTION_NAME)
            print(f"✓ Using existing collection: {COLLECTION_NAME}")
        except:
            self.qdrant_client.create_collection(
                collection_name=COLLECTION_NAME,
                vectors_config=VectorParams(
                    size=3072,  # text-embedding-3-large dimension
                    distance=Distance.COSINE
                )
            )
            print(f"✓ Created new collection: {COLLECTION_NAME}")
    
    def ingest_documents(self, documents: List[str], metadatas: List[Dict] = None):
        """
        摄取文档
        
        Args:
            documents: 文档文本列表
            metadatas: 文档元数据列表（可选）
        """
        print(f"\n📥 Ingesting {len(documents)} documents...")
        
        # 分割文档
        all_splits = []
        all_metadatas = []
        
        for idx, doc in enumerate(documents):
            splits = self.text_splitter.split_text(doc)
            all_splits.extend(splits)
            
            # 添加元数据
            if metadatas and idx < len(metadatas):
                metadata = metadatas[idx]
            else:
                metadata = {"source": f"document_{idx}"}
            
            metadata["ingested_at"] = datetime.now().isoformat()
            all_metadatas.extend([metadata] * len(splits))
        
        # 添加到向量数据库
        self.vector_store.add_texts(
            texts=all_splits,
            metadatas=all_metadatas
        )
        
        print(f"✓ Ingested {len(all_splits)} chunks")
    
    def search(self, query: str, top_k: int = None) -> List[Dict]:
        """
        搜索相关文档
        
        Args:
            query: 查询文本
            top_k: 返回结果数量
        
        Returns:
            相关文档列表
        """
        if top_k is None:
            top_k = self.top_k
        
        results = self.vector_store.similarity_search_with_score(
            query, k=top_k
        )
        
        formatted_results = []
        for doc, score in results:
            formatted_results.append({
                "content": doc.page_content,
                "metadata": doc.metadata,
                "score": float(score)
            })
        
        return formatted_results
    
    def _build_prompt(self, query: str, context_docs: List[Dict]) -> str:
        """构建提示词"""
        
        # 构建上下文
        context_parts = []
        for idx, doc in enumerate(context_docs, 1):
            context_parts.append(f"[文档 {idx}]\n{doc['content']}\n")
        
        context = "\n".join(context_parts)
        
        # 构建对话历史
        history_text = ""
        if self.conversation_history:
            history_parts = []
            for human_msg, ai_msg in self.conversation_history[-3:]:  # 只保留最近3轮
                history_parts.append(f"用户: {human_msg}")
                history_parts.append(f"助手: {ai_msg}")
            history_text = "\n".join(history_parts)
        
        # 构建完整提示
        prompt = f"""你是一个有帮助的AI助手。请基于以下上下文信息回答用户的问题。

上下文信息：
{context}

"""
        
        if history_text:
            prompt += f"""对话历史：
{history_text}

"""
        
        prompt += f"""当前问题：
{query}

请提供详细且准确的回答。如果上下文中没有相关信息，请诚实地说"我不知道"或"上下文中没有提供足够的信息"。

回答："""
        
        return prompt
    
    async def chat(self, query: str, stream: bool = False) -> str:
        """
        与聊天机器人对话
        
        Args:
            query: 用户问题
            stream: 是否流式输出
        
        Returns:
            AI回答
        """
        print(f"\n💬 User: {query}")
        
        # 1. 检索相关文档
        print(f"🔍 Searching knowledge base...")
        relevant_docs = self.search(query, top_k=self.top_k)
        
        if not relevant_docs:
            response = "抱歉，我的知识库中没有找到相关信息。"
            self.conversation_history.append((query, response))
            print(f"🤖 Assistant: {response}")
            return response
        
        print(f"✓ Found {len(relevant_docs)} relevant documents")
        
        # 2. 构建提示
        prompt = self._build_prompt(query, relevant_docs)
        
        # 3. 生成回答
        if stream:
            print("🤖 Assistant: ", end="", flush=True)
            response_parts = []
            
            async for chunk in self.llm.astream([HumanMessage(content=prompt)]):
                if hasattr(chunk, 'content'):
                    content = chunk.content
                    response_parts.append(content)
                    print(content, end="", flush=True)
            
            print()  # 换行
            response = "".join(response_parts)
        else:
            print("🤖 Assistant: ", end="", flush=True)
            result = await self.llm.ainvoke([HumanMessage(content=prompt)])
            response = result.content
            print(response)
        
        # 4. 保存对话历史
        self.conversation_history.append((query, response))
        
        return response
    
    def clear_history(self):
        """清除对话历史"""
        self.conversation_history = []
        print("✓ Conversation history cleared")
    
    def show_stats(self):
        """显示统计信息"""
        try:
            collection_info = self.qdrant_client.get_collection(COLLECTION_NAME)
            print(f"\n📊 Knowledge Base Stats:")
            print(f"  Total vectors: {collection_info.points_count}")
            print(f"  Conversation turns: {len(self.conversation_history)}")
        except Exception as e:
            print(f"⚠️  Could not get stats: {e}")


# ============ 示例使用 ============

async def main():
    """主函数"""
    
    print("="*60)
    print("🤖 RAG Chatbot Demo")
    print("="*60)
    
    # 初始化聊天机器人
    chatbot = RAGChatbot(
        model_name="gpt-4-turbo",
        temperature=0.7,
        top_k=3
    )
    
    # 示例文档
    sample_documents = [
        """
        Python 3.13的革命性特性
        
        Python 3.13引入了两个革命性特性：Free-Threaded模式和JIT编译器。
        
        Free-Threaded模式（无GIL）：
        - 移除了全局解释器锁（GIL）
        - 允许真正的多线程并行执行
        - 在多核CPU上性能提升2-8倍
        - 特别适合CPU密集型任务
        
        JIT编译器：
        - 即时编译技术
        - 可以将热点代码编译为机器码
        - 纯Python代码性能提升20-60%
        - 无需修改代码即可获得加速
        
        这两个特性标志着Python在高性能计算领域迈出了重要一步。
        """,
        
        """
        现代Python开发工具链（2025）
        
        uv - 超快速包管理器：
        - 使用Rust编写
        - 比pip快10-100倍
        - 统一管理依赖、虚拟环境
        - 支持pyproject.toml
        
        ruff - 极速代码检查器：
        - 比Black快90倍
        - 集成了10+个工具的功能
        - 支持自动修复
        - 配置简单
        
        mypy - 静态类型检查：
        - 捕获类型错误
        - 提高代码质量
        - 支持渐进式类型注解
        
        pytest - 现代测试框架：
        - 简洁的测试语法
        - 丰富的插件生态
        - 支持异步测试
        """,
        
        """
        FastAPI最佳实践（2025）
        
        FastAPI是2025年最受欢迎的Python Web框架。
        
        核心优势：
        1. 高性能：基于ASGI，性能媲美Node.js
        2. 自动文档：生成OpenAPI和Swagger文档
        3. 类型安全：基于Pydantic，100%类型注解
        4. 异步支持：原生支持async/await
        
        最佳实践：
        - 使用依赖注入管理数据库连接
        - 使用Pydantic模型验证数据
        - 使用后台任务处理耗时操作
        - 使用uvicorn作为生产服务器
        - 配置CORS和安全头
        
        性能优化：
        - 使用Redis缓存
        - 使用连接池
        - 启用响应压缩
        - 使用CDN分发静态资源
        """
    ]
    
    # 摄取文档
    chatbot.ingest_documents(
        documents=sample_documents,
        metadatas=[
            {"source": "python_313_features.md", "category": "language"},
            {"source": "modern_toolchain.md", "category": "tools"},
            {"source": "fastapi_best_practices.md", "category": "web"}
        ]
    )
    
    # 显示统计
    chatbot.show_stats()
    
    # 示例对话
    print("\n" + "="*60)
    print("💬 Sample Conversations")
    print("="*60)
    
    # 问题1
    await chatbot.chat(
        "Python 3.13有哪些新特性？性能提升如何？",
        stream=True
    )
    
    # 问题2
    await chatbot.chat(
        "推荐一些现代Python开发工具",
        stream=True
    )
    
    # 问题3（基于上下文的追问）
    await chatbot.chat(
        "uv相比pip有什么优势？",
        stream=True
    )
    
    # 问题4
    await chatbot.chat(
        "使用FastAPI需要注意什么？",
        stream=True
    )
    
    # 问题5（知识库外的问题）
    await chatbot.chat(
        "如何做红烧肉？",
        stream=True
    )
    
    # 显示最终统计
    print("\n" + "="*60)
    chatbot.show_stats()
    print("="*60)
    
    # 交互模式（可选）
    print("\n💡 Tip: You can now ask questions interactively")
    print("   Type 'quit' to exit, 'clear' to clear history\n")
    
    while True:
        try:
            user_input = input("You: ").strip()
            
            if not user_input:
                continue
            
            if user_input.lower() in ['quit', 'exit', 'q']:
                print("👋 Goodbye!")
                break
            
            if user_input.lower() == 'clear':
                chatbot.clear_history()
                continue
            
            if user_input.lower() == 'stats':
                chatbot.show_stats()
                continue
            
            await chatbot.chat(user_input, stream=True)
            
        except KeyboardInterrupt:
            print("\n\n👋 Goodbye!")
            break
        except Exception as e:
            print(f"❌ Error: {e}")


if __name__ == "__main__":
    # 检查API密钥
    if OPENAI_API_KEY == "your-api-key-here":
        print("⚠️  Warning: Please set OPENAI_API_KEY environment variable")
        print("   export OPENAI_API_KEY='your-api-key'")
        exit(1)
    
    # 运行
    asyncio.run(main())

