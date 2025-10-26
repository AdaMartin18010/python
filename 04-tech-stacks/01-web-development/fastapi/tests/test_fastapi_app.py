"""
FastAPI - 完整测试套件

测试覆盖率目标: 90%+

包含：
1. 认证测试
2. 用户CRUD测试
3. 商品CRUD测试
4. 权限测试
5. 异常处理测试
"""

import pytest
from httpx import AsyncClient
from sqlalchemy.ext.asyncio import AsyncSession, create_async_engine, async_sessionmaker
from sqlalchemy.pool import StaticPool

import sys
from pathlib import Path
sys.path.insert(0, str(Path(__file__).parent.parent))

from fastapi_app import (
    app,
    Base,
    get_db,
    User,
    Item,
    UserCreate,
    ItemCreate,
    get_password_hash
)

# 测试数据库配置
TEST_DATABASE_URL = "sqlite+aiosqlite:///:memory:"

engine = create_async_engine(
    TEST_DATABASE_URL,
    connect_args={"check_same_thread": False},
    poolclass=StaticPool,
)

TestingSessionLocal = async_sessionmaker(
    engine, class_=AsyncSession, expire_on_commit=False
)


async def override_get_db():
    """覆盖数据库依赖"""
    async with TestingSessionLocal() as session:
        yield session


app.dependency_overrides[get_db] = override_get_db


@pytest.fixture
async def client():
    """异步测试客户端"""
    async with AsyncClient(app=app, base_url="http://test") as ac:
        # 创建表
        async with engine.begin() as conn:
            await conn.run_sync(Base.metadata.create_all)
        
        yield ac
        
        # 清理
        async with engine.begin() as conn:
            await conn.run_sync(Base.metadata.drop_all)


@pytest.fixture
async def test_user(client: AsyncClient):
    """创建测试用户"""
    response = await client.post(
        "/register",
        json={
            "username": "testuser",
            "email": "test@example.com",
            "password": "password123"
        }
    )
    assert response.status_code == 200
    return response.json()["data"]


@pytest.fixture
async def auth_token(client: AsyncClient, test_user):
    """获取认证令牌"""
    response = await client.post(
        "/token",
        data={"username": "testuser", "password": "password123"}
    )
    assert response.status_code == 200
    return response.json()["access_token"]


# ============================================================================
# 1. 认证测试
# ============================================================================


@pytest.mark.asyncio
async def test_register(client: AsyncClient):
    """测试用户注册"""
    response = await client.post(
        "/register",
        json={
            "username": "newuser",
            "email": "new@example.com",
            "password": "password123"
        }
    )
    
    assert response.status_code == 200
    data = response.json()
    assert data["code"] == 200
    assert data["data"]["username"] == "newuser"


@pytest.mark.asyncio
async def test_register_duplicate(client: AsyncClient, test_user):
    """测试重复注册"""
    response = await client.post(
        "/register",
        json={
            "username": "testuser",
            "email": "test@example.com",
            "password": "password123"
        }
    )
    
    assert response.status_code == 400


@pytest.mark.asyncio
async def test_login(client: AsyncClient, test_user):
    """测试登录"""
    response = await client.post(
        "/token",
        data={"username": "testuser", "password": "password123"}
    )
    
    assert response.status_code == 200
    data = response.json()
    assert "access_token" in data
    assert data["token_type"] == "bearer"


@pytest.mark.asyncio
async def test_login_wrong_password(client: AsyncClient, test_user):
    """测试错误密码"""
    response = await client.post(
        "/token",
        data={"username": "testuser", "password": "wrongpassword"}
    )
    
    assert response.status_code == 401


# ============================================================================
# 2. 用户CRUD测试
# ============================================================================


@pytest.mark.asyncio
async def test_get_current_user(client: AsyncClient, auth_token):
    """测试获取当前用户"""
    response = await client.get(
        "/users/me",
        headers={"Authorization": f"Bearer {auth_token}"}
    )
    
    assert response.status_code == 200
    data = response.json()
    assert data["username"] == "testuser"


@pytest.mark.asyncio
async def test_list_users(client: AsyncClient, auth_token):
    """测试列出用户"""
    response = await client.get(
        "/users/",
        headers={"Authorization": f"Bearer {auth_token}"}
    )
    
    assert response.status_code == 200
    data = response.json()
    assert isinstance(data, list)
    assert len(data) > 0


@pytest.mark.asyncio
async def test_get_user(client: AsyncClient, auth_token, test_user):
    """测试获取用户"""
    response = await client.get(
        f"/users/{test_user['id']}",
        headers={"Authorization": f"Bearer {auth_token}"}
    )
    
    assert response.status_code == 200
    data = response.json()
    assert data["id"] == test_user["id"]


@pytest.mark.asyncio
async def test_update_user(client: AsyncClient, auth_token, test_user):
    """测试更新用户"""
    response = await client.put(
        f"/users/{test_user['id']}",
        json={"username": "updateduser"},
        headers={"Authorization": f"Bearer {auth_token}"}
    )
    
    assert response.status_code == 200
    data = response.json()
    assert data["username"] == "updateduser"


# ============================================================================
# 3. 商品CRUD测试
# ============================================================================


