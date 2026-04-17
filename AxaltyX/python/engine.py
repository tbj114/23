#!/usr/bin/env python3
# Python计算引擎

import numpy as np
import pandas as pd
import sys
import os

# 添加StatsLib库到Python路径
sys.path.append(os.path.abspath('/workspace/StatsLib'))

# 导入StatsLib库的各个模块
from core.descriptive import DescriptiveStats
from core.hypothesis_test import HypothesisTest
from core.regression import Regression
from advanced.advanced_stats import AdvancedStats
from survival.survival_analysis import SurvivalAnalysis
from time_series.time_series_analysis import TimeSeriesAnalysis
from bayesian.bayesian_analysis import BayesianAnalysis
from machine_learning.machine_learning import MachineLearning
from data_management.data_management import DataManagement
from visualization.visualization import Visualization

class StatsEngine:
    def __init__(self):
        """初始化统计引擎"""
        self.data = None
    
    def load_data(self, data):
        """加载数据
        
        Args:
            data: 字典或DataFrame格式的数据
        """
        if isinstance(data, dict):
            self.data = pd.DataFrame(data)
        else:
            self.data = data
    
    def descriptive_stats(self, variables=None):
        """计算描述性统计量
        
        Args:
            variables: 要分析的变量列表
            
        Returns:
            描述性统计结果
        """
        if variables:
            return DescriptiveStats.descriptive_statistics(self.data, variables)
        else:
            return DescriptiveStats.descriptive_statistics(self.data)
    
    def frequency_analysis(self, variable):
        """频数分析
        
        Args:
            variable: 要分析的变量
            
        Returns:
            频数分析结果
        """
        return DescriptiveStats.frequency_analysis(self.data, variable)
    
    def cross_tabulation(self, variable1, variable2):
        """交叉表分析
        
        Args:
            variable1: 第一个变量
            variable2: 第二个变量
            
        Returns:
            交叉表分析结果
        """
        return DescriptiveStats.cross_tabulation(self.data, variable1, variable2)
    
    def chi_square_test(self, variable1, variable2):
        """卡方检验
        
        Args:
            variable1: 第一个变量
            variable2: 第二个变量
            
        Returns:
            卡方检验结果
        """
        return DescriptiveStats.chi_square_test(self.data, variable1, variable2)
    
    def mean_comparison(self, variables, group_variable):
        """均值比较
        
        Args:
            variables: 要分析的变量列表
            group_variable: 分组变量
            
        Returns:
            均值比较结果
        """
        results = {}
        for var in variables:
            results[var] = DescriptiveStats.mean_comparison(self.data, group_variable, var)
        return results
    
    def normality_test(self, variable, test_type='shapiro'):
        """正态性检验
        
        Args:
            variable: 要分析的变量
            test_type: 检验类型 ('shapiro', 'kurtosis', 'skewness')
            
        Returns:
            正态性检验结果
        """
        return DescriptiveStats.normality_test(self.data, variable)
    
    def t_test_one_sample(self, variable, population_mean):
        """单样本t检验
        
        Args:
            variable: 要分析的变量
            population_mean: 总体均值
            
        Returns:
            t检验结果
        """
        return HypothesisTest.t_test_one_sample(self.data, variable, population_mean)
    
    def t_test_independent(self, variable, group_variable):
        """独立样本t检验
        
        Args:
            variable: 要分析的变量
            group_variable: 分组变量
            
        Returns:
            t检验结果
        """
        return HypothesisTest.t_test_independent(self.data, variable, group_variable)
    
    def t_test_paired(self, variable1, variable2):
        """配对样本t检验
        
        Args:
            variable1: 第一个变量
            variable2: 第二个变量
            
        Returns:
            t检验结果
        """
        return HypothesisTest.t_test_paired(self.data, variable1, variable2)
    
    def anova_one_way(self, variable, group_variable):
        """单因素方差分析
        
        Args:
            variable: 要分析的变量
            group_variable: 分组变量
            
        Returns:
            方差分析结果
        """
        return HypothesisTest.anova_one_way(self.data, variable, group_variable)
    
    def anova_two_way(self, variable, group_variable1, group_variable2):
        """多因素方差分析
        
        Args:
            variable: 要分析的变量
            group_variable1: 第一个分组变量
            group_variable2: 第二个分组变量
            
        Returns:
            方差分析结果
        """
        return HypothesisTest.anova_two_way(self.data, variable, group_variable1, group_variable2)
    
    def ancova(self, dependent, covariate, group_variable):
        """协方差分析
        
        Args:
            dependent: 因变量
            covariate: 协变量
            group_variable: 分组变量
            
        Returns:
            协方差分析结果
        """
        return HypothesisTest.ancova(self.data, dependent, covariate, group_variable)
    
    def manova(self, dependents, group_variable):
        """多元方差分析
        
        Args:
            dependents: 因变量列表
            group_variable: 分组变量
            
        Returns:
            多元方差分析结果
        """
        return HypothesisTest.manova(self.data, dependents, group_variable)
    
    def non_parametric_test(self, variable, group_variable):
        """非参数检验
        
        Args:
            variable: 因变量
            group_variable: 分组变量
            
        Returns:
            非参数检验结果
        """
        return HypothesisTest.non_parametric_test(self.data, variable, group_variable)
    
    def correlation(self, variables):
        """相关分析
        
        Args:
            variables: 要分析的变量列表
            
        Returns:
            相关矩阵
        """
        return self.data[variables].corr().to_dict()
    
    def linear_regression(self, dependent, independents):
        """线性回归分析
        
        Args:
            dependent: 因变量
            independents: 自变量列表
            
        Returns:
            回归分析结果
        """
        return Regression.linear_regression(self.data, dependent, independents)
    
    def logistic_regression(self, dependent, independents):
        """Logistic回归分析
        
        Args:
            dependent: 因变量
            independents: 自变量列表
            
        Returns:
            回归分析结果
        """
        return Regression.logistic_regression(self.data, dependent, independents)
    
    def ordinal_regression(self, dependent, independents):
        """有序回归分析
        
        Args:
            dependent: 因变量
            independents: 自变量列表
            
        Returns:
            回归分析结果
        """
        return Regression.ordinal_regression(self.data, dependent, independents)
    
    def nonlinear_regression(self, X, y, model_type='logistic'):
        """非线性回归分析
        
        Args:
            X: 自变量
            y: 因变量
            model_type: 模型类型 ('logistic', 'exponential', 'power', 'polynomial')
            
        Returns:
            回归分析结果
        """
        return Regression.nonlinear_regression(X, y, model_type)
    
    def curve_fitting(self, x, y, model_type='polynomial', degree=2):
        """曲线估计
        
        Args:
            x: 自变量
            y: 因变量
            model_type: 模型类型 ('polynomial', 'exponential', 'logarithmic', 'power')
            degree: 多项式次数
            
        Returns:
            曲线拟合结果
        """
        return Regression.curve_fitting(x, y, model_type, degree)
    
    def factor_analysis(self, variables, n_factors=2, rotation='varimax'):
        """因子分析
        
        Args:
            variables: 要分析的变量列表
            n_factors: 因子数量
            rotation: 旋转方法
            
        Returns:
            因子分析结果
        """
        return AdvancedStats.factor_analysis(self.data[variables], n_factors, rotation)
    
    def principal_component_analysis(self, variables, n_components=2):
        """主成分分析
        
        Args:
            variables: 要分析的变量列表
            n_components: 主成分数量
            
        Returns:
            主成分分析结果
        """
        return AdvancedStats.principal_component_analysis(self.data[variables], n_components)
    
    def clustering(self, variables, method='kmeans', n_clusters=3, **kwargs):
        """聚类分析
        
        Args:
            variables: 要分析的变量列表
            method: 聚类方法 ('kmeans', 'hierarchical', 'dbscan')
            n_clusters: 聚类数量
            **kwargs: 其他参数
            
        Returns:
            聚类分析结果
        """
        return AdvancedStats.clustering(self.data[variables], method, n_clusters, **kwargs)
    
    def discriminant_analysis(self, independents, dependent, method='linear'):
        """判别分析
        
        Args:
            independents: 自变量列表
            dependent: 因变量
            method: 判别方法 ('linear', 'quadratic')
            
        Returns:
            判别分析结果
        """
        return AdvancedStats.discriminant_analysis(self.data[independents], self.data[dependent], method)
    
    def correspondence_analysis(self, variable1, variable2):
        """对应分析
        
        Args:
            variable1: 第一个变量
            variable2: 第二个变量
            
        Returns:
            对应分析结果
        """
        contingency_table = pd.crosstab(self.data[variable1], self.data[variable2])
        return AdvancedStats.correspondence_analysis(contingency_table)
    
    def reliability_analysis(self, variables):
        """信度分析
        
        Args:
            variables: 要分析的变量列表
            
        Returns:
            信度分析结果
        """
        return AdvancedStats.reliability_analysis(self.data[variables])
    
    def kaplan_meier_analysis(self, time_variable, event_variable, group_variable=None):
        """Kaplan-Meier生存分析
        
        Args:
            time_variable: 生存时间变量
            event_variable: 事件指示符变量
            group_variable: 分组变量
            
        Returns:
            生存分析结果
        """
        time = self.data[time_variable].values
        event = self.data[event_variable].values
        group = self.data[group_variable].values if group_variable else None
        return SurvivalAnalysis.kaplan_meier_analysis(time, event, group)
    
    def cox_regression(self, time_variable, event_variable, covariates):
        """Cox比例风险回归
        
        Args:
            time_variable: 生存时间变量
            event_variable: 事件指示符变量
            covariates: 协变量列表
            
        Returns:
            Cox回归结果
        """
        return SurvivalAnalysis.cox_regression(self.data, time_variable, event_variable, covariates)
    
    def arima_analysis(self, variable, order=(1, 1, 1)):
        """ARIMA模型分析
        
        Args:
            variable: 时间序列变量
            order: ARIMA模型阶数
            
        Returns:
            ARIMA分析结果
        """
        return TimeSeriesAnalysis.arima_analysis(self.data[variable].values, order)
    
    def random_forest(self, independents, dependent, task='classification', n_estimators=100, max_depth=None, test_size=0.2):
        """随机森林
        
        Args:
            independents: 自变量列表
            dependent: 因变量
            task: 任务类型 ('classification', 'regression')
            n_estimators: 树的数量
            max_depth: 树的最大深度
            test_size: 测试集比例
            
        Returns:
            随机森林结果
        """
        return MachineLearning.random_forest(self.data[independents].values, self.data[dependent].values, task, n_estimators, max_depth, test_size)
    
    def clean_data(self, remove_duplicates=True, drop_na=False, na_threshold=0.5):
        """数据清洗
        
        Args:
            remove_duplicates: 是否移除重复行
            drop_na: 是否删除含有缺失值的行
            na_threshold: 缺失值阈值
            
        Returns:
            清洗后的数据
        """
        cleaned_data = DataManagement.clean_data(self.data, remove_duplicates, drop_na, na_threshold)
        if isinstance(cleaned_data, dict) and 'error' in cleaned_data:
            return cleaned_data
        self.data = cleaned_data
        return cleaned_data.to_dict()
    
    def handle_missing_values(self, method='mean', columns=None):
        """缺失值处理
        
        Args:
            method: 处理方法 ('mean', 'median', 'mode', 'drop')
            columns: 要处理的列名列表
            
        Returns:
            处理后的数据
        """
        handled_data = DataManagement.handle_missing_values(self.data, method, columns)
        if isinstance(handled_data, dict) and 'error' in handled_data:
            return handled_data
        self.data = handled_data
        return handled_data.to_dict()
    
    def bar_chart(self, x, y, title='Bar Chart', xlabel=None, ylabel=None, color=None):
        """条形图
        
        Args:
            x: x轴变量
            y: y轴变量
            title: 图表标题
            xlabel: x轴标签
            ylabel: y轴标签
            color: 颜色变量
            
        Returns:
            图表配置
        """
        return Visualization.bar_chart(self.data, x, y, title, xlabel, ylabel, color)
    
    def scatter_plot(self, x, y, title='Scatter Plot', xlabel=None, ylabel=None, color=None, size=None):
        """散点图
        
        Args:
            x: x轴变量
            y: y轴变量
            title: 图表标题
            xlabel: x轴标签
            ylabel: y轴标签
            color: 颜色变量
            size: 大小变量
            
        Returns:
            图表配置
        """
        return Visualization.scatter_plot(self.data, x, y, title, xlabel, ylabel, color, size)
    
    def line_chart(self, x, y, title='Line Chart', xlabel=None, ylabel=None, color=None):
        """折线图
        
        Args:
            x: x轴变量
            y: y轴变量
            title: 图表标题
            xlabel: x轴标签
            ylabel: y轴标签
            color: 颜色变量
            
        Returns:
            图表配置
        """
        return Visualization.line_chart(self.data, x, y, title, xlabel, ylabel, color)
    
    def box_plot(self, x, y, title='Box Plot', xlabel=None, ylabel=None, color=None):
        """箱线图
        
        Args:
            x: x轴变量
            y: y轴变量
            title: 图表标题
            xlabel: x轴标签
            ylabel: y轴标签
            color: 颜色变量
            
        Returns:
            图表配置
        """
        return Visualization.box_plot(self.data, x, y, title, xlabel, ylabel, color)

