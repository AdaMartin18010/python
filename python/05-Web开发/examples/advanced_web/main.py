#!/usr/bin/env python3
"""
高级Web开发示例
展示FastAPI的高级功能，包括中间件、依赖注入、WebSocket等
"""

from fastapi import FastAPI, Depends, HTTPException, status, WebSocket, WebSocketDisconnect
from fastapi.middleware.cors import CORSMiddleware
from fastapi.middleware.trustedhost import TrustedHostMiddleware
from fastapi.middleware.gzip import GZipMiddleware
from fastapi.security import HTTPBearer, HTTPAuthorizationCredentials
from fastapi.responses import JSONResponse, HTMLResponse, StreamingResponse
from pydantic import BaseModel, Field, validator
from typing import List, Dict, Any, Optional, AsyncGenerator
from datetime import datetime, timedelta
import asyncio
import json
import logging
import time
import uuid
from contextlib import asynccontextmanager
from jose import JWTError, jwt
from passlib.context import CryptContext
import uvicorn

# 配置日志
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# 配置
SECRET_KEY = "your-secret-key-change-in-production"
ALGORITHM = "HS256"
ACCESS_TOKEN_EXPIRE_MINUTES = 30

# 密码加密
pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")

# 安全方案
security = HTTPBearer()

# 数据模型
class UserBase(BaseModel):
    """用户基础模型"""
    username: str = Field(..., min_length=3, max_length=50)
    email: str = Field(..., regex=r'^[\w\.-]+@[\w\.-]+\.\w+$')
    full_name: Optional[str] = Field(None, max_length=100)
    age: Optional[int] = Field(None, ge=0, le=150)

class UserCreate(UserBase):
    """创建用户模型"""
    password: str = Field(..., min_length=8)

class UserLogin(BaseModel):
    """用户登录模型"""
    username: str
    password: str

class User(UserBase):
    """用户响应模型"""
    id: int
    is_active: bool = True
    created_at: datetime
    
    class Config:
        from_attributes = True

class Token(BaseModel):
    """令牌模型"""
    access_token: str
    token_type: str

class TokenData(BaseModel):
    """令牌数据模型"""
    username: Optional[str] = None

class Message(BaseModel):
    """消息模型"""
    id: str
    content: str
    sender: str
    timestamp: datetime
    room: str = "general"

class ChatRoom(BaseModel):
    """聊天室模型"""
    name: str
    description: Optional[str] = None
    created_by: str
    created_at: datetime
    participants: List[str] = []

class FileUpload(BaseModel):
    """文件上传模型"""
    filename: str
    content_type: str
    size: int
    uploaded_by: str
    uploaded_at: datetime

# 模拟数据库
users_db = []
messages_db = []
chat_rooms_db = []
files_db = []

# 用户ID计数器
user_id_counter = 1

# WebSocket连接管理
class ConnectionManager:
    """WebSocket连接管理器"""
    
    def __init__(self):
        self.active_connections: Dict[str, WebSocket] = {}
        self.room_connections: Dict[str, List[str]] = {}
    
    async def connect(self, websocket: WebSocket, client_id: str):
        """连接WebSocket"""
        await websocket.accept()
        self.active_connections[client_id] = websocket
        logger.info(f"客户端 {client_id} 已连接")
    
    def disconnect(self, client_id: str):
        """断开WebSocket连接"""
        if client_id in self.active_connections:
            del self.active_connections[client_id]
        
        # 从所有房间中移除
        for room, participants in self.room_connections.items():
            if client_id in participants:
                participants.remove(client_id)
        
        logger.info(f"客户端 {client_id} 已断开")
    
    async def send_personal_message(self, message: str, client_id: str):
        """发送个人消息"""
        if client_id in self.active_connections:
            websocket = self.active_connections[client_id]
            await websocket.send_text(message)
    
    async def broadcast_to_room(self, message: str, room: str):
        """向房间广播消息"""
        if room in self.room_connections:
            for client_id in self.room_connections[room]:
                await self.send_personal_message(message, client_id)
    
    async def join_room(self, client_id: str, room: str):
        """加入房间"""
        if room not in self.room_connections:
            self.room_connections[room] = []
        
        if client_id not in self.room_connections[room]:
            self.room_connections[room].append(client_id)
            await self.broadcast_to_room(f"用户 {client_id} 加入了房间 {room}", room)
    
    async def leave_room(self, client_id: str, room: str):
        """离开房间"""
        if room in self.room_connections and client_id in self.room_connections[room]:
            self.room_connections[room].remove(client_id)
            await self.broadcast_to_room(f"用户 {client_id} 离开了房间 {room}", room)

