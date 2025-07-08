# Python机器学习最佳实践指南

## 1. 数据工程基础

### 1.1 数据加载与预处理

```python
import pandas as pd
import numpy as np
from typing import Tuple, List, Dict, Any
from sklearn.preprocessing import StandardScaler, LabelEncoder
from sklearn.model_selection import train_test_split
import polars as pl

class DataEngineering:
    """数据工程最佳实践"""
    
    @staticmethod
    def load_data_efficiently(file_path: str) -> pd.DataFrame:
        """高效加载数据"""
        # 使用polars进行快速数据加载
        if file_path.endswith('.csv'):
            df = pl.read_csv(file_path)
            return df.to_pandas()
        elif file_path.endswith('.parquet'):
            df = pl.read_parquet(file_path)
            return df.to_pandas()
        else:
            return pd.read_csv(file_path)
    
    @staticmethod
    def handle_missing_values(df: pd.DataFrame, strategy: str = 'auto') -> pd.DataFrame:
        """处理缺失值"""
        if strategy == 'auto':
            # 数值列用中位数填充
            numeric_columns = df.select_dtypes(include=[np.number]).columns
            df[numeric_columns] = df[numeric_columns].fillna(df[numeric_columns].median())
            
            # 分类列用众数填充
            categorical_columns = df.select_dtypes(include=['object']).columns
            for col in categorical_columns:
                df[col] = df[col].fillna(df[col].mode()[0])
        
        elif strategy == 'drop':
            df = df.dropna()
        
        elif strategy == 'interpolate':
            df = df.interpolate()
        
        return df
    
    @staticmethod
    def detect_outliers(df: pd.DataFrame, method: str = 'iqr') -> Dict[str, List[int]]:
        """检测异常值"""
        outliers = {}
        
        numeric_columns = df.select_dtypes(include=[np.number]).columns
        
        for col in numeric_columns:
            if method == 'iqr':
                Q1 = df[col].quantile(0.25)
                Q3 = df[col].quantile(0.75)
                IQR = Q3 - Q1
                lower_bound = Q1 - 1.5 * IQR
                upper_bound = Q3 + 1.5 * IQR
                
                outlier_indices = df[(df[col] < lower_bound) | (df[col] > upper_bound)].index.tolist()
                outliers[col] = outlier_indices
            
            elif method == 'zscore':
                z_scores = np.abs((df[col] - df[col].mean()) / df[col].std())
                outlier_indices = df[z_scores > 3].index.tolist()
                outliers[col] = outlier_indices
        
        return outliers
    
    @staticmethod
    def feature_engineering(df: pd.DataFrame) -> pd.DataFrame:
        """特征工程"""
        # 创建时间特征
        if 'date' in df.columns:
            df['date'] = pd.to_datetime(df['date'])
            df['year'] = df['date'].dt.year
            df['month'] = df['date'].dt.month
            df['day'] = df['date'].dt.day
            df['day_of_week'] = df['date'].dt.dayofweek
        
        # 创建交互特征
        numeric_columns = df.select_dtypes(include=[np.number]).columns
        if len(numeric_columns) >= 2:
            for i in range(len(numeric_columns)):
                for j in range(i+1, len(numeric_columns)):
                    col1, col2 = numeric_columns[i], numeric_columns[j]
                    df[f'{col1}_{col2}_product'] = df[col1] * df[col2]
                    df[f'{col1}_{col2}_ratio'] = df[col1] / (df[col2] + 1e-8)
        
        # 创建多项式特征
        for col in numeric_columns[:3]:  # 限制特征数量
            df[f'{col}_squared'] = df[col] ** 2
            df[f'{col}_cubed'] = df[col] ** 3
        
        return df

# 使用示例
data_engineer = DataEngineering()

# 加载数据
df = data_engineer.load_data_efficiently('data.csv')

# 处理缺失值
df = data_engineer.handle_missing_values(df, strategy='auto')

# 检测异常值
outliers = data_engineer.detect_outliers(df, method='iqr')

# 特征工程
df = data_engineer.feature_engineering(df)
```

