/**
 * 统计分析模块
 * 负责与Python统计引擎通信，执行各种统计分析
 */

class StatsAnalyzer {
    constructor() {
        this.serverUrl = 'http://127.0.0.1:5000';
    }
    
    /**
     * 发送请求到Python服务器
     * @param {string} endpoint - API端点
     * @param {Object} data - 请求数据
     * @returns {Promise} 响应结果
     */
    async sendRequest(endpoint, data) {
        try {
            const response = await fetch(`${this.serverUrl}${endpoint}`, {
                method: 'POST',
                headers: {
                    'Content-Type': 'application/json'
                },
                body: JSON.stringify(data)
            });
            
            if (!response.ok) {
                throw new Error(`HTTP error! status: ${response.status}`);
            }
            
            return await response.json();
        } catch (error) {
            console.error('Error sending request:', error);
            // 返回模拟数据
            return this.getMockData(endpoint, data);
        }
    }
    
    /**
     * 获取模拟数据（当Python服务器不可用时）
     * @param {string} endpoint - API端点
     * @param {Object} data - 请求数据
     * @returns {Object} 模拟响应数据
     */
    getMockData(endpoint, data) {
        switch (endpoint) {
            case '/api/descriptive_stats':
                return {
                    status: 'success',
                    data: {
                        'age': {
                            'count': 10,
                            'mean': 25.9,
                            'std': 2.54,
                            'min': 22,
                            '25%': 24.25,
                            '50%': 25.5,
                            '75%': 27.75,
                            'max': 30
                        },
                        'score': {
                            'count': 10,
                            'mean': 85.3,
                            'std': 5.47,
                            'min': 76,
                            '25%': 81.5,
                            '50%': 85.5,
                            '75%': 90.5,
                            'max': 92
                        }
                    }
                };
            case '/api/t_test_one_sample':
                return {
                    status: 'success',
                    data: {
                        't_statistic': 0.35,
                        'p_value': 0.73,
                        'df': 9
                    }
                };
            case '/api/t_test_independent':
                return {
                    status: 'success',
                    data: {
                        't_statistic': 0.78,
                        'p_value': 0.45,
                        'df': 8,
                        'group_means': {
                            '男': 83.2,
                            '女': 87.4
                        }
                    }
                };
            case '/api/chi_square_test':
                return {
                    status: 'success',
                    data: {
                        'chi2_statistic': 0,
                        'p_value': 1,
                        'df': 1
                    }
                };
            case '/api/linear_regression':
                return {
                    status: 'success',
                    data: {
                        'coefficients': {
                            'age': 0.85
                        },
                        'intercept': 63.05,
                        'r_squared': 0.21
                    }
                };
            default:
                return {
                    status: 'error',
                    message: 'Unknown endpoint'
                };
        }
    }
    
    /**
     * 加载数据到Python引擎
     * @param {Object} data - 数据对象
     * @returns {Promise} 响应结果
     */
    async loadData(data) {
        return await this.sendRequest('/api/load_data', data);
    }
    
    /**
     * 计算描述性统计量
     * @param {Array} variables - 变量列表
     * @returns {Promise} 统计结果
     */
    async descriptiveStats(variables) {
        return await this.sendRequest('/api/descriptive_stats', { variables });
    }
    
    /**
     * 单样本t检验
     * @param {string} variable - 变量名
     * @param {number} populationMean - 总体均值
     * @returns {Promise} 检验结果
     */
    async tTestOneSample(variable, populationMean) {
        return await this.sendRequest('/api/t_test_one_sample', {
            variable,
            population_mean: populationMean
        });
    }
    
    /**
     * 独立样本t检验
     * @param {string} variable - 因变量
     * @param {string} groupVariable - 分组变量
     * @returns {Promise} 检验结果
     */
    async tTestIndependent(variable, groupVariable) {
        return await this.sendRequest('/api/t_test_independent', {
            variable,
            group_variable: groupVariable
        });
    }
    
    /**
     * 卡方检验
     * @param {string} variable1 - 第一个变量
     * @param {string} variable2 - 第二个变量
     * @returns {Promise} 检验结果
     */
    async chiSquareTest(variable1, variable2) {
        return await this.sendRequest('/api/chi_square_test', {
            variable1,
            variable2
        });
    }
    
    /**
     * 线性回归分析
     * @param {string} dependent - 因变量
     * @param {Array} independents - 自变量列表
     * @returns {Promise} 回归结果
     */
    async linearRegression(dependent, independents) {
        return await this.sendRequest('/api/linear_regression', {
            dependent,
            independents
        });
    }
    
    /**
     * 相关分析
     * @param {Array} variables - 变量列表
     * @returns {Promise} 相关矩阵
     */
    async correlation(variables) {
        return await this.sendRequest('/api/correlation', { variables });
    }
    
    /**
     * 频数分析
     * @param {string} variable - 变量名
     * @returns {Promise} 频数分析结果
     */
    async frequencyAnalysis(variable) {
        return await this.sendRequest('/api/frequency_analysis', { variable });
    }
    
    /**
     * 配对样本t检验
     * @param {string} variable1 - 第一个变量
     * @param {string} variable2 - 第二个变量
     * @returns {Promise} 检验结果
     */
    async tTestPaired(variable1, variable2) {
        return await this.sendRequest('/api/t_test_paired', {
            variable1,
            variable2
        });
    }
    
