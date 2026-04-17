import numpy as np
import pandas as pd
from scipy import stats
from statsmodels.formula.api import ols
from statsmodels.stats.anova import anova_lm
from statsmodels.stats.multicomp import pairwise_tukeyhsd

class HypothesisTest:
    """假设检验模块"""
    
    @staticmethod
    def t_test_one_sample(data, variable, population_mean):
        """单样本t检验
        
        Args:
            data: 数据集
            variable: 要分析的变量
            population_mean: 总体均值
            
        Returns:
            t检验结果
        """
        if isinstance(data, pd.DataFrame):
            values = data[variable].dropna()
        elif isinstance(data, dict):
            df = pd.DataFrame(data)
            values = df[variable].dropna()
        else:
            raise ValueError("数据格式不支持")
        
        stat, p_value = stats.ttest_1samp(values, population_mean)
        
        return {
            't_statistic': stat,
            'p_value': p_value,
            'df': len(values) - 1,
            'mean': values.mean(),
            'std': values.std()
        }
    
    @staticmethod
    def t_test_independent(data, variable, group_variable):
        """独立样本t检验
        
        Args:
            data: 数据集
            variable: 要分析的变量
            group_variable: 分组变量
            
        Returns:
            t检验结果
        """
        if isinstance(data, pd.DataFrame):
            groups = data[group_variable].unique()
            if len(groups) != 2:
                raise ValueError("分组变量必须只有两个水平")
            group1 = data[data[group_variable] == groups[0]][variable].dropna()
            group2 = data[data[group_variable] == groups[1]][variable].dropna()
        elif isinstance(data, dict):
            df = pd.DataFrame(data)
            groups = df[group_variable].unique()
            if len(groups) != 2:
                raise ValueError("分组变量必须只有两个水平")
            group1 = df[df[group_variable] == groups[0]][variable].dropna()
            group2 = df[df[group_variable] == groups[1]][variable].dropna()
        else:
            raise ValueError("数据格式不支持")
        
        stat, p_value = stats.ttest_ind(group1, group2)
        
        return {
            't_statistic': stat,
            'p_value': p_value,
            'df': len(group1) + len(group2) - 2,
            'group_means': {
                groups[0]: group1.mean(),
                groups[1]: group2.mean()
            },
            'group_std': {
                groups[0]: group1.std(),
                groups[1]: group2.std()
            }
        }
    
    @staticmethod
    def t_test_paired(data, variable1, variable2):
        """配对样本t检验
        
        Args:
            data: 数据集
            variable1: 第一个变量
            variable2: 第二个变量
            
        Returns:
            t检验结果
        """
        if isinstance(data, pd.DataFrame):
            values1 = data[variable1].dropna()
            values2 = data[variable2].dropna()
        elif isinstance(data, dict):
            df = pd.DataFrame(data)
            values1 = df[variable1].dropna()
            values2 = df[variable2].dropna()
        else:
            raise ValueError("数据格式不支持")
        
        # 确保两个变量长度相同
        min_length = min(len(values1), len(values2))
        values1 = values1[:min_length]
        values2 = values2[:min_length]
        
        stat, p_value = stats.ttest_rel(values1, values2)
        
        return {
            't_statistic': stat,
            'p_value': p_value,
            'df': min_length - 1,
            'mean_diff': (values1 - values2).mean(),
            'std_diff': (values1 - values2).std()
        }
    
    @staticmethod
    def anova_one_way(data, variable, group_variable):
        """单因素方差分析
        
        Args:
            data: 数据集
            variable: 因变量
            group_variable: 分组变量
            
        Returns:
            方差分析结果
        """
        if isinstance(data, pd.DataFrame):
            model = ols(f'{variable} ~ C({group_variable})', data=data).fit()
            anova_table = anova_lm(model)
        elif isinstance(data, dict):
            df = pd.DataFrame(data)
            model = ols(f'{variable} ~ C({group_variable})', data=df).fit()
            anova_table = anova_lm(model)
        else:
            raise ValueError("数据格式不支持")
        
        # 多重比较
        if isinstance(data, pd.DataFrame):
            tukey = pairwise_tukeyhsd(endog=data[variable], groups=data[group_variable], alpha=0.05)
        else:
            df = pd.DataFrame(data)
            tukey = pairwise_tukeyhsd(endog=df[variable], groups=df[group_variable], alpha=0.05)
        
        return {
            'anova_table': anova_table.to_dict(),
            'tukey_results': {
                'groups': tukey.groupsunique.tolist(),
                'meandiffs': tukey.meandiffs.tolist(),
                'pvalues': tukey.pvalues.tolist(),
                'reject': tukey.reject.tolist()
            }
        }
    
    @staticmethod
    def anova_two_way(data, dependent, factor1, factor2):
        """多因素方差分析
        
        Args:
            data: 数据集
            dependent: 因变量
            factor1: 第一个因素
            factor2: 第二个因素
            
        Returns:
            方差分析结果
        """
        if isinstance(data, pd.DataFrame):
            model = ols(f'{dependent} ~ C({factor1}) + C({factor2}) + C({factor1}):C({factor2})', data=data).fit()
            anova_table = anova_lm(model)
        elif isinstance(data, dict):
            df = pd.DataFrame(data)
            model = ols(f'{dependent} ~ C({factor1}) + C({factor2}) + C({factor1}):C({factor2})', data=df).fit()
            anova_table = anova_lm(model)
        else:
            raise ValueError("数据格式不支持")
        
        return {
            'anova_table': anova_table.to_dict()
        }
    
    @staticmethod
    def ancova(data, dependent, covariate, factor):
        """协方差分析
        
        Args:
            data: 数据集
            dependent: 因变量
            covariate: 协变量
            factor: 因素
            
        Returns:
            协方差分析结果
        """
        if isinstance(data, pd.DataFrame):
            model = ols(f'{dependent} ~ {covariate} + C({factor})', data=data).fit()
            anova_table = anova_lm(model)
        elif isinstance(data, dict):
            df = pd.DataFrame(data)
            model = ols(f'{dependent} ~ {covariate} + C({factor})', data=df).fit()
            anova_table = anova_lm(model)
        else:
            raise ValueError("数据格式不支持")
        
        return {
            'anova_table': anova_table.to_dict(),
            'model_summary': model.summary().as_text()
        }
    
    @staticmethod
    def manova(data, dependents, factor):
        """多元方差分析
        
        Args:
            data: 数据集
            dependents: 因变量列表
            factor: 因素
            
        Returns:
            多元方差分析结果
        """
        from statsmodels.multivariate.manova import MANOVA
        
        if isinstance(data, pd.DataFrame):
            formula = f"{'+'.join(dependents)} ~ C({factor})"
            manova = MANOVA.from_formula(formula, data=data)
            result = manova.mv_test()
        elif isinstance(data, dict):
            df = pd.DataFrame(data)
            formula = f"{'+'.join(dependents)} ~ C({factor})"
            manova = MANOVA.from_formula(formula, data=df)
            result = manova.mv_test()
        else:
            raise ValueError("数据格式不支持")
        
        return {
            'manova_result': str(result)
        }
    
    @staticmethod
    def non_parametric_test(data, variable, group_variable):
        """非参数检验
        
        Args:
            data: 数据集
            variable: 因变量
            group_variable: 分组变量
            
        Returns:
            非参数检验结果
        """
        if isinstance(data, pd.DataFrame):
            groups = data[group_variable].unique()
            group_data = [data[data[group_variable] == group][variable].dropna() for group in groups]
        elif isinstance(data, dict):
            df = pd.DataFrame(data)
            groups = df[group_variable].unique()
            group_data = [df[df[group_variable] == group][variable].dropna() for group in groups]
        else:
            raise ValueError("数据格式不支持")
        
        if len(groups) == 2:
            # Mann-Whitney U检验
            stat, p_value = stats.mannwhitneyu(group_data[0], group_data[1])
            return {
                'test_type': 'Mann-Whitney U',
                'statistic': stat,
                'p_value': p_value
            }
        else:
            # Kruskal-Wallis检验
            stat, p_value = stats.kruskal(*group_data)
            return {
                'test_type': 'Kruskal-Wallis',
                'statistic': stat,
                'p_value': p_value,
                'df': len(groups) - 1
            }