#!/usr/bin/env python3
# Python服务器，用于与Electron前端通信

from flask import Flask, request, jsonify
import json
import sys
import os

# 添加当前目录到Python路径
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

from engine import StatsEngine

app = Flask(__name__)
engine = StatsEngine()

@app.route('/api/load_data', methods=['POST'])
def load_data():
    """加载数据"""
    try:
        data = request.json
        engine.load_data(data)
        return jsonify({'status': 'success', 'message': '数据加载成功'})
    except Exception as e:
        return jsonify({'status': 'error', 'message': str(e)})

@app.route('/api/descriptive_stats', methods=['POST'])
def descriptive_stats():
    """计算描述性统计量"""
    try:
        variables = request.json.get('variables', None)
        result = engine.descriptive_stats(variables)
        return jsonify({'status': 'success', 'data': result})
    except Exception as e:
        return jsonify({'status': 'error', 'message': str(e)})

@app.route('/api/frequency_analysis', methods=['POST'])
def frequency_analysis():
    """频数分析"""
    try:
        variable = request.json.get('variable')
        result = engine.frequency_analysis(variable)
        return jsonify({'status': 'success', 'data': result})
    except Exception as e:
        return jsonify({'status': 'error', 'message': str(e)})

@app.route('/api/cross_tabulation', methods=['POST'])
def cross_tabulation():
    """交叉表分析"""
    try:
        variable1 = request.json.get('variable1')
        variable2 = request.json.get('variable2')
        result = engine.cross_tabulation(variable1, variable2)
        return jsonify({'status': 'success', 'data': result})
    except Exception as e:
        return jsonify({'status': 'error', 'message': str(e)})

@app.route('/api/chi_square_test', methods=['POST'])
def chi_square_test():
    """卡方检验"""
    try:
        variable1 = request.json.get('variable1')
        variable2 = request.json.get('variable2')
        result = engine.chi_square_test(variable1, variable2)
        return jsonify({'status': 'success', 'data': result})
    except Exception as e:
        return jsonify({'status': 'error', 'message': str(e)})

@app.route('/api/mean_comparison', methods=['POST'])
def mean_comparison():
    """均值比较"""
    try:
        variables = request.json.get('variables')
        group_variable = request.json.get('group_variable')
        result = engine.mean_comparison(variables, group_variable)
        return jsonify({'status': 'success', 'data': result})
    except Exception as e:
        return jsonify({'status': 'error', 'message': str(e)})

@app.route('/api/normality_test', methods=['POST'])
def normality_test():
    """正态性检验"""
    try:
        variable = request.json.get('variable')
        test_type = request.json.get('test_type', 'shapiro')
        result = engine.normality_test(variable, test_type)
        return jsonify({'status': 'success', 'data': result})
    except Exception as e:
        return jsonify({'status': 'error', 'message': str(e)})

@app.route('/api/t_test_one_sample', methods=['POST'])
def t_test_one_sample():
    """单样本t检验"""
    try:
        variable = request.json.get('variable')
        population_mean = request.json.get('population_mean')
        result = engine.t_test_one_sample(variable, population_mean)
        return jsonify({'status': 'success', 'data': result})
    except Exception as e:
        return jsonify({'status': 'error', 'message': str(e)})

@app.route('/api/t_test_independent', methods=['POST'])
def t_test_independent():
    """独立样本t检验"""
    try:
        variable = request.json.get('variable')
        group_variable = request.json.get('group_variable')
        result = engine.t_test_independent(variable, group_variable)
        return jsonify({'status': 'success', 'data': result})
    except Exception as e:
        return jsonify({'status': 'error', 'message': str(e)})

@app.route('/api/t_test_paired', methods=['POST'])
def t_test_paired():
    """配对样本t检验"""
    try:
        variable1 = request.json.get('variable1')
        variable2 = request.json.get('variable2')
        result = engine.t_test_paired(variable1, variable2)
        return jsonify({'status': 'success', 'data': result})
    except Exception as e:
        return jsonify({'status': 'error', 'message': str(e)})

@app.route('/api/anova_one_way', methods=['POST'])
def anova_one_way():
    """单因素方差分析"""
    try:
        variable = request.json.get('variable')
        group_variable = request.json.get('group_variable')
        result = engine.anova_one_way(variable, group_variable)
        return jsonify({'status': 'success', 'data': result})
    except Exception as e:
        return jsonify({'status': 'error', 'message': str(e)})

