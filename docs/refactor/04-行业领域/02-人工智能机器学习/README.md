# 02-人工智能/机器学习

## 概述

人工智能和机器学习是现代软件工程的重要领域，涉及算法设计、模型训练、数据处理、系统部署等多个方面。本领域基于形式科学理论，提供严格的形式化定义和可实现的代码示例。

## 目录结构

```
02-人工智能机器学习/
├── 01-机器学习基础/
│   ├── 01-监督学习.md
│   ├── 02-无监督学习.md
│   ├── 03-强化学习.md
│   └── 04-深度学习.md
├── 02-数据处理/
│   ├── 01-数据预处理.md
│   ├── 02-特征工程.md
│   ├── 03-数据清洗.md
│   └── 04-数据增强.md
├── 03-模型架构/
│   ├── 01-神经网络.md
│   ├── 02-卷积神经网络.md
│   ├── 03-循环神经网络.md
│   └── 04-Transformer.md
├── 04-训练与优化/
│   ├── 01-损失函数.md
│   ├── 02-优化算法.md
│   ├── 03-正则化.md
│   └── 04-超参数调优.md
├── 05-模型部署/
│   ├── 01-模型服务化.md
│   ├── 02-模型压缩.md
│   ├── 03-边缘部署.md
│   └── 04-模型监控.md
└── 06-应用场景/
    ├── 01-计算机视觉.md
    ├── 02-自然语言处理.md
    ├── 03-推荐系统.md
    └── 04-时间序列分析.md
```

## 核心概念

### 1. 机器学习基础

#### 形式化定义

```python
from typing import TypeVar, Generic, List, Tuple, Callable, Any
from abc import ABC, abstractmethod
import numpy as np
from dataclasses import dataclass

T = TypeVar('T')
X = TypeVar('X')  # 特征空间
Y = TypeVar('Y')  # 标签空间

@dataclass
class Dataset(Generic[X, Y]):
    """数据集的形式化定义"""
    features: List[X]
    labels: List[Y]
    
    def __len__(self) -> int:
        return len(self.features)
    
    def __getitem__(self, idx: int) -> Tuple[X, Y]:
        return self.features[idx], self.labels[idx]

class Model(ABC, Generic[X, Y]):
    """机器学习模型的抽象定义"""
    
    @abstractmethod
    def fit(self, dataset: Dataset[X, Y]) -> None:
        """训练模型"""
        pass
    
    @abstractmethod
    def predict(self, x: X) -> Y:
        """预测"""
        pass
    
    @abstractmethod
    def evaluate(self, dataset: Dataset[X, Y]) -> float:
        """评估模型性能"""
        pass

class SupervisedLearning(Model[X, Y]):
    """监督学习"""
    
    def __init__(self, algorithm: str):
        self.algorithm = algorithm
        self.is_trained = False
    
    def fit(self, dataset: Dataset[X, Y]) -> None:
        """训练监督学习模型"""
        # 实现训练逻辑
        self.is_trained = True
    
    def predict(self, x: X) -> Y:
        """预测"""
        if not self.is_trained:
            raise ValueError("模型尚未训练")
        # 实现预测逻辑
        return None
    
    def evaluate(self, dataset: Dataset[X, Y]) -> float:
        """评估模型"""
        if not self.is_trained:
            raise ValueError("模型尚未训练")
        # 实现评估逻辑
        return 0.0

class UnsupervisedLearning(Model[X, Y]):
    """无监督学习"""
    
    def __init__(self, algorithm: str):
        self.algorithm = algorithm
        self.is_trained = False
    
    def fit(self, dataset: Dataset[X, Y]) -> None:
        """训练无监督学习模型"""
        # 实现训练逻辑
        self.is_trained = True
    
    def predict(self, x: X) -> Y:
        """预测"""
        if not self.is_trained:
            raise ValueError("模型尚未训练")
        # 实现预测逻辑
        return None
    
    def evaluate(self, dataset: Dataset[X, Y]) -> float:
        """评估模型"""
        if not self.is_trained:
            raise ValueError("模型尚未训练")
        # 实现评估逻辑
        return 0.0
```

