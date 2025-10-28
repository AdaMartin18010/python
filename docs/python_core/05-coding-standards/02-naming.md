# Python 命名约定与规范

**命名最佳实践完全指南**

---

## 📋 目录

- [命名基本原则](#命名基本原则)
- [命名风格](#命名风格)
- [领域特定命名](#领域特定命名)
- [反模式](#反模式)
- [重构建议](#重构建议)

---

## 命名基本原则

### 命名的重要性

```python
"""
好的命名 = 自文档化代码
"""

# ❌ 糟糕的命名
def calc(a, b, c):
    return a * b * c

# ✅ 清晰的命名
def calculate_box_volume(length: float, width: float, height: float) -> float:
    """计算长方体体积"""
    return length * width * height

# 命名原则:
# 1. 见名知义
# 2. 避免歧义
# 3. 保持一致
# 4. 遵循约定
# 5. 考虑作用域
```

### 命名清晰度

```python
"""
清晰度优于简洁性
"""

# ❌ 过于简洁
d = {}  # 什么字典?
t = datetime.now()  # t代表什么?
lst = []  # 什么列表?

# ✅ 清晰表达
user_data = {}
current_timestamp = datetime.now()
active_users = []

# ❌ 缩写难懂
def proc_usr_req(req):
    pass

# ✅ 完整单词
def process_user_request(request):
    pass

# 例外: 公认的缩写
http_client = HTTPClient()  # HTTP是公认缩写
db_connection = connect()   # db是公认缩写
max_size = 100  # max是公认缩写
```

---

## 命名风格

### 模块和包

```python
"""
模块和包命名: lowercase_with_underscores
"""

# ✅ 模块名
# my_module.py
# user_service.py
# data_processor.py

# ✅ 包名
# my_package/
# user_management/
# data_processing/

# ❌ 避免
# MyModule.py  # 不要用CapWords
# user-service.py  # 不要用连字符
# dataProcessor.py  # 不要用camelCase

# 特殊情况: 单字母模块名要有意义
# 数学模块
import math
import numpy as np  # 公认缩写

# 不要创建无意义的单字母模块
# a.py, b.py  # ❌
```

### 类名

```python
"""
类名: CapWords (PascalCase)
"""

# ✅ 标准类名
class User:
    pass

class UserAccount:
    pass

class HTTPConnection:
    pass

class XMLParser:
    pass

# ✅ 异常类: 加Error后缀
class ValidationError(Exception):
    pass

class NetworkConnectionError(Exception):
    pass

# ✅ 类型变量: CapWords
from typing import TypeVar

T = TypeVar('T')
UserT = TypeVar('UserT', bound='User')
KeyType = TypeVar('KeyType')

# ❌ 避免
class user:  # 不要用lowercase
    pass

class user_account:  # 不要用snake_case
    pass

class userAccount:  # 不要用camelCase
    pass
```

### 函数和方法

```python
"""
函数和方法: lowercase_with_underscores
"""

# ✅ 函数命名
def get_user():
    pass

def create_user_account():
    pass

def validate_email_address():
    pass

# ✅ 布尔函数: is/has/can前缀
def is_valid():
    return True

def has_permission():
    return True

def can_edit():
    return True

# ✅ 查询函数: get/find/search
def get_user_by_id(user_id):
    pass

def find_users_by_name(name):
    pass

def search_products(query):
    pass

# ✅ 修改函数: 动词开头
def update_user_profile():
    pass

def delete_account():
    pass

def save_settings():
    pass

# ❌ 避免
def GetUser():  # 不要用CapWords
    pass

def getUserAccount():  # 不要用camelCase
    pass
```

### 变量

```python
"""
变量: lowercase_with_underscores
"""

# ✅ 变量命名
user_name = "Alice"
user_age = 30
is_active = True
total_count = 100

# ✅ 布尔变量: is/has/can前缀
is_authenticated = True
has_error = False
can_proceed = True

# ✅ 计数器: count/total/num后缀
user_count = 10
total_items = 100
num_retries = 3

# ✅ 集合: 复数形式
users = []
accounts = {}
products = set()

# ✅ 临时变量: 简短但有意义
for user in users:
    print(user.name)

for i in range(10):  # 循环计数器
    pass

# ❌ 避免
UserName = "Alice"  # 不要用CapWords
userName = "Alice"  # 不要用camelCase
```

### 常量

```python
"""
常量: UPPERCASE_WITH_UNDERSCORES
"""

# ✅ 常量命名
MAX_SIZE = 100
DEFAULT_TIMEOUT = 30
API_KEY = "secret-key"
DATABASE_URL = "postgresql://localhost/db"

# ✅ 配置常量
DEBUG = True
ALLOWED_HOSTS = ["localhost", "127.0.0.1"]
SECRET_KEY = "django-secret-key"

# ✅ 枚举常量
from enum import Enum

class Status(Enum):
    PENDING = "pending"
    RUNNING = "running"
    SUCCESS = "success"
    FAILED = "failed"

# ❌ 避免
max_size = 100  # 常量应该用大写
MaxSize = 100   # 不要用CapWords
```

### 私有和内部

```python
"""
私有和内部命名
"""

# ✅ 单前导下划线: 内部使用
class MyClass:
    def _internal_method(self):
        """内部方法,不应被外部调用"""
        pass
    
    def __init__(self):
        self._internal_state = 0

# ✅ 双前导下划线: 名称修饰
class MyClass:
    def __init__(self):
        self.__private = 1  # 变成_MyClass__private
    
    def __private_method(self):  # 变成_MyClass__private_method
        pass

# ✅ 模块级私有
_internal_function = lambda x: x * 2
_INTERNAL_CONSTANT = 100

# ✅ 避免与关键字冲突: 单后缀下划线
def function(class_=None):  # 避免与class冲突
    pass

# ❌ 避免
def __function():  # 模块级不要用双下划线
    pass
```

---

## 领域特定命名

### Web开发

```python
"""
Web开发命名约定
"""

# ✅ 视图/控制器
class UserListView:
    pass

class UserDetailView:
    pass

def index_view(request):
    pass

def user_detail_view(request, user_id):
    pass

# ✅ 模型
class User(models.Model):
    username = models.CharField()
    email = models.EmailField()
    created_at = models.DateTimeField()

# ✅ 序列化器
class UserSerializer:
    pass

# ✅ 表单
class UserForm:
    pass

class LoginForm:
    pass

# ✅ 中间件
class AuthenticationMiddleware:
    pass

# ✅ URL模式
urlpatterns = [
    path('users/', user_list_view, name='user-list'),
    path('users/<int:user_id>/', user_detail_view, name='user-detail'),
]
```

### 数据科学

```python
"""
数据科学命名约定
"""

# ✅ DataFrame
df = pd.DataFrame()  # 公认缩写
df_users = pd.DataFrame()
df_clean = df_users.dropna()

# ✅ 数组/向量/矩阵
X = np.array([[1, 2], [3, 4]])  # 特征矩阵
y = np.array([0, 1])  # 标签向量
X_train, X_test = train_test_split(X)

# ✅ 模型
model = RandomForestClassifier()
clf = LogisticRegression()  # classifier
reg = LinearRegression()    # regressor

# ✅ 参数
n_samples = 100
n_features = 10
learning_rate = 0.01
max_iter = 1000

# ✅ 评估指标
accuracy_score = 0.95
f1_score = 0.92
```

### 测试

```python
"""
测试命名约定
"""

# ✅ 测试文件: test_*.py 或 *_test.py
# test_user_service.py
# user_service_test.py

# ✅ 测试类: Test前缀
class TestUserService:
    pass

class TestUserAuthentication:
    pass

# ✅ 测试方法: test_前缀
def test_user_creation():
    pass

def test_user_login_success():
    pass

def test_user_login_with_invalid_credentials():
    pass

# ✅ Fixture
@pytest.fixture
def user():
    return User(name="Alice")

@pytest.fixture
def db_session():
    pass

# ✅ Mock
def test_api_call(mocker):
    mock_response = mocker.Mock()
    mock_client = mocker.patch('requests.get')
```

---

## 反模式

### 避免的命名

```python
"""
常见命名反模式
"""

# ❌ 单字母无意义
a = get_data()
b = process(a)
c = save(b)

# ✅ 改进
raw_data = get_data()
processed_data = process(raw_data)
save_result = save(processed_data)

# 例外: 数学代码中的约定
x, y = 10, 20  # 坐标
i, j, k = 0, 1, 2  # 索引

# ❌ 类型编码 (匈牙利命名法)
str_name = "Alice"
int_age = 30
list_users = []

# ✅ 改进 (Python有类型注解)
name: str = "Alice"
age: int = 30
users: list[User] = []

# ❌ 冗余前缀
def user_get_user_name(user):
    pass

# ✅ 改进
def get_user_name(user):
    pass

# 或使用方法
class User:
    def get_name(self):
        pass

# ❌ 数字后缀
user1 = User()
user2 = User()
user3 = User()

# ✅ 改进
admin_user = User()
guest_user = User()
regular_user = User()

# ❌ 含糊不清
data = fetch()  # 什么数据?
info = get()    # 什么信息?
temp = x        # 临时什么?

# ✅ 改进
user_data = fetch()
user_info = get()
original_value = x
```

### 避免的模式

```python
"""
避免的命名模式
"""

# ❌ 魔法数字
if status == 1:
    pass

# ✅ 使用常量
STATUS_ACTIVE = 1
if status == STATUS_ACTIVE:
    pass

# 更好: 使用枚举
from enum import Enum

class Status(Enum):
    PENDING = 1
    ACTIVE = 2
    INACTIVE = 3

if status == Status.ACTIVE:
    pass

# ❌ 布尔陷阱
def create_user(name, flag):  # flag是什么?
    pass

# ✅ 明确的参数名
def create_user(name: str, is_admin: bool = False):
    pass

# ❌ 否定式布尔
is_not_valid = False
if not is_not_valid:  # 双重否定,难理解
    pass

# ✅ 肯定式布尔
is_valid = True
if is_valid:
    pass
```

---

## 重构建议

### 重命名检查清单

```python
"""
何时需要重命名
"""

# 检查清单:
# ☐ 名称是否清晰表达意图?
# ☐ 是否避免了缩写?
# ☐ 是否遵循项目约定?
# ☐ 是否避免了歧义?
# ☐ 作用域是否合适?

# ❌ 需要重构
def proc(d):
    r = []
    for i in d:
        r.append(i * 2)
    return r

# ✅ 重构后
def double_values(numbers: list[int]) -> list[int]:
    """将列表中的每个数字翻倍"""
    doubled = []
    for number in numbers:
        doubled.append(number * 2)
    return doubled

# 更好: 使用列表推导
def double_values(numbers: list[int]) -> list[int]:
    """将列表中的每个数字翻倍"""
    return [number * 2 for number in numbers]
```

### IDE重构支持

```python
"""
使用IDE重构工具
"""

# VSCode: F2 重命名符号
# PyCharm: Shift+F6 重命名

# 重命名步骤:
# 1. 选择要重命名的符号
# 2. 触发重命名 (F2)
# 3. 输入新名称
# 4. 确认 (Enter)
# 5. IDE自动更新所有引用

# 重构前
class OldClassName:
    def old_method_name(self):
        pass

# 重构后 (IDE自动完成)
class NewClassName:
    def new_method_name(self):
        pass
```

---

## 📚 核心要点

### 命名风格

- ✅ **模块/包**: lowercase_with_underscores
- ✅ **类**: CapWords
- ✅ **函数/方法**: lowercase_with_underscores
- ✅ **变量**: lowercase_with_underscores
- ✅ **常量**: UPPERCASE_WITH_UNDERSCORES

### 命名原则

- ✅ **清晰**: 见名知义
- ✅ **一致**: 遵循约定
- ✅ **准确**: 表达意图
- ✅ **简洁**: 不过度冗长
- ✅ **避免**: 歧义和缩写

### 特殊命名

- ✅ **布尔**: is/has/can前缀
- ✅ **查询**: get/find/search
- ✅ **修改**: update/delete/save
- ✅ **私有**: _leading_underscore
- ✅ **内部**: __double_leading

### 领域约定

- ✅ **Web**: View/Serializer/Form后缀
- ✅ **数据科学**: df/X/y等约定
- ✅ **测试**: test_前缀
- ✅ **枚举**: CapWords类名

### 避免

- ❌ 单字母无意义变量
- ❌ 匈牙利命名法
- ❌ 数字后缀
- ❌ 双重否定布尔
- ❌ 魔法数字

---

**好的命名是代码可读性的基石！** 📝✨

**相关文档**:
- [01-pep8.md](01-pep8.md) - PEP 8代码风格
- [03-documentation.md](03-documentation.md) - 文档字符串

**最后更新**: 2025年10月28日

