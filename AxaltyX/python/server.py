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

if __name__ == '__main__':
    app.run(host='127.0.0.1', port=5000, debug=True)