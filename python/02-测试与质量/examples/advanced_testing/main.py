#!/usr/bin/env python3
"""
高级测试示例
展示pytest的高级功能，包括参数化、夹具、标记等
"""

import pytest
import asyncio
from typing import List, Dict, Any
from unittest.mock import Mock, patch, MagicMock
import tempfile
import os
import json
from dataclasses import dataclass
from datetime import datetime, timedelta

# 测试目标类
@dataclass
class User:
    """用户类"""
    id: int
    name: str
    email: str
    age: int
    is_active: bool = True
    created_at: datetime = None
    
    def __post_init__(self):
        if self.created_at is None:
            self.created_at = datetime.now()
    
    def to_dict(self) -> Dict[str, Any]:
        """转换为字典"""
        return {
            'id': self.id,
            'name': self.name,
            'email': self.email,
            'age': self.age,
            'is_active': self.is_active,
            'created_at': self.created_at.isoformat()
        }
    
    @classmethod
    def from_dict(cls, data: Dict[str, Any]) -> 'User':
        """从字典创建用户"""
        data = data.copy()
        if 'created_at' in data and isinstance(data['created_at'], str):
            data['created_at'] = datetime.fromisoformat(data['created_at'])
        return cls(**data)

class UserService:
    """用户服务类"""
    
    def __init__(self, db_connection=None):
        self.db_connection = db_connection
        self.users: List[User] = []
    
    def create_user(self, name: str, email: str, age: int) -> User:
        """创建用户"""
        if not name or not email:
            raise ValueError("姓名和邮箱不能为空")
        
        if age < 0 or age > 150:
            raise ValueError("年龄必须在0-150之间")
        
        # 检查邮箱是否已存在
        if any(user.email == email for user in self.users):
            raise ValueError("邮箱已存在")
        
        user_id = len(self.users) + 1
        user = User(id=user_id, name=name, email=email, age=age)
        self.users.append(user)
        
        return user
    
    def get_user(self, user_id: int) -> User:
        """获取用户"""
        for user in self.users:
            if user.id == user_id:
                return user
        raise ValueError("用户不存在")
    
    def update_user(self, user_id: int, **kwargs) -> User:
        """更新用户"""
        user = self.get_user(user_id)
        
        for key, value in kwargs.items():
            if hasattr(user, key):
                setattr(user, key, value)
        
        return user
    
    def delete_user(self, user_id: int) -> bool:
        """删除用户"""
        for i, user in enumerate(self.users):
            if user.id == user_id:
                del self.users[i]
                return True
        return False
    
    def get_users_by_age_range(self, min_age: int, max_age: int) -> List[User]:
        """根据年龄范围获取用户"""
        return [user for user in self.users if min_age <= user.age <= max_age]
    
    async def async_create_user(self, name: str, email: str, age: int) -> User:
        """异步创建用户"""
        await asyncio.sleep(0.1)  # 模拟异步操作
        return self.create_user(name, email, age)

class DataProcessor:
    """数据处理器"""
    
    def __init__(self):
        self.processed_count = 0
    
    def process_data(self, data: List[Dict[str, Any]]) -> List[Dict[str, Any]]:
        """处理数据"""
        processed = []
        for item in data:
            if 'value' in item:
                item['processed_value'] = item['value'] * 2
                item['processed_at'] = datetime.now().isoformat()
                processed.append(item)
        self.processed_count += len(processed)
        return processed
    
    def save_to_file(self, data: List[Dict[str, Any]], file_path: str) -> bool:
        """保存数据到文件"""
        try:
            with open(file_path, 'w') as f:
                json.dump(data, f, indent=2)
            return True
        except Exception:
            return False
    
    def load_from_file(self, file_path: str) -> List[Dict[str, Any]]:
        """从文件加载数据"""
        try:
            with open(file_path, 'r') as f:
                return json.load(f)
        except Exception:
            return []

