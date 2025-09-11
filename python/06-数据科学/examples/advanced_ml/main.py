#!/usr/bin/env python3
"""
高级机器学习示例
展示scikit-learn、pandas、numpy等库的高级功能
"""

import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns
from sklearn.model_selection import train_test_split, cross_val_score, GridSearchCV
from sklearn.ensemble import RandomForestClassifier, GradientBoostingClassifier
from sklearn.linear_model import LogisticRegression
from sklearn.svm import SVC
from sklearn.metrics import classification_report, confusion_matrix, roc_auc_score, roc_curve
from sklearn.preprocessing import StandardScaler, LabelEncoder, OneHotEncoder
from sklearn.pipeline import Pipeline
from sklearn.compose import ColumnTransformer
from sklearn.impute import SimpleImputer
from sklearn.feature_selection import SelectKBest, f_classif
from sklearn.decomposition import PCA
from sklearn.cluster import KMeans
from sklearn.manifold import TSNE
import joblib
import json
from typing import Dict, List, Tuple, Any, Optional
from dataclasses import dataclass, asdict
from datetime import datetime
import warnings
warnings.filterwarnings('ignore')

# 设置中文字体
plt.rcParams['font.sans-serif'] = ['SimHei', 'DejaVu Sans']
plt.rcParams['axes.unicode_minus'] = False

@dataclass
class ModelResult:
    """模型结果"""
    model_name: str
    accuracy: float
    precision: float
    recall: float
    f1_score: float
    auc_score: float
    training_time: float
    prediction_time: float
    cross_val_scores: List[float]
    feature_importance: Optional[Dict[str, float]] = None