@app.route('/api/anova_two_way', methods=['POST'])
def anova_two_way():
    """多因素方差分析"""
    try:
        variable = request.json.get('variable')
        group_variable1 = request.json.get('group_variable1')
        group_variable2 = request.json.get('group_variable2')
        result = engine.anova_two_way(variable, group_variable1, group_variable2)
        return jsonify({'status': 'success', 'data': result})
    except Exception as e:
        return jsonify({'status': 'error', 'message': str(e)})

@app.route('/api/ancova', methods=['POST'])
def ancova():
    """协方差分析"""
    try:
        dependent = request.json.get('dependent')
        covariate = request.json.get('covariate')
        group_variable = request.json.get('group_variable')
        result = engine.ancova(dependent, covariate, group_variable)
        return jsonify({'status': 'success', 'data': result})
    except Exception as e:
        return jsonify({'status': 'error', 'message': str(e)})

@app.route('/api/correlation', methods=['POST'])
def correlation():
    """相关分析"""
    try:
        variables = request.json.get('variables')
        result = engine.correlation(variables)
        return jsonify({'status': 'success', 'data': result})
    except Exception as e:
        return jsonify({'status': 'error', 'message': str(e)})

@app.route('/api/linear_regression', methods=['POST'])
def linear_regression():
    """线性回归分析"""
    try:
        dependent = request.json.get('dependent')
        independents = request.json.get('independents')
        result = engine.linear_regression(dependent, independents)
        return jsonify({'status': 'success', 'data': result})
    except Exception as e:
        return jsonify({'status': 'error', 'message': str(e)})

@app.route('/api/logistic_regression', methods=['POST'])
def logistic_regression():
    """Logistic回归分析"""
    try:
        dependent = request.json.get('dependent')
        independents = request.json.get('independents')
        result = engine.logistic_regression(dependent, independents)
        return jsonify({'status': 'success', 'data': result})
    except Exception as e:
        return jsonify({'status': 'error', 'message': str(e)})

@app.route('/api/factor_analysis', methods=['POST'])
def factor_analysis():
    """因子分析"""
    try:
        variables = request.json.get('variables')
        n_factors = request.json.get('n_factors', 2)
        rotation = request.json.get('rotation', 'varimax')
        result = engine.factor_analysis(variables, n_factors, rotation)
        return jsonify({'status': 'success', 'data': result})
    except Exception as e:
        return jsonify({'status': 'error', 'message': str(e)})

@app.route('/api/principal_component_analysis', methods=['POST'])
def principal_component_analysis():
    """主成分分析"""
    try:
        variables = request.json.get('variables')
        n_components = request.json.get('n_components', 2)
        result = engine.principal_component_analysis(variables, n_components)
        return jsonify({'status': 'success', 'data': result})
    except Exception as e:
        return jsonify({'status': 'error', 'message': str(e)})

@app.route('/api/clustering', methods=['POST'])
def clustering():
    """聚类分析"""
    try:
        variables = request.json.get('variables')
        method = request.json.get('method', 'kmeans')
        n_clusters = request.json.get('n_clusters', 3)
        result = engine.clustering(variables, method, n_clusters)
        return jsonify({'status': 'success', 'data': result})
    except Exception as e:
        return jsonify({'status': 'error', 'message': str(e)})

@app.route('/api/reliability_analysis', methods=['POST'])
def reliability_analysis():
    """信度分析"""
    try:
        variables = request.json.get('variables')
        result = engine.reliability_analysis(variables)
        return jsonify({'status': 'success', 'data': result})
    except Exception as e:
        return jsonify({'status': 'error', 'message': str(e)})

@app.route('/api/kaplan_meier_analysis', methods=['POST'])
def kaplan_meier_analysis():
    """Kaplan-Meier生存分析"""
    try:
        time_variable = request.json.get('time_variable')
        event_variable = request.json.get('event_variable')
        group_variable = request.json.get('group_variable', None)
        result = engine.kaplan_meier_analysis(time_variable, event_variable, group_variable)
        return jsonify({'status': 'success', 'data': result})
    except Exception as e:
        return jsonify({'status': 'error', 'message': str(e)})

@app.route('/api/cox_regression', methods=['POST'])
def cox_regression():
    """Cox比例风险回归"""
    try:
        time_variable = request.json.get('time_variable')
        event_variable = request.json.get('event_variable')
        covariates = request.json.get('covariates')
        result = engine.cox_regression(time_variable, event_variable, covariates)
        return jsonify({'status': 'success', 'data': result})
    except Exception as e:
        return jsonify({'status': 'error', 'message': str(e)})

