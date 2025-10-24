"""
安全API测试用例
测试认证、授权、速率限制等功能

运行方式:
    pytest tests/test_security.py -v
"""

import pytest
from fastapi.testclient import TestClient
from secure_api_example import app, fake_users_db, fake_documents_db

# 创建测试客户端
client = TestClient(app)

# ============ 辅助函数 ============

def get_auth_token(username: str, password: str) -> str:
    """获取认证令牌"""
    response = client.post(
        "/token",
        data={"username": username, "password": password}
    )
    assert response.status_code == 200
    return response.json()["access_token"]


@pytest.fixture
def admin_token():
    """管理员令牌"""
    return get_auth_token("admin", "Admin123!@#")


@pytest.fixture
def user_token():
    """普通用户令牌"""
    return get_auth_token("testuser", "Test123!@#")


@pytest.fixture
def auth_headers_admin(admin_token):
    """管理员认证头"""
    return {"Authorization": f"Bearer {admin_token}"}


@pytest.fixture
def auth_headers_user(user_token):
    """用户认证头"""
    return {"Authorization": f"Bearer {user_token}"}


@pytest.fixture(autouse=True)
def reset_data():
    """每个测试前重置数据"""
    fake_documents_db.clear()
    yield


# ============ 认证测试 ============

class TestAuthentication:
    """认证功能测试"""
    
    def test_login_success(self):
        """测试：成功登录"""
        response = client.post(
            "/token",
            data={"username": "admin", "password": "Admin123!@#"}
        )
        assert response.status_code == 200
        data = response.json()
        assert "access_token" in data
        assert data["token_type"] == "bearer"
    
    def test_login_wrong_password(self):
        """测试：错误密码"""
        response = client.post(
            "/token",
            data={"username": "admin", "password": "WrongPassword"}
        )
        assert response.status_code == 401
        assert "Incorrect username or password" in response.json()["detail"]
    
    def test_login_nonexistent_user(self):
        """测试：不存在的用户"""
        response = client.post(
            "/token",
            data={"username": "nonexistent", "password": "password"}
        )
        assert response.status_code == 401
    
    def test_access_protected_without_token(self):
        """测试：未授权访问受保护端点"""
        response = client.get("/users/me")
        assert response.status_code == 401
    
    def test_access_protected_with_token(self, auth_headers_user):
        """测试：有令牌访问受保护端点"""
        response = client.get("/users/me", headers=auth_headers_user)
        assert response.status_code == 200
        data = response.json()
        assert data["username"] == "testuser"


# ============ 用户注册测试 ============

class TestUserRegistration:
    """用户注册测试"""
    
    def test_create_user_success(self):
        """测试：成功创建用户"""
        response = client.post(
            "/users",
            json={
                "username": "newuser",
                "email": "newuser@example.com",
                "password": "NewUser123!@#"
            }
        )
        assert response.status_code == 200
        data = response.json()
        assert data["username"] == "newuser"
        assert data["email"] == "newuser@example.com"
        assert "password" not in data
    
    def test_create_user_weak_password(self):
        """测试：弱密码"""
        response = client.post(
            "/users",
            json={
                "username": "newuser",
                "email": "newuser@example.com",
                "password": "weak"
            }
        )
        assert response.status_code == 422  # Validation error
    
    def test_create_user_duplicate_username(self):
        """测试：重复用户名"""
        response = client.post(
            "/users",
            json={
                "username": "admin",  # 已存在
                "email": "another@example.com",
                "password": "ValidPass123!@#"
            }
        )
        assert response.status_code == 400
        assert "already registered" in response.json()["detail"]
    
    def test_create_user_invalid_email(self):
        """测试：无效邮箱"""
        response = client.post(
            "/users",
            json={
                "username": "newuser",
                "email": "invalid-email",
                "password": "ValidPass123!@#"
            }
        )
        assert response.status_code == 422


# ============ 授权测试 ============

class TestAuthorization:
    """授权和权限测试"""
    
    def test_user_can_read(self, auth_headers_user):
        """测试：普通用户有读权限"""
        response = client.get("/documents", headers=auth_headers_user)
        assert response.status_code == 200
    
    def test_user_can_write(self, auth_headers_user):
        """测试：普通用户有写权限"""
        response = client.post(
            "/documents",
            headers=auth_headers_user,
            json={
                "title": "Test Document",
                "content": "Test content",
                "is_public": False
            }
        )
        assert response.status_code == 200
    
    def test_user_cannot_access_admin(self, auth_headers_user):
        """测试：普通用户无管理员权限"""
        response = client.get("/admin/audit-logs", headers=auth_headers_user)
        assert response.status_code == 403
        assert "admin" in response.json()["detail"].lower()
    
    def test_admin_can_access_admin(self, auth_headers_admin):
        """测试：管理员可以访问管理员端点"""
        response = client.get("/admin/audit-logs", headers=auth_headers_admin)
        assert response.status_code == 200