#### 学习理论

```python
class LearningTheory:
    """学习理论"""
    
    @staticmethod
    def pac_learning_bound(complexity: int, sample_size: int, confidence: float) -> float:
        """PAC学习界"""
        # 计算泛化误差上界
        epsilon = np.sqrt((complexity * np.log(sample_size) + np.log(1/confidence)) / sample_size)
        return epsilon
    
    @staticmethod
    def vc_dimension_analysis(model_class: str) -> int:
        """VC维分析"""
        vc_dims = {
            'linear_classifier': 2,
            'neural_network': float('inf'),
            'decision_tree': float('inf')
        }
        return vc_dims.get(model_class, 0)
    
    @staticmethod
    def bias_variance_decomposition(true_function: Callable, 
                                   model_predictions: List[Callable]) -> Tuple[float, float]:
        """偏差-方差分解"""
        # 计算偏差
        bias = np.mean([(true_function(x) - np.mean([f(x) for f in model_predictions]))**2 
                       for x in range(100)])
        
        # 计算方差
        variance = np.mean([np.var([f(x) for f in model_predictions]) 
                           for x in range(100)])
        
        return bias, variance

# 示例：学习理论应用
learning_theory = LearningTheory()

# PAC学习界
epsilon = learning_theory.pac_learning_bound(
    complexity=10, 
    sample_size=1000, 
    confidence=0.95
)
print(f"PAC学习界: ε ≤ {epsilon:.4f}")

# VC维分析
vc_dim = learning_theory.vc_dimension_analysis('linear_classifier')
print(f"线性分类器的VC维: {vc_dim}")

# 偏差-方差分解
def true_function(x): return x**2
model_predictions = [lambda x: x**2 + np.random.normal(0, 0.1) for _ in range(10)]
bias, variance = learning_theory.bias_variance_decomposition(true_function, model_predictions)
print(f"偏差: {bias:.4f}, 方差: {variance:.4f}")
```

### 2. 数据处理

#### 数据预处理

```python
class DataPreprocessing:
    """数据预处理"""
    
    @staticmethod
    def normalization(data: np.ndarray, method: str = 'minmax') -> np.ndarray:
        """数据标准化"""
        if method == 'minmax':
            return (data - np.min(data)) / (np.max(data) - np.min(data))
        elif method == 'zscore':
            return (data - np.mean(data)) / np.std(data)
        else:
            raise ValueError(f"未知的标准化方法: {method}")
    
    @staticmethod
    def feature_scaling(features: np.ndarray) -> Tuple[np.ndarray, Callable]:
        """特征缩放"""
        mean = np.mean(features, axis=0)
        std = np.std(features, axis=0)
        
        scaled_features = (features - mean) / std
        
        def inverse_transform(scaled_data):
            return scaled_data * std + mean
        
        return scaled_features, inverse_transform
    
    @staticmethod
    def handle_missing_values(data: np.ndarray, strategy: str = 'mean') -> np.ndarray:
        """处理缺失值"""
        if strategy == 'mean':
            return np.where(np.isnan(data), np.nanmean(data), data)
        elif strategy == 'median':
            return np.where(np.isnan(data), np.nanmedian(data), data)
        elif strategy == 'mode':
            from scipy.stats import mode
            mode_val = mode(data[~np.isnan(data)])[0][0]
            return np.where(np.isnan(data), mode_val, data)
        else:
            raise ValueError(f"未知的缺失值处理策略: {strategy}")

# 示例：数据预处理
preprocessing = DataPreprocessing()

# 生成示例数据
data = np.random.randn(100, 5)
data[0, 0] = np.nan  # 添加缺失值

# 标准化
normalized_data = preprocessing.normalization(data, 'minmax')
print(f"标准化后数据范围: [{np.min(normalized_data):.4f}, {np.max(normalized_data):.4f}]")

# 特征缩放
scaled_data, inverse_func = preprocessing.feature_scaling(data)
print(f"缩放后数据均值: {np.mean(scaled_data):.4f}, 标准差: {np.std(scaled_data):.4f}")

# 处理缺失值
cleaned_data = preprocessing.handle_missing_values(data, 'mean')
print(f"缺失值处理后是否有NaN: {np.any(np.isnan(cleaned_data))}")
```

