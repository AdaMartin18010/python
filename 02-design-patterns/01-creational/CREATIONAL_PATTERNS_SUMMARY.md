# 创建型模式总结与对比

**分类**: 创建型设计模式 (Creational Design Patterns)  
**完成日期**: 2025-10-25  
**模式数量**: 5个

---

## 📋 模式总览

| 模式 | 目的 | 核心思想 | 复杂度 | 使用频率 |
|-----|------|---------|--------|---------|
| **Singleton** | 确保唯一实例 | 限制实例化 | ⭐⭐ | ⭐⭐⭐⭐⭐ |
| **Factory Method** | 创建单一产品 | 多态创建 | ⭐⭐⭐ | ⭐⭐⭐⭐⭐ |
| **Abstract Factory** | 创建产品族 | 产品族一致性 | ⭐⭐⭐⭐ | ⭐⭐⭐⭐ |
| **Builder** | 构建复杂对象 | 分步骤构建 | ⭐⭐⭐ | ⭐⭐⭐⭐ |
| **Prototype** | 克隆对象 | 原型复制 | ⭐⭐ | ⭐⭐⭐ |

---

## 🎯 使用场景决策树

```
需要创建对象？
├─ 需要唯一实例？
│  └─ ✅ Singleton
│
├─ 创建过程复杂？
│  ├─ 多个步骤？
│  │  └─ ✅ Builder
│  └─ 基于已有对象？
│     └─ ✅ Prototype
│
└─ 需要解耦创建？
   ├─ 单一产品？
   │  └─ ✅ Factory Method
   └─ 产品族？
      └─ ✅ Abstract Factory
```

---

## 📊 详细对比

### 1. Singleton vs Factory Method

| 维度 | Singleton | Factory Method |
|-----|-----------|----------------|
| **目的** | 唯一实例 | 创建对象 |
| **实例数** | 1个 | 多个 |
| **创建方式** | 限制构造 | 工厂方法 |
| **扩展性** | 差 | 好 |
| **使用场景** | 配置、日志 | 数据库连接 |

### 2. Factory Method vs Abstract Factory

| 维度 | Factory Method | Abstract Factory |
|-----|----------------|------------------|
| **创建对象** | 一个产品 | 一系列产品 |
| **产品层次** | 单一产品线 | 多个产品线 |
| **工厂方法** | 1个 | 多个 |
| **扩展方向** | 新产品类型 | 新产品族 |
| **复杂度** | 较低 | 较高 |

### 3. Builder vs Prototype

| 维度 | Builder | Prototype |
|-----|---------|-----------|
| **创建方式** | 分步构建 | 克隆复制 |
| **对象复杂度** | 高 | 不限 |
| **灵活性** | 高 | 中 |
| **性能** | 中 | 高 |
| **适用场景** | 不可变对象 | 相似对象 |

---

## 🔄 模式组合

### 常见组合模式

1. **Singleton + Factory Method**
   ```python
   class SingletonFactory(metaclass=SingletonMeta):
       def create_product(self, type: str) -> Product:
           return self._factories[type]()
   ```

2. **Abstract Factory + Singleton**
   ```python
   class UIFactory(AbstractFactory, metaclass=SingletonMeta):
       pass
   ```

3. **Builder + Factory Method**
   ```python
   class ProductFactory:
       def create(self) -> Product:
           return (ProductBuilder()
                   .set_property1("value")
                   .build())
   ```

4. **Prototype + Factory Method**
   ```python
   class PrototypeFactory:
       def create(self, name: str) -> Product:
           return copy.deepcopy(self._prototypes[name])
   ```

---

## 💡 选择指南

### 按需求选择

**需要全局唯一访问点** → **Singleton**
- 配置管理器
- 日志系统
- 数据库连接池

**需要解耦对象创建** → **Factory Method**
- 不同类型的解析器
- 多种数据格式支持
- 插件系统

**需要创建相关对象族** → **Abstract Factory**
- 跨平台UI组件
- 不同风格主题
- 数据库访问层

**需要构建复杂对象** → **Builder**
- HTTP请求构建
- SQL查询构建
- 配置对象创建

**需要克隆已有对象** → **Prototype**
- 大量相似对象
- 对象创建成本高
- 动态配置对象

---

## 📈 性能对比

| 模式 | 创建速度 | 内存占用 | 线程安全 | 推荐场景 |
|-----|---------|---------|---------|---------|
| Singleton | ⭐⭐⭐⭐⭐ | ⭐⭐⭐⭐⭐ | ⚠️需注意 | 全局唯一 |
| Factory Method | ⭐⭐⭐⭐ | ⭐⭐⭐⭐ | ✅ | 多态创建 |
| Abstract Factory | ⭐⭐⭐ | ⭐⭐⭐ | ✅ | 产品族 |
| Builder | ⭐⭐⭐ | ⭐⭐⭐⭐ | ✅ | 复杂对象 |
| Prototype | ⭐⭐⭐⭐⭐ | ⭐⭐⭐ | ✅ | 对象克隆 |

---

## 🐍 Python特色实现

每个模式都提供Python特有的实现方式：

1. **元类 (Metaclass)** - Singleton
2. **装饰器 (Decorator)** - Factory注册
3. **Protocol** - 鸭子类型
4. **泛型 (Generic)** - 类型安全
5. **数据类 (Dataclass)** - 简化定义

---

## 📚 学习路径建议

### 初学者
1. **Singleton** - 最简单，理解唯一实例
2. **Factory Method** - 理解多态和解耦
3. **Prototype** - 理解对象复制

### 中级
4. **Builder** - 理解复杂对象构建
5. **Abstract Factory** - 理解产品族概念

### 进阶
- 组合使用多个模式
- 根据实际需求灵活运用
- 理解权衡和选择

---

## ✅ 最佳实践

1. **不要过度设计** - 简单场景不要使用复杂模式
2. **优先组合** - 组合优于继承
3. **遵循SOLID原则** - 单一职责、开闭、依赖倒置等
4. **考虑Python特性** - 利用Python的动态特性
5. **保持简洁** - Python的简洁性是优势

---

## 🎓 知识图谱

```
创建型模式核心理念
│
├── 控制实例化
│   └── Singleton
│
├── 解耦创建过程
│   ├── Factory Method (单一产品)
│   └── Abstract Factory (产品族)
│
└── 优化创建方式
    ├── Builder (分步构建)
    └── Prototype (原型克隆)
```

---

**总结**: 5个创建型模式各有特色，根据具体需求选择合适的模式。在Python中，可以灵活运用语言特性，实现更Pythonic的设计模式。