@pytest.mark.asyncio
async def test_create_item(client: AsyncClient, auth_token):
    """测试创建商品"""
    response = await client.post(
        "/items/",
        json={
            "title": "Test Item",
            "description": "Test Description",
            "price": 99.99
        },
        headers={"Authorization": f"Bearer {auth_token}"}
    )
    
    assert response.status_code == 200
    data = response.json()
    assert data["title"] == "Test Item"
    assert data["price"] == 99.99


@pytest.mark.asyncio
async def test_list_items(client: AsyncClient):
    """测试列出商品"""
    response = await client.get("/items/")
    
    assert response.status_code == 200
    data = response.json()
    assert isinstance(data, list)


@pytest.mark.asyncio
async def test_get_item(client: AsyncClient, auth_token):
    """测试获取商品"""
    # 先创建商品
    create_response = await client.post(
        "/items/",
        json={
            "title": "Test Item",
            "description": "Test Description",
            "price": 99.99
        },
        headers={"Authorization": f"Bearer {auth_token}"}
    )
    item_id = create_response.json()["id"]
    
    # 获取商品
    response = await client.get(f"/items/{item_id}")
    
    assert response.status_code == 200
    data = response.json()
    assert data["id"] == item_id


@pytest.mark.asyncio
async def test_update_item(client: AsyncClient, auth_token):
    """测试更新商品"""
    # 先创建商品
    create_response = await client.post(
        "/items/",
        json={
            "title": "Test Item",
            "description": "Test Description",
            "price": 99.99
        },
        headers={"Authorization": f"Bearer {auth_token}"}
    )
    item_id = create_response.json()["id"]
    
    # 更新商品
    response = await client.put(
        f"/items/{item_id}",
        json={"title": "Updated Item"},
        headers={"Authorization": f"Bearer {auth_token}"}
    )
    
    assert response.status_code == 200
    data = response.json()
    assert data["title"] == "Updated Item"


@pytest.mark.asyncio
async def test_delete_item(client: AsyncClient, auth_token):
    """测试删除商品"""
    # 先创建商品
    create_response = await client.post(
        "/items/",
        json={
            "title": "Test Item",
            "description": "Test Description",
            "price": 99.99
        },
        headers={"Authorization": f"Bearer {auth_token}"}
    )
    item_id = create_response.json()["id"]
    
    # 删除商品
    response = await client.delete(
        f"/items/{item_id}",
        headers={"Authorization": f"Bearer {auth_token}"}
    )
    
    assert response.status_code == 204


# ============================================================================
# 4. 权限测试
# ============================================================================


@pytest.mark.asyncio
async def test_unauthorized_access(client: AsyncClient):
    """测试未授权访问"""
    response = await client.get("/users/me")
    
    assert response.status_code == 401


@pytest.mark.asyncio
async def test_update_other_user_item(client: AsyncClient, auth_token):
    """测试更新其他用户的商品"""
    # 创建第二个用户
    await client.post(
        "/register",
        json={
            "username": "user2",
            "email": "user2@example.com",
            "password": "password123"
        }
    )
    
    # 第二个用户登录
    response2 = await client.post(
        "/token",
        data={"username": "user2", "password": "password123"}
    )
    token2 = response2.json()["access_token"]
    
    # 用户1创建商品
    create_response = await client.post(
        "/items/",
        json={
            "title": "Test Item",
            "description": "Test Description",
            "price": 99.99
        },
        headers={"Authorization": f"Bearer {auth_token}"}
    )
    item_id = create_response.json()["id"]
    
    # 用户2尝试更新用户1的商品
    response = await client.put(
        f"/items/{item_id}",
        json={"title": "Updated Item"},
        headers={"Authorization": f"Bearer {token2}"}
    )
    
    assert response.status_code == 403


# ============================================================================
# 5. 异常处理测试
# ============================================================================


@pytest.mark.asyncio
async def test_get_nonexistent_user(client: AsyncClient, auth_token):
    """测试获取不存在的用户"""
    response = await client.get(
        "/users/9999",
        headers={"Authorization": f"Bearer {auth_token}"}
    )
    
    assert response.status_code == 404


@pytest.mark.asyncio
async def test_get_nonexistent_item(client: AsyncClient):
    """测试获取不存在的商品"""
    response = await client.get("/items/9999")
    
    assert response.status_code == 404


@pytest.mark.asyncio
async def test_invalid_registration_data(client: AsyncClient):
    """测试无效的注册数据"""
    response = await client.post(
        "/register",
        json={
            "username": "ab",  # 太短
            "email": "invalid-email",  # 无效邮箱
            "password": "123"  # 太短
        }
    )
    
    assert response.status_code == 422


# ============================================================================
# 6. 其他功能测试
# ============================================================================


@pytest.mark.asyncio
async def test_root_endpoint(client: AsyncClient):
    """测试根端点"""
    response = await client.get("/")
    
    assert response.status_code == 200
    data = response.json()
    assert "message" in data


@pytest.mark.asyncio
async def test_health_check(client: AsyncClient):
    """测试健康检查"""
    response = await client.get("/health")
    
    assert response.status_code == 200
    data = response.json()
    assert data["status"] == "healthy"


@pytest.mark.asyncio
async def test_upload_file(client: AsyncClient):
    """测试文件上传"""
    files = {"file": ("test.txt", b"test content", "text/plain")}
    response = await client.post("/uploadfile/", files=files)
    
    assert response.status_code == 200
    data = response.json()
    assert data["filename"] == "test.txt"


if __name__ == "__main__":
    pytest.main([__file__, "-v"])

