import numpy as np
import pandas as pd
from sklearn.decomposition import PCA, FactorAnalysis
from sklearn.cluster import KMeans, AgglomerativeClustering, DBSCAN
from sklearn.discriminant_analysis import LinearDiscriminantAnalysis, QuadraticDiscriminantAnalysis
from sklearn.manifold import MDS
from sklearn.preprocessing import StandardScaler
from scipy.cluster.hierarchy import linkage, dendrogram
from scipy.spatial.distance import pdist
import matplotlib.pyplot as plt


class AdvancedStats:
    @staticmethod
    def factor_analysis(data, n_factors=2, rotation='varimax'):
        """
        因子分析
        
        参数:
        data: DataFrame - 输入数据
        n_factors: int - 因子数量
        rotation: str - 旋转方法
        
        返回:
        dict - 因子分析结果
        """
        try:
            # 标准化数据
            scaler = StandardScaler()
            scaled_data = scaler.fit_transform(data)
            
            # 因子分析
            fa = FactorAnalysis(n_components=n_factors, rotation=rotation)
            factors = fa.fit_transform(scaled_data)
            
            # 计算因子载荷
            loadings = fa.components_.T
            
            # 计算 communalities
            communalities = np.sum(loadings ** 2, axis=1)
            
            # 计算解释方差
            explained_variance = fa.noise_variance_  # 噪声方差
            total_variance = np.var(scaled_data, axis=0).sum()
            explained_variance_ratio = 1 - np.sum(explained_variance) / total_variance
            
            return {
                'factors': factors,
                'loadings': loadings,
                'communalities': communalities,
                'explained_variance_ratio': explained_variance_ratio,
                'n_factors': n_factors
            }
        except Exception as e:
            return {'error': str(e)}

    @staticmethod
    def principal_component_analysis(data, n_components=2):
        """
        主成分分析
        
        参数:
        data: DataFrame - 输入数据
        n_components: int - 主成分数量
        
        返回:
        dict - 主成分分析结果
        """
        try:
            # 标准化数据
            scaler = StandardScaler()
            scaled_data = scaler.fit_transform(data)
            
            # 主成分分析
            pca = PCA(n_components=n_components)
            components = pca.fit_transform(scaled_data)
            
            # 计算解释方差
            explained_variance = pca.explained_variance_
            explained_variance_ratio = pca.explained_variance_ratio_
            cumulative_variance = np.cumsum(explained_variance_ratio)
            
            return {
                'components': components,
                'explained_variance': explained_variance,
                'explained_variance_ratio': explained_variance_ratio,
                'cumulative_variance': cumulative_variance,
                'n_components': n_components
            }
        except Exception as e:
            return {'error': str(e)}

    @staticmethod
    def clustering(data, method='kmeans', n_clusters=3, **kwargs):
        """
        聚类分析
        
        参数:
        data: DataFrame - 输入数据
        method: str - 聚类方法 ('kmeans', 'hierarchical', 'dbscan')
        n_clusters: int - 聚类数量
        **kwargs: 其他参数
        
        返回:
        dict - 聚类结果
        """
        try:
            # 标准化数据
            scaler = StandardScaler()
            scaled_data = scaler.fit_transform(data)
            
            if method == 'kmeans':
                # K均值聚类
                kmeans = KMeans(n_clusters=n_clusters, **kwargs)
                labels = kmeans.fit_predict(scaled_data)
                centers = kmeans.cluster_centers_
            elif method == 'hierarchical':
                # 层次聚类
                hierarchical = AgglomerativeClustering(n_clusters=n_clusters, **kwargs)
                labels = hierarchical.fit_predict(scaled_data)
                centers = None
            elif method == 'dbscan':
                # DBSCAN聚类
                dbscan = DBSCAN(**kwargs)
                labels = dbscan.fit_predict(scaled_data)
                centers = None
            else:
                return {'error': 'Unknown clustering method'}
            
            return {
                'labels': labels,
                'centers': centers,
                'method': method,
                'n_clusters': n_clusters if method != 'dbscan' else len(set(labels)) - (1 if -1 in labels else 0)
            }
        except Exception as e:
            return {'error': str(e)}

    @staticmethod
    def discriminant_analysis(X, y, method='linear'):
        """
        判别分析
        
        参数:
        X: DataFrame - 特征数据
        y: Series - 目标变量
        method: str - 判别方法 ('linear', 'quadratic')
        
        返回:
        dict - 判别分析结果
        """
        try:
            # 标准化数据
            scaler = StandardScaler()
            X_scaled = scaler.fit_transform(X)
            
            if method == 'linear':
                # 线性判别分析
                lda = LinearDiscriminantAnalysis()
                lda.fit(X_scaled, y)
                predictions = lda.predict(X_scaled)
                accuracy = lda.score(X_scaled, y)
            elif method == 'quadratic':
                # 二次判别分析
                qda = QuadraticDiscriminantAnalysis()
                qda.fit(X_scaled, y)
                predictions = qda.predict(X_scaled)
                accuracy = qda.score(X_scaled, y)
            else:
                return {'error': 'Unknown discriminant method'}
            
            return {
                'predictions': predictions,
                'accuracy': accuracy,
                'method': method
            }
        except Exception as e:
            return {'error': str(e)}

    @staticmethod
    def correspondence_analysis(data):
        """
        对应分析
        
        参数:
        data: DataFrame - 交叉表数据
        
        返回:
        dict - 对应分析结果
        """
        try:
            # 计算行和列的边缘频率
            row_sums = data.sum(axis=1)
            col_sums = data.sum(axis=0)
            total = data.sum().sum()
            
            # 计算期望频率
            expected = np.outer(row_sums, col_sums) / total
            
            # 计算残差
            residual = (data - expected) / np.sqrt(expected)
            
            # 奇异值分解
            U, S, Vt = np.linalg.svd(residual, full_matrices=False)
            
            # 计算行和列的坐标
            row_coords = U * S
            col_coords = Vt.T * S
            
            return {
                'row_coords': row_coords,
                'col_coords': col_coords,
                'singular_values': S,
                'inertia': np.sum(S ** 2)
            }
        except Exception as e:
            return {'error': str(e)}

    @staticmethod
    def reliability_analysis(data):
        """
        信度分析 (Cronbach's Alpha)
        
        参数:
        data: DataFrame - 输入数据
        
        返回:
        dict - 信度分析结果
        """
        try:
            # 计算Cronbach's Alpha
            n = data.shape[1]  # 项目数量
            var_total = data.var(axis=0).sum()  # 总方差
            var_sum = data.sum(axis=1).var()  # 总和方差
            
            cronbach_alpha = (n / (n - 1)) * (1 - var_total / var_sum)
            
            return {
                'cronbach_alpha': cronbach_alpha,
                'n_items': n
            }
        except Exception as e:
            return {'error': str(e)}

    @staticmethod
    def multidimensional_scaling(data, n_components=2, metric=True):
        """
        多维尺度分析
        
        参数:
        data: DataFrame - 输入数据或距离矩阵
        n_components: int - 维度数量
        metric: bool - 是否使用度量MDS
        
        返回:
        dict - MDS结果
        """
        try:
            # 计算距离矩阵
            if data.shape[0] == data.shape[1]:
                # 已经是距离矩阵
                dissimilarities = data.values
            else:
                # 计算欧氏距离
                dissimilarities = pdist(data.values)
            
            # 多维尺度分析
            if metric:
                from sklearn.manifold import MDS as MetricMDS
                mds = MetricMDS(n_components=n_components, dissimilarity='precomputed' if data.shape[0] == data.shape[1] else 'euclidean')
            else:
                from sklearn.manifold import MDS as NonMetricMDS
                mds = NonMetricMDS(n_components=n_components, dissimilarity='precomputed' if data.shape[0] == data.shape[1] else 'euclidean')
            
            coordinates = mds.fit_transform(dissimilarities if data.shape[0] == data.shape[1] else data.values)
            
            return {
                'coordinates': coordinates,
                'stress': mds.stress_ if hasattr(mds, 'stress_') else None,
                'n_components': n_components,
                'metric': metric
            }
        except Exception as e:
            return {'error': str(e)}
