# Hypothesis 属性测试

**基于属性的测试框架**

---

## 📋 概述

Hypothesis是Python的属性测试库，自动生成测试用例来发现边界情况。

### 核心特性

- 🎲 **自动生成** - 自动生成测试数据
- 🐛 **发现边界** - 找到极端情况
- 🔄 **可重现** - 失败用例可重现
- 🎯 **智能缩减** - 最小化失败用例

---

## 🚀 快速开始

### 安装

```bash
uv add hypothesis
```

### 基本示例

```python
from hypothesis import given
from hypothesis import strategies as st

@given(st.integers(), st.integers())
def test_addition_commutative(a, b):
    assert a + b == b + a

@given(st.lists(st.integers()))
def test_reverse_twice(lst):
    assert list(reversed(list(reversed(lst)))) == lst
```

---

## 💻 策略 (Strategies)

### 基本类型

```python
from hypothesis import strategies as st

# 整数
st.integers()
st.integers(min_value=0, max_value=100)

# 浮点数
st.floats()
st.floats(min_value=0.0, max_value=1.0)

# 字符串
st.text()
st.text(min_size=1, max_size=10)

# 布尔值
st.booleans()
```

### 复合类型

```python
# 列表
st.lists(st.integers())
st.lists(st.text(), min_size=1, max_size=10)

# 字典
st.dictionaries(keys=st.text(), values=st.integers())

# 元组
st.tuples(st.integers(), st.text(), st.booleans())
```

### 自定义策略

```python
from hypothesis import strategies as st

@st.composite
def user_strategy(draw):
    return {
        'name': draw(st.text(min_size=1)),
        'age': draw(st.integers(min_value=0, max_value=120)),
        'email': draw(st.emails())
    }

@given(user_strategy())
def test_user(user):
    assert user['age'] >= 0
    assert '@' in user['email']
```

---

## 🎯 实战示例

### 测试排序函数

```python
@given(st.lists(st.integers()))
def test_sorted_is_ordered(lst):
    sorted_lst = sorted(lst)
    # 检查是否有序
    for i in range(len(sorted_lst) - 1):
        assert sorted_lst[i] <= sorted_lst[i + 1]
    # 检查长度不变
    assert len(sorted_lst) == len(lst)
```

### 测试解析器

```python
@given(st.integers())
def test_int_parser(n):
    s = str(n)
    assert int(s) == n
```

---

## 🔧 配置

```python
from hypothesis import given, settings

@settings(max_examples=1000)  # 运行1000个例子
@given(st.integers())
def test_example(n):
    assert n == n
```

---

## 📚 最佳实践

### 1. 测试不变量

```python
@given(st.lists(st.integers()))
def test_reverse_invariant(lst):
    # 两次反转应该得到原列表
    assert list(reversed(list(reversed(lst)))) == lst
```

### 2. 测试往返

```python
@given(st.text())
def test_json_roundtrip(s):
    # JSON序列化往返测试
    assert json.loads(json.dumps(s)) == s
```

---

## 🔗 相关资源

- [官方文档](https://hypothesis.readthedocs.io/)

---

**最后更新**: 2025年10月28日