#### 特征工程

```python
class FeatureEngineering:
    """特征工程"""
    
    @staticmethod
    def polynomial_features(features: np.ndarray, degree: int = 2) -> np.ndarray:
        """多项式特征"""
        from sklearn.preprocessing import PolynomialFeatures
        poly = PolynomialFeatures(degree=degree)
        return poly.fit_transform(features)
    
    @staticmethod
    def interaction_features(features: np.ndarray) -> np.ndarray:
        """交互特征"""
        n_features = features.shape[1]
        interactions = []
        
        for i in range(n_features):
            for j in range(i+1, n_features):
                interaction = features[:, i] * features[:, j]
                interactions.append(interaction)
        
        return np.column_stack([features] + interactions)
    
    @staticmethod
    def temporal_features(timestamps: np.ndarray) -> np.ndarray:
        """时间特征"""
        import pandas as pd
        df = pd.DataFrame({'timestamp': timestamps})
        
        # 提取时间特征
        df['hour'] = pd.to_datetime(df['timestamp']).dt.hour
        df['day_of_week'] = pd.to_datetime(df['timestamp']).dt.dayofweek
        df['month'] = pd.to_datetime(df['timestamp']).dt.month
        df['is_weekend'] = df['day_of_week'].isin([5, 6]).astype(int)
        
        return df[['hour', 'day_of_week', 'month', 'is_weekend']].values
    
    @staticmethod
    def text_features(texts: List[str]) -> np.ndarray:
        """文本特征"""
        from sklearn.feature_extraction.text import TfidfVectorizer
        
        vectorizer = TfidfVectorizer(max_features=1000)
        return vectorizer.fit_transform(texts).toarray()

# 示例：特征工程
feature_engineering = FeatureEngineering()

# 生成示例数据
features = np.random.randn(100, 3)
timestamps = pd.date_range('2023-01-01', periods=100, freq='H')

# 多项式特征
poly_features = feature_engineering.polynomial_features(features, degree=2)
print(f"多项式特征形状: {poly_features.shape}")

# 交互特征
interaction_features = feature_engineering.interaction_features(features)
print(f"交互特征形状: {interaction_features.shape}")

# 时间特征
temporal_features = feature_engineering.temporal_features(timestamps)
print(f"时间特征形状: {temporal_features.shape}")

# 文本特征
texts = ["hello world", "machine learning", "artificial intelligence"]
text_features = feature_engineering.text_features(texts)
print(f"文本特征形状: {text_features.shape}")
```

### 3. 模型架构

#### 神经网络