### 1.2 数据可视化与分析

```python
import matplotlib.pyplot as plt
import seaborn as sns
from typing import List, Optional
import plotly.express as px
import plotly.graph_objects as go

class DataVisualization:
    """数据可视化最佳实践"""
    
    def __init__(self):
        plt.style.use('seaborn-v0_8')
        sns.set_palette("husl")
    
    def plot_distribution(self, df: pd.DataFrame, columns: List[str], 
                         plot_type: str = 'histogram'):
        """绘制分布图"""
        fig, axes = plt.subplots(1, len(columns), figsize=(5*len(columns), 4))
        
        if len(columns) == 1:
            axes = [axes]
        
        for i, col in enumerate(columns):
            if plot_type == 'histogram':
                axes[i].hist(df[col].dropna(), bins=30, alpha=0.7)
            elif plot_type == 'box':
                axes[i].boxplot(df[col].dropna())
            elif plot_type == 'violin':
                axes[i].violinplot(df[col].dropna())
            
            axes[i].set_title(f'{col} Distribution')
            axes[i].set_xlabel(col)
        
        plt.tight_layout()
        plt.show()
    
    def plot_correlation_matrix(self, df: pd.DataFrame, 
                              method: str = 'pearson'):
        """绘制相关性矩阵"""
        numeric_df = df.select_dtypes(include=[np.number])
        correlation_matrix = numeric_df.corr(method=method)
        
        plt.figure(figsize=(10, 8))
        sns.heatmap(correlation_matrix, annot=True, cmap='coolwarm', 
                   center=0, square=True)
        plt.title(f'{method.capitalize()} Correlation Matrix')
        plt.tight_layout()
        plt.show()
    
    def plot_feature_importance(self, feature_names: List[str], 
                               importance_scores: List[float], 
                               top_n: int = 20):
        """绘制特征重要性"""
        # 排序并选择前N个特征
        sorted_indices = np.argsort(importance_scores)[::-1][:top_n]
        sorted_features = [feature_names[i] for i in sorted_indices]
        sorted_scores = [importance_scores[i] for i in sorted_indices]
        
        plt.figure(figsize=(10, 8))
        plt.barh(range(len(sorted_features)), sorted_scores)
        plt.yticks(range(len(sorted_features)), sorted_features)
        plt.xlabel('Feature Importance')
        plt.title('Top Feature Importance')
        plt.gca().invert_yaxis()
        plt.tight_layout()
        plt.show()
    
    def interactive_scatter_plot(self, df: pd.DataFrame, x_col: str, 
                                y_col: str, color_col: Optional[str] = None):
        """交互式散点图"""
        fig = px.scatter(df, x=x_col, y=y_col, color=color_col,
                        title=f'{x_col} vs {y_col}')
        fig.show()

# 使用示例
viz = DataVisualization()

# 绘制分布图
viz.plot_distribution(df, ['age', 'income'], plot_type='histogram')

# 绘制相关性矩阵
viz.plot_correlation_matrix(df)

# 交互式散点图
viz.interactive_scatter_plot(df, 'age', 'income', 'gender')
```

## 2. 模型开发

### 2.1 模型选择与评估