class AdvancedMLPipeline:
    """高级机器学习管道"""
    
    def __init__(self):
        self.data: Optional[pd.DataFrame] = None
        self.X_train: Optional[pd.DataFrame] = None
        self.X_test: Optional[pd.DataFrame] = None
        self.y_train: Optional[pd.Series] = None
        self.y_test: Optional[pd.Series] = None
        self.models: Dict[str, Any] = {}
        self.results: Dict[str, ModelResult] = {}
        self.scaler = StandardScaler()
        self.preprocessor = None
    
    def load_sample_data(self) -> pd.DataFrame:
        """加载示例数据"""
        print("生成示例数据...")
        
        np.random.seed(42)
        n_samples = 1000
        
        # 生成特征数据
        data = {
            'age': np.random.randint(18, 80, n_samples),
            'income': np.random.normal(50000, 20000, n_samples),
            'education_years': np.random.randint(8, 20, n_samples),
            'experience_years': np.random.randint(0, 40, n_samples),
            'gender': np.random.choice(['Male', 'Female'], n_samples),
            'marital_status': np.random.choice(['Single', 'Married', 'Divorced'], n_samples),
            'city': np.random.choice(['Beijing', 'Shanghai', 'Guangzhou', 'Shenzhen'], n_samples),
            'credit_score': np.random.randint(300, 850, n_samples),
            'loan_amount': np.random.normal(100000, 50000, n_samples),
            'debt_ratio': np.random.uniform(0.1, 0.8, n_samples),
        }
        
        # 生成目标变量（基于特征的逻辑关系）
        df = pd.DataFrame(data)
        
        # 创建目标变量：是否获得贷款批准
        # 基于多个特征的组合逻辑
        loan_approved = (
            (df['income'] > 40000) &
            (df['credit_score'] > 600) &
            (df['debt_ratio'] < 0.5) &
            (df['education_years'] > 12)
        ).astype(int)
        
        # 添加一些随机性
        noise = np.random.random(n_samples) < 0.1
        loan_approved = loan_approved ^ noise
        
        df['loan_approved'] = loan_approved
        
        self.data = df
        print(f"数据加载完成，形状: {df.shape}")
        return df
    
    def explore_data(self):
        """数据探索"""
        if self.data is None:
            raise ValueError("数据未加载")
        
        print("=== 数据探索 ===")
        
        # 基本信息
        print("\n1. 数据基本信息:")
        print(f"数据形状: {self.data.shape}")
        print(f"数据类型:\n{self.data.dtypes}")
        print(f"缺失值:\n{self.data.isnull().sum()}")
        
        # 描述性统计
        print("\n2. 描述性统计:")
        print(self.data.describe())
        
        # 目标变量分布
        print("\n3. 目标变量分布:")
        target_dist = self.data['loan_approved'].value_counts()
        print(target_dist)
        print(f"正例比例: {target_dist[1] / len(self.data):.2%}")
        
        # 相关性分析
        print("\n4. 特征相关性:")
        numeric_cols = self.data.select_dtypes(include=[np.number]).columns
        correlation_matrix = self.data[numeric_cols].corr()
        print(correlation_matrix['loan_approved'].sort_values(ascending=False))
        
        # 可视化
        self._create_exploration_plots()
    
    def _create_exploration_plots(self):
        """创建探索性分析图表"""
        fig, axes = plt.subplots(2, 3, figsize=(18, 12))
        
        # 目标变量分布
        self.data['loan_approved'].value_counts().plot(kind='bar', ax=axes[0, 0])
        axes[0, 0].set_title('目标变量分布')
        axes[0, 0].set_xlabel('贷款批准')
        axes[0, 0].set_ylabel('数量')
        
        # 年龄分布
        self.data['age'].hist(bins=30, ax=axes[0, 1], alpha=0.7)
        axes[0, 1].set_title('年龄分布')
        axes[0, 1].set_xlabel('年龄')
        axes[0, 1].set_ylabel('频次')
        
        # 收入分布
        self.data['income'].hist(bins=30, ax=axes[0, 2], alpha=0.7)
        axes[0, 2].set_title('收入分布')
        axes[0, 2].set_xlabel('收入')
        axes[0, 2].set_ylabel('频次')
        
        # 性别与贷款批准的关系
        gender_loan = pd.crosstab(self.data['gender'], self.data['loan_approved'])
        gender_loan.plot(kind='bar', ax=axes[1, 0])
        axes[1, 0].set_title('性别与贷款批准')
        axes[1, 0].set_xlabel('性别')
        axes[1, 0].set_ylabel('数量')
        axes[1, 0].legend(['未批准', '批准'])
        
        # 收入与贷款批准的关系
        self.data.boxplot(column='income', by='loan_approved', ax=axes[1, 1])
        axes[1, 1].set_title('收入与贷款批准')
        axes[1, 1].set_xlabel('贷款批准')
        axes[1, 1].set_ylabel('收入')
        
        # 相关性热力图
        numeric_cols = self.data.select_dtypes(include=[np.number]).columns
        correlation_matrix = self.data[numeric_cols].corr()
        sns.heatmap(correlation_matrix, annot=True, cmap='coolwarm', center=0,
                   square=True, fmt='.2f', ax=axes[1, 2])
        axes[1, 2].set_title('特征相关性热力图')
        
        plt.tight_layout()
        plt.show()
    
    def preprocess_data(self):
        """数据预处理"""
        if self.data is None:
            raise ValueError("数据未加载")
        
        print("=== 数据预处理 ===")
        
        # 分离特征和目标
        X = self.data.drop('loan_approved', axis=1)
        y = self.data['loan_approved']
        
        # 分离数值型和分类型特征
        numeric_features = X.select_dtypes(include=[np.number]).columns.tolist()
        categorical_features = X.select_dtypes(include=['object']).columns.tolist()
        
        print(f"数值型特征: {numeric_features}")
        print(f"分类型特征: {categorical_features}")
        
        # 创建预处理管道
        numeric_transformer = Pipeline(steps=[
            ('imputer', SimpleImputer(strategy='median')),
            ('scaler', StandardScaler())
        ])
        
        categorical_transformer = Pipeline(steps=[
            ('imputer', SimpleImputer(strategy='constant', fill_value='missing')),
            ('onehot', OneHotEncoder(handle_unknown='ignore'))
        ])
        
        self.preprocessor = ColumnTransformer(
            transformers=[
                ('num', numeric_transformer, numeric_features),
                ('cat', categorical_transformer, categorical_features)
            ]
        )
        
        # 应用预处理
        X_processed = self.preprocessor.fit_transform(X)
        
        # 分割数据
        self.X_train, self.X_test, self.y_train, self.y_test = train_test_split(
            X_processed, y, test_size=0.2, random_state=42, stratify=y
        )
        
        print(f"训练集形状: {self.X_train.shape}")
        print(f"测试集形状: {self.X_test.shape}")
        print(f"训练集目标分布: {np.bincount(self.y_train)}")
        print(f"测试集目标分布: {np.bincount(self.y_test)}")
    
    def train_models(self):
        """训练多个模型"""
        if self.X_train is None:
            raise ValueError("数据未预处理")
        
        print("=== 模型训练 ===")
        
        # 定义模型
        models = {
            'Logistic Regression': LogisticRegression(random_state=42, max_iter=1000),
            'Random Forest': RandomForestClassifier(n_estimators=100, random_state=42),
            'Gradient Boosting': GradientBoostingClassifier(n_estimators=100, random_state=42),
            'SVM': SVC(random_state=42, probability=True)
        }
        
        # 训练和评估每个模型
        for name, model in models.items():
            print(f"\n训练 {name}...")
            
            start_time = datetime.now()
            
            # 训练模型
            model.fit(self.X_train, self.y_train)
            
            training_time = (datetime.now() - start_time).total_seconds()
            
            # 预测
            start_time = datetime.now()
            y_pred = model.predict(self.X_test)
            y_pred_proba = model.predict_proba(self.X_test)[:, 1]
            prediction_time = (datetime.now() - start_time).total_seconds()
            
            # 交叉验证
            cv_scores = cross_val_score(model, self.X_train, self.y_train, cv=5)
            
            # 计算指标
            from sklearn.metrics import accuracy_score, precision_score, recall_score, f1_score
            
            accuracy = accuracy_score(self.y_test, y_pred)
            precision = precision_score(self.y_test, y_pred)
            recall = recall_score(self.y_test, y_pred)
            f1 = f1_score(self.y_test, y_pred)
            auc = roc_auc_score(self.y_test, y_pred_proba)
            
            # 特征重要性（如果模型支持）
            feature_importance = None
            if hasattr(model, 'feature_importances_'):
                feature_names = self._get_feature_names()
                feature_importance = dict(zip(feature_names, model.feature_importances_))
            elif hasattr(model, 'coef_'):
                feature_names = self._get_feature_names()
                feature_importance = dict(zip(feature_names, abs(model.coef_[0])))
            
            # 保存结果
            result = ModelResult(
                model_name=name,
                accuracy=accuracy,
                precision=precision,
                recall=recall,
                f1_score=f1,
                auc_score=auc,
                training_time=training_time,
                prediction_time=prediction_time,
                cross_val_scores=cv_scores.tolist(),
                feature_importance=feature_importance
            )
            
            self.models[name] = model
            self.results[name] = result
            
            print(f"准确率: {accuracy:.4f}")
            print(f"精确率: {precision:.4f}")
            print(f"召回率: {recall:.4f}")
            print(f"F1分数: {f1:.4f}")
            print(f"AUC: {auc:.4f}")
            print(f"交叉验证平均分数: {cv_scores.mean():.4f} (+/- {cv_scores.std() * 2:.4f})")
    
    def _get_feature_names(self) -> List[str]:
        """获取特征名称"""
        if self.preprocessor is None:
            return []
        
        feature_names = []
        
        # 数值型特征
        numeric_features = self.data.select_dtypes(include=[np.number]).columns.tolist()
        feature_names.extend(numeric_features)
        
        # 分类型特征（独热编码后）
        categorical_features = self.data.select_dtypes(include=['object']).columns.tolist()
        for feature in categorical_features:
            unique_values = self.data[feature].unique()
            for value in unique_values:
                feature_names.append(f"{feature}_{value}")
        
        return feature_names
    
    def hyperparameter_tuning(self, model_name: str = 'Random Forest'):
        """超参数调优"""
        if model_name not in self.models:
            raise ValueError(f"模型 {model_name} 不存在")
        
        print(f"=== {model_name} 超参数调优 ===")
        
        # 定义参数网格
        if model_name == 'Random Forest':
            param_grid = {
                'n_estimators': [50, 100, 200],
                'max_depth': [None, 10, 20, 30],
                'min_samples_split': [2, 5, 10],
                'min_samples_leaf': [1, 2, 4]
            }
            base_model = RandomForestClassifier(random_state=42)
        elif model_name == 'Gradient Boosting':
            param_grid = {
                'n_estimators': [50, 100, 200],
                'learning_rate': [0.01, 0.1, 0.2],
                'max_depth': [3, 5, 7],
                'subsample': [0.8, 0.9, 1.0]
            }
            base_model = GradientBoostingClassifier(random_state=42)
        else:
            print(f"模型 {model_name} 暂不支持超参数调优")
            return
        
        # 网格搜索
        grid_search = GridSearchCV(
            base_model, param_grid, cv=5, scoring='roc_auc', n_jobs=-1
        )
        
        grid_search.fit(self.X_train, self.y_train)
        
        print(f"最佳参数: {grid_search.best_params_}")
        print(f"最佳交叉验证分数: {grid_search.best_score_:.4f}")
        
        # 更新模型
        self.models[f"{model_name} (Tuned)"] = grid_search.best_estimator_
        
        # 评估调优后的模型
        y_pred = grid_search.predict(self.X_test)
        y_pred_proba = grid_search.predict_proba(self.X_test)[:, 1]
        
        from sklearn.metrics import accuracy_score, precision_score, recall_score, f1_score
        
        accuracy = accuracy_score(self.y_test, y_pred)
        precision = precision_score(self.y_test, y_pred)
        recall = recall_score(self.y_test, y_pred)
        f1 = f1_score(self.y_test, y_pred)
        auc = roc_auc_score(self.y_test, y_pred_proba)
        
        result = ModelResult(
            model_name=f"{model_name} (Tuned)",
            accuracy=accuracy,
            precision=precision,
            recall=recall,
            f1_score=f1,
            auc_score=auc,
            training_time=0,  # 网格搜索时间较长，这里不计算
            prediction_time=0,
            cross_val_scores=[grid_search.best_score_]
        )
        
        self.results[f"{model_name} (Tuned)"] = result
        
        print(f"调优后准确率: {accuracy:.4f}")
        print(f"调优后AUC: {auc:.4f}")
    
    def feature_selection(self, k: int = 10):
        """特征选择"""
        if self.X_train is None:
            raise ValueError("数据未预处理")
        
        print(f"=== 特征选择 (选择前{k}个特征) ===")
        
        # 使用SelectKBest进行特征选择
        selector = SelectKBest(score_func=f_classif, k=k)
        X_train_selected = selector.fit_transform(self.X_train, self.y_train)
        X_test_selected = selector.transform(self.X_test)
        
        # 获取选中的特征
        feature_names = self._get_feature_names()
        selected_features = [feature_names[i] for i in selector.get_support(indices=True)]
        
        print(f"选中的特征: {selected_features}")
        
        # 使用选中的特征训练模型
        model = RandomForestClassifier(n_estimators=100, random_state=42)
        model.fit(X_train_selected, self.y_train)
        
        y_pred = model.predict(X_test_selected)
        y_pred_proba = model.predict_proba(X_test_selected)[:, 1]
        
        from sklearn.metrics import accuracy_score, roc_auc_score
        
        accuracy = accuracy_score(self.y_test, y_pred)
        auc = roc_auc_score(self.y_test, y_pred_proba)
        
        print(f"特征选择后准确率: {accuracy:.4f}")
        print(f"特征选择后AUC: {auc:.4f}")
        
        return selected_features
    
    def dimensionality_reduction(self):
        """降维分析"""
        if self.X_train is None:
            raise ValueError("数据未预处理")
        
        print("=== 降维分析 ===")
        
        # PCA降维
        pca = PCA(n_components=2)
        X_pca = pca.fit_transform(self.X_train)
        
        print(f"PCA解释方差比: {pca.explained_variance_ratio_}")
        print(f"累计解释方差比: {np.cumsum(pca.explained_variance_ratio_)}")
        
        # t-SNE降维
        tsne = TSNE(n_components=2, random_state=42)
        X_tsne = tsne.fit_transform(self.X_train)
        
        # 可视化降维结果
        fig, axes = plt.subplots(1, 2, figsize=(15, 6))
        
        # PCA可视化
        scatter = axes[0].scatter(X_pca[:, 0], X_pca[:, 1], c=self.y_train, cmap='viridis', alpha=0.6)
        axes[0].set_title('PCA降维可视化')
        axes[0].set_xlabel('第一主成分')
        axes[0].set_ylabel('第二主成分')
        plt.colorbar(scatter, ax=axes[0])
        
        # t-SNE可视化
        scatter = axes[1].scatter(X_tsne[:, 0], X_tsne[:, 1], c=self.y_train, cmap='viridis', alpha=0.6)
        axes[1].set_title('t-SNE降维可视化')
        axes[1].set_xlabel('t-SNE 1')
        axes[1].set_ylabel('t-SNE 2')
        plt.colorbar(scatter, ax=axes[1])
        
        plt.tight_layout()
        plt.show()
    
    def clustering_analysis(self):
        """聚类分析"""
        if self.X_train is None:
            raise ValueError("数据未预处理")
        
        print("=== 聚类分析 ===")
        
        # K-means聚类
        kmeans = KMeans(n_clusters=2, random_state=42)
        cluster_labels = kmeans.fit_predict(self.X_train)
        
        # 分析聚类结果
        cluster_df = pd.DataFrame({
            'cluster': cluster_labels,
            'target': self.y_train
        })
        
        print("聚类结果与目标变量的关系:")
        print(pd.crosstab(cluster_df['cluster'], cluster_df['target']))
        
        # 可视化聚类结果（使用PCA降维）
        pca = PCA(n_components=2)
        X_pca = pca.fit_transform(self.X_train)
        
        fig, axes = plt.subplots(1, 2, figsize=(15, 6))
        
        # 原始目标变量
        scatter = axes[0].scatter(X_pca[:, 0], X_pca[:, 1], c=self.y_train, cmap='viridis', alpha=0.6)
        axes[0].set_title('原始目标变量')
        axes[0].set_xlabel('第一主成分')
        axes[0].set_ylabel('第二主成分')
        plt.colorbar(scatter, ax=axes[0])
        
        # 聚类结果
        scatter = axes[1].scatter(X_pca[:, 0], X_pca[:, 1], c=cluster_labels, cmap='viridis', alpha=0.6)
        axes[1].set_title('K-means聚类结果')
        axes[1].set_xlabel('第一主成分')
        axes[1].set_ylabel('第二主成分')
        plt.colorbar(scatter, ax=axes[1])
        
        plt.tight_layout()
        plt.show()
    
    def model_evaluation(self):
        """模型评估和比较"""
        if not self.results:
            raise ValueError("没有训练好的模型")
        
        print("=== 模型评估和比较 ===")
        
        # 创建结果比较表
        comparison_data = []
        for name, result in self.results.items():
            comparison_data.append({
                '模型': name,
                '准确率': result.accuracy,
                '精确率': result.precision,
                '召回率': result.recall,
                'F1分数': result.f1_score,
                'AUC': result.auc_score,
                '训练时间(秒)': result.training_time,
                '预测时间(秒)': result.prediction_time
            })
        
        comparison_df = pd.DataFrame(comparison_data)
        print(comparison_df.round(4))
        
        # 可视化模型比较
        self._create_model_comparison_plots()
        
        # ROC曲线
        self._plot_roc_curves()
        
        # 特征重要性
        self._plot_feature_importance()
    
    def _create_model_comparison_plots(self):
        """创建模型比较图表"""
        fig, axes = plt.subplots(2, 2, figsize=(15, 12))
        
        # 准确率比较
        model_names = list(self.results.keys())
        accuracies = [self.results[name].accuracy for name in model_names]
        axes[0, 0].bar(model_names, accuracies)
        axes[0, 0].set_title('模型准确率比较')
        axes[0, 0].set_ylabel('准确率')
        axes[0, 0].tick_params(axis='x', rotation=45)
        
        # AUC比较
        aucs = [self.results[name].auc_score for name in model_names]
        axes[0, 1].bar(model_names, aucs)
        axes[0, 1].set_title('模型AUC比较')
        axes[0, 1].set_ylabel('AUC')
        axes[0, 1].tick_params(axis='x', rotation=45)
        
        # 训练时间比较
        training_times = [self.results[name].training_time for name in model_names]
        axes[1, 0].bar(model_names, training_times)
        axes[1, 0].set_title('模型训练时间比较')
        axes[1, 0].set_ylabel('训练时间(秒)')
        axes[1, 0].tick_params(axis='x', rotation=45)
        
        # 预测时间比较
        prediction_times = [self.results[name].prediction_time for name in model_names]
        axes[1, 1].bar(model_names, prediction_times)
        axes[1, 1].set_title('模型预测时间比较')
        axes[1, 1].set_ylabel('预测时间(秒)')
        axes[1, 1].tick_params(axis='x', rotation=45)
        
        plt.tight_layout()
        plt.show()
    
    def _plot_roc_curves(self):
        """绘制ROC曲线"""
        plt.figure(figsize=(10, 8))
        
        for name, model in self.models.items():
            y_pred_proba = model.predict_proba(self.X_test)[:, 1]
            fpr, tpr, _ = roc_curve(self.y_test, y_pred_proba)
            auc = roc_auc_score(self.y_test, y_pred_proba)
            
            plt.plot(fpr, tpr, label=f'{name} (AUC = {auc:.3f})')
        
        plt.plot([0, 1], [0, 1], 'k--', label='随机分类器')
        plt.xlabel('假正率')
        plt.ylabel('真正率')
        plt.title('ROC曲线比较')
        plt.legend()
        plt.grid(True)
        plt.show()
    
    def _plot_feature_importance(self):
        """绘制特征重要性"""
        # 找到有特征重要性的模型
        models_with_importance = []
        for name, result in self.results.items():
            if result.feature_importance is not None:
                models_with_importance.append((name, result.feature_importance))
        
        if not models_with_importance:
            print("没有模型提供特征重要性信息")
            return
        
        # 绘制特征重要性
        n_models = len(models_with_importance)
        fig, axes = plt.subplots(1, n_models, figsize=(5 * n_models, 8))
        
        if n_models == 1:
            axes = [axes]
        
        for i, (name, importance) in enumerate(models_with_importance):
            # 选择前10个最重要的特征
            sorted_features = sorted(importance.items(), key=lambda x: x[1], reverse=True)[:10]
            features, scores = zip(*sorted_features)
            
            axes[i].barh(features, scores)
            axes[i].set_title(f'{name} - 特征重要性')
            axes[i].set_xlabel('重要性分数')
        
        plt.tight_layout()
        plt.show()
    
    def save_models(self, directory: str = "models"):
        """保存模型"""
        import os
        os.makedirs(directory, exist_ok=True)
        
        print(f"=== 保存模型到 {directory} ===")
        
        for name, model in self.models.items():
            filename = f"{directory}/{name.replace(' ', '_').lower()}.joblib"
            joblib.dump(model, filename)
            print(f"保存模型: {filename}")
        
        # 保存预处理器
        if self.preprocessor is not None:
            joblib.dump(self.preprocessor, f"{directory}/preprocessor.joblib")
            print(f"保存预处理器: {directory}/preprocessor.joblib")
        
        # 保存结果
        results_data = {name: asdict(result) for name, result in self.results.items()}
        with open(f"{directory}/results.json", 'w') as f:
            json.dump(results_data, f, indent=2)
        print(f"保存结果: {directory}/results.json")
    
    def load_models(self, directory: str = "models"):
        """加载模型"""
        import os
        
        if not os.path.exists(directory):
            print(f"目录 {directory} 不存在")
            return
        
        print(f"=== 从 {directory} 加载模型 ===")
        
        # 加载预处理器
        preprocessor_file = f"{directory}/preprocessor.joblib"
        if os.path.exists(preprocessor_file):
            self.preprocessor = joblib.load(preprocessor_file)
            print(f"加载预处理器: {preprocessor_file}")
        
        # 加载结果
        results_file = f"{directory}/results.json"
        if os.path.exists(results_file):
            with open(results_file, 'r') as f:
                results_data = json.load(f)
            
            self.results = {}
            for name, data in results_data.items():
                self.results[name] = ModelResult(**data)
            print(f"加载结果: {results_file}")

def main():
    """主函数"""
    print("高级机器学习示例")
    print("=" * 50)
    
    # 创建ML管道
    ml_pipeline = AdvancedMLPipeline()
    
    # 1. 加载数据
    ml_pipeline.load_sample_data()
    
    # 2. 数据探索
    ml_pipeline.explore_data()
    
    # 3. 数据预处理
    ml_pipeline.preprocess_data()
    
    # 4. 训练模型
    ml_pipeline.train_models()
    
    # 5. 超参数调优
    ml_pipeline.hyperparameter_tuning('Random Forest')
    
    # 6. 特征选择
    ml_pipeline.feature_selection(k=10)
    
    # 7. 降维分析
    ml_pipeline.dimensionality_reduction()
    
    # 8. 聚类分析
    ml_pipeline.clustering_analysis()
    
    # 9. 模型评估
    ml_pipeline.model_evaluation()
    
    # 10. 保存模型
    ml_pipeline.save_models()
    
    print("\n机器学习流程完成!")

if __name__ == "__main__":
    main()