```python
class NeuralNetwork:
    """神经网络"""
    
    def __init__(self, layers: List[int], activation: str = 'relu'):
        self.layers = layers
        self.activation = activation
        self.weights = []
        self.biases = []
        self.initialize_parameters()
    
    def initialize_parameters(self):
        """初始化参数"""
        for i in range(len(self.layers) - 1):
            # He初始化
            w = np.random.randn(self.layers[i+1], self.layers[i]) * np.sqrt(2.0 / self.layers[i])
            b = np.zeros((self.layers[i+1], 1))
            self.weights.append(w)
            self.biases.append(b)
    
    def forward(self, x: np.ndarray) -> np.ndarray:
        """前向传播"""
        a = x
        for i in range(len(self.weights)):
            z = np.dot(self.weights[i], a) + self.biases[i]
            if i == len(self.weights) - 1:
                # 输出层使用softmax
                a = self.softmax(z)
            else:
                a = self.activation_function(z)
        return a
    
    def activation_function(self, z: np.ndarray) -> np.ndarray:
        """激活函数"""
        if self.activation == 'relu':
            return np.maximum(0, z)
        elif self.activation == 'sigmoid':
            return 1 / (1 + np.exp(-z))
        elif self.activation == 'tanh':
            return np.tanh(z)
        else:
            raise ValueError(f"未知的激活函数: {self.activation}")
    
    def softmax(self, z: np.ndarray) -> np.ndarray:
        """Softmax函数"""
        exp_z = np.exp(z - np.max(z, axis=0, keepdims=True))
        return exp_z / np.sum(exp_z, axis=0, keepdims=True)
    
    def backward(self, x: np.ndarray, y: np.ndarray, learning_rate: float = 0.01):
        """反向传播"""
        m = x.shape[1]
        
        # 前向传播
        activations = [x]
        zs = []
        
        a = x
        for i in range(len(self.weights)):
            z = np.dot(self.weights[i], a) + self.biases[i]
            zs.append(z)
            
            if i == len(self.weights) - 1:
                a = self.softmax(z)
            else:
                a = self.activation_function(z)
            activations.append(a)
        
        # 反向传播
        delta = activations[-1] - y
        
        for i in range(len(self.weights) - 1, -1, -1):
            # 计算梯度
            dw = np.dot(delta, activations[i].T) / m
            db = np.sum(delta, axis=1, keepdims=True) / m
            
            # 更新参数
            self.weights[i] -= learning_rate * dw
            self.biases[i] -= learning_rate * db
            
            # 计算下一层的误差
            if i > 0:
                delta = np.dot(self.weights[i].T, delta) * self.activation_derivative(zs[i-1])
    
    def activation_derivative(self, z: np.ndarray) -> np.ndarray:
        """激活函数导数"""
        if self.activation == 'relu':
            return np.where(z > 0, 1, 0)
        elif self.activation == 'sigmoid':
            s = 1 / (1 + np.exp(-z))
            return s * (1 - s)
        elif self.activation == 'tanh':
            return 1 - np.tanh(z)**2
        else:
            raise ValueError(f"未知的激活函数: {self.activation}")

# 示例：神经网络
nn = NeuralNetwork([2, 10, 5, 3], activation='relu')

# 生成示例数据
X = np.random.randn(2, 100)
y = np.random.randint(0, 3, (3, 100))

# 训练
for epoch in range(100):
    nn.backward(X, y, learning_rate=0.01)

# 预测
predictions = nn.forward(X)
print(f"预测形状: {predictions.shape}")
```

#### 卷积神经网络

```python
class ConvolutionalNeuralNetwork:
    """卷积神经网络"""
    
    def __init__(self, input_shape: Tuple[int, int, int]):
        self.input_shape = input_shape
        self.layers = []
    
    def add_conv_layer(self, filters: int, kernel_size: int, stride: int = 1, padding: str = 'same'):
        """添加卷积层"""
        conv_layer = {
            'type': 'conv',
            'filters': filters,
            'kernel_size': kernel_size,
            'stride': stride,
            'padding': padding
        }
        self.layers.append(conv_layer)
    
    def add_pool_layer(self, pool_size: int, stride: int = 2):
        """添加池化层"""
        pool_layer = {
            'type': 'pool',
            'pool_size': pool_size,
            'stride': stride
        }
        self.layers.append(pool_layer)
    
    def add_dense_layer(self, units: int, activation: str = 'relu'):
        """添加全连接层"""
        dense_layer = {
            'type': 'dense',
            'units': units,
            'activation': activation
        }
        self.layers.append(dense_layer)
    
    def conv2d(self, x: np.ndarray, filters: np.ndarray, stride: int = 1, padding: str = 'same') -> np.ndarray:
        """2D卷积操作"""
        batch_size, height, width, channels = x.shape
        filter_height, filter_width, in_channels, out_channels = filters.shape
        
        if padding == 'same':
            pad_h = (filter_height - 1) // 2
            pad_w = (filter_width - 1) // 2
            x_padded = np.pad(x, ((0, 0), (pad_h, pad_h), (pad_w, pad_w), (0, 0)), mode='constant')
        else:
            x_padded = x
        
        out_height = (height + 2 * pad_h - filter_height) // stride + 1
        out_width = (width + 2 * pad_w - filter_width) // stride + 1
        
        output = np.zeros((batch_size, out_height, out_width, out_channels))
        
        for i in range(out_height):
            for j in range(out_width):
                h_start = i * stride
                h_end = h_start + filter_height
                w_start = j * stride
                w_end = w_start + filter_width
                
                x_slice = x_padded[:, h_start:h_end, w_start:w_end, :]
                for k in range(out_channels):
                    output[:, i, j, k] = np.sum(x_slice * filters[:, :, :, k], axis=(1, 2, 3))
        
        return output
    
    def max_pool2d(self, x: np.ndarray, pool_size: int, stride: int = 2) -> np.ndarray:
        """2D最大池化"""
        batch_size, height, width, channels = x.shape
        
        out_height = (height - pool_size) // stride + 1
        out_width = (width - pool_size) // stride + 1
        
        output = np.zeros((batch_size, out_height, out_width, channels))
        
        for i in range(out_height):
            for j in range(out_width):
                h_start = i * stride
                h_end = h_start + pool_size
                w_start = j * stride
                w_end = w_start + pool_size
                
                x_slice = x[:, h_start:h_end, w_start:w_end, :]
                output[:, i, j, :] = np.max(x_slice, axis=(1, 2))
        
        return output

# 示例：卷积神经网络
cnn = ConvolutionalNeuralNetwork(input_shape=(32, 32, 3))

# 添加层
cnn.add_conv_layer(filters=32, kernel_size=3)
cnn.add_pool_layer(pool_size=2)
cnn.add_conv_layer(filters=64, kernel_size=3)
cnn.add_pool_layer(pool_size=2)
cnn.add_dense_layer(units=128)
cnn.add_dense_layer(units=10, activation='softmax')

print(f"CNN层数: {len(cnn.layers)}")
```