# 创建连接管理器
manager = ConnectionManager()

# 认证相关函数
def verify_password(plain_password: str, hashed_password: str) -> bool:
    """验证密码"""
    return pwd_context.verify(plain_password, hashed_password)

def get_password_hash(password: str) -> str:
    """获取密码哈希"""
    return pwd_context.hash(password)

def create_access_token(data: dict, expires_delta: Optional[timedelta] = None):
    """创建访问令牌"""
    to_encode = data.copy()
    if expires_delta:
        expire = datetime.utcnow() + expires_delta
    else:
        expire = datetime.utcnow() + timedelta(minutes=15)
    
    to_encode.update({"exp": expire})
    encoded_jwt = jwt.encode(to_encode, SECRET_KEY, algorithm=ALGORITHM)
    return encoded_jwt

def verify_token(token: str) -> Optional[str]:
    """验证令牌"""
    try:
        payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
        username: str = payload.get("sub")
        if username is None:
            return None
        return username
    except JWTError:
        return None

# 依赖注入
async def get_current_user(credentials: HTTPAuthorizationCredentials = Depends(security)) -> User:
    """获取当前用户"""
    token = credentials.credentials
    username = verify_token(token)
    
    if username is None:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="无效的认证信息",
            headers={"WWW-Authenticate": "Bearer"},
        )
    
    # 从数据库获取用户
    user = next((u for u in users_db if u.username == username), None)
    if user is None:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="用户不存在",
            headers={"WWW-Authenticate": "Bearer"},
        )
    
    return user

async def get_current_active_user(current_user: User = Depends(get_current_user)) -> User:
    """获取当前活跃用户"""
    if not current_user.is_active:
        raise HTTPException(status_code=400, detail="用户已被禁用")
    return current_user

# 中间件
@asynccontextmanager
async def lifespan(app: FastAPI):
    """应用生命周期管理"""
    # 启动时执行
    logger.info("应用启动")
    
    # 创建默认用户
    if not users_db:
        default_user = User(
            id=1,
            username="admin",
            email="admin@example.com",
            full_name="管理员",
            age=30,
            is_active=True,
            created_at=datetime.now()
        )
        users_db.append(default_user)
        logger.info("创建默认用户: admin")
    
    yield
    
    # 关闭时执行
    logger.info("应用关闭")

# 创建FastAPI应用
app = FastAPI(
    title="高级Web开发示例",
    description="展示FastAPI高级功能的示例应用",
    version="1.0.0",
    lifespan=lifespan
)

# 添加中间件
app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:3000", "https://example.com"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.add_middleware(
    TrustedHostMiddleware,
    allowed_hosts=["localhost", "127.0.0.1", "*.example.com"]
)

app.add_middleware(GZipMiddleware, minimum_size=1000)

# 请求日志中间件
@app.middleware("http")
async def log_requests(request, call_next):
    """请求日志中间件"""
    start_time = time.time()
    
    response = await call_next(request)
    
    process_time = time.time() - start_time
    
    logger.info(
        f"{request.method} {request.url} - {response.status_code} - {process_time:.3f}s"
    )
    
    response.headers["X-Process-Time"] = str(process_time)
    
    return response

# 异常处理器
@app.exception_handler(HTTPException)
async def http_exception_handler(request, exc):
    """HTTP异常处理器"""
    return JSONResponse(
        status_code=exc.status_code,
        content={
            "error": {
                "code": exc.status_code,
                "message": exc.detail,
                "timestamp": datetime.now().isoformat()
            }
        }
    )