```python
from sklearn.ensemble import RandomForestClassifier, GradientBoostingClassifier
from sklearn.linear_model import LogisticRegression, LinearRegression
from sklearn.svm import SVC, SVR
from sklearn.metrics import classification_report, confusion_matrix, roc_auc_score
from sklearn.model_selection import cross_val_score, GridSearchCV
import xgboost as xgb
import lightgbm as lgb

class ModelDevelopment:
    """模型开发最佳实践"""
    
    def __init__(self):
        self.models = {
            'classification': {
                'logistic_regression': LogisticRegression(random_state=42),
                'random_forest': RandomForestClassifier(random_state=42),
                'gradient_boosting': GradientBoostingClassifier(random_state=42),
                'xgboost': xgb.XGBClassifier(random_state=42),
                'lightgbm': lgb.LGBMClassifier(random_state=42),
                'svm': SVC(random_state=42, probability=True)
            },
            'regression': {
                'linear_regression': LinearRegression(),
                'random_forest': RandomForestRegressor(random_state=42),
                'gradient_boosting': GradientBoostingRegressor(random_state=42),
                'xgboost': xgb.XGBRegressor(random_state=42),
                'lightgbm': lgb.LGBMRegressor(random_state=42),
                'svr': SVR()
            }
        }
    
    def compare_models(self, X_train: np.ndarray, X_test: np.ndarray,
                      y_train: np.ndarray, y_test: np.ndarray,
                      task_type: str = 'classification') -> Dict[str, float]:
        """比较多个模型性能"""
        results = {}
        
        for name, model in self.models[task_type].items():
            # 训练模型
            model.fit(X_train, y_train)
            
            # 预测
            y_pred = model.predict(X_test)
            
            # 评估
            if task_type == 'classification':
                score = roc_auc_score(y_test, y_pred)
            else:
                score = model.score(X_test, y_test)
            
            results[name] = score
        
        return results
    
    def hyperparameter_tuning(self, model, param_grid: Dict[str, List],
                             X_train: np.ndarray, y_train: np.ndarray,
                             cv: int = 5) -> Dict[str, Any]:
        """超参数调优"""
        grid_search = GridSearchCV(
            model, param_grid, cv=cv, scoring='roc_auc' if hasattr(model, 'predict_proba') else 'r2',
            n_jobs=-1, verbose=1
        )
        grid_search.fit(X_train, y_train)
        
        return {
            'best_params': grid_search.best_params_,
            'best_score': grid_search.best_score_,
            'best_model': grid_search.best_estimator_
        }
    
    def evaluate_model(self, model, X_test: np.ndarray, y_test: np.ndarray,
                      task_type: str = 'classification') -> Dict[str, Any]:
        """模型评估"""
        y_pred = model.predict(X_test)
        
        if task_type == 'classification':
            y_pred_proba = model.predict_proba(X_test)[:, 1] if hasattr(model, 'predict_proba') else None
            
            results = {
                'classification_report': classification_report(y_test, y_pred),
                'confusion_matrix': confusion_matrix(y_test, y_pred),
                'roc_auc_score': roc_auc_score(y_test, y_pred_proba) if y_pred_proba is not None else None
            }
        else:
            results = {
                'r2_score': model.score(X_test, y_test),
                'mse': np.mean((y_test - y_pred) ** 2),
                'mae': np.mean(np.abs(y_test - y_pred))
            }
        
        return results

# 使用示例
model_dev = ModelDevelopment()

# 准备数据
X = df.drop('target', axis=1)
y = df['target']
X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)

# 比较模型
results = model_dev.compare_models(X_train, X_test, y_train, y_test, 'classification')

# 超参数调优
param_grid = {
    'n_estimators': [100, 200, 300],
    'max_depth': [3, 5, 7, None],
    'min_samples_split': [2, 5, 10]
}

best_model_info = model_dev.hyperparameter_tuning(
    RandomForestClassifier(random_state=42),
    param_grid, X_train, y_train
)

# 评估最佳模型
evaluation = model_dev.evaluate_model(
    best_model_info['best_model'], X_test, y_test, 'classification'
)
```

### 2.2 深度学习模型