### 4. 训练与优化

#### 损失函数

```python
class LossFunctions:
    """损失函数"""
    
    @staticmethod
    def mean_squared_error(y_true: np.ndarray, y_pred: np.ndarray) -> float:
        """均方误差"""
        return np.mean((y_true - y_pred) ** 2)
    
    @staticmethod
    def cross_entropy(y_true: np.ndarray, y_pred: np.ndarray) -> float:
        """交叉熵损失"""
        epsilon = 1e-15
        y_pred = np.clip(y_pred, epsilon, 1 - epsilon)
        return -np.mean(np.sum(y_true * np.log(y_pred), axis=1))
    
    @staticmethod
    def binary_cross_entropy(y_true: np.ndarray, y_pred: np.ndarray) -> float:
        """二元交叉熵"""
        epsilon = 1e-15
        y_pred = np.clip(y_pred, epsilon, 1 - epsilon)
        return -np.mean(y_true * np.log(y_pred) + (1 - y_true) * np.log(1 - y_pred))
    
    @staticmethod
    def hinge_loss(y_true: np.ndarray, y_pred: np.ndarray) -> float:
        """铰链损失"""
        return np.mean(np.maximum(0, 1 - y_true * y_pred))
    
    @staticmethod
    def huber_loss(y_true: np.ndarray, y_pred: np.ndarray, delta: float = 1.0) -> float:
        """Huber损失"""
        error = y_true - y_pred
        abs_error = np.abs(error)
        quadratic = np.minimum(abs_error, delta)
        linear = abs_error - quadratic
        return np.mean(0.5 * quadratic ** 2 + delta * linear)

# 示例：损失函数
loss_functions = LossFunctions()

# 生成示例数据
y_true = np.array([1, 0, 1, 0])
y_pred = np.array([0.9, 0.1, 0.8, 0.2])

# 计算各种损失
mse = loss_functions.mean_squared_error(y_true, y_pred)
bce = loss_functions.binary_cross_entropy(y_true, y_pred)
hinge = loss_functions.hinge_loss(y_true, y_pred)
huber = loss_functions.huber_loss(y_true, y_pred)

print(f"MSE: {mse:.4f}")
print(f"Binary Cross Entropy: {bce:.4f}")
print(f"Hinge Loss: {hinge:.4f}")
print(f"Huber Loss: {huber:.4f}")
```

#### 优化算法