# ============ 文档CRUD测试 ============

class TestDocumentCRUD:
    """文档CRUD操作测试"""
    
    def test_create_document(self, auth_headers_user):
        """测试：创建文档"""
        response = client.post(
            "/documents",
            headers=auth_headers_user,
            json={
                "title": "My Document",
                "content": "Document content",
                "is_public": False
            }
        )
        assert response.status_code == 200
        data = response.json()
        assert data["title"] == "My Document"
        assert data["owner_id"] == "testuser"
        assert "id" in data
    
    def test_list_documents(self, auth_headers_user):
        """测试：列出文档"""
        # 创建文档
        client.post(
            "/documents",
            headers=auth_headers_user,
            json={
                "title": "Doc 1",
                "content": "Content 1",
                "is_public": False
            }
        )
        
        # 列出文档
        response = client.get("/documents", headers=auth_headers_user)
        assert response.status_code == 200
        docs = response.json()
        assert len(docs) >= 1
    
    def test_delete_own_document(self, auth_headers_user):
        """测试：删除自己的文档"""
        # 创建文档
        create_response = client.post(
            "/documents",
            headers=auth_headers_user,
            json={
                "title": "To Delete",
                "content": "Will be deleted",
                "is_public": False
            }
        )
        doc_id = create_response.json()["id"]
        
        # 删除文档
        delete_response = client.delete(
            f"/documents/{doc_id}",
            headers=auth_headers_user
        )
        assert delete_response.status_code == 200
    
    def test_cannot_delete_others_document(
        self, auth_headers_user, auth_headers_admin
    ):
        """测试：不能删除他人文档"""
        # 管理员创建文档
        create_response = client.post(
            "/documents",
            headers=auth_headers_admin,
            json={
                "title": "Admin Doc",
                "content": "Admin content",
                "is_public": False
            }
        )
        doc_id = create_response.json()["id"]
        
        # 普通用户尝试删除
        delete_response = client.delete(
            f"/documents/{doc_id}",
            headers=auth_headers_user
        )
        assert delete_response.status_code == 403
    
    def test_admin_can_delete_any_document(
        self, auth_headers_user, auth_headers_admin
    ):
        """测试：管理员可以删除任何文档"""
        # 用户创建文档
        create_response = client.post(
            "/documents",
            headers=auth_headers_user,
            json={
                "title": "User Doc",
                "content": "User content",
                "is_public": False
            }
        )
        doc_id = create_response.json()["id"]
        
        # 管理员删除
        delete_response = client.delete(
            f"/documents/{doc_id}",
            headers=auth_headers_admin
        )
        assert delete_response.status_code == 200


# ============ 速率限制测试 ============

class TestRateLimit:
    """速率限制测试"""
    
    @pytest.mark.skip(reason="速率限制测试会影响其他测试，需要隔离运行")
    def test_login_rate_limit(self):
        """测试：登录速率限制"""
        # 尝试多次失败登录
        for i in range(6):
            response = client.post(
                "/token",
                data={"username": "admin", "password": "wrong"}
            )
            if i < 5:
                assert response.status_code == 401
            else:
                # 第6次应该被限制
                assert response.status_code == 429
                assert "Too many" in response.json()["detail"]


# ============ 数据验证测试 ============

class TestDataValidation:
    """数据验证测试"""
    
    def test_document_title_too_short(self, auth_headers_user):
        """测试：文档标题太短"""
        response = client.post(
            "/documents",
            headers=auth_headers_user,
            json={
                "title": "",  # 空标题
                "content": "Content",
                "is_public": False
            }
        )
        assert response.status_code == 422
    
    def test_document_title_too_long(self, auth_headers_user):
        """测试：文档标题太长"""
        response = client.post(
            "/documents",
            headers=auth_headers_user,
            json={
                "title": "x" * 300,  # 超长标题
                "content": "Content",
                "is_public": False
            }
        )
        assert response.status_code == 422


# ============ 安全头测试 ============

class TestSecurityHeaders:
    """安全响应头测试"""
    
    def test_security_headers_present(self):
        """测试：安全响应头存在"""
        response = client.get("/")
        
        # 检查各种安全头
        assert "X-Content-Type-Options" in response.headers
        assert response.headers["X-Content-Type-Options"] == "nosniff"
        
        assert "X-Frame-Options" in response.headers
        assert response.headers["X-Frame-Options"] == "DENY"
        
        assert "Strict-Transport-Security" in response.headers
        assert "max-age=" in response.headers["Strict-Transport-Security"]
        
        assert "Content-Security-Policy" in response.headers


# ============ 运行测试 ============

if __name__ == "__main__":
    pytest.main([__file__, "-v", "--tb=short"])