```python
import torch
import torch.nn as nn
import torch.optim as optim
from torch.utils.data import DataLoader, TensorDataset
from sklearn.preprocessing import StandardScaler
import numpy as np

class DeepLearningModel:
    """深度学习模型最佳实践"""
    
    def __init__(self, input_size: int, hidden_sizes: List[int], 
                 output_size: int, dropout_rate: float = 0.2):
        self.input_size = input_size
        self.hidden_sizes = hidden_sizes
        self.output_size = output_size
        self.dropout_rate = dropout_rate
        
        self.model = self._build_model()
        self.device = torch.device('cuda' if torch.cuda.is_available() else 'cpu')
        self.model.to(self.device)
    
    def _build_model(self) -> nn.Module:
        """构建神经网络"""
        layers = []
        prev_size = self.input_size
        
        for hidden_size in self.hidden_sizes:
            layers.extend([
                nn.Linear(prev_size, hidden_size),
                nn.ReLU(),
                nn.Dropout(self.dropout_rate),
                nn.BatchNorm1d(hidden_size)
            ])
            prev_size = hidden_size
        
        layers.append(nn.Linear(prev_size, self.output_size))
        
        if self.output_size == 1:
            layers.append(nn.Sigmoid())
        else:
            layers.append(nn.Softmax(dim=1))
        
        return nn.Sequential(*layers)
    
    def prepare_data(self, X: np.ndarray, y: np.ndarray, 
                     batch_size: int = 32) -> DataLoader:
        """准备数据加载器"""
        # 标准化特征
        scaler = StandardScaler()
        X_scaled = scaler.fit_transform(X)
        
        # 转换为张量
        X_tensor = torch.FloatTensor(X_scaled)
        y_tensor = torch.FloatTensor(y).reshape(-1, 1)
        
        # 创建数据集和数据加载器
        dataset = TensorDataset(X_tensor, y_tensor)
        dataloader = DataLoader(dataset, batch_size=batch_size, shuffle=True)
        
        return dataloader, scaler
    
    def train(self, train_loader: DataLoader, epochs: int = 100,
              learning_rate: float = 0.001) -> List[float]:
        """训练模型"""
        criterion = nn.BCELoss()
        optimizer = optim.Adam(self.model.parameters(), lr=learning_rate)
        scheduler = optim.lr_scheduler.ReduceLROnPlateau(optimizer, patience=10)
        
        train_losses = []
        
        for epoch in range(epochs):
            self.model.train()
            epoch_loss = 0
            
            for batch_X, batch_y in train_loader:
                batch_X, batch_y = batch_X.to(self.device), batch_y.to(self.device)
                
                optimizer.zero_grad()
                outputs = self.model(batch_X)
                loss = criterion(outputs, batch_y)
                loss.backward()
                optimizer.step()
                
                epoch_loss += loss.item()
            
            avg_loss = epoch_loss / len(train_loader)
            train_losses.append(avg_loss)
            scheduler.step(avg_loss)
            
            if epoch % 10 == 0:
                print(f'Epoch {epoch}, Loss: {avg_loss:.4f}')
        
        return train_losses
    
    def predict(self, X: np.ndarray, scaler: StandardScaler) -> np.ndarray:
        """预测"""
        self.model.eval()
        X_scaled = scaler.transform(X)
        X_tensor = torch.FloatTensor(X_scaled).to(self.device)
        
        with torch.no_grad():
            predictions = self.model(X_tensor)
        
        return predictions.cpu().numpy()

# 使用示例
# 准备数据
X = df.drop('target', axis=1).values
y = df['target'].values
X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)

# 创建深度学习模型
dl_model = DeepLearningModel(
    input_size=X_train.shape[1],
    hidden_sizes=[128, 64, 32],
    output_size=1
)

# 准备数据加载器
train_loader, scaler = dl_model.prepare_data(X_train, y_train, batch_size=32)

# 训练模型
losses = dl_model.train(train_loader, epochs=50)

# 预测
predictions = dl_model.predict(X_test, scaler)
```

## 3. 模型部署与生产

### 3.1 模型序列化与部署