```python
class Optimizers:
    """优化算法"""
    
    @staticmethod
    def sgd(params: List[np.ndarray], grads: List[np.ndarray], 
            learning_rate: float = 0.01) -> List[np.ndarray]:
        """随机梯度下降"""
        updated_params = []
        for param, grad in zip(params, grads):
            updated_param = param - learning_rate * grad
            updated_params.append(updated_param)
        return updated_params
    
    @staticmethod
    def momentum(params: List[np.ndarray], grads: List[np.ndarray], 
                 velocities: List[np.ndarray], learning_rate: float = 0.01, 
                 momentum_rate: float = 0.9) -> Tuple[List[np.ndarray], List[np.ndarray]]:
        """带动量的SGD"""
        updated_params = []
        updated_velocities = []
        
        for param, grad, velocity in zip(params, grads, velocities):
            new_velocity = momentum_rate * velocity - learning_rate * grad
            updated_param = param + new_velocity
            updated_params.append(updated_param)
            updated_velocities.append(new_velocity)
        
        return updated_params, updated_velocities
    
    @staticmethod
    def adam(params: List[np.ndarray], grads: List[np.ndarray], 
             m: List[np.ndarray], v: List[np.ndarray], t: int,
             learning_rate: float = 0.001, beta1: float = 0.9, 
             beta2: float = 0.999, epsilon: float = 1e-8) -> Tuple[List[np.ndarray], List[np.ndarray], List[np.ndarray]]:
        """Adam优化器"""
        updated_params = []
        updated_m = []
        updated_v = []
        
        for param, grad, m_t, v_t in zip(params, grads, m, v):
            # 更新偏置修正的一阶矩估计
            m_t_new = beta1 * m_t + (1 - beta1) * grad
            # 更新偏置修正的二阶矩估计
            v_t_new = beta2 * v_t + (1 - beta2) * grad ** 2
            
            # 计算偏置修正
            m_hat = m_t_new / (1 - beta1 ** t)
            v_hat = v_t_new / (1 - beta2 ** t)
            
            # 更新参数
            updated_param = param - learning_rate * m_hat / (np.sqrt(v_hat) + epsilon)
            
            updated_params.append(updated_param)
            updated_m.append(m_t_new)
            updated_v.append(v_t_new)
        
        return updated_params, updated_m, updated_v

# 示例：优化算法
optimizers = Optimizers()

# 生成示例参数和梯度
params = [np.random.randn(2, 2), np.random.randn(2, 1)]
grads = [np.random.randn(2, 2), np.random.randn(2, 1)]

# SGD
updated_params_sgd = optimizers.sgd(params, grads, learning_rate=0.01)
print(f"SGD更新后参数数量: {len(updated_params_sgd)}")

# Momentum
velocities = [np.zeros_like(p) for p in params]
updated_params_momentum, updated_velocities = optimizers.momentum(
    params, grads, velocities, learning_rate=0.01, momentum_rate=0.9
)
print(f"Momentum更新后参数数量: {len(updated_params_momentum)}")

# Adam
m = [np.zeros_like(p) for p in params]
v = [np.zeros_like(p) for p in params]
updated_params_adam, updated_m, updated_v = optimizers.adam(
    params, grads, m, v, t=1, learning_rate=0.001
)
print(f"Adam更新后参数数量: {len(updated_params_adam)}")
```

### 5. 模型部署

#### 模型服务化

