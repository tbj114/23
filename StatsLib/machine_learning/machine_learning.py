import numpy as np
import pandas as pd
from sklearn.ensemble import RandomForestClassifier, RandomForestRegressor, GradientBoostingClassifier, GradientBoostingRegressor
from sklearn.svm import SVC, SVR
from sklearn.neural_network import MLPClassifier, MLPRegressor
from sklearn.model_selection import train_test_split, cross_val_score
from sklearn.metrics import accuracy_score, precision_score, recall_score, f1_score, mean_squared_error, r2_score
from sklearn.preprocessing import StandardScaler


class MachineLearning:
    @staticmethod
    def random_forest(X, y, task='classification', n_estimators=100, max_depth=None, test_size=0.2):
        """
        随机森林
        
        参数:
        X: array - 特征数据
        y: array - 目标变量
        task: str - 任务类型 ('classification', 'regression')
        n_estimators: int - 树的数量
        max_depth: int - 树的最大深度
        test_size: float - 测试集比例
        
        返回:
        dict - 随机森林结果
        """
        try:
            # 划分训练集和测试集
            X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=test_size)
            
            # 标准化数据
            scaler = StandardScaler()
            X_train_scaled = scaler.fit_transform(X_train)
            X_test_scaled = scaler.transform(X_test)
            
            # 选择模型
            if task == 'classification':
                model = RandomForestClassifier(n_estimators=n_estimators, max_depth=max_depth)
            else:
                model = RandomForestRegressor(n_estimators=n_estimators, max_depth=max_depth)
            
            # 训练模型
            model.fit(X_train_scaled, y_train)
            
            # 预测
            y_pred = model.predict(X_test_scaled)
            
            # 评估
            if task == 'classification':
                metrics = {
                    'accuracy': accuracy_score(y_test, y_pred),
                    'precision': precision_score(y_test, y_pred, average='weighted'),
                    'recall': recall_score(y_test, y_pred, average='weighted'),
                    'f1_score': f1_score(y_test, y_pred, average='weighted')
                }
            else:
                metrics = {
                    'mse': mean_squared_error(y_test, y_pred),
                    'rmse': np.sqrt(mean_squared_error(y_test, y_pred)),
                    'r2': r2_score(y_test, y_pred)
                }
            
            # 交叉验证
            cv_scores = cross_val_score(model, X, y, cv=5)
            
            return {
                'model': model,
                'metrics': metrics,
                'cv_scores': cv_scores.tolist(),
                'mean_cv_score': np.mean(cv_scores),
                'feature_importances': model.feature_importances_.tolist() if hasattr(model, 'feature_importances_') else None
            }
        except Exception as e:
            return {'error': str(e)}

    @staticmethod
    def support_vector_machine(X, y, task='classification', kernel='rbf', C=1.0, test_size=0.2):
        """
        支持向量机
        
        参数:
        X: array - 特征数据
        y: array - 目标变量
        task: str - 任务类型 ('classification', 'regression')
        kernel: str - 核函数类型
        C: float - 正则化参数
        test_size: float - 测试集比例
        
        返回:
        dict - 支持向量机结果
        """
        try:
            # 划分训练集和测试集
            X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=test_size)
            
            # 标准化数据
            scaler = StandardScaler()
            X_train_scaled = scaler.fit_transform(X_train)
            X_test_scaled = scaler.transform(X_test)
            
            # 选择模型
            if task == 'classification':
                model = SVC(kernel=kernel, C=C)
            else:
                model = SVR(kernel=kernel, C=C)
            
            # 训练模型
            model.fit(X_train_scaled, y_train)
            
            # 预测
            y_pred = model.predict(X_test_scaled)
            
            # 评估
            if task == 'classification':
                metrics = {
                    'accuracy': accuracy_score(y_test, y_pred),
                    'precision': precision_score(y_test, y_pred, average='weighted'),
                    'recall': recall_score(y_test, y_pred, average='weighted'),
                    'f1_score': f1_score(y_test, y_pred, average='weighted')
                }
            else:
                metrics = {
                    'mse': mean_squared_error(y_test, y_pred),
                    'rmse': np.sqrt(mean_squared_error(y_test, y_pred)),
                    'r2': r2_score(y_test, y_pred)
                }
            
            # 交叉验证
            cv_scores = cross_val_score(model, X, y, cv=5)
            
            return {
                'model': model,
                'metrics': metrics,
                'cv_scores': cv_scores.tolist(),
                'mean_cv_score': np.mean(cv_scores)
            }
        except Exception as e:
            return {'error': str(e)}

    @staticmethod
    def gradient_boosting(X, y, task='classification', n_estimators=100, learning_rate=0.1, max_depth=3, test_size=0.2):
        """
        梯度提升树
        
        参数:
        X: array - 特征数据
        y: array - 目标变量
        task: str - 任务类型 ('classification', 'regression')
        n_estimators: int - 树的数量
        learning_rate: float - 学习率
        max_depth: int - 树的最大深度
        test_size: float - 测试集比例
        
        返回:
        dict - 梯度提升树结果
        """
        try:
            # 划分训练集和测试集
            X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=test_size)
            
            # 标准化数据
            scaler = StandardScaler()
            X_train_scaled = scaler.fit_transform(X_train)
            X_test_scaled = scaler.transform(X_test)
            
            # 选择模型
            if task == 'classification':
                model = GradientBoostingClassifier(n_estimators=n_estimators, learning_rate=learning_rate, max_depth=max_depth)
            else:
                model = GradientBoostingRegressor(n_estimators=n_estimators, learning_rate=learning_rate, max_depth=max_depth)
            
            # 训练模型
            model.fit(X_train_scaled, y_train)
            
            # 预测
            y_pred = model.predict(X_test_scaled)
            
            # 评估
            if task == 'classification':
                metrics = {
                    'accuracy': accuracy_score(y_test, y_pred),
                    'precision': precision_score(y_test, y_pred, average='weighted'),
                    'recall': recall_score(y_test, y_pred, average='weighted'),
                    'f1_score': f1_score(y_test, y_pred, average='weighted')
                }
            else:
                metrics = {
                    'mse': mean_squared_error(y_test, y_pred),
                    'rmse': np.sqrt(mean_squared_error(y_test, y_pred)),
                    'r2': r2_score(y_test, y_pred)
                }
            
            # 交叉验证
            cv_scores = cross_val_score(model, X, y, cv=5)
            
            return {
                'model': model,
                'metrics': metrics,
                'cv_scores': cv_scores.tolist(),
                'mean_cv_score': np.mean(cv_scores),
                'feature_importances': model.feature_importances_.tolist() if hasattr(model, 'feature_importances_') else None
            }
        except Exception as e:
            return {'error': str(e)}

    @staticmethod
    def neural_network(X, y, task='classification', hidden_layer_sizes=(100,), activation='relu', solver='adam', test_size=0.2):
        """
        神经网络
        
        参数:
        X: array - 特征数据
        y: array - 目标变量
        task: str - 任务类型 ('classification', 'regression')
        hidden_layer_sizes: tuple - 隐藏层大小
        activation: str - 激活函数
        solver: str - 优化器
        test_size: float - 测试集比例
        
        返回:
        dict - 神经网络结果
        """
        try:
            # 划分训练集和测试集
            X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=test_size)
            
            # 标准化数据
            scaler = StandardScaler()
            X_train_scaled = scaler.fit_transform(X_train)
            X_test_scaled = scaler.transform(X_test)
            
            # 选择模型
            if task == 'classification':
                model = MLPClassifier(hidden_layer_sizes=hidden_layer_sizes, activation=activation, solver=solver, max_iter=1000)
            else:
                model = MLPRegressor(hidden_layer_sizes=hidden_layer_sizes, activation=activation, solver=solver, max_iter=1000)
            
            # 训练模型
            model.fit(X_train_scaled, y_train)
            
            # 预测
            y_pred = model.predict(X_test_scaled)
            
            # 评估
            if task == 'classification':
                metrics = {
                    'accuracy': accuracy_score(y_test, y_pred),
                    'precision': precision_score(y_test, y_pred, average='weighted'),
                    'recall': recall_score(y_test, y_pred, average='weighted'),
                    'f1_score': f1_score(y_test, y_pred, average='weighted')
                }
            else:
                metrics = {
                    'mse': mean_squared_error(y_test, y_pred),
                    'rmse': np.sqrt(mean_squared_error(y_test, y_pred)),
                    'r2': r2_score(y_test, y_pred)
                }
            
            # 交叉验证
            cv_scores = cross_val_score(model, X, y, cv=5)
            
            return {
                'model': model,
                'metrics': metrics,
                'cv_scores': cv_scores.tolist(),
                'mean_cv_score': np.mean(cv_scores)
            }
        except Exception as e:
            return {'error': str(e)}

    @staticmethod
    def text_mining(texts, task='classification', n_features=1000):
        """
        文本挖掘
        
        参数:
        texts: list - 文本列表
        task: str - 任务类型 ('classification', 'clustering')
        n_features: int - 特征数量
        
        返回:
        dict - 文本挖掘结果
        """
        try:
            from sklearn.feature_extraction.text import TfidfVectorizer
            from sklearn.cluster import KMeans
            
            # 文本向量化
            vectorizer = TfidfVectorizer(max_features=n_features)
            X = vectorizer.fit_transform(texts)
            
            if task == 'clustering':
                # K均值聚类
                kmeans = KMeans(n_clusters=5, random_state=42)
                clusters = kmeans.fit_predict(X)
                
                return {
                    'clusters': clusters.tolist(),
                    'feature_names': vectorizer.get_feature_names_out().tolist(),
                    'n_features': n_features
                }
            else:
                return {
                    'X': X.toarray().tolist(),
                    'feature_names': vectorizer.get_feature_names_out().tolist(),
                    'n_features': n_features
                }
        except Exception as e:
            return {'error': str(e)}

    @staticmethod
    def sentiment_analysis(texts):
        """
        情感分析
        
        参数:
        texts: list - 文本列表
        
        返回:
        dict - 情感分析结果
        """
        try:
            from textblob import TextBlob
            
            sentiments = []
            for text in texts:
                blob = TextBlob(text)
                sentiments.append({
                    'text': text,
                    'polarity': blob.sentiment.polarity,
                    'subjectivity': blob.sentiment.subjectivity
                })
            
            return {
                'sentiments': sentiments
            }
        except Exception as e:
            return {'error': str(e)}
