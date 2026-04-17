import numpy as np
import pandas as pd
import matplotlib.pyplot as plt

# 尝试导入pymc3和arviz
try:
    import pymc3 as pm
    import arviz as az
    BAYESIAN_AVAILABLE = True
except ImportError:
    BAYESIAN_AVAILABLE = False


class BayesianAnalysis:
    @staticmethod
    def bayesian_linear_regression(X, y, n_draws=1000):
        """
        贝叶斯线性回归
        
        参数:
        X: array - 特征数据
        y: array - 目标变量
        n_draws: int - MCMC采样次数
        
        返回:
        dict - 贝叶斯线性回归结果
        """
        if not BAYESIAN_AVAILABLE:
            return {'error': 'Bayesian analysis requires pymc3 and arviz, which are not installed. Please install them to use this feature.'}
        
        try:
            with pm.Model() as model:
                # 先验分布
                beta = pm.Normal('beta', mu=0, sigma=10, shape=X.shape[1])
                alpha = pm.Normal('alpha', mu=0, sigma=10)
                sigma = pm.HalfNormal('sigma', sigma=1)
                
                # 似然函数
                y_obs = pm.Normal('y_obs', mu=alpha + pm.math.dot(X, beta), sigma=sigma, observed=y)
                
                # MCMC采样
                trace = pm.sample(n_draws, return_inferencedata=True)
            
            # 提取结果
            summary = az.summary(trace)
            
            return {
                'trace': trace,
                'summary': summary.to_dict(),
                'posterior_predictive': az.extract(trace, group='posterior_predictive').to_dict() if 'posterior_predictive' in trace.groups() else None
            }
        except Exception as e:
            return {'error': str(e)}

    @staticmethod
    def bayesian_logistic_regression(X, y, n_draws=1000):
        """
        贝叶斯逻辑回归
        
        参数:
        X: array - 特征数据
        y: array - 目标变量 (0或1)
        n_draws: int - MCMC采样次数
        
        返回:
        dict - 贝叶斯逻辑回归结果
        """
        if not BAYESIAN_AVAILABLE:
            return {'error': 'Bayesian analysis requires pymc3 and arviz, which are not installed. Please install them to use this feature.'}
        
        try:
            with pm.Model() as model:
                # 先验分布
                beta = pm.Normal('beta', mu=0, sigma=10, shape=X.shape[1])
                alpha = pm.Normal('alpha', mu=0, sigma=10)
                
                # 似然函数
                p = pm.math.sigmoid(alpha + pm.math.dot(X, beta))
                y_obs = pm.Bernoulli('y_obs', p=p, observed=y)
                
                # MCMC采样
                trace = pm.sample(n_draws, return_inferencedata=True)
            
            # 提取结果
            summary = az.summary(trace)
            
            return {
                'trace': trace,
                'summary': summary.to_dict(),
                'posterior_predictive': az.extract(trace, group='posterior_predictive').to_dict() if 'posterior_predictive' in trace.groups() else None
            }
        except Exception as e:
            return {'error': str(e)}

    @staticmethod
    def bayesian_factor_analysis(data, n_factors=2, n_draws=1000):
        """
        贝叶斯因子分析
        
        参数:
        data: DataFrame - 输入数据
        n_factors: int - 因子数量
        n_draws: int - MCMC采样次数
        
        返回:
        dict - 贝叶斯因子分析结果
        """
        if not BAYESIAN_AVAILABLE:
            return {'error': 'Bayesian analysis requires pymc3 and arviz, which are not installed. Please install them to use this feature.'}
        
        try:
            with pm.Model() as model:
                n_obs, n_vars = data.shape
                
                # 先验分布
                mu = pm.Normal('mu', mu=0, sigma=10, shape=n_vars)
                
                # 因子载荷
                Lambda = pm.Normal('Lambda', mu=0, sigma=10, shape=(n_vars, n_factors))
                
                # 误差方差
                psi = pm.HalfNormal('psi', sigma=1, shape=n_vars)
                
                # 因子得分
                F = pm.Normal('F', mu=0, sigma=1, shape=(n_obs, n_factors))
                
                # 似然函数
                mu_obs = mu[None, :] + pm.math.dot(F, Lambda.T)
                y_obs = pm.Normal('y_obs', mu=mu_obs, sigma=pm.math.sqrt(psi), observed=data.values)
                
                # MCMC采样
                trace = pm.sample(n_draws, return_inferencedata=True)
            
            # 提取结果
            summary = az.summary(trace)
            
            return {
                'trace': trace,
                'summary': summary.to_dict(),
                'n_factors': n_factors
            }
        except Exception as e:
            return {'error': str(e)}

    @staticmethod
    def bayesian_clustering(data, n_clusters=3, n_draws=1000):
        """
        贝叶斯聚类分析
        
        参数:
        data: DataFrame - 输入数据
        n_clusters: int - 聚类数量
        n_draws: int - MCMC采样次数
        
        返回:
        dict - 贝叶斯聚类分析结果
        """
        if not BAYESIAN_AVAILABLE:
            return {'error': 'Bayesian analysis requires pymc3 and arviz, which are not installed. Please install them to use this feature.'}
        
        try:
            with pm.Model() as model:
                n_obs, n_vars = data.shape
                
                # 先验分布
                # 聚类均值
                mu = pm.Normal('mu', mu=0, sigma=10, shape=(n_clusters, n_vars))
                
                # 聚类协方差
                packed_L = pm.LKJCholeskyCov('packed_L', n=n_vars, eta=2.0, sd_dist=pm.HalfCauchy.dist(2.5))
                L = pm.expand_packed_triangular(n_vars, packed_L)
                Sigma = pm.Deterministic('Sigma', L.dot(L.T))
                
                # 聚类分配
                z = pm.Categorical('z', p=pm.Dirichlet('pi', a=np.ones(n_clusters)), shape=n_obs)
                
                # 似然函数
                y_obs = pm.MvNormal('y_obs', mu=mu[z], chol=L, observed=data.values)
                
                # MCMC采样
                trace = pm.sample(n_draws, return_inferencedata=True)
            
            # 提取结果
            summary = az.summary(trace)
            
            return {
                'trace': trace,
                'summary': summary.to_dict(),
                'n_clusters': n_clusters
            }
        except Exception as e:
            return {'error': str(e)}

    @staticmethod
    def bayesian_hierarchical_model(X, y, groups, n_draws=1000):
        """
        贝叶斯分层模型
        
        参数:
        X: array - 特征数据
        y: array - 目标变量
        groups: array - 分组变量
        n_draws: int - MCMC采样次数
        
        返回:
        dict - 贝叶斯分层模型结果
        """
        if not BAYESIAN_AVAILABLE:
            return {'error': 'Bayesian analysis requires pymc3 and arviz, which are not installed. Please install them to use this feature.'}
        
        try:
            unique_groups = np.unique(groups)
            n_groups = len(unique_groups)
            group_indices = {g: i for i, g in enumerate(unique_groups)}
            group_idx = np.array([group_indices[g] for g in groups])
            
            with pm.Model() as model:
                # 全局先验
                mu_alpha = pm.Normal('mu_alpha', mu=0, sigma=10)
                sigma_alpha = pm.HalfNormal('sigma_alpha', sigma=10)
                mu_beta = pm.Normal('mu_beta', mu=0, sigma=10, shape=X.shape[1])
                sigma_beta = pm.HalfNormal('sigma_beta', sigma=10, shape=X.shape[1])
                
                # 组级先验
                alpha = pm.Normal('alpha', mu=mu_alpha, sigma=sigma_alpha, shape=n_groups)
                beta = pm.Normal('beta', mu=mu_beta, sigma=sigma_beta, shape=(n_groups, X.shape[1]))
                sigma = pm.HalfNormal('sigma', sigma=1)
                
                # 似然函数
                y_obs = pm.Normal('y_obs', 
                                 mu=alpha[group_idx] + pm.math.sum(beta[group_idx] * X, axis=1), 
                                 sigma=sigma, 
                                 observed=y)
                
                # MCMC采样
                trace = pm.sample(n_draws, return_inferencedata=True)
            
            # 提取结果
            summary = az.summary(trace)
            
            return {
                'trace': trace,
                'summary': summary.to_dict(),
                'n_groups': n_groups
            }
        except Exception as e:
            return {'error': str(e)}

    @staticmethod
    def bayesian_survival_analysis(time, event, covariates, n_draws=1000):
        """
        贝叶斯生存分析
        
        参数:
        time: array - 生存时间
        event: array - 事件指示符 (1=事件发生, 0=删失)
        covariates: array - 协变量
        n_draws: int - MCMC采样次数
        
        返回:
        dict - 贝叶斯生存分析结果
        """
        if not BAYESIAN_AVAILABLE:
            return {'error': 'Bayesian analysis requires pymc3 and arviz, which are not installed. Please install them to use this feature.'}
        
        try:
            with pm.Model() as model:
                # 先验分布
                beta = pm.Normal('beta', mu=0, sigma=10, shape=covariates.shape[1])
                
                # 风险函数
                hazard = pm.math.exp(pm.math.dot(covariates, beta))
                
                # 似然函数 (指数分布)
                y_obs = pm.Exponential('y_obs', lam=hazard, observed=time, shape=len(time))
                
                # MCMC采样
                trace = pm.sample(n_draws, return_inferencedata=True)
            
            # 提取结果
            summary = az.summary(trace)
            
            return {
                'trace': trace,
                'summary': summary.to_dict()
            }
        except Exception as e:
            return {'error': str(e)}