```python
class ModelServing:
    """模型服务化"""
    
    def __init__(self, model: Any):
        self.model = model
        self.is_loaded = False
    
    def load_model(self, model_path: str):
        """加载模型"""
        # 实际实现中会加载保存的模型
        self.is_loaded = True
        print(f"模型已从 {model_path} 加载")
    
    def predict(self, input_data: np.ndarray) -> np.ndarray:
        """预测"""
        if not self.is_loaded:
            raise ValueError("模型尚未加载")
        return self.model.predict(input_data)
    
    def batch_predict(self, input_batch: List[np.ndarray]) -> List[np.ndarray]:
        """批量预测"""
        if not self.is_loaded:
            raise ValueError("模型尚未加载")
        return [self.predict(data) for data in input_batch]
    
    def get_model_info(self) -> Dict[str, Any]:
        """获取模型信息"""
        return {
            'model_type': type(self.model).__name__,
            'is_loaded': self.is_loaded,
            'input_shape': getattr(self.model, 'input_shape', None),
            'output_shape': getattr(self.model, 'output_shape', None)
        }

class ModelCompression:
    """模型压缩"""
    
    @staticmethod
    def quantization(model_weights: List[np.ndarray], bits: int = 8) -> List[np.ndarray]:
        """量化"""
        quantized_weights = []
        scale = 2 ** (bits - 1) - 1
        
        for weight in model_weights:
            # 归一化到[0, 1]
            normalized = (weight - np.min(weight)) / (np.max(weight) - np.min(weight))
            # 量化
            quantized = np.round(normalized * scale) / scale
            # 反归一化
            dequantized = quantized * (np.max(weight) - np.min(weight)) + np.min(weight)
            quantized_weights.append(dequantized)
        
        return quantized_weights
    
    @staticmethod
    def pruning(model_weights: List[np.ndarray], sparsity: float = 0.5) -> List[np.ndarray]:
        """剪枝"""
        pruned_weights = []
        
        for weight in model_weights:
            # 计算阈值
            threshold = np.percentile(np.abs(weight), (1 - sparsity) * 100)
            # 剪枝
            pruned = np.where(np.abs(weight) > threshold, weight, 0)
            pruned_weights.append(pruned)
        
        return pruned_weights
    
    @staticmethod
    def knowledge_distillation(teacher_model: Any, student_model: Any, 
                              temperature: float = 3.0) -> Callable:
        """知识蒸馏损失"""
        def distillation_loss(y_true: np.ndarray, y_pred: np.ndarray) -> float:
            # 教师模型预测
            teacher_pred = teacher_model.predict(y_true)
            
            # 软标签
            soft_labels = teacher_pred / temperature
            soft_predictions = y_pred / temperature
            
            # 交叉熵损失
            return LossFunctions.cross_entropy(soft_labels, soft_predictions)
        
        return distillation_loss

# 示例：模型部署
model_serving = ModelServing(None)
model_serving.load_model("model.pkl")

# 模型压缩
model_weights = [np.random.randn(10, 10), np.random.randn(10, 1)]

# 量化
quantized_weights = ModelCompression.quantization(model_weights, bits=8)
print(f"量化后权重数量: {len(quantized_weights)}")

# 剪枝
pruned_weights = ModelCompression.pruning(model_weights, sparsity=0.5)
print(f"剪枝后权重数量: {len(pruned_weights)}")

# 知识蒸馏
teacher_model = NeuralNetwork([10, 5, 1])
student_model = NeuralNetwork([10, 3, 1])
distillation_loss = ModelCompression.knowledge_distillation(teacher_model, student_model)
print(f"知识蒸馏损失函数: {distillation_loss}")
```

## 应用场景

### 1. 计算机视觉

```python
class ComputerVision:
    """计算机视觉应用"""
    
    @staticmethod
    def image_classification(image: np.ndarray, model: Any) -> str:
        """图像分类"""
        # 预处理
        processed_image = image / 255.0  # 归一化
        processed_image = np.expand_dims(processed_image, axis=0)  # 添加batch维度
        
        # 预测
        prediction = model.predict(processed_image)
        class_id = np.argmax(prediction)
        
        # 类别映射
        classes = ['cat', 'dog', 'bird']
        return classes[class_id]
    
    @staticmethod
    def object_detection(image: np.ndarray, model: Any) -> List[Dict[str, Any]]:
        """目标检测"""
        # 预处理
        processed_image = image / 255.0
        processed_image = np.expand_dims(processed_image, axis=0)
        
        # 预测
        predictions = model.predict(processed_image)
        
        # 解析预测结果
        detections = []
        for pred in predictions[0]:
            if pred[4] > 0.5:  # 置信度阈值
                detection = {
                    'bbox': pred[:4],  # 边界框
                    'confidence': pred[4],  # 置信度
                    'class': int(pred[5])  # 类别
                }
                detections.append(detection)
        
        return detections
    
    @staticmethod
    def image_segmentation(image: np.ndarray, model: Any) -> np.ndarray:
        """图像分割"""
        # 预处理
        processed_image = image / 255.0
        processed_image = np.expand_dims(processed_image, axis=0)
        
        # 预测
        segmentation = model.predict(processed_image)
        
        return segmentation[0]

# 示例：计算机视觉
cv = ComputerVision()

# 生成示例图像
image = np.random.randint(0, 255, (224, 224, 3), dtype=np.uint8)

# 图像分类
classification_result = cv.image_classification(image, None)
print(f"图像分类结果: {classification_result}")

# 目标检测
detection_results = cv.object_detection(image, None)
print(f"检测到 {len(detection_results)} 个目标")

# 图像分割
segmentation_result = cv.image_segmentation(image, None)
print(f"分割结果形状: {segmentation_result.shape}")
```

