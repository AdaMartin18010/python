# unittest 标准库测试

**Python内置测试框架**

---

## 📋 概述

unittest是Python标准库中的测试框架，提供面向对象的测试方式。

### 核心特性

- 📦 **标准库** - 无需安装
- 🎯 **xUnit风格** - 经典测试风格
- 🔧 **Setup/Teardown** - 测试准备和清理
- 📊 **测试套件** - 组织测试

---

## 🚀 快速开始

### 基本测试

```python
import unittest

class TestMath(unittest.TestCase):
    def test_addition(self):
        self.assertEqual(1 + 1, 2)
    
    def test_subtraction(self):
        self.assertEqual(5 - 3, 2)

if __name__ == '__main__':
    unittest.main()
```

---

## 💻 核心功能

### 断言方法

```python
class TestAssertions(unittest.TestCase):
    def test_equality(self):
        self.assertEqual(1, 1)
        self.assertNotEqual(1, 2)
    
    def test_boolean(self):
        self.assertTrue(True)
        self.assertFalse(False)
    
    def test_none(self):
        self.assertIsNone(None)
        self.assertIsNotNone(1)
    
    def test_membership(self):
        self.assertIn(1, [1, 2, 3])
        self.assertNotIn(4, [1, 2, 3])
    
    def test_exceptions(self):
        with self.assertRaises(ValueError):
            raise ValueError("Error")
```

### Setup和Teardown

```python
class TestDatabase(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        """整个类执行前运行一次"""
        cls.db = Database()
        cls.db.connect()
    
    @classmethod
    def tearDownClass(cls):
        """整个类执行后运行一次"""
        cls.db.close()
    
    def setUp(self):
        """每个测试前运行"""
        self.user = User(name="Test")
    
    def tearDown(self):
        """每个测试后运行"""
        self.user.delete()
    
    def test_user_creation(self):
        self.assertEqual(self.user.name, "Test")
```

---

## 🔧 Mock

```python
from unittest.mock import Mock, patch

class TestAPI(unittest.TestCase):
    @patch('requests.get')
    def test_api_call(self, mock_get):
        # 设置mock返回值
        mock_get.return_value.json.return_value = {'status': 'ok'}
        
        result = api_call()
        
        # 验证
        mock_get.assert_called_once()
        self.assertEqual(result['status'], 'ok')
```

---

## 📚 最佳实践

### 跳过测试

```python
class TestFeatures(unittest.TestCase):
    @unittest.skip("Not implemented yet")
    def test_future_feature(self):
        pass
    
    @unittest.skipIf(sys.version_info < (3, 10), "Requires Python 3.10+")
    def test_new_syntax(self):
        pass
```

### 子测试

```python
class TestMath(unittest.TestCase):
    def test_even_numbers(self):
        for i in range(0, 10, 2):
            with self.subTest(i=i):
                self.assertEqual(i % 2, 0)
```

---

## 🔗 相关资源

- [官方文档](https://docs.python.org/3/library/unittest.html)
- [unittest.mock文档](https://docs.python.org/3/library/unittest.mock.html)

---

**最后更新**: 2025年10月28日

