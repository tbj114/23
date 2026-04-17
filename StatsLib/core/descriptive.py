import numpy as np
import pandas as pd
from scipy import stats

class DescriptiveStats:
    """描述性统计分析"""
    
    @staticmethod
    def descriptive_statistics(data, variables=None):
        """计算描述性统计量
        
        Args:
            data: 数据集
            variables: 要分析的变量列表
            
        Returns:
            描述性统计结果
        """
        if isinstance(data, pd.DataFrame):
            if variables:
                return data[variables].describe().to_dict()
            else:
                return data.describe().to_dict()
        elif isinstance(data, dict):
            df = pd.DataFrame(data)
            if variables:
                return df[variables].describe().to_dict()
            else:
                return df.describe().to_dict()
        else:
            raise ValueError("数据格式不支持")
    
    @staticmethod
    def frequency_analysis(data, variable):
        """频数分析
        
        Args:
            data: 数据集
            variable: 要分析的变量
            
        Returns:
            频数分析结果
        """
        if isinstance(data, pd.DataFrame):
            freq = data[variable].value_counts()
            total = len(data)
        elif isinstance(data, dict):
            df = pd.DataFrame(data)
            freq = df[variable].value_counts()
            total = len(df)
        else:
            raise ValueError("数据格式不支持")
        
        return {
            'frequency': freq.to_dict(),
            'percentage': (freq / total * 100).to_dict()
        }
    
    @staticmethod
    def cross_tabulation(data, variable1, variable2):
        """交叉表分析
        
        Args:
            data: 数据集
            variable1: 第一个变量
            variable2: 第二个变量
            
        Returns:
            交叉表结果
        """
        if isinstance(data, pd.DataFrame):
            cross_tab = pd.crosstab(data[variable1], data[variable2])
        elif isinstance(data, dict):
            df = pd.DataFrame(data)
            cross_tab = pd.crosstab(df[variable1], df[variable2])
        else:
            raise ValueError("数据格式不支持")
        
        return cross_tab.to_dict()
    
    @staticmethod
    def chi_square_test(data, variable1, variable2):
        """卡方检验
        
        Args:
            data: 数据集
            variable1: 第一个变量
            variable2: 第二个变量
            
        Returns:
            卡方检验结果
        """
        if isinstance(data, pd.DataFrame):
            cross_tab = pd.crosstab(data[variable1], data[variable2])
        elif isinstance(data, dict):
            df = pd.DataFrame(data)
            cross_tab = pd.crosstab(df[variable1], df[variable2])
        else:
            raise ValueError("数据格式不支持")
        
        stat, p_value, df, expected = stats.chi2_contingency(cross_tab)
        
        return {
            'chi2_statistic': stat,
            'p_value': p_value,
            'df': df,
            'expected': expected.tolist()
        }
    
    @staticmethod
    def mean_comparison(data, group_variable, value_variable):
        """均值比较
        
        Args:
            data: 数据集
            group_variable: 分组变量
            value_variable: 值变量
            
        Returns:
            均值比较结果
        """
        if isinstance(data, pd.DataFrame):
            groups = data[group_variable].unique()
            results = {}
            for group in groups:
                group_data = data[data[group_variable] == group][value_variable]
                results[group] = {
                    'mean': group_data.mean(),
                    'std': group_data.std(),
                    'count': len(group_data)
                }
            return results
        elif isinstance(data, dict):
            df = pd.DataFrame(data)
            groups = df[group_variable].unique()
            results = {}
            for group in groups:
                group_data = df[df[group_variable] == group][value_variable]
                results[group] = {
                    'mean': group_data.mean(),
                    'std': group_data.std(),
                    'count': len(group_data)
                }
            return results
        else:
            raise ValueError("数据格式不支持")
    
    @staticmethod
    def normality_test(data, variable):
        """正态性检验
        
        Args:
            data: 数据集
            variable: 要检验的变量
            
        Returns:
            正态性检验结果
        """
        if isinstance(data, pd.DataFrame):
            values = data[variable].dropna()
        elif isinstance(data, dict):
            df = pd.DataFrame(data)
            values = df[variable].dropna()
        else:
            raise ValueError("数据格式不支持")
        
        # Shapiro-Wilk检验
        stat, p_value = stats.shapiro(values)
        
        # Kolmogorov-Smirnov检验
        ks_stat, ks_p_value = stats.kstest(values, 'norm', args=(values.mean(), values.std()))
        
        return {
            'shapiro': {
                'statistic': stat,
                'p_value': p_value,
                'is_normal': p_value > 0.05
            },
            'kolmogorov_smirnov': {
                'statistic': ks_stat,
                'p_value': ks_p_value,
                'is_normal': ks_p_value > 0.05
            }
        }