# 测试类
class TestUser:
    """用户类测试"""
    
    def test_user_creation(self):
        """测试用户创建"""
        user = User(id=1, name="张三", email="zhangsan@example.com", age=25)
        
        assert user.id == 1
        assert user.name == "张三"
        assert user.email == "zhangsan@example.com"
        assert user.age == 25
        assert user.is_active is True
        assert user.created_at is not None
    
    def test_user_to_dict(self):
        """测试用户转字典"""
        user = User(id=1, name="张三", email="zhangsan@example.com", age=25)
        user_dict = user.to_dict()
        
        assert user_dict['id'] == 1
        assert user_dict['name'] == "张三"
        assert user_dict['email'] == "zhangsan@example.com"
        assert user_dict['age'] == 25
        assert user_dict['is_active'] is True
        assert 'created_at' in user_dict
    
    def test_user_from_dict(self):
        """测试从字典创建用户"""
        user_dict = {
            'id': 1,
            'name': '张三',
            'email': 'zhangsan@example.com',
            'age': 25,
            'is_active': True,
            'created_at': '2024-01-01T00:00:00'
        }
        
        user = User.from_dict(user_dict)
        
        assert user.id == 1
        assert user.name == "张三"
        assert user.email == "zhangsan@example.com"
        assert user.age == 25
        assert user.is_active is True
        assert user.created_at == datetime(2024, 1, 1)

class TestUserService:
    """用户服务测试"""
    
    @pytest.fixture
    def user_service(self):
        """用户服务夹具"""
        return UserService()
    
    @pytest.fixture
    def sample_users(self, user_service):
        """示例用户夹具"""
        users = []
        users.append(user_service.create_user("张三", "zhangsan@example.com", 25))
        users.append(user_service.create_user("李四", "lisi@example.com", 30))
        users.append(user_service.create_user("王五", "wangwu@example.com", 35))
        return users
    
    def test_create_user_success(self, user_service):
        """测试成功创建用户"""
        user = user_service.create_user("张三", "zhangsan@example.com", 25)
        
        assert user.name == "张三"
        assert user.email == "zhangsan@example.com"
        assert user.age == 25
        assert user.id == 1
        assert len(user_service.users) == 1
    
    @pytest.mark.parametrize("name,email,age,expected_error", [
        ("", "test@example.com", 25, "姓名和邮箱不能为空"),
        ("张三", "", 25, "姓名和邮箱不能为空"),
        ("张三", "test@example.com", -1, "年龄必须在0-150之间"),
        ("张三", "test@example.com", 151, "年龄必须在0-150之间"),
    ])
    def test_create_user_validation(self, user_service, name, email, age, expected_error):
        """测试创建用户验证"""
        with pytest.raises(ValueError, match=expected_error):
            user_service.create_user(name, email, age)
    
    def test_create_duplicate_email(self, user_service):
        """测试创建重复邮箱用户"""
        user_service.create_user("张三", "test@example.com", 25)
        
        with pytest.raises(ValueError, match="邮箱已存在"):
            user_service.create_user("李四", "test@example.com", 30)
    
    def test_get_user_success(self, user_service, sample_users):
        """测试成功获取用户"""
        user = user_service.get_user(1)
        assert user.name == "张三"
        assert user.email == "zhangsan@example.com"
    
    def test_get_user_not_found(self, user_service):
        """测试获取不存在的用户"""
        with pytest.raises(ValueError, match="用户不存在"):
            user_service.get_user(999)
    
    def test_update_user(self, user_service, sample_users):
        """测试更新用户"""
        updated_user = user_service.update_user(1, name="张三三", age=26)
        
        assert updated_user.name == "张三三"
        assert updated_user.age == 26
        assert updated_user.email == "zhangsan@example.com"  # 未更新的字段保持不变
    
    def test_delete_user(self, user_service, sample_users):
        """测试删除用户"""
        assert user_service.delete_user(1) is True
        assert len(user_service.users) == 2
        
        with pytest.raises(ValueError, match="用户不存在"):
            user_service.get_user(1)
    
    def test_delete_nonexistent_user(self, user_service):
        """测试删除不存在的用户"""
        assert user_service.delete_user(999) is False
    
    def test_get_users_by_age_range(self, user_service, sample_users):
        """测试根据年龄范围获取用户"""
        users = user_service.get_users_by_age_range(25, 30)
        
        assert len(users) == 2
        assert all(25 <= user.age <= 30 for user in users)
    
    @pytest.mark.asyncio
    async def test_async_create_user(self, user_service):
        """测试异步创建用户"""
        user = await user_service.async_create_user("张三", "zhangsan@example.com", 25)
        
        assert user.name == "张三"
        assert user.email == "zhangsan@example.com"
        assert user.age == 25