### 2. 自然语言处理

```python
class NaturalLanguageProcessing:
    """自然语言处理应用"""
    
    @staticmethod
    def text_classification(text: str, model: Any, tokenizer: Any) -> str:
        """文本分类"""
        # 分词
        tokens = tokenizer.tokenize(text)
        token_ids = tokenizer.convert_tokens_to_ids(tokens)
        
        # 预测
        prediction = model.predict([token_ids])
        class_id = np.argmax(prediction)
        
        # 类别映射
        classes = ['positive', 'negative', 'neutral']
        return classes[class_id]
    
    @staticmethod
    def named_entity_recognition(text: str, model: Any, tokenizer: Any) -> List[Dict[str, Any]]:
        """命名实体识别"""
        # 分词
        tokens = tokenizer.tokenize(text)
        token_ids = tokenizer.convert_tokens_to_ids(tokens)
        
        # 预测
        predictions = model.predict([token_ids])
        
        # 解析实体
        entities = []
        current_entity = None
        
        for i, (token, pred) in enumerate(zip(tokens, predictions[0])):
            if pred.startswith('B-'):  # 实体开始
                if current_entity:
                    entities.append(current_entity)
                current_entity = {
                    'text': token,
                    'type': pred[2:],
                    'start': i
                }
            elif pred.startswith('I-') and current_entity and pred[2:] == current_entity['type']:
                # 实体继续
                current_entity['text'] += ' ' + token
            else:
                # 实体结束
                if current_entity:
                    current_entity['end'] = i
                    entities.append(current_entity)
                    current_entity = None
        
        return entities
    
    @staticmethod
    def machine_translation(source_text: str, model: Any, tokenizer: Any) -> str:
        """机器翻译"""
        # 编码
        source_tokens = tokenizer.tokenize(source_text)
        source_ids = tokenizer.convert_tokens_to_ids(source_tokens)
        
        # 预测
        target_ids = model.predict([source_ids])
        
        # 解码
        target_tokens = tokenizer.convert_ids_to_tokens(target_ids[0])
        target_text = ' '.join(target_tokens)
        
        return target_text

# 示例：自然语言处理
nlp = NaturalLanguageProcessing()

# 文本分类
text = "I love this movie, it's amazing!"
classification_result = nlp.text_classification(text, None, None)
print(f"文本分类结果: {classification_result}")

# 命名实体识别
text = "John Smith works at Google in New York."
entities = nlp.named_entity_recognition(text, None, None)
print(f"识别到的实体: {entities}")

# 机器翻译
source_text = "Hello world"
translation = nlp.machine_translation(source_text, None, None)
print(f"翻译结果: {translation}")
```

## 总结

人工智能/机器学习领域为软件工程提供了：

1. **算法基础**: 监督学习、无监督学习、强化学习
2. **数据处理**: 预处理、特征工程、数据清洗
3. **模型架构**: 神经网络、CNN、RNN、Transformer
4. **训练优化**: 损失函数、优化算法、正则化
5. **部署应用**: 模型服务化、压缩、监控

## 交叉引用

- **形式科学**: [01-形式科学](../01-形式科学/README.md)
- **理论基础**: [02-理论基础](../02-理论基础/README.md)
- **具体科学**: [03-具体科学](../03-具体科学/README.md)
- **架构领域**: [05-架构领域](../05-架构领域/README.md) 