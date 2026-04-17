import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
import plotly.express as px
import plotly.graph_objects as go
from scipy import stats


class Visualization:
    @staticmethod
    def bar_chart(data, x, y, title='Bar Chart', xlabel=None, ylabel=None, color=None):
        """
        条形图
        
        参数:
        data: DataFrame - 输入数据
        x: str - x轴变量
        y: str - y轴变量
        title: str - 图表标题
        xlabel: str - x轴标签
        ylabel: str - y轴标签
        color: str - 颜色变量
        
        返回:
        dict - 图表配置
        """
        try:
            fig = px.bar(data, x=x, y=y, color=color, title=title, labels={x: xlabel or x, y: ylabel or y})
            return fig.to_dict()
        except Exception as e:
            return {'error': str(e)}

    @staticmethod
    def stacked_bar_chart(data, x, y, color, title='Stacked Bar Chart', xlabel=None, ylabel=None):
        """
        堆叠条形图
        
        参数:
        data: DataFrame - 输入数据
        x: str - x轴变量
        y: str - y轴变量
        color: str - 堆叠颜色变量
        title: str - 图表标题
        xlabel: str - x轴标签
        ylabel: str - y轴标签
        
        返回:
        dict - 图表配置
        """
        try:
            fig = px.bar(data, x=x, y=y, color=color, title=title, labels={x: xlabel or x, y: ylabel or y}, barmode='stack')
            return fig.to_dict()
        except Exception as e:
            return {'error': str(e)}

    @staticmethod
    def grouped_bar_chart(data, x, y, color, title='Grouped Bar Chart', xlabel=None, ylabel=None):
        """
        分组条形图
        
        参数:
        data: DataFrame - 输入数据
        x: str - x轴变量
        y: str - y轴变量
        color: str - 分组颜色变量
        title: str - 图表标题
        xlabel: str - x轴标签
        ylabel: str - y轴标签
        
        返回:
        dict - 图表配置
        """
        try:
            fig = px.bar(data, x=x, y=y, color=color, title=title, labels={x: xlabel or x, y: ylabel or y}, barmode='group')
            return fig.to_dict()
        except Exception as e:
            return {'error': str(e)}

    @staticmethod
    def pie_chart(data, values, names, title='Pie Chart', hole=0):
        """
        饼图/环图
        
        参数:
        data: DataFrame - 输入数据
        values: str - 值变量
        names: str - 名称变量
        title: str - 图表标题
        hole: float - 环图的洞大小 (0为饼图)
        
        返回:
        dict - 图表配置
        """
        try:
            fig = px.pie(data, values=values, names=names, title=title, hole=hole)
            return fig.to_dict()
        except Exception as e:
            return {'error': str(e)}

    @staticmethod
    def histogram(data, x, title='Histogram', xlabel=None, ylabel='Frequency', bins=20):
        """
        直方图
        
        参数:
        data: DataFrame - 输入数据
        x: str - 变量
        title: str - 图表标题
        xlabel: str - x轴标签
        ylabel: str - y轴标签
        bins: int -  bins数量
        
        返回:
        dict - 图表配置
        """
        try:
            fig = px.histogram(data, x=x, title=title, labels={x: xlabel or x, 'count': ylabel}, bins=bins)
            return fig.to_dict()
        except Exception as e:
            return {'error': str(e)}

    @staticmethod
    def density_plot(data, x, title='Density Plot', xlabel=None, ylabel='Density', color=None):
        """
        密度图
        
        参数:
        data: DataFrame - 输入数据
        x: str - 变量
        title: str - 图表标题
        xlabel: str - x轴标签
        ylabel: str - y轴标签
        color: str - 颜色变量
        
        返回:
        dict - 图表配置
        """
        try:
            fig = px.density_contour(data, x=x, color=color, title=title, labels={x: xlabel or x, 'density': ylabel})
            return fig.to_dict()
        except Exception as e:
            return {'error': str(e)}

    @staticmethod
    def scatter_plot(data, x, y, title='Scatter Plot', xlabel=None, ylabel=None, color=None, size=None):
        """
        散点图
        
        参数:
        data: DataFrame - 输入数据
        x: str - x轴变量
        y: str - y轴变量
        title: str - 图表标题
        xlabel: str - x轴标签
        ylabel: str - y轴标签
        color: str - 颜色变量
        size: str - 大小变量
        
        返回:
        dict - 图表配置
        """
        try:
            fig = px.scatter(data, x=x, y=y, color=color, size=size, title=title, labels={x: xlabel or x, y: ylabel or y})
            return fig.to_dict()
        except Exception as e:
            return {'error': str(e)}

    @staticmethod
    def matrix_scatter_plot(data, variables, title='Matrix Scatter Plot'):
        """
        矩阵散点图
        
        参数:
        data: DataFrame - 输入数据
        variables: list - 变量列表
        title: str - 图表标题
        
        返回:
        dict - 图表配置
        """
        try:
            fig = px.scatter_matrix(data, dimensions=variables, title=title)
            return fig.to_dict()
        except Exception as e:
            return {'error': str(e)}

    @staticmethod
    def three_d_scatter_plot(data, x, y, z, title='3D Scatter Plot', xlabel=None, ylabel=None, zlabel=None, color=None):
        """
        三维散点图
        
        参数:
        data: DataFrame - 输入数据
        x: str - x轴变量
        y: str - y轴变量
        z: str - z轴变量
        title: str - 图表标题
        xlabel: str - x轴标签
        ylabel: str - y轴标签
        zlabel: str - z轴标签
        color: str - 颜色变量
        
        返回:
        dict - 图表配置
        """
        try:
            fig = px.scatter_3d(data, x=x, y=y, z=z, color=color, title=title, labels={x: xlabel or x, y: ylabel or y, z: zlabel or z})
            return fig.to_dict()
        except Exception as e:
            return {'error': str(e)}

    @staticmethod
    def line_chart(data, x, y, title='Line Chart', xlabel=None, ylabel=None, color=None):
        """
        折线图
        
        参数:
        data: DataFrame - 输入数据
        x: str - x轴变量
        y: str - y轴变量
        title: str - 图表标题
        xlabel: str - x轴标签
        ylabel: str - y轴标签
        color: str - 颜色变量
        
        返回:
        dict - 图表配置
        """
        try:
            fig = px.line(data, x=x, y=y, color=color, title=title, labels={x: xlabel or x, y: ylabel or y})
            return fig.to_dict()
        except Exception as e:
            return {'error': str(e)}

    @staticmethod
    def area_chart(data, x, y, title='Area Chart', xlabel=None, ylabel=None, color=None):
        """
        面积图
        
        参数:
        data: DataFrame - 输入数据
        x: str - x轴变量
        y: str - y轴变量
        title: str - 图表标题
        xlabel: str - x轴标签
        ylabel: str - y轴标签
        color: str - 颜色变量
        
        返回:
        dict - 图表配置
        """
        try:
            fig = px.area(data, x=x, y=y, color=color, title=title, labels={x: xlabel or x, y: ylabel or y})
            return fig.to_dict()
        except Exception as e:
            return {'error': str(e)}

    @staticmethod
    def box_plot(data, x, y, title='Box Plot', xlabel=None, ylabel=None, color=None):
        """
        箱线图
        
        参数:
        data: DataFrame - 输入数据
        x: str - x轴变量
        y: str - y轴变量
        title: str - 图表标题
        xlabel: str - x轴标签
        ylabel: str - y轴标签
        color: str - 颜色变量
        
        返回:
        dict - 图表配置
        """
        try:
            fig = px.box(data, x=x, y=y, color=color, title=title, labels={x: xlabel or x, y: ylabel or y})
            return fig.to_dict()
        except Exception as e:
            return {'error': str(e)}

    @staticmethod
    def heatmap(data, x, y, z, title='Heatmap', xlabel=None, ylabel=None, zlabel=None):
        """
        热图
        
        参数:
        data: DataFrame - 输入数据
        x: str - x轴变量
        y: str - y轴变量
        z: str - z轴变量（热力值）
        title: str - 图表标题
        xlabel: str - x轴标签
        ylabel: str - y轴标签
        zlabel: str - z轴标签
        
        返回:
        dict - 图表配置
        """
        try:
            fig = px.density_heatmap(data, x=x, y=y, z=z, title=title, labels={x: xlabel or x, y: ylabel or y, z: zlabel or z})
            return fig.to_dict()
        except Exception as e:
            return {'error': str(e)}

    @staticmethod
    def roc_curve(fpr, tpr, auc=None, title='ROC Curve'):
        """
        ROC曲线图
        
        参数:
        fpr: array - 假阳性率
        tpr: array - 真阳性率
        auc: float - AUC值
        title: str - 图表标题
        
        返回:
        dict - 图表配置
        """
        try:
            fig = go.Figure()
            fig.add_trace(go.Scatter(x=fpr, y=tpr, mode='lines', name='ROC Curve'))
            fig.add_trace(go.Scatter(x=[0, 1], y=[0, 1], mode='lines', line=dict(dash='dash'), name='Random Guess'))
            fig.update_layout(title=title, xaxis_title='False Positive Rate', yaxis_title='True Positive Rate')
            if auc is not None:
                fig.update_layout(title=f'{title} (AUC = {auc:.4f})')
            return fig.to_dict()
        except Exception as e:
            return {'error': str(e)}

    @staticmethod
    def qq_plot(data, distribution='norm', title='Q-Q Plot'):
        """
        Q-Q图
        
        参数:
        data: array - 输入数据
        distribution: str - 分布类型 ('norm', 'expon', 'gamma', 'weibull_min')
        title: str - 图表标题
        
        返回:
        dict - 图表配置
        """
        try:
            if distribution == 'norm':
                theoretical_quantiles = stats.norm.ppf(np.linspace(0.01, 0.99, len(data)))
            elif distribution == 'expon':
                theoretical_quantiles = stats.expon.ppf(np.linspace(0.01, 0.99, len(data)))
            elif distribution == 'gamma':
                theoretical_quantiles = stats.gamma.ppf(np.linspace(0.01, 0.99, len(data)), 2)
            elif distribution == 'weibull_min':
                theoretical_quantiles = stats.weibull_min.ppf(np.linspace(0.01, 0.99, len(data)), 2)
            else:
                return {'error': 'Unknown distribution'}
            
            sample_quantiles = np.sort(data)
            
            fig = go.Figure()
            fig.add_trace(go.Scatter(x=theoretical_quantiles, y=sample_quantiles, mode='markers', name='Data'))
            min_val = min(min(theoretical_quantiles), min(sample_quantiles))
            max_val = max(max(theoretical_quantiles), max(sample_quantiles))
            fig.add_trace(go.Scatter(x=[min_val, max_val], y=[min_val, max_val], mode='lines', line=dict(dash='dash'), name='Ideal'))
            fig.update_layout(title=title, xaxis_title='Theoretical Quantiles', yaxis_title='Sample Quantiles')
            return fig.to_dict()
        except Exception as e:
            return {'error': str(e)}

    @staticmethod
    def survival_curve(time, event, group=None, title='Survival Curve'):
        """
        生存曲线
        
        参数:
        time: array - 生存时间
        event: array - 事件指示符
        group: array - 分组变量
        title: str - 图表标题
        
        返回:
        dict - 图表配置
        """
        try:
            from lifelines import KaplanMeierFitter
            kmf = KaplanMeierFitter()
            
            fig = go.Figure()
            
            if group is not None:
                groups = np.unique(group)
                for g in groups:
                    mask = group == g
                    kmf.fit(time[mask], event[mask], label=str(g))
                    fig.add_trace(go.Scatter(x=kmf.survival_function_.index, y=kmf.survival_function_.values.flatten(), mode='lines', name=str(g)))
            else:
                kmf.fit(time, event)
                fig.add_trace(go.Scatter(x=kmf.survival_function_.index, y=kmf.survival_function_.values.flatten(), mode='lines', name='Overall'))
            
            fig.update_layout(title=title, xaxis_title='Time', yaxis_title='Survival Probability')
            return fig.to_dict()
        except Exception as e:
            return {'error': str(e)}

    @staticmethod
    def word_cloud(texts, title='Word Cloud'):
        """
        词云图
        
        参数:
        texts: list - 文本列表
        title: str - 图表标题
        
        返回:
        dict - 图表配置
        """
        try:
            from wordcloud import WordCloud
            import matplotlib.pyplot as plt
            
            # 合并文本
            text = ' '.join(texts)
            
            # 生成词云
            wordcloud = WordCloud(width=800, height=400, background_color='white').generate(text)
            
            # 转换为plotly图表
            fig = go.Figure()
            fig.add_trace(go.Image(z=wordcloud.to_array()))
            fig.update_layout(title=title, xaxis_showticklabels=False, yaxis_showticklabels=False)
            return fig.to_dict()
        except Exception as e:
            return {'error': str(e)}
