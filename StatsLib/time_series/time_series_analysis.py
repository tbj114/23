import numpy as np
import pandas as pd
from statsmodels.tsa.arima.model import ARIMA
from statsmodels.tsa.vector_ar.var_model import VAR
from statsmodels.tsa.statespace.sarimax import SARIMAX
from statsmodels.tsa.holtwinters import ExponentialSmoothing
from statsmodels.tsa.stattools import adfuller, kpss, acf, pacf
from statsmodels.graphics.tsaplots import plot_acf, plot_pacf
import matplotlib.pyplot as plt


class TimeSeriesAnalysis:
    @staticmethod
    def arima_analysis(data, order=(1, 1, 1)):
        """
        ARIMA模型分析
        
        参数:
        data: array - 时间序列数据
        order: tuple - ARIMA模型阶数 (p, d, q)
        
        返回:
        dict - ARIMA分析结果
        """
        try:
            # 拟合ARIMA模型
            model = ARIMA(data, order=order)
            model_fit = model.fit()
            
            # 预测
            forecast = model_fit.forecast(steps=10)
            
            # 模型摘要
            summary = model_fit.summary()
            
            return {
                'forecast': forecast.tolist(),
                'aic': model_fit.aic,
                'bic': model_fit.bic,
                'params': model_fit.params.to_dict(),
                'residuals': model_fit.resid.tolist(),
                'summary': str(summary)
            }
        except Exception as e:
            return {'error': str(e)}

    @staticmethod
    def sarima_analysis(data, order=(1, 1, 1), seasonal_order=(1, 1, 1, 12)):
        """
        SARIMA模型分析
        
        参数:
        data: array - 时间序列数据
        order: tuple - ARIMA模型阶数 (p, d, q)
        seasonal_order: tuple - 季节性ARIMA阶数 (P, D, Q, s)
        
        返回:
        dict - SARIMA分析结果
        """
        try:
            # 拟合SARIMA模型
            model = SARIMAX(data, order=order, seasonal_order=seasonal_order)
            model_fit = model.fit()
            
            # 预测
            forecast = model_fit.forecast(steps=10)
            
            # 模型摘要
            summary = model_fit.summary()
            
            return {
                'forecast': forecast.tolist(),
                'aic': model_fit.aic,
                'bic': model_fit.bic,
                'params': model_fit.params.to_dict(),
                'residuals': model_fit.resid.tolist(),
                'summary': str(summary)
            }
        except Exception as e:
            return {'error': str(e)}

    @staticmethod
    def var_analysis(data, maxlags=1):
        """
        VAR模型分析
        
        参数:
        data: DataFrame - 多变量时间序列数据
        maxlags: int - 最大滞后阶数
        
        返回:
        dict - VAR分析结果
        """
        try:
            # 拟合VAR模型
            model = VAR(data)
            model_fit = model.fit(maxlags=maxlags)
            
            # 预测
            forecast = model_fit.forecast(data.values, steps=10)
            
            # 模型摘要
            summary = model_fit.summary()
            
            return {
                'forecast': forecast.tolist(),
                'aic': model_fit.aic,
                'bic': model_fit.bic,
                'params': model_fit.params.tolist(),
                'residuals': model_fit.resid.tolist(),
                'summary': str(summary)
            }
        except Exception as e:
            return {'error': str(e)}

    @staticmethod
    def exponential_smoothing(data, trend='add', seasonal='add', seasonal_periods=12):
        """
        指数平滑法
        
        参数:
        data: array - 时间序列数据
        trend: str - 趋势类型 ('add', 'mul', 'additive', 'multiplicative')
        seasonal: str - 季节性类型 ('add', 'mul', 'additive', 'multiplicative')
        seasonal_periods: int - 季节性周期
        
        返回:
        dict - 指数平滑分析结果
        """
        try:
            # 拟合指数平滑模型
            model = ExponentialSmoothing(data, trend=trend, seasonal=seasonal, seasonal_periods=seasonal_periods)
            model_fit = model.fit()
            
            # 预测
            forecast = model_fit.forecast(steps=10)
            
            return {
                'forecast': forecast.tolist(),
                'fittedvalues': model_fit.fittedvalues.tolist(),
                'residuals': model_fit.resid.tolist(),
                'params': {
                    'smoothing_level': model_fit.params['smoothing_level'],
                    'smoothing_trend': model_fit.params['smoothing_trend'],
                    'smoothing_seasonal': model_fit.params['smoothing_seasonal']
                }
            }
        except Exception as e:
            return {'error': str(e)}

    @staticmethod
    def unit_root_test(data, test_type='adf'):
        """
        单位根检验
        
        参数:
        data: array - 时间序列数据
        test_type: str - 检验类型 ('adf', 'kpss')
        
        返回:
        dict - 单位根检验结果
        """
        try:
            if test_type == 'adf':
                # ADF检验
                result = adfuller(data)
                return {
                    'test_statistic': result[0],
                    'p_value': result[1],
                    'critical_values': result[4],
                    'n_lags': result[2],
                    'n_obs': result[3],
                    'test_type': 'ADF'
                }
            elif test_type == 'kpss':
                # KPSS检验
                result = kpss(data)
                return {
                    'test_statistic': result[0],
                    'p_value': result[1],
                    'critical_values': result[3],
                    'n_lags': result[2],
                    'test_type': 'KPSS'
                }
            else:
                return {'error': 'Unknown test type'}
        except Exception as e:
            return {'error': str(e)}

    @staticmethod
    def acf_pacf_analysis(data, nlags=20):
        """
        ACF和PACF分析
        
        参数:
        data: array - 时间序列数据
        nlags: int - 滞后阶数
        
        返回:
        dict - ACF和PACF分析结果
        """
        try:
            # 计算ACF和PACF
            acf_values = acf(data, nlags=nlags)
            pacf_values = pacf(data, nlags=nlags)
            
            return {
                'acf': acf_values.tolist(),
                'pacf': pacf_values.tolist(),
                'nlags': nlags
            }
        except Exception as e:
            return {'error': str(e)}

    @staticmethod
    def seasonal_decomposition(data, model='additive', period=12):
        """
        时间序列季节性分解
        
        参数:
        data: array - 时间序列数据
        model: str - 分解模型 ('additive', 'multiplicative')
        period: int - 季节性周期
        
        返回:
        dict - 季节性分解结果
        """
        try:
            from statsmodels.tsa.seasonal import seasonal_decompose
            
            # 执行季节性分解
            decomposition = seasonal_decompose(data, model=model, period=period)
            
            return {
                'trend': decomposition.trend.dropna().tolist() if decomposition.trend is not None else None,
                'seasonal': decomposition.seasonal.dropna().tolist() if decomposition.seasonal is not None else None,
                'residual': decomposition.resid.dropna().tolist() if decomposition.resid is not None else None,
                'observed': decomposition.observed.tolist(),
                'model': model,
                'period': period
            }
        except Exception as e:
            return {'error': str(e)}