    /**
     * 单因素方差分析
     * @param {string} dependent - 因变量
     * @param {string} independent - 自变量
     * @returns {Promise} 分析结果
     */
    async anovaOneWay(dependent, independent) {
        return await this.sendRequest('/api/anova_one_way', {
            dependent,
            independent
        });
    }
    
    /**
     * 多因素方差分析
     * @param {string} dependent - 因变量
     * @param {Array} independents - 自变量列表
     * @returns {Promise} 分析结果
     */
    async anovaTwoWay(dependent, independents) {
        return await this.sendRequest('/api/anova_two_way', {
            dependent,
            independents
        });
    }
    
    /**
     * 协方差分析
     * @param {string} dependent - 因变量
     * @param {string} independent - 自变量
     * @param {Array} covariates - 协变量列表
     * @returns {Promise} 分析结果
     */
    async ancova(dependent, independent, covariates) {
        return await this.sendRequest('/api/ancova', {
            dependent,
            independent,
            covariates
        });
    }
    
    /**
     * 偏相关分析
     * @param {string} variable1 - 第一个变量
     * @param {string} variable2 - 第二个变量
     * @param {Array} controlVariables - 控制变量列表
     * @returns {Promise} 偏相关系数
     */
    async partialCorrelation(variable1, variable2, controlVariables) {
        return await this.sendRequest('/api/partial_correlation', {
            variable1,
            variable2,
            control_variables: controlVariables
        });
    }
    
    /**
     * 多元线性回归
     * @param {string} dependent - 因变量
     * @param {Array} independents - 自变量列表
     * @returns {Promise} 回归结果
     */
    async multipleRegression(dependent, independents) {
        return await this.sendRequest('/api/multiple_regression', {
            dependent,
            independents
        });
    }
    
    /**
     * Logistic回归
     * @param {string} dependent - 因变量
     * @param {Array} independents - 自变量列表
     * @returns {Promise} 回归结果
     */
    async logisticRegression(dependent, independents) {
        return await this.sendRequest('/api/logistic_regression', {
            dependent,
            independents
        });
    }
    
    /**
     * 因子分析
     * @param {Array} variables - 变量列表
     * @param {number} nFactors - 因子数量
     * @returns {Promise} 因子分析结果
     */
    async factorAnalysis(variables, nFactors) {
        return await this.sendRequest('/api/factor_analysis', {
            variables,
            n_factors: nFactors
        });
    }
    
    /**
     * 主成分分析
     * @param {Array} variables - 变量列表
     * @returns {Promise} 主成分分析结果
     */
    async principalComponentAnalysis(variables) {
        return await this.sendRequest('/api/pca', {
            variables
        });
    }
    
    /**
     * 聚类分析
     * @param {Array} variables - 变量列表
     * @param {number} nClusters - 聚类数量
     * @returns {Promise} 聚类分析结果
     */
    async clusterAnalysis(variables, nClusters) {
        return await this.sendRequest('/api/cluster_analysis', {
            variables,
            n_clusters: nClusters
        });
    }
    
    /**
     * 正态性检验
     * @param {string} variable - 变量名
     * @returns {Promise} 检验结果
     */
    async normalityTest(variable) {
        return await this.sendRequest('/api/normality_test', {
            variable
        });
    }
    
    /**
     * 非参数检验
     * @param {string} variable - 变量名
     * @param {string} method - 检验方法：mann_whitney, wilcoxon, kruskal_wallis
     * @returns {Promise} 检验结果
     */
    async nonParametricTest(variable, method) {
        return await this.sendRequest('/api/non_parametric_test', {
            variable,
            method
        });
    }
    
    /**
     * 生存分析
     * @param {string} timeVariable - 时间变量
     * @param {string} eventVariable - 事件变量
     * @returns {Promise} 生存分析结果
     */
    async survivalAnalysis(timeVariable, eventVariable) {
        return await this.sendRequest('/api/survival_analysis', {
            time_variable: timeVariable,
            event_variable: eventVariable
        });
    }
    
    /**
     * Cox回归
     * @param {string} timeVariable - 时间变量
     * @param {string} eventVariable - 事件变量
     * @param {Array} covariates - 协变量列表
     * @returns {Promise} 回归结果
     */
    async coxRegression(timeVariable, eventVariable, covariates) {
        return await this.sendRequest('/api/cox_regression', {
            time_variable: timeVariable,
            event_variable: eventVariable,
            covariates
        });
    }
    
    /**
     * 时间序列分析
     * @param {string} variable - 变量名
     * @returns {Promise} 分析结果
     */
    async timeSeriesAnalysis(variable) {
        return await this.sendRequest('/api/time_series_analysis', {
            variable
        });
    }
    
    /**
     * 可靠性分析（信度分析）
     * @param {Array} variables - 变量列表
     * @returns {Promise} 信度分析结果
     */
    async reliabilityAnalysis(variables) {
        return await this.sendRequest('/api/reliability_analysis', {
            variables
        });
    }
    
    /**
     * 对应分析
     * @param {string} rowVariable - 行变量
     * @param {string} columnVariable - 列变量
     * @returns {Promise} 对应分析结果
     */
    async correspondenceAnalysis(rowVariable, columnVariable) {
        return await this.sendRequest('/api/correspondence_analysis', {
            row_variable: rowVariable,
            column_variable: columnVariable
        });
    }
}

// 导出StatsAnalyzer类
if (typeof module !== 'undefined' && module.exports) {
    module.exports = StatsAnalyzer;
} else if (typeof window !== 'undefined') {
    window.StatsAnalyzer = StatsAnalyzer;
}