class TestDataProcessor:
    """数据处理器测试"""
    
    @pytest.fixture
    def data_processor(self):
        """数据处理器夹具"""
        return DataProcessor()
    
    @pytest.fixture
    def sample_data(self):
        """示例数据夹具"""
        return [
            {'id': 1, 'value': 10, 'name': 'item1'},
            {'id': 2, 'value': 20, 'name': 'item2'},
            {'id': 3, 'name': 'item3'},  # 没有value字段
        ]
    
    def test_process_data(self, data_processor, sample_data):
        """测试数据处理"""
        processed = data_processor.process_data(sample_data)
        
        assert len(processed) == 2  # 只有包含value字段的项目被处理
        assert processed[0]['processed_value'] == 20  # 10 * 2
        assert processed[1]['processed_value'] == 40  # 20 * 2
        assert 'processed_at' in processed[0]
        assert data_processor.processed_count == 2
    
    def test_save_and_load_file(self, data_processor, sample_data):
        """测试文件保存和加载"""
        with tempfile.NamedTemporaryFile(mode='w', suffix='.json', delete=False) as f:
            file_path = f.name
        
        try:
            # 测试保存
            assert data_processor.save_to_file(sample_data, file_path) is True
            
            # 测试加载
            loaded_data = data_processor.load_from_file(file_path)
            assert loaded_data == sample_data
        finally:
            os.unlink(file_path)
    
    def test_save_file_error(self, data_processor, sample_data):
        """测试文件保存错误"""
        # 使用无效路径
        result = data_processor.save_to_file(sample_data, "/invalid/path/file.json")
        assert result is False
    
    def test_load_file_error(self, data_processor):
        """测试文件加载错误"""
        # 加载不存在的文件
        result = data_processor.load_from_file("/nonexistent/file.json")
        assert result == []

class TestMocking:
    """模拟测试"""
    
    def test_mock_external_service(self):
        """测试模拟外部服务"""
        # 创建模拟对象
        mock_service = Mock()
        mock_service.get_data.return_value = {'status': 'success', 'data': [1, 2, 3]}
        
        # 使用模拟对象
        result = mock_service.get_data()
        
        assert result['status'] == 'success'
        assert result['data'] == [1, 2, 3]
        mock_service.get_data.assert_called_once()
    
    @patch('builtins.open', create=True)
    def test_mock_file_operations(self, mock_open):
        """测试模拟文件操作"""
        mock_file = MagicMock()
        mock_open.return_value.__enter__.return_value = mock_file
        
        # 测试文件写入
        with open('test.txt', 'w') as f:
            f.write('test content')
        
        mock_open.assert_called_once_with('test.txt', 'w')
        mock_file.write.assert_called_once_with('test content')
    
    def test_mock_with_side_effect(self):
        """测试带副作用的模拟"""
        mock_func = Mock(side_effect=[1, 2, 3])
        
        assert mock_func() == 1
        assert mock_func() == 2
        assert mock_func() == 3
    
    def test_mock_with_exception(self):
        """测试模拟异常"""
        mock_func = Mock(side_effect=ValueError("模拟错误"))
        
        with pytest.raises(ValueError, match="模拟错误"):
            mock_func()

# 标记测试
@pytest.mark.slow
class TestSlowOperations:
    """慢速操作测试"""
    
    def test_slow_calculation(self):
        """慢速计算测试"""
        import time
        time.sleep(0.1)  # 模拟慢速操作
        assert 1 + 1 == 2

@pytest.mark.integration
class TestIntegration:
    """集成测试"""
    
    def test_user_service_integration(self):
        """用户服务集成测试"""
        service = UserService()
        
        # 创建用户
        user1 = service.create_user("张三", "zhangsan@example.com", 25)
        user2 = service.create_user("李四", "lisi@example.com", 30)
        
        # 更新用户
        service.update_user(user1.id, name="张三三")
        
        # 删除用户
        service.delete_user(user2.id)
        
        # 验证结果
        assert len(service.users) == 1
        assert service.users[0].name == "张三三"

# 参数化测试
@pytest.mark.parametrize("input_value,expected", [
    (1, 2),
    (2, 4),
    (3, 6),
    (0, 0),
    (-1, -2),
])
def test_double_function(input_value, expected):
    """参数化测试示例"""
    def double(x):
        return x * 2
    
    assert double(input_value) == expected

# 夹具作用域测试
@pytest.fixture(scope="session")
def session_data():
    """会话级夹具"""
    return {"session_id": "test_session_123"}

@pytest.fixture(scope="module")
def module_data():
    """模块级夹具"""
    return {"module_id": "test_module_456"}

def test_fixture_scope(session_data, module_data):
    """测试夹具作用域"""
    assert "session_id" in session_data
    assert "module_id" in module_data

if __name__ == "__main__":
    # 运行测试
    pytest.main([__file__, "-v", "--tb=short"])