if __name__ == "__main__":
    # 测试统计引擎
    engine = StatsEngine()
    
    # 测试数据
    test_data = {
        'age': [25, 28, 23, 30, 26, 24, 27, 29, 22, 25],
        'score': [85, 92, 78, 88, 90, 82, 87, 91, 76, 84],
        'gender': ['男', '女', '男', '女', '男', '女', '男', '女', '男', '女'],
        'group': ['A', 'B', 'A', 'B', 'A', 'B', 'A', 'B', 'A', 'B']
    }
    
    engine.load_data(test_data)
    
    # 测试描述性统计
    print("描述性统计:")
    print(engine.descriptive_stats(['age', 'score']))
    print()
    
    # 测试频数分析
    print("频数分析:")
    print(engine.frequency_analysis('gender'))
    print()
    
    # 测试单样本t检验
    print("单样本t检验:")
    print(engine.t_test_one_sample('age', 25))
    print()
    
    # 测试独立样本t检验
    print("独立样本t检验:")
    print(engine.t_test_independent('score', 'gender'))
    print()
    
    # 测试相关分析
    print("相关分析:")
    print(engine.correlation(['age', 'score']))
    print()
    
    # 测试线性回归
    print("线性回归:")
    print(engine.linear_regression('score', ['age']))
    print()
    
    # 测试卡方检验
    print("卡方检验:")
    print(engine.chi_square_test('gender', 'group'))