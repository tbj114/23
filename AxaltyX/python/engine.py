#!/usr/bin/env python3
# Python计算引擎

import numpy as np
import pandas as pd
from scipy import stats

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
            return self.data[variables].describe().to_dict()
        else:
            return self.data.describe().to_dict()
    
    def frequency_analysis(self, variable):
        """频数分析
        
        Args:
            variable: 要分析的变量
            
        Returns:
            频数分析结果
        """
        freq = self.data[variable].value_counts()
        return {
            'frequency': freq.to_dict(),
            'percentage': (freq / len(self.data) * 100).to_dict()
        }
    
    def t_test_one_sample(self, variable, population_mean):
        """单样本t检验
        
        Args:
            variable: 要分析的变量
            population_mean: 总体均值
            
        Returns:
            t检验结果
        """
        stat, p_value = stats.ttest_1samp(self.data[variable], population_mean)
        return {
            't_statistic': stat,
            'p_value': p_value,
            'df': len(self.data) - 1
        }
    
    def t_test_independent(self, variable, group_variable):
        """独立样本t检验
        
        Args:
            variable: 要分析的变量
            group_variable: 分组变量
            
        Returns:
            t检验结果
        """
        groups = self.data[group_variable].unique()
        if len(groups) != 2:
            raise ValueError("分组变量必须只有两个水平")
        
        group1 = self.data[self.data[group_variable] == groups[0]][variable]
        group2 = self.data[self.data[group_variable] == groups[1]][variable]
        
        stat, p_value = stats.ttest_ind(group1, group2)
        return {
            't_statistic': stat,
            'p_value': p_value,
            'df': len(group1) + len(group2) - 2,
            'group_means': {
                groups[0]: group1.mean(),
                groups[1]: group2.mean()
            }
        }
    
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
        from sklearn.linear_model import LinearRegression
        
        X = self.data[independents]
        y = self.data[dependent]
        
        model = LinearRegression()
        model.fit(X, y)
        
        return {
            'coefficients': dict(zip(independents, model.coef_.tolist())),
            'intercept': model.intercept_,
            'r_squared': model.score(X, y)
        }
    
    def chi_square_test(self, variable1, variable2):
        """卡方检验
        
        Args:
            variable1: 第一个变量
            variable2: 第二个变量
            
        Returns:
            卡方检验结果
        """
        contingency_table = pd.crosstab(self.data[variable1], self.data[variable2])
        stat, p_value, df, expected = stats.chi2_contingency(contingency_table)
        
        return {
            'chi2_statistic': stat,
            'p_value': p_value,
            'df': df,
            'contingency_table': contingency_table.to_dict()
        }

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