@app.route('/api/arima_analysis', methods=['POST'])
def arima_analysis():
    """ARIMA模型分析"""
    try:
        variable = request.json.get('variable')
        order = tuple(request.json.get('order', [1, 1, 1]))
        result = engine.arima_analysis(variable, order)
        return jsonify({'status': 'success', 'data': result})
    except Exception as e:
        return jsonify({'status': 'error', 'message': str(e)})

@app.route('/api/random_forest', methods=['POST'])
def random_forest():
    """随机森林"""
    try:
        independents = request.json.get('independents')
        dependent = request.json.get('dependent')
        task = request.json.get('task', 'classification')
        n_estimators = request.json.get('n_estimators', 100)
        max_depth = request.json.get('max_depth', None)
        test_size = request.json.get('test_size', 0.2)
        result = engine.random_forest(independents, dependent, task, n_estimators, max_depth, test_size)
        return jsonify({'status': 'success', 'data': result})
    except Exception as e:
        return jsonify({'status': 'error', 'message': str(e)})

@app.route('/api/clean_data', methods=['POST'])
def clean_data():
    """数据清洗"""
    try:
        remove_duplicates = request.json.get('remove_duplicates', True)
        drop_na = request.json.get('drop_na', False)
        na_threshold = request.json.get('na_threshold', 0.5)
        result = engine.clean_data(remove_duplicates, drop_na, na_threshold)
        return jsonify({'status': 'success', 'data': result})
    except Exception as e:
        return jsonify({'status': 'error', 'message': str(e)})

@app.route('/api/handle_missing_values', methods=['POST'])
def handle_missing_values():
    """缺失值处理"""
    try:
        method = request.json.get('method', 'mean')
        columns = request.json.get('columns', None)
        result = engine.handle_missing_values(method, columns)
        return jsonify({'status': 'success', 'data': result})
    except Exception as e:
        return jsonify({'status': 'error', 'message': str(e)})

@app.route('/api/bar_chart', methods=['POST'])
def bar_chart():
    """条形图"""
    try:
        x = request.json.get('x')
        y = request.json.get('y')
        title = request.json.get('title', 'Bar Chart')
        xlabel = request.json.get('xlabel', None)
        ylabel = request.json.get('ylabel', None)
        color = request.json.get('color', None)
        result = engine.bar_chart(x, y, title, xlabel, ylabel, color)
        return jsonify({'status': 'success', 'data': result})
    except Exception as e:
        return jsonify({'status': 'error', 'message': str(e)})

@app.route('/api/scatter_plot', methods=['POST'])
def scatter_plot():
    """散点图"""
    try:
        x = request.json.get('x')
        y = request.json.get('y')
        title = request.json.get('title', 'Scatter Plot')
        xlabel = request.json.get('xlabel', None)
        ylabel = request.json.get('ylabel', None)
        color = request.json.get('color', None)
        size = request.json.get('size', None)
        result = engine.scatter_plot(x, y, title, xlabel, ylabel, color, size)
        return jsonify({'status': 'success', 'data': result})
    except Exception as e:
        return jsonify({'status': 'error', 'message': str(e)})

@app.route('/api/line_chart', methods=['POST'])
def line_chart():
    """折线图"""
    try:
        x = request.json.get('x')
        y = request.json.get('y')
        title = request.json.get('title', 'Line Chart')
        xlabel = request.json.get('xlabel', None)
        ylabel = request.json.get('ylabel', None)
        color = request.json.get('color', None)
        result = engine.line_chart(x, y, title, xlabel, ylabel, color)
        return jsonify({'status': 'success', 'data': result})
    except Exception as e:
        return jsonify({'status': 'error', 'message': str(e)})

@app.route('/api/box_plot', methods=['POST'])
def box_plot():
    """箱线图"""
    try:
        x = request.json.get('x')
        y = request.json.get('y')
        title = request.json.get('title', 'Box Plot')
        xlabel = request.json.get('xlabel', None)
        ylabel = request.json.get('ylabel', None)
        color = request.json.get('color', None)
        result = engine.box_plot(x, y, title, xlabel, ylabel, color)
        return jsonify({'status': 'success', 'data': result})
    except Exception as e:
        return jsonify({'status': 'error', 'message': str(e)})

if __name__ == '__main__':
    app.run(host='127.0.0.1', port=5000, debug=True)