# 序列化工具

**Python数据序列化方案**

---

## 📋 概述

序列化是将数据结构转换为可存储或传输格式的过程。

---

## 🚀 JSON

### 标准库json

```python
import json

# 序列化
data = {'name': 'Alice', 'age': 25}
json_str = json.dumps(data)
json_str = json.dumps(data, indent=2)  # 格式化

# 反序列化
data = json.loads(json_str)

# 文件操作
with open('data.json', 'w') as f:
    json.dump(data, f, indent=2)

with open('data.json', 'r') as f:
    data = json.load(f)
```

### orjson (高性能)

```bash
uv add orjson
```

```python
import orjson

# 比标准库快2-3倍
json_bytes = orjson.dumps(data)
data = orjson.loads(json_bytes)
```

---

## 📄 YAML

```bash
uv add pyyaml
```

```python
import yaml

# 序列化
yaml_str = yaml.dump(data, default_flow_style=False)

# 反序列化
data = yaml.safe_load(yaml_str)

# 文件操作
with open('config.yaml', 'w') as f:
    yaml.dump(data, f)
```

---

## 📦 MessagePack

```bash
uv add msgpack
```

```python
import msgpack

# 比JSON更紧凑
packed = msgpack.packb(data)
data = msgpack.unpackb(packed)
```

---

## 🔧 Pickle

```python
import pickle

# Python对象序列化
obj = {'data': [1, 2, 3], 'model': MyClass()}

# 序列化
with open('data.pkl', 'wb') as f:
    pickle.dump(obj, f)

# 反序列化
with open('data.pkl', 'rb') as f:
    obj = pickle.load(f)
```

⚠️ **警告**: 不要反序列化不信任的数据！

---

## 📚 最佳实践

### 选择序列化格式

| 格式 | 场景 | 优点 | 缺点 |
|------|------|------|------|
| JSON | API、配置 | 通用、可读 | 体积大 |
| MessagePack | 内部通信 | 紧凑、快速 | 二进制 |
| YAML | 配置文件 | 可读性好 | 解析慢 |
| Pickle | Python对象 | 完整性 | 不安全 |

---

## 🔗 相关资源

- [json文档](https://docs.python.org/3/library/json.html)
- [PyYAML](https://pyyaml.org/)
- [MessagePack](https://msgpack.org/)

---

**最后更新**: 2025年10月28日