```python
import pickle
import joblib
import json
from typing import Any, Dict
import mlflow
import mlflow.sklearn

class ModelDeployment:
    """模型部署最佳实践"""
    
    def __init__(self):
        self.model = None
        self.scaler = None
        self.feature_names = None
    
    def save_model(self, model: Any, scaler: Any, feature_names: List[str],
                   filepath: str, format: str = 'pickle'):
        """保存模型"""
        if format == 'pickle':
            with open(filepath, 'wb') as f:
                pickle.dump({
                    'model': model,
                    'scaler': scaler,
                    'feature_names': feature_names
                }, f)
        
        elif format == 'joblib':
            joblib.dump({
                'model': model,
                'scaler': scaler,
                'feature_names': feature_names
            }, filepath)
        
        elif format == 'mlflow':
            mlflow.sklearn.log_model(model, "model")
            mlflow.log_artifact(scaler, "scaler")
            mlflow.log_param("feature_names", json.dumps(feature_names))
    
    def load_model(self, filepath: str, format: str = 'pickle') -> Dict[str, Any]:
        """加载模型"""
        if format == 'pickle':
            with open(filepath, 'rb') as f:
                model_data = pickle.load(f)
        
        elif format == 'joblib':
            model_data = joblib.load(filepath)
        
        self.model = model_data['model']
        self.scaler = model_data['scaler']
        self.feature_names = model_data['feature_names']
        
        return model_data
    
    def predict_single(self, features: Dict[str, Any]) -> float:
        """单样本预测"""
        # 确保特征顺序正确
        feature_vector = []
        for feature_name in self.feature_names:
            feature_vector.append(features.get(feature_name, 0))
        
        # 转换为numpy数组
        X = np.array([feature_vector])
        
        # 标准化
        X_scaled = self.scaler.transform(X)
        
        # 预测
        prediction = self.model.predict(X_scaled)[0]
        
        return prediction
    
    def predict_batch(self, features_list: List[Dict[str, Any]]) -> List[float]:
        """批量预测"""
        predictions = []
        
        for features in features_list:
            prediction = self.predict_single(features)
            predictions.append(prediction)
        
        return predictions

# 使用示例
deployment = ModelDeployment()

# 保存模型
deployment.save_model(
    model=best_model_info['best_model'],
    scaler=scaler,
    feature_names=list(X.columns),
    filepath='model.pkl',
    format='pickle'
)

# 加载模型
model_data = deployment.load_model('model.pkl', format='pickle')

# 单样本预测
sample_features = {
    'age': 30,
    'income': 50000,
    'education': 'bachelor'
}
prediction = deployment.predict_single(sample_features)
```

### 3.2 API服务开发

```python
from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
from typing import List, Dict, Any
import uvicorn

class PredictionRequest(BaseModel):
    """预测请求模型"""
    features: Dict[str, Any]

class PredictionResponse(BaseModel):
    """预测响应模型"""
    prediction: float
    confidence: float
    model_version: str

class MLAPI:
    """机器学习API服务"""
    
    def __init__(self, model_path: str):
        self.app = FastAPI(title="ML Prediction API")
        self.deployment = ModelDeployment()
        self.model_data = self.deployment.load_model(model_path)
        self.model_version = "1.0.0"
        
        self._setup_routes()
    
    def _setup_routes(self):
        """设置API路由"""
        
        @self.app.post("/predict", response_model=PredictionResponse)
        async def predict(request: PredictionRequest):
            try:
                prediction = self.deployment.predict_single(request.features)
                
                # 计算置信度（这里使用简单的启发式方法）
                confidence = 0.8  # 实际应用中需要更复杂的置信度计算
                
                return PredictionResponse(
                    prediction=float(prediction),
                    confidence=confidence,
                    model_version=self.model_version
                )
            
            except Exception as e:
                raise HTTPException(status_code=400, detail=str(e))
        
        @self.app.get("/health")
        async def health_check():
            return {"status": "healthy", "model_version": self.model_version}
        
        @self.app.get("/model_info")
        async def model_info():
            return {
                "model_type": type(self.deployment.model).__name__,
                "feature_names": self.deployment.feature_names,
                "model_version": self.model_version
            }
    
    def run(self, host: str = "0.0.0.0", port: int = 8000):
        """运行API服务"""
        uvicorn.run(self.app, host=host, port=port)

# 使用示例
api = MLAPI("model.pkl")

# 运行API服务
# api.run(host="0.0.0.0", port=8000)
```

## 4. 模型监控与维护

### 4.1 模型性能监控

