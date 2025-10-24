# Python AI集成开发完整指南 (2025)

**最后更新：** 2025年10月24日  
**状态：** ✅ 生产就绪

---

## 📋 目录

- [Python AI集成开发完整指南 (2025)](#python-ai集成开发完整指南-2025)
  - [📋 目录](#-目录)
  - [🚀 技术栈概览](#-技术栈概览)
    - [2025年推荐AI技术栈](#2025年推荐ai技术栈)
    - [AI应用架构演进](#ai应用架构演进)
    - [成本对比（2025）](#成本对比2025)
  - [🦜 LangChain 3.0](#-langchain-30)
    - [快速开始](#快速开始)
      - [1. 安装依赖](#1-安装依赖)
      - [2. 基础LLM调用](#2-基础llm调用)
    - [3. LangChain Chains](#3-langchain-chains)
    - [4. LangGraph - 复杂工作流](#4-langgraph---复杂工作流)
  - [🤖 AI Agent开发](#-ai-agent开发)
    - [1. Function Calling Agent](#1-function-calling-agent)
    - [2. AutoGPT风格Agent](#2-autogpt风格agent)
  - [🗂️ 向量数据库](#️-向量数据库)
    - [Qdrant集成](#qdrant集成)
  - [📝 RAG系统](#-rag系统)
    - [完整RAG实现](#完整rag实现)
  - [📊 AI监控与评估](#-ai监控与评估)
    - [LangSmith集成](#langsmith集成)
    - [性能评估](#性能评估)
  - [💡 生产最佳实践](#-生产最佳实践)
    - [1. 错误处理与重试](#1-错误处理与重试)
    - [2. 成本控制](#2-成本控制)
    - [3. 缓存策略](#3-缓存策略)
  - [📚 参考资源](#-参考资源)
    - [官方文档](#官方文档)
    - [学习资源](#学习资源)

---

## 🚀 技术栈概览

### 2025年推荐AI技术栈

| 类别 | 工具 | 版本 | 用途 |
|------|------|------|------|
| **框架** | LangChain | 3.0+ | AI应用开发框架 |
| **AI Agent** | AutoGPT | 2025+ | 自主AI代理 |
| **LLM** | OpenAI GPT-4/GPT-5 | - | 大语言模型 |
| **本地LLM** | Ollama | 0.5+ | 本地模型运行 |
| **嵌入模型** | OpenAI Embeddings | text-embedding-3 | 文本向量化 |
| **向量数据库** | Qdrant | 1.12+ | 向量存储和搜索 |
| **向量数据库** | Weaviate | 1.27+ | AI原生向量数据库 |
| **深度学习** | PyTorch | 2.5+ | 模型训练 |
| **推理服务** | vLLM | 0.6+ | 高性能推理 |
| **模型量化** | BitsAndBytes | 0.44+ | 模型压缩 |
| **监控** | LangSmith | - | LangChain监控 |

### AI应用架构演进

```text
传统架构              →  2024架构           →  2025架构
──────────────────────────────────────────────────────────────
规则引擎              →  LLM调用          →  Multi-Agent系统
固定流程              →  Prompt工程       →  自主规划
本地数据              →  RAG检索          →  知识图谱融合
单模型                →  模型组合         →  模型微调+工具调用
后端批处理            →  实时推理         →  流式输出+并行推理
```

### 成本对比（2025）

| 模型 | 每百万Token成本 | 速度 | 质量 | 适用场景 |
|------|----------------|------|------|---------|
| **GPT-4 Turbo** | $10 | 中等 | 最高 | 复杂推理、创作 |
| **GPT-3.5 Turbo** | $0.5 | 快 | 高 | 通用对话、分类 |
| **Claude 3.5** | $8 | 快 | 最高 | 长文本、代码 |
| **Llama 3.3 (8B)** | 免费（自托管） | 快 | 中高 | 本地部署 |
| **Mistral 7B** | 免费（自托管） | 极快 | 中 | 轻量任务 |

---

## 🦜 LangChain 3.0

### 快速开始

#### 1. 安装依赖

```bash
# 使用uv安装（推荐）
uv add langchain==3.0.0
uv add langchain-openai==3.0.0
uv add langchain-community==3.0.0
uv add langgraph==2.0.0
uv add langsmith==0.5.0

# 或使用pip
pip install langchain==3.0.0 langchain-openai langchain-community
```

#### 2. 基础LLM调用

```python
# app/ai/llm_basic.py
from langchain_openai import ChatOpenAI
from langchain.schema import HumanMessage, SystemMessage
from typing import List
import os

# 配置API密钥
os.environ["OPENAI_API_KEY"] = "your-api-key-here"

class LLMService:
    """LLM服务封装"""
    
    def __init__(self, model: str = "gpt-4-turbo", temperature: float = 0.7):
        self.llm = ChatOpenAI(
            model=model,
            temperature=temperature,
            max_tokens=2000,
            timeout=30,
            max_retries=3
        )
    
    async def chat(self, messages: List[dict]) -> str:
        """异步聊天"""
        # 转换消息格式
        langchain_messages = [
            SystemMessage(content=msg["content"]) if msg["role"] == "system"
            else HumanMessage(content=msg["content"])
            for msg in messages
        ]
        
        # 调用LLM
        response = await self.llm.ainvoke(langchain_messages)
        return response.content
    
    async def stream_chat(self, messages: List[dict]):
        """流式输出"""
        langchain_messages = [
            SystemMessage(content=msg["content"]) if msg["role"] == "system"
            else HumanMessage(content=msg["content"])
            for msg in messages
        ]
        
        # 流式调用
        async for chunk in self.llm.astream(langchain_messages):
            if hasattr(chunk, 'content'):
                yield chunk.content


# FastAPI集成
from fastapi import FastAPI, HTTPException
from fastapi.responses import StreamingResponse
from pydantic import BaseModel

app = FastAPI()
llm_service = LLMService()

class ChatRequest(BaseModel):
    messages: List[dict]

@app.post("/api/chat")
async def chat(request: ChatRequest):
    """聊天接口"""
    try:
        response = await llm_service.chat(request.messages)
        return {"response": response}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@app.post("/api/chat/stream")
async def chat_stream(request: ChatRequest):
    """流式聊天接口"""
    async def generate():
        try:
            async for chunk in llm_service.stream_chat(request.messages):
                yield f"data: {chunk}\n\n"
        except Exception as e:
            yield f"data: [ERROR] {str(e)}\n\n"
    
    return StreamingResponse(generate(), media_type="text/event-stream")
```

### 3. LangChain Chains

```python
# app/ai/chains.py
from langchain.chains import LLMChain
from langchain.prompts import PromptTemplate
from langchain_openai import ChatOpenAI

class ContentGenerator:
    """内容生成器（使用Chain）"""
    
    def __init__(self):
        self.llm = ChatOpenAI(model="gpt-4-turbo", temperature=0.9)
        
        # 定义Prompt模板
        self.blog_template = PromptTemplate(
            input_variables=["topic", "tone", "length"],
            template="""
你是一位专业的内容创作者。请根据以下要求撰写一篇博客文章：

主题：{topic}
语气：{tone}
长度：{length}字

要求：
1. 结构清晰，分段合理
2. 语言生动，引人入胜
3. 包含具体案例或数据支撑
4. 以行动号召结尾

开始创作：
"""
        )
        
        # 创建Chain
        self.blog_chain = LLMChain(
            llm=self.llm,
            prompt=self.blog_template
        )
    
    async def generate_blog(self, topic: str, tone: str = "专业", length: int = 1000) -> str:
        """生成博客文章"""
        result = await self.blog_chain.ainvoke({
            "topic": topic,
            "tone": tone,
            "length": length
        })
        return result["text"]


# 使用示例
generator = ContentGenerator()
blog = await generator.generate_blog(
    topic="Python 3.13的革命性特性",
    tone="专业且易懂",
    length=1500
)
```

### 4. LangGraph - 复杂工作流

```python
# app/ai/workflows.py
from langgraph.graph import StateGraph, END
from typing import TypedDict, Annotated, Sequence
from langchain_openai import ChatOpenAI
from langchain.schema import HumanMessage, AIMessage
import operator

# 定义状态
class AgentState(TypedDict):
    """Agent状态"""
    messages: Annotated[Sequence[HumanMessage | AIMessage], operator.add]
    next: str

# 创建工作流
workflow = StateGraph(AgentState)

# 定义节点
async def research_node(state: AgentState) -> AgentState:
    """研究节点"""
    llm = ChatOpenAI(model="gpt-4-turbo")
    
    # 执行研究
    research_prompt = HumanMessage(
        content=f"请对以下主题进行深入研究：{state['messages'][-1].content}"
    )
    response = await llm.ainvoke([research_prompt])
    
    return {
        "messages": [response],
        "next": "analyze"
    }

async def analyze_node(state: AgentState) -> AgentState:
    """分析节点"""
    llm = ChatOpenAI(model="gpt-4-turbo")
    
    # 分析研究结果
    analyze_prompt = HumanMessage(
        content=f"请分析以下研究结果并提取关键见解：{state['messages'][-1].content}"
    )
    response = await llm.ainvoke([analyze_prompt])
    
    return {
        "messages": [response],
        "next": "report"
    }

async def report_node(state: AgentState) -> AgentState:
    """报告节点"""
    llm = ChatOpenAI(model="gpt-4-turbo")
    
    # 生成报告
    report_prompt = HumanMessage(
        content=f"基于以下分析，生成一份结构化报告：{state['messages'][-1].content}"
    )
    response = await llm.ainvoke([report_prompt])
    
    return {
        "messages": [response],
        "next": END
    }

# 添加节点
workflow.add_node("research", research_node)
workflow.add_node("analyze", analyze_node)
workflow.add_node("report", report_node)

# 定义边
workflow.set_entry_point("research")
workflow.add_edge("research", "analyze")
workflow.add_edge("analyze", "report")
workflow.add_edge("report", END)

# 编译工作流
app = workflow.compile()

# 使用示例
async def run_research_workflow(topic: str) -> str:
    """运行研究工作流"""
    initial_state = {
        "messages": [HumanMessage(content=topic)],
        "next": "research"
    }
    
    result = await app.ainvoke(initial_state)
    return result["messages"][-1].content
```

---

## 🤖 AI Agent开发

### 1. Function Calling Agent

```python
# app/ai/agents/function_calling.py
from langchain_openai import ChatOpenAI
from langchain.tools import tool
from langchain.agents import create_openai_functions_agent, AgentExecutor
from langchain.prompts import ChatPromptTemplate, MessagesPlaceholder
from typing import List, Dict

# 定义工具
@tool
def search_database(query: str) -> str:
    """搜索数据库获取信息
    
    Args:
        query: 搜索查询
    """
    # 实际的数据库查询逻辑
    return f"数据库查询结果：{query}"

@tool
def calculate(expression: str) -> float:
    """计算数学表达式
    
    Args:
        expression: 数学表达式，如 "2 + 2"
    """
    try:
        return eval(expression)
    except Exception as e:
        return f"计算错误：{str(e)}"

@tool
def send_email(to: str, subject: str, body: str) -> str:
    """发送电子邮件
    
    Args:
        to: 收件人邮箱
        subject: 邮件主题
        body: 邮件正文
    """
    # 实际的邮件发送逻辑
    return f"邮件已发送至 {to}"


class FunctionCallingAgent:
    """函数调用Agent"""
    
    def __init__(self):
        # 初始化LLM
        self.llm = ChatOpenAI(
            model="gpt-4-turbo",
            temperature=0
        )
        
        # 定义工具列表
        self.tools = [search_database, calculate, send_email]
        
        # 定义Prompt
        self.prompt = ChatPromptTemplate.from_messages([
            ("system", """你是一个智能助手，可以使用以下工具来帮助用户：
            
1. search_database - 搜索数据库
2. calculate - 计算数学表达式
3. send_email - 发送邮件

请根据用户的请求，选择合适的工具并执行。"""),
            MessagesPlaceholder(variable_name="chat_history", optional=True),
            ("human", "{input}"),
            MessagesPlaceholder(variable_name="agent_scratchpad"),
        ])
        
        # 创建Agent
        agent = create_openai_functions_agent(
            llm=self.llm,
            tools=self.tools,
            prompt=self.prompt
        )
        
        # 创建Executor
        self.agent_executor = AgentExecutor(
            agent=agent,
            tools=self.tools,
            verbose=True,
            max_iterations=5
        )
    
    async def run(self, user_input: str, chat_history: List[Dict] = None) -> str:
        """运行Agent"""
        result = await self.agent_executor.ainvoke({
            "input": user_input,
            "chat_history": chat_history or []
        })
        return result["output"]


# 使用示例
agent = FunctionCallingAgent()

# 简单查询
response = await agent.run("帮我查询user_123的订单信息")
# Agent会自动调用 search_database("user_123的订单")

# 复杂任务
response = await agent.run("""
请执行以下任务：
1. 查询user_456的总订单金额
2. 计算折扣后的金额（打8折）
3. 发送邮件给user_456@example.com，主题是"您的订单总额"
""")
# Agent会自动拆解任务并依次调用工具
```

### 2. AutoGPT风格Agent

```python
# app/ai/agents/autogpt.py
from typing import List, Dict, Optional
from langchain_openai import ChatOpenAI
from langchain.schema import HumanMessage, AIMessage, SystemMessage
import json

class AutoGPTAgent:
    """AutoGPT风格的自主Agent"""
    
    def __init__(self, goal: str):
        self.goal = goal
        self.llm = ChatOpenAI(model="gpt-4-turbo", temperature=0.7)
        self.thoughts: List[str] = []
        self.actions: List[Dict] = []
        self.max_iterations = 10
    
    async def run(self) -> str:
        """运行Agent直到完成目标"""
        system_prompt = f"""
你是一个自主AI代理。你的目标是：{self.goal}

你需要：
1. 分析当前状态
2. 规划下一步行动
3. 执行行动
4. 评估结果
5. 决定是否继续或完成

请以JSON格式输出你的思考和行动：
{{
    "thought": "你的思考过程",
    "action": "下一步行动",
    "action_type": "search|calculate|complete",
    "action_input": "行动的输入",
    "reasoning": "选择该行动的理由"
}}
"""
        
        messages = [SystemMessage(content=system_prompt)]
        
        for iteration in range(self.max_iterations):
            # Agent思考
            response = await self.llm.ainvoke(messages)
            
            try:
                decision = json.loads(response.content)
            except json.JSONDecodeError:
                continue
            
            # 记录思考
            self.thoughts.append(decision["thought"])
            
            # 执行行动
            if decision["action_type"] == "complete":
                return decision["action_input"]
            
            action_result = await self._execute_action(
                decision["action_type"],
                decision["action_input"]
            )
            
            # 记录行动
            self.actions.append({
                "iteration": iteration,
                "action": decision["action"],
                "result": action_result
            })
            
            # 添加结果到对话历史
            messages.append(AIMessage(content=response.content))
            messages.append(HumanMessage(
                content=f"行动结果：{action_result}\n\n继续下一步。"
            ))
        
        return "达到最大迭代次数，任务未完成。"
    
    async def _execute_action(self, action_type: str, action_input: str) -> str:
        """执行具体行动"""
        if action_type == "search":
            # 实际的搜索逻辑
            return f"搜索结果：{action_input}"
        elif action_type == "calculate":
            try:
                return str(eval(action_input))
            except Exception as e:
                return f"计算错误：{str(e)}"
        return "未知行动类型"


# 使用示例
agent = AutoGPTAgent(goal="研究Python 3.13的新特性并生成总结报告")
result = await agent.run()
print(result)
```

---

## 🗂️ 向量数据库

### Qdrant集成

```python
# app/ai/vector_store.py
from qdrant_client import QdrantClient
from qdrant_client.models import Distance, VectorParams, PointStruct
from langchain_openai import OpenAIEmbeddings
from typing import List, Dict
import uuid

class VectorStore:
    """向量数据库管理"""
    
    def __init__(self, collection_name: str = "documents"):
        # 连接Qdrant
        self.client = QdrantClient(host="localhost", port=6333)
        self.collection_name = collection_name
        
        # 初始化嵌入模型
        self.embeddings = OpenAIEmbeddings(
            model="text-embedding-3-large",
            dimensions=1536
        )
        
        # 创建集合
        self._create_collection()
    
    def _create_collection(self):
        """创建向量集合"""
        try:
            self.client.get_collection(self.collection_name)
        except:
            self.client.create_collection(
                collection_name=self.collection_name,
                vectors_config=VectorParams(
                    size=1536,
                    distance=Distance.COSINE
                )
            )
    
    async def add_documents(self, documents: List[Dict]) -> None:
        """添加文档"""
        points = []
        
        for doc in documents:
            # 生成嵌入向量
            vector = await self.embeddings.aembed_query(doc["text"])
            
            # 创建点
            point = PointStruct(
                id=str(uuid.uuid4()),
                vector=vector,
                payload={
                    "text": doc["text"],
                    "metadata": doc.get("metadata", {})
                }
            )
            points.append(point)
        
        # 批量插入
        self.client.upsert(
            collection_name=self.collection_name,
            points=points
        )
    
    async def search(self, query: str, limit: int = 5) -> List[Dict]:
        """搜索相似文档"""
        # 生成查询向量
        query_vector = await self.embeddings.aembed_query(query)
        
        # 搜索
        results = self.client.search(
            collection_name=self.collection_name,
            query_vector=query_vector,
            limit=limit
        )
        
        return [
            {
                "text": hit.payload["text"],
                "metadata": hit.payload["metadata"],
                "score": hit.score
            }
            for hit in results
        ]
    
    def delete_collection(self) -> None:
        """删除集合"""
        self.client.delete_collection(self.collection_name)


# 使用示例
vector_store = VectorStore(collection_name="knowledge_base")

# 添加文档
await vector_store.add_documents([
    {
        "text": "Python 3.13引入了Free-Threaded模式...",
        "metadata": {"source": "docs", "category": "python"}
    },
    {
        "text": "JIT编译器可以显著提升性能...",
        "metadata": {"source": "docs", "category": "performance"}
    }
])

# 搜索
results = await vector_store.search("Python性能优化", limit=3)
for result in results:
    print(f"相关度：{result['score']:.2f}")
    print(f"内容：{result['text']}")
```

---

## 📝 RAG系统

### 完整RAG实现

```python
# app/ai/rag_system.py
from langchain_openai import ChatOpenAI, OpenAIEmbeddings
from langchain.text_splitter import RecursiveCharacterTextSplitter
from langchain.chains import RetrievalQA
from langchain.prompts import PromptTemplate
from typing import List
import asyncio

class RAGSystem:
    """检索增强生成系统"""
    
    def __init__(self, vector_store: VectorStore):
        self.vector_store = vector_store
        self.llm = ChatOpenAI(model="gpt-4-turbo", temperature=0)
        
        # 定义RAG Prompt
        self.rag_prompt = PromptTemplate(
            input_variables=["context", "question"],
            template="""
基于以下上下文信息回答问题。如果上下文中没有相关信息，请诚实地说"我不知道"。

上下文：
{context}

问题：{question}

详细回答：
"""
        )
    
    async def ingest_documents(self, documents: List[str]) -> None:
        """摄取文档"""
        # 文本分割
        text_splitter = RecursiveCharacterTextSplitter(
            chunk_size=1000,
            chunk_overlap=200,
            separators=["\n\n", "\n", "。", "！", "？", ".", "!", "?", " ", ""]
        )
        
        chunks = []
        for doc in documents:
            splits = text_splitter.split_text(doc)
            chunks.extend([
                {"text": split, "metadata": {"source": "upload"}}
                for split in splits
            ])
        
        # 存入向量数据库
        await self.vector_store.add_documents(chunks)
    
    async def query(self, question: str, top_k: int = 3) -> Dict:
        """查询RAG系统"""
        # 1. 检索相关文档
        relevant_docs = await self.vector_store.search(question, limit=top_k)
        
        # 2. 构建上下文
        context = "\n\n".join([
            f"[文档{i+1}] {doc['text']}"
            for i, doc in enumerate(relevant_docs)
        ])
        
        # 3. 生成回答
        prompt = self.rag_prompt.format(context=context, question=question)
        response = await self.llm.ainvoke([HumanMessage(content=prompt)])
        
        return {
            "answer": response.content,
            "sources": relevant_docs,
            "context_length": len(context)
        }


# FastAPI集成
from fastapi import FastAPI, UploadFile, File
from pydantic import BaseModel

app = FastAPI()
vector_store = VectorStore(collection_name="rag_kb")
rag_system = RAGSystem(vector_store)

class QueryRequest(BaseModel):
    question: str
    top_k: int = 3

@app.post("/api/rag/ingest")
async def ingest_document(file: UploadFile = File(...)):
    """上传并摄取文档"""
    content = await file.read()
    text = content.decode("utf-8")
    
    await rag_system.ingest_documents([text])
    
    return {"message": "Document ingested successfully"}

@app.post("/api/rag/query")
async def query_rag(request: QueryRequest):
    """查询RAG系统"""
    result = await rag_system.query(request.question, request.top_k)
    return result
```

---

## 📊 AI监控与评估

### LangSmith集成

```python
# app/ai/monitoring.py
from langsmith import Client
from langchain.callbacks.tracers import LangChainTracer
import os

# 配置LangSmith
os.environ["LANGCHAIN_TRACING_V2"] = "true"
os.environ["LANGCHAIN_ENDPOINT"] = "https://api.smith.langchain.com"
os.environ["LANGCHAIN_API_KEY"] = "your-api-key"
os.environ["LANGCHAIN_PROJECT"] = "production"

# 创建Tracer
tracer = LangChainTracer(project_name="production")

# 在LLM调用中使用
async def monitored_chat(messages: List[dict]) -> str:
    """带监控的聊天"""
    llm = ChatOpenAI(
        model="gpt-4-turbo",
        callbacks=[tracer]  # 添加监控
    )
    
    response = await llm.ainvoke(messages)
    return response.content
```

### 性能评估

```python
# app/ai/evaluation.py
from typing import List, Dict
import asyncio

class AIEvaluator:
    """AI系统评估"""
    
    @staticmethod
    async def evaluate_rag_quality(
        test_cases: List[Dict],
        rag_system: RAGSystem
    ) -> Dict:
        """评估RAG质量"""
        results = {
            "total": len(test_cases),
            "passed": 0,
            "failed": 0,
            "average_score": 0.0
        }
        
        scores = []
        
        for case in test_cases:
            question = case["question"]
            expected_answer = case["expected_answer"]
            
            # 获取RAG回答
            result = await rag_system.query(question)
            actual_answer = result["answer"]
            
            # 评估相似度（使用LLM作为评判）
            score = await AIEvaluator._evaluate_answer_similarity(
                expected_answer,
                actual_answer
            )
            
            scores.append(score)
            
            if score >= 0.7:
                results["passed"] += 1
            else:
                results["failed"] += 1
        
        results["average_score"] = sum(scores) / len(scores)
        
        return results
    
    @staticmethod
    async def _evaluate_answer_similarity(
        expected: str,
        actual: str
    ) -> float:
        """评估回答相似度"""
        llm = ChatOpenAI(model="gpt-4-turbo", temperature=0)
        
        prompt = f"""
请评估以下两个回答的相似度（0-1之间的分数）：

期望回答：{expected}

实际回答：{actual}

只返回数字分数，不需要解释。
"""
        
        response = await llm.ainvoke([HumanMessage(content=prompt)])
        
        try:
            return float(response.content.strip())
        except ValueError:
            return 0.0
```

---

## 💡 生产最佳实践

### 1. 错误处理与重试

```python
# app/ai/resilience.py
from tenacity import retry, stop_after_attempt, wait_exponential
from functools import wraps
import logging

logger = logging.getLogger(__name__)

@retry(
    stop=stop_after_attempt(3),
    wait=wait_exponential(multiplier=1, min=4, max=10),
    reraise=True
)
async def resilient_llm_call(llm, messages):
    """带重试的LLM调用"""
    try:
        return await llm.ainvoke(messages)
    except Exception as e:
        logger.error(f"LLM call failed: {str(e)}")
        raise

# 降级策略
async def llm_with_fallback(primary_llm, fallback_llm, messages):
    """LLM降级策略"""
    try:
        return await resilient_llm_call(primary_llm, messages)
    except Exception as e:
        logger.warning(f"Primary LLM failed, using fallback: {str(e)}")
        return await fallback_llm.ainvoke(messages)
```

### 2. 成本控制

```python
# app/ai/cost_control.py
from typing import Dict
import tiktoken

class CostController:
    """成本控制器"""
    
    # 2025年定价（每百万Token）
    PRICING = {
        "gpt-4-turbo": {"input": 10.0, "output": 30.0},
        "gpt-3.5-turbo": {"input": 0.5, "output": 1.5},
        "claude-3.5": {"input": 8.0, "output": 24.0}
    }
    
    def __init__(self, budget_limit: float):
        self.budget_limit = budget_limit
        self.total_cost = 0.0
        self.encoding = tiktoken.encoding_for_model("gpt-4")
    
    def calculate_cost(
        self,
        model: str,
        input_text: str,
        output_text: str
    ) -> float:
        """计算调用成本"""
        input_tokens = len(self.encoding.encode(input_text))
        output_tokens = len(self.encoding.encode(output_text))
        
        pricing = self.PRICING.get(model, {"input": 10.0, "output": 30.0})
        
        cost = (
            (input_tokens / 1_000_000) * pricing["input"] +
            (output_tokens / 1_000_000) * pricing["output"]
        )
        
        return cost
    
    def check_budget(self, estimated_cost: float) -> bool:
        """检查预算"""
        return (self.total_cost + estimated_cost) <= self.budget_limit
    
    def record_cost(self, cost: float) -> None:
        """记录成本"""
        self.total_cost += cost
```

### 3. 缓存策略

```python
# app/ai/caching.py
from functools import wraps
import hashlib
import json

def cache_llm_response(ttl: int = 3600):
    """缓存LLM响应"""
    def decorator(func):
        @wraps(func)
        async def wrapper(*args, **kwargs):
            # 生成缓存键
            cache_key = hashlib.md5(
                json.dumps([args, kwargs], sort_keys=True).encode()
            ).hexdigest()
            
            # 尝试从缓存获取
            cached = await redis_cache.get(f"llm:{cache_key}")
            if cached:
                return cached
            
            # 调用LLM
            result = await func(*args, **kwargs)
            
            # 存入缓存
            await redis_cache.set(f"llm:{cache_key}", result, ttl)
            
            return result
        return wrapper
    return decorator
```

---

## 📚 参考资源

### 官方文档

- **LangChain**: <https://python.langchain.com/>
- **LangSmith**: <https://docs.smith.langchain.com/>
- **OpenAI**: <https://platform.openai.com/docs/>
- **Qdrant**: <https://qdrant.tech/documentation/>

### 学习资源

- [LangChain Cookbook](https://github.com/langchain-ai/langchain/tree/master/cookbook)
- [RAG从入门到精通](https://www.deeplearning.ai/short-courses/building-applications-vector-databases/)
- [Prompt Engineering Guide](https://www.promptingguide.ai/)

---

**更新日期：** 2025年10月24日  
**维护者：** Python Knowledge Base Team  
**返回目录：** [../README.md](../README.md)