# 路由定义
@app.get("/", response_class=HTMLResponse)
async def root():
    """根路径"""
    return """
    <html>
        <head>
            <title>高级Web开发示例</title>
        </head>
        <body>
            <h1>高级Web开发示例</h1>
            <p>这是一个展示FastAPI高级功能的示例应用</p>
            <ul>
                <li><a href="/docs">API文档</a></li>
                <li><a href="/redoc">ReDoc文档</a></li>
                <li><a href="/chat">聊天室</a></li>
            </ul>
        </body>
    </html>
    """

@app.get("/health")
async def health_check():
    """健康检查"""
    return {
        "status": "healthy",
        "timestamp": datetime.now().isoformat(),
        "version": "1.0.0"
    }

# 用户相关路由
@app.post("/auth/register", response_model=User, status_code=201)
async def register(user: UserCreate):
    """用户注册"""
    # 检查用户名是否已存在
    if any(u.username == user.username for u in users_db):
        raise HTTPException(status_code=400, detail="用户名已存在")
    
    # 检查邮箱是否已存在
    if any(u.email == user.email for u in users_db):
        raise HTTPException(status_code=400, detail="邮箱已存在")
    
    # 创建用户
    global user_id_counter
    new_user = User(
        id=user_id_counter,
        username=user.username,
        email=user.email,
        full_name=user.full_name,
        age=user.age,
        is_active=True,
        created_at=datetime.now()
    )
    
    users_db.append(new_user)
    user_id_counter += 1
    
    logger.info(f"新用户注册: {user.username}")
    
    return new_user

@app.post("/auth/login", response_model=Token)
async def login(user_login: UserLogin):
    """用户登录"""
    # 验证用户
    user = next((u for u in users_db if u.username == user_login.username), None)
    
    if not user or not verify_password(user_login.password, "hashed_password"):
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="用户名或密码错误",
            headers={"WWW-Authenticate": "Bearer"},
        )
    
    # 创建访问令牌
    access_token_expires = timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)
    access_token = create_access_token(
        data={"sub": user.username}, expires_delta=access_token_expires
    )
    
    return {"access_token": access_token, "token_type": "bearer"}

@app.get("/users/me", response_model=User)
async def read_users_me(current_user: User = Depends(get_current_active_user)):
    """获取当前用户信息"""
    return current_user

@app.get("/users", response_model=List[User])
async def get_users(skip: int = 0, limit: int = 100):
    """获取用户列表"""
    return users_db[skip:skip + limit]

# 聊天相关路由
@app.get("/chat", response_class=HTMLResponse)
async def chat_page():
    """聊天页面"""
    return """
    <!DOCTYPE html>
    <html>
        <head>
            <title>聊天室</title>
            <style>
                body { font-family: Arial, sans-serif; margin: 20px; }
                #messages { border: 1px solid #ccc; height: 400px; overflow-y: scroll; padding: 10px; }
                #messageInput { width: 70%; padding: 5px; }
                #sendButton { width: 20%; padding: 5px; }
                .message { margin: 5px 0; padding: 5px; border-radius: 5px; }
                .own-message { background-color: #e3f2fd; text-align: right; }
                .other-message { background-color: #f5f5f5; }
            </style>
        </head>
        <body>
            <h1>聊天室</h1>
            <div id="messages"></div>
            <input type="text" id="messageInput" placeholder="输入消息...">
            <button id="sendButton">发送</button>
            
            <script>
                const ws = new WebSocket("ws://localhost:8000/ws/chat");
                const messages = document.getElementById('messages');
                const messageInput = document.getElementById('messageInput');
                const sendButton = document.getElementById('sendButton');
                
                ws.onmessage = function(event) {
                    const message = JSON.parse(event.data);
                    const messageDiv = document.createElement('div');
                    messageDiv.className = 'message';
                    messageDiv.innerHTML = `<strong>${message.sender}:</strong> ${message.content}`;
                    messages.appendChild(messageDiv);
                    messages.scrollTop = messages.scrollHeight;
                };
                
                function sendMessage() {
                    const content = messageInput.value.trim();
                    if (content) {
                        ws.send(JSON.stringify({
                            content: content,
                            room: 'general'
                        }));
                        messageInput.value = '';
                    }
                }
                
                sendButton.onclick = sendMessage;
                messageInput.onkeypress = function(e) {
                    if (e.key === 'Enter') {
                        sendMessage();
                    }
                };
            </script>
        </body>
    </html>
    """