```python
import time
from datetime import datetime, timedelta
from typing import Dict, List, Any
import logging

class ModelMonitoring:
    """模型监控最佳实践"""
    
    def __init__(self):
        self.predictions_log = []
        self.performance_metrics = {}
        self.setup_logging()
    
    def setup_logging(self):
        """设置日志"""
        logging.basicConfig(
            level=logging.INFO,
            format='%(asctime)s - %(levelname)s - %(message)s',
            handlers=[
                logging.FileHandler('model_monitoring.log'),
                logging.StreamHandler()
            ]
        )
        self.logger = logging.getLogger(__name__)
    
    def log_prediction(self, features: Dict[str, Any], prediction: float,
                      actual: float = None, timestamp: datetime = None):
        """记录预测"""
        if timestamp is None:
            timestamp = datetime.now()
        
        log_entry = {
            'timestamp': timestamp,
            'features': features,
            'prediction': prediction,
            'actual': actual,
            'error': abs(prediction - actual) if actual is not None else None
        }
        
        self.predictions_log.append(log_entry)
        self.logger.info(f"Prediction logged: {prediction}")
    
    def calculate_performance_metrics(self, window_days: int = 30) -> Dict[str, float]:
        """计算性能指标"""
        cutoff_time = datetime.now() - timedelta(days=window_days)
        recent_predictions = [
            entry for entry in self.predictions_log
            if entry['timestamp'] >= cutoff_time and entry['actual'] is not None
        ]
        
        if not recent_predictions:
            return {}
        
        errors = [entry['error'] for entry in recent_predictions]
        
        metrics = {
            'mae': np.mean(errors),
            'rmse': np.sqrt(np.mean(np.array(errors) ** 2)),
            'prediction_count': len(recent_predictions),
            'avg_prediction': np.mean([entry['prediction'] for entry in recent_predictions])
        }
        
        return metrics
    
    def detect_data_drift(self, reference_data: pd.DataFrame,
                          current_data: pd.DataFrame) -> Dict[str, float]:
        """检测数据漂移"""
        drift_metrics = {}
        
        for column in reference_data.columns:
            if column in current_data.columns:
                # 计算分布差异
                ref_mean = reference_data[column].mean()
                curr_mean = current_data[column].mean()
                
                drift_metrics[f'{column}_mean_drift'] = abs(curr_mean - ref_mean) / ref_mean
        
        return drift_metrics
    
    def generate_monitoring_report(self) -> Dict[str, Any]:
        """生成监控报告"""
        performance_metrics = self.calculate_performance_metrics()
        
        report = {
            'timestamp': datetime.now(),
            'performance_metrics': performance_metrics,
            'total_predictions': len(self.predictions_log),
            'recent_predictions': len([
                entry for entry in self.predictions_log
                if entry['timestamp'] >= datetime.now() - timedelta(hours=24)
            ])
        }
        
        return report

# 使用示例
monitoring = ModelMonitoring()

# 记录预测
monitoring.log_prediction(
    features={'age': 30, 'income': 50000},
    prediction=0.75,
    actual=0.8
)

# 计算性能指标
metrics = monitoring.calculate_performance_metrics()

# 生成监控报告
report = monitoring.generate_monitoring_report()
```

### 4.2 模型重训练策略

```python
from sklearn.metrics import mean_squared_error
from typing import Callable, Optional

class ModelRetraining:
    """模型重训练策略"""
    
    def __init__(self, model, retraining_threshold: float = 0.1):
        self.model = model
        self.retraining_threshold = retraining_threshold
        self.baseline_performance = None
    
    def set_baseline_performance(self, X_test: np.ndarray, y_test: np.ndarray):
        """设置基线性能"""
        y_pred = self.model.predict(X_test)
        self.baseline_performance = mean_squared_error(y_test, y_pred)
    
    def should_retrain(self, current_performance: float) -> bool:
        """判断是否需要重训练"""
        if self.baseline_performance is None:
            return False
        
        performance_degradation = (self.baseline_performance - current_performance) / self.baseline_performance
        
        return performance_degradation > self.retraining_threshold
    
    def retrain_model(self, X_train: np.ndarray, y_train: np.ndarray,
                     X_test: np.ndarray, y_test: np.ndarray) -> Dict[str, Any]:
        """重训练模型"""
        # 重训练模型
        self.model.fit(X_train, y_train)
        
        # 评估新性能
        y_pred = self.model.predict(X_test)
        new_performance = mean_squared_error(y_test, y_pred)
        
        # 更新基线性能
        self.baseline_performance = new_performance
        
        return {
            'new_performance': new_performance,
            'performance_improvement': self.baseline_performance - new_performance
        }

# 使用示例
retraining = ModelRetraining(best_model_info['best_model'])

# 设置基线性能
retraining.set_baseline_performance(X_test, y_test)

# 检查是否需要重训练
current_performance = 0.15  # 假设当前性能
should_retrain = retraining.should_retrain(current_performance)

if should_retrain:
    retraining_result = retraining.retrain_model(X_train, y_train, X_test, y_test)
```

