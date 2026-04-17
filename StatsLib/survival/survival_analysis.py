import numpy as np
import pandas as pd
from lifelines import KaplanMeierFitter, CoxPHFitter
from lifelines.statistics import logrank_test
from lifelines.utils import concordance_index
import matplotlib.pyplot as plt


class SurvivalAnalysis:
    @staticmethod
    def kaplan_meier_analysis(time, event, group=None):
        """
        Kaplan-Meier生存分析
        
        参数:
        time: array - 生存时间
        event: array - 事件指示符 (1=事件发生, 0=删失)
        group: array - 分组变量
        
        返回:
        dict - Kaplan-Meier分析结果
        """
        try:
            kmf = KaplanMeierFitter()
            
            if group is not None:
                # 按组分析
                groups = np.unique(group)
                survival_curves = {}
                for g in groups:
                    mask = group == g
                    kmf.fit(time[mask], event[mask], label=str(g))
                    survival_curves[str(g)] = {
                        'survival_function': kmf.survival_function_.values.flatten(),
                        'times': kmf.survival_function_.index.values,
                        'confidence_interval_lower': kmf.confidence_interval_.iloc[:, 0].values,
                        'confidence_interval_upper': kmf.confidence_interval_.iloc[:, 1].values
                    }
                
                # 对数秩检验
                results = {}
                for i, g1 in enumerate(groups):
                    for j, g2 in enumerate(groups):
                        if i < j:
                            mask1 = group == g1
                            mask2 = group == g2
                            test_result = logrank_test(time[mask1], time[mask2], event[mask1], event[mask2])
                            results[f'{g1}_vs_{g2}'] = {
                                'test_statistic': test_result.test_statistic,
                                'p_value': test_result.p_value
                            }
                
                return {
                    'survival_curves': survival_curves,
                    'logrank_test': results,
                    'n_groups': len(groups)
                }
            else:
                # 整体分析
                kmf.fit(time, event)
                return {
                    'survival_function': kmf.survival_function_.values.flatten(),
                    'times': kmf.survival_function_.index.values,
                    'confidence_interval_lower': kmf.confidence_interval_.iloc[:, 0].values,
                    'confidence_interval_upper': kmf.confidence_interval_.iloc[:, 1].values,
                    'median_survival_time': kmf.median_survival_time_ if hasattr(kmf, 'median_survival_time_') else None
                }
        except Exception as e:
            return {'error': str(e)}

    @staticmethod
    def cox_regression(data, time_col, event_col, covariates):
        """
        Cox比例风险回归
        
        参数:
        data: DataFrame - 输入数据
        time_col: str - 生存时间列名
        event_col: str - 事件指示符列名
        covariates: list - 协变量列名列表
        
        返回:
        dict - Cox回归结果
        """
        try:
            cph = CoxPHFitter()
            
            # 选择列
            cols = [time_col, event_col] + covariates
            model_data = data[cols]
            
            # 拟合模型
            cph.fit(model_data, duration_col=time_col, event_col=event_col)
            
            # 计算C指数
            c_index = concordance_index(data[time_col], -cph.predict_partial_hazard(data), data[event_col])
            
            # 获取系数
            coefficients = cph.summary['coef'].to_dict()
            p_values = cph.summary['p'].to_dict()
            hazard_ratios = np.exp(cph.summary['coef']).to_dict()
            
            return {
                'coefficients': coefficients,
                'p_values': p_values,
                'hazard_ratios': hazard_ratios,
                'c_index': c_index,
                'summary': cph.summary.to_dict()
            }
        except Exception as e:
            return {'error': str(e)}

    @staticmethod
    def nelson_aalen_analysis(time, event, group=None):
        """
        Nelson-Aalen累积风险估计
        
        参数:
        time: array - 生存时间
        event: array - 事件指示符 (1=事件发生, 0=删失)
        group: array - 分组变量
        
        返回:
        dict - Nelson-Aalen分析结果
        """
        try:
            from lifelines import NelsonAalenFitter
            naf = NelsonAalenFitter()
            
            if group is not None:
                # 按组分析
                groups = np.unique(group)
                cumulative_hazards = {}
                for g in groups:
                    mask = group == g
                    naf.fit(time[mask], event[mask], label=str(g))
                    cumulative_hazards[str(g)] = {
                        'cumulative_hazard': naf.cumulative_hazard_.values.flatten(),
                        'times': naf.cumulative_hazard_.index.values
                    }
                
                return {
                    'cumulative_hazards': cumulative_hazards,
                    'n_groups': len(groups)
                }
            else:
                # 整体分析
                naf.fit(time, event)
                return {
                    'cumulative_hazard': naf.cumulative_hazard_.values.flatten(),
                    'times': naf.cumulative_hazard_.index.values
                }
        except Exception as e:
            return {'error': str(e)}

    @staticmethod
    def cox_time_varying_covariates(data, id_col, time_col, event_col, covariates):
        """
        带有时间依变协变量的Cox回归
        
        参数:
        data: DataFrame - 输入数据 (长格式)
        id_col: str - 个体ID列名
        time_col: str - 生存时间列名
        event_col: str - 事件指示符列名
        covariates: list - 协变量列名列表
        
        返回:
        dict - 时间依变Cox回归结果
        """
        try:
            from lifelines import CoxTimeVaryingFitter
            ctv = CoxTimeVaryingFitter()
            
            # 选择列
            cols = [id_col, time_col, event_col] + covariates
            model_data = data[cols]
            
            # 拟合模型
            ctv.fit(model_data, id_col=id_col, duration_col=time_col, event_col=event_col)
            
            # 获取系数
            coefficients = ctv.summary['coef'].to_dict()
            p_values = ctv.summary['p'].to_dict()
            hazard_ratios = np.exp(ctv.summary['coef']).to_dict()
            
            return {
                'coefficients': coefficients,
                'p_values': p_values,
                'hazard_ratios': hazard_ratios,
                'summary': ctv.summary.to_dict()
            }
        except Exception as e:
            return {'error': str(e)}

    @staticmethod
    def competing_risks_analysis(time, event, event_type, group=None):
        """
        竞争风险分析
        
        参数:
        time: array - 生存时间
        event: array - 事件指示符 (1=事件发生, 0=删失)
        event_type: array - 事件类型
        group: array - 分组变量
        
        返回:
        dict - 竞争风险分析结果
        """
        try:
            from lifelines import CumulativeIncidenceFunctionFitter
            cif = CumulativeIncidenceFunctionFitter()
            
            if group is not None:
                # 按组分析
                groups = np.unique(group)
                cumulative_incidences = {}
                for g in groups:
                    mask = group == g
                    cif.fit(time[mask], event[mask], event_type[mask], label=str(g))
                    cumulative_incidences[str(g)] = {}
                    for et in np.unique(event_type[mask]):
                        if et > 0:
                            cumulative_incidences[str(g)][str(et)] = {
                                'cumulative_incidence': cif.cumulative_incidence_[et].values,
                                'times': cif.cumulative_incidence_.index.values
                            }
                
                return {
                    'cumulative_incidences': cumulative_incidences,
                    'n_groups': len(groups)
                }
            else:
                # 整体分析
                cif.fit(time, event, event_type)
                cumulative_incidences = {}
                for et in np.unique(event_type):
                    if et > 0:
                        cumulative_incidences[str(et)] = {
                            'cumulative_incidence': cif.cumulative_incidence_[et].values,
                            'times': cif.cumulative_incidence_.index.values
                        }
                
                return {
                    'cumulative_incidences': cumulative_incidences
                }
        except Exception as e:
            return {'error': str(e)}
