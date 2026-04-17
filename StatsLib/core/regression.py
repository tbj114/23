import numpy as np
import pandas as pd
from scipy import stats
from sklearn.linear_model import LinearRegression, LogisticRegression, Ridge, Lasso, ElasticNet
from sklearn.preprocessing import PolynomialFeatures
from sklearn.pipeline import make_pipeline
from statsmodels.formula.api import ols, logit, mnlogit
from statsmodels.regression.quantile_regression import QuantReg

class Regression:
    """回归分析模块"""
    
    @staticmethod
    def linear_regression(data, dependent, independents):
        """多元线性回归
        
        Args:
            data: 数据集
            dependent: 因变量
            independents: 自变量列表
            
        Returns:
            回归分析结果
        """
        if isinstance(data, pd.DataFrame):
            X = data[independents]
            y = data[dependent]
        elif isinstance(data, dict):
            df = pd.DataFrame(data)
            X = df[independents]
            y = df[dependent]
        else:
            raise ValueError("数据格式不支持")
        
        model = LinearRegression()
        model.fit(X, y)
        
        return {
            'coefficients': dict(zip(independents, model.coef_.tolist())),
            'intercept': model.intercept_,
            'r_squared': model.score(X, y),
            'n_samples': len(X)
        }
    
    @staticmethod
    def logistic_regression(data, dependent, independents):
        """Logistic回归
        
        Args:
            data: 数据集
            dependent: 因变量
            independents: 自变量列表
            
        Returns:
            回归分析结果
        """
        if isinstance(data, pd.DataFrame):
            X = data[independents]
            y = data[dependent]
        elif isinstance(data, dict):
            df = pd.DataFrame(data)
            X = df[independents]
            y = df[dependent]
        else:
            raise ValueError("数据格式不支持")
        
        model = LogisticRegression()
        model.fit(X, y)
        
        return {
            'coefficients': dict(zip(independents, model.coef_[0].tolist())),
            'intercept': model.intercept_[0],
            'accuracy': model.score(X, y),
            'n_samples': len(X)
        }
    
    @staticmethod
    def ordinal_regression(data, dependent, independents):
        """有序回归
        
        Args:
            data: 数据集
            dependent: 因变量
            independents: 自变量列表
            
        Returns:
            回归分析结果
        """
        # 使用statsmodels实现有序回归
        if isinstance(data, pd.DataFrame):
            formula = f"{dependent} ~ {' + '.join(independents)}"
            # 这里需要使用有序回归模型，statsmodels暂时没有直接支持
            # 这里使用多元Logistic回归作为替代
            model = mnlogit(formula, data=data).fit()
        elif isinstance(data, dict):
            df = pd.DataFrame(data)
            formula = f"{dependent} ~ {' + '.join(independents)}"
            model = mnlogit(formula, data=df).fit()
        else:
            raise ValueError("数据格式不支持")
        
        return {
            'summary': model.summary().as_text(),
            'params': model.params.to_dict(),
            'pvalues': model.pvalues.to_dict()
        }
    
    @staticmethod
    def nonlinear_regression(data, dependent, independent, degree=2):
        """非线性回归（多项式回归）
        
        Args:
            data: 数据集
            dependent: 因变量
            independent: 自变量
            degree: 多项式次数
            
        Returns:
            回归分析结果
        """
        if isinstance(data, pd.DataFrame):
            X = data[[independent]]
            y = data[dependent]
        elif isinstance(data, dict):
            df = pd.DataFrame(data)
            X = df[[independent]]
            y = df[dependent]
        else:
            raise ValueError("数据格式不支持")
        
        model = make_pipeline(PolynomialFeatures(degree), LinearRegression())
        model.fit(X, y)
        
        return {
            'degree': degree,
            'r_squared': model.score(X, y),
            'n_samples': len(X)
        }
    
    @staticmethod
    def curve_fitting(data, dependent, independent, model_type='quadratic'):
        """曲线估计
        
        Args:
            data: 数据集
            dependent: 因变量
            independent: 自变量
            model_type: 模型类型 ('linear', 'quadratic', 'cubic', 'exponential', 'logarithmic', 'power')
            
        Returns:
            曲线拟合结果
        """
        if isinstance(data, pd.DataFrame):
            x = data[independent].values
            y = data[dependent].values
        elif isinstance(data, dict):
            df = pd.DataFrame(data)
            x = df[independent].values
            y = df[dependent].values
        else:
            raise ValueError("数据格式不支持")
        
        if model_type == 'linear':
            coeffs = np.polyfit(x, y, 1)
        elif model_type == 'quadratic':
            coeffs = np.polyfit(x, y, 2)
        elif model_type == 'cubic':
            coeffs = np.polyfit(x, y, 3)
        elif model_type == 'exponential':
            # 指数拟合: y = a * e^(b*x)
            log_y = np.log(y)
            coeffs = np.polyfit(x, log_y, 1)
            coeffs = [np.exp(coeffs[1]), coeffs[0]]
        elif model_type == 'logarithmic':
            # 对数拟合: y = a + b * log(x)
            log_x = np.log(x)
            coeffs = np.polyfit(log_x, y, 1)
        elif model_type == 'power':
            # 幂函数拟合: y = a * x^b
            log_x = np.log(x)
            log_y = np.log(y)
            coeffs = np.polyfit(log_x, log_y, 1)
            coeffs = [np.exp(coeffs[1]), coeffs[0]]
        else:
            raise ValueError("不支持的模型类型")
        
        return {
            'model_type': model_type,
            'coefficients': coeffs.tolist() if hasattr(coeffs, 'tolist') else coeffs
        }
    
    @staticmethod
    def ridge_regression(data, dependent, independents, alpha=1.0):
        """岭回归
        
        Args:
            data: 数据集
            dependent: 因变量
            independents: 自变量列表
            alpha: 正则化参数
            
        Returns:
            回归分析结果
        """
        if isinstance(data, pd.DataFrame):
            X = data[independents]
            y = data[dependent]
        elif isinstance(data, dict):
            df = pd.DataFrame(data)
            X = df[independents]
            y = df[dependent]
        else:
            raise ValueError("数据格式不支持")
        
        model = Ridge(alpha=alpha)
        model.fit(X, y)
        
        return {
            'coefficients': dict(zip(independents, model.coef_.tolist())),
            'intercept': model.intercept_,
            'r_squared': model.score(X, y),
            'alpha': alpha
        }
    
    @staticmethod
    def lasso_regression(data, dependent, independents, alpha=1.0):
        """Lasso回归
        
        Args:
            data: 数据集
            dependent: 因变量
            independents: 自变量列表
            alpha: 正则化参数
            
        Returns:
            回归分析结果
        """
        if isinstance(data, pd.DataFrame):
            X = data[independents]
            y = data[dependent]
        elif isinstance(data, dict):
            df = pd.DataFrame(data)
            X = df[independents]
            y = df[dependent]
        else:
            raise ValueError("数据格式不支持")
        
        model = Lasso(alpha=alpha)
        model.fit(X, y)
        
        return {
            'coefficients': dict(zip(independents, model.coef_.tolist())),
            'intercept': model.intercept_,
            'r_squared': model.score(X, y),
            'alpha': alpha
        }
    
    @staticmethod
    def elastic_net_regression(data, dependent, independents, alpha=1.0, l1_ratio=0.5):
        """弹性网回归
        
        Args:
            data: 数据集
            dependent: 因变量
            independents: 自变量列表
            alpha: 正则化参数
            l1_ratio: L1正则化比例
            
        Returns:
            回归分析结果
        """
        if isinstance(data, pd.DataFrame):
            X = data[independents]
            y = data[dependent]
        elif isinstance(data, dict):
            df = pd.DataFrame(data)
            X = df[independents]
            y = df[dependent]
        else:
            raise ValueError("数据格式不支持")
        
        model = ElasticNet(alpha=alpha, l1_ratio=l1_ratio)
        model.fit(X, y)
        
        return {
            'coefficients': dict(zip(independents, model.coef_.tolist())),
            'intercept': model.intercept_,
            'r_squared': model.score(X, y),
            'alpha': alpha,
            'l1_ratio': l1_ratio
        }
    
    @staticmethod
    def quantile_regression(data, dependent, independents, quantile=0.5):
        """分位数回归
        
        Args:
            data: 数据集
            dependent: 因变量
            independents: 自变量列表
            quantile: 分位数
            
        Returns:
            回归分析结果
        """
        if isinstance(data, pd.DataFrame):
            formula = f"{dependent} ~ {' + '.join(independents)}"
            model = QuantReg.from_formula(formula, data=data).fit(q=quantile)
        elif isinstance(data, dict):
            df = pd.DataFrame(data)
            formula = f"{dependent} ~ {' + '.join(independents)}"
            model = QuantReg.from_formula(formula, data=df).fit(q=quantile)
        else:
            raise ValueError("数据格式不支持")
        
        return {
            'summary': model.summary().as_text(),
            'params': model.params.to_dict(),
            'pvalues': model.pvalues.to_dict(),
            'quantile': quantile
        }