## 5. 实验管理

### 5.1 MLflow实验跟踪

```python
import mlflow
import mlflow.sklearn
from sklearn.metrics import accuracy_score, precision_score, recall_score, f1_score

class ExperimentTracking:
    """实验跟踪最佳实践"""
    
    def __init__(self, experiment_name: str = "ml_experiment"):
        mlflow.set_experiment(experiment_name)
        self.experiment_name = experiment_name
    
    def log_experiment(self, model, X_train: np.ndarray, X_test: np.ndarray,
                      y_train: np.ndarray, y_test: np.ndarray,
                      model_name: str, parameters: Dict[str, Any]):
        """记录实验"""
        with mlflow.start_run():
            # 记录参数
            mlflow.log_params(parameters)
            
            # 训练模型
            model.fit(X_train, y_train)
            
            # 预测
            y_pred = model.predict(X_test)
            
            # 计算指标
            metrics = {
                'accuracy': accuracy_score(y_test, y_pred),
                'precision': precision_score(y_test, y_pred, average='weighted'),
                'recall': recall_score(y_test, y_pred, average='weighted'),
                'f1_score': f1_score(y_test, y_pred, average='weighted')
            }
            
            # 记录指标
            mlflow.log_metrics(metrics)
            
            # 记录模型
            mlflow.sklearn.log_model(model, "model")
            
            # 记录特征重要性（如果可用）
            if hasattr(model, 'feature_importances_'):
                feature_importance = dict(zip(X_train.columns, model.feature_importances_))
                mlflow.log_dict(feature_importance, "feature_importance.json")
    
    def compare_experiments(self, experiment_name: str = None) -> pd.DataFrame:
        """比较实验"""
        if experiment_name is None:
            experiment_name = self.experiment_name
        
        # 获取实验运行记录
        experiment = mlflow.get_experiment_by_name(experiment_name)
        runs = mlflow.search_runs(experiment.experiment_id)
        
        return runs

# 使用示例
tracking = ExperimentTracking("classification_experiment")

# 记录随机森林实验
rf_params = {
    'n_estimators': 100,
    'max_depth': 10,
    'random_state': 42
}

tracking.log_experiment(
    model=RandomForestClassifier(**rf_params),
    X_train=X_train, X_test=X_test,
    y_train=y_train, y_test=y_test,
    model_name="RandomForest",
    parameters=rf_params
)

# 比较实验
experiment_comparison = tracking.compare_experiments()
```

---

## 总结

Python机器学习最佳实践指南涵盖了以下关键领域：

1. **数据工程基础**：数据加载、预处理、可视化和分析
2. **模型开发**：模型选择、评估、超参数调优和深度学习
3. **模型部署与生产**：模型序列化、API服务开发
4. **模型监控与维护**：性能监控、数据漂移检测、重训练策略
5. **实验管理**：MLflow实验跟踪和比较

通过这些最佳实践，开发者可以：
- 构建高质量的机器学习模型
- 实现高效的模型部署和监控
- 建立可重复的实验流程
- 确保模型在生产环境中的稳定性

建议根据具体项目需求选择合适的实践，并持续优化和改进。 