@app.websocket("/ws/chat")
async def websocket_chat(websocket: WebSocket):
    """WebSocket聊天"""
    client_id = str(uuid.uuid4())
    
    await manager.connect(websocket, client_id)
    
    try:
        while True:
            # 接收消息
            data = await websocket.receive_text()
            message_data = json.loads(data)
            
            # 创建消息对象
            message = Message(
                id=str(uuid.uuid4()),
                content=message_data.get('content', ''),
                sender=client_id,
                timestamp=datetime.now(),
                room=message_data.get('room', 'general')
            )
            
            # 保存消息
            messages_db.append(message)
            
            # 广播消息
            await manager.broadcast_to_room(
                json.dumps({
                    'id': message.id,
                    'content': message.content,
                    'sender': message.sender,
                    'timestamp': message.timestamp.isoformat(),
                    'room': message.room
                }),
                message.room
            )
            
    except WebSocketDisconnect:
        manager.disconnect(client_id)

# 文件上传相关路由
@app.post("/upload", response_model=FileUpload)
async def upload_file(current_user: User = Depends(get_current_active_user)):
    """文件上传（模拟）"""
    # 这里应该处理实际的文件上传
    file_info = FileUpload(
        filename="example.txt",
        content_type="text/plain",
        size=1024,
        uploaded_by=current_user.username,
        uploaded_at=datetime.now()
    )
    
    files_db.append(file_info)
    
    return file_info

@app.get("/files", response_model=List[FileUpload])
async def get_files(current_user: User = Depends(get_current_active_user)):
    """获取文件列表"""
    return files_db

# 流式响应示例
@app.get("/stream")
async def stream_data():
    """流式数据响应"""
    async def generate_data():
        for i in range(10):
            yield f"data: {i}\n\n"
            await asyncio.sleep(0.5)
    
    return StreamingResponse(generate_data(), media_type="text/plain")

# 服务器发送事件示例
@app.get("/events")
async def server_sent_events():
    """服务器发送事件"""
    async def event_generator():
        for i in range(10):
            yield f"data: {json.dumps({'id': i, 'message': f'事件 {i}'})}\n\n"
            await asyncio.sleep(1)
    
    return StreamingResponse(
        event_generator(),
        media_type="text/event-stream",
        headers={
            "Cache-Control": "no-cache",
            "Connection": "keep-alive",
        }
    )

# 聊天室管理
@app.post("/rooms", response_model=ChatRoom)
async def create_room(
    name: str,
    description: Optional[str] = None,
    current_user: User = Depends(get_current_active_user)
):
    """创建聊天室"""
    room = ChatRoom(
        name=name,
        description=description,
        created_by=current_user.username,
        created_at=datetime.now(),
        participants=[current_user.username]
    )
    
    chat_rooms_db.append(room)
    
    return room

@app.get("/rooms", response_model=List[ChatRoom])
async def get_rooms():
    """获取聊天室列表"""
    return chat_rooms_db

@app.get("/rooms/{room_name}/messages", response_model=List[Message])
async def get_room_messages(room_name: str, limit: int = 50):
    """获取房间消息"""
    room_messages = [m for m in messages_db if m.room == room_name]
    return room_messages[-limit:]

# 性能测试路由
@app.get("/performance/test")
async def performance_test():
    """性能测试"""
    start_time = time.time()
    
    # 模拟一些计算
    result = sum(i * i for i in range(10000))
    
    end_time = time.time()
    
    return {
        "result": result,
        "execution_time": end_time - start_time,
        "timestamp": datetime.now().isoformat()
    }

# 错误测试路由
@app.get("/error/test")
async def error_test():
    """错误测试"""
    raise HTTPException(status_code=500, detail="这是一个测试错误")

if __name__ == "__main__":
    uvicorn.run(
        "main:app",
        host="0.0.0.0",
        port=8000,
        reload=True,
        log_level="info"
    )
