/**
 * 绘图功能模块
 * 负责生成各种图表，包括基础图表、高级图表和交互式可视化
 */

class ChartManager {
    constructor() {
        this.charts = {};
    }
    
    /**
     * 初始化图表
     * @param {string} containerId - 容器ID
     * @returns {Object} ECharts实例
     */
    initChart(containerId) {
        const container = document.getElementById(containerId);
        if (!container) return null;
        
        const chart = echarts.init(container);
        this.charts[containerId] = chart;
        
        // 响应式调整
        window.addEventListener('resize', () => {
            chart.resize();
        });
        
        return chart;
    }
    
    /**
     * 生成条形图
     * @param {string} containerId - 容器ID
     * @param {Object} data - 数据
     * @param {string} xField - X轴字段
     * @param {string} yField - Y轴字段
     */
    barChart(containerId, data, xField, yField) {
        const chart = this.initChart(containerId);
        if (!chart) return;
        
        const xData = data[xField];
        const yData = data[yField];
        
        const option = {
            title: {
                text: `${yField} by ${xField}`
            },
            tooltip: {
                trigger: 'axis',
                axisPointer: {
                    type: 'shadow'
                }
            },
            grid: {
                left: '3%',
                right: '4%',
                bottom: '3%',
                containLabel: true
            },
            xAxis: {
                type: 'category',
                data: xData,
                axisLabel: {
                    rotate: 45
                }
            },
            yAxis: {
                type: 'value'
            },
            series: [{
                name: yField,
                type: 'bar',
                data: yData,
                itemStyle: {
                    color: '#1890ff'
                }
            }]
        };
        
        chart.setOption(option);
    }
    
    /**
     * 生成折线图
     * @param {string} containerId - 容器ID
     * @param {Object} data - 数据
     * @param {string} xField - X轴字段
     * @param {string} yField - Y轴字段
     */
    lineChart(containerId, data, xField, yField) {
        const chart = this.initChart(containerId);
        if (!chart) return;
        
        const xData = data[xField];
        const yData = data[yField];
        
        const option = {
            title: {
                text: `${yField} over ${xField}`
            },
            tooltip: {
                trigger: 'axis'
            },
            grid: {
                left: '3%',
                right: '4%',
                bottom: '3%',
                containLabel: true
            },
            xAxis: {
                type: 'category',
                data: xData
            },
            yAxis: {
                type: 'value'
            },
            series: [{
                name: yField,
                type: 'line',
                data: yData,
                smooth: true,
                itemStyle: {
                    color: '#1890ff'
                }
            }]
        };
        
        chart.setOption(option);
    }
    
    /**
     * 生成散点图
     * @param {string} containerId - 容器ID
     * @param {Object} data - 数据
     * @param {string} xField - X轴字段
     * @param {string} yField - Y轴字段
     */
    scatterChart(containerId, data, xField, yField) {
        const chart = this.initChart(containerId);
        if (!chart) return;
        
        const xData = data[xField];
        const yData = data[yField];
        
        const seriesData = xData.map((x, index) => [x, yData[index]]);
        
        const option = {
            title: {
                text: `${yField} vs ${xField}`
            },
            tooltip: {
                trigger: 'item',
                formatter: function(params) {
                    return `${xField}: ${params.value[0]}<br/>${yField}: ${params.value[1]}`;
                }
            },
            grid: {
                left: '3%',
                right: '4%',
                bottom: '3%',
                containLabel: true
            },
            xAxis: {
                type: 'value',
                name: xField
            },
            yAxis: {
                type: 'value',
                name: yField
            },
            series: [{
                name: 'Data',
                type: 'scatter',
                data: seriesData,
                itemStyle: {
                    color: '#1890ff'
                }
            }]
        };
        
        chart.setOption(option);
    }
    
    /**
     * 生成直方图
     * @param {string} containerId - 容器ID
     * @param {Object} data - 数据
     * @param {string} field - 字段名
     */
    histogramChart(containerId, data, field) {
        const chart = this.initChart(containerId);
        if (!chart) return;
        
        const values = data[field];
        
        // 计算直方图数据
        const min = Math.min(...values);
        const max = Math.max(...values);
        const binCount = 10;
        const binWidth = (max - min) / binCount;
        
        const bins = new Array(binCount).fill(0);
        const binLabels = [];
        
        for (let i = 0; i < binCount; i++) {
            const binStart = min + i * binWidth;
            const binEnd = binStart + binWidth;
            binLabels.push(`${binStart.toFixed(1)}-${binEnd.toFixed(1)}`);
        }
        
        values.forEach(value => {
            const binIndex = Math.min(Math.floor((value - min) / binWidth), binCount - 1);
            bins[binIndex]++;
        });
        
        const option = {
            title: {
                text: `Histogram of ${field}`
            },
            tooltip: {
                trigger: 'axis',
                axisPointer: {
                    type: 'shadow'
                }
            },
            grid: {
                left: '3%',
                right: '4%',
                bottom: '3%',
                containLabel: true
            },
            xAxis: {
                type: 'category',
                data: binLabels,
                axisLabel: {
                    rotate: 45
                }
            },
            yAxis: {
                type: 'value',
                name: 'Frequency'
            },
            series: [{
                name: 'Frequency',
                type: 'bar',
                data: bins,
                itemStyle: {
                    color: '#1890ff'
                }
            }]
        };
        
        chart.setOption(option);
    }
    
    /**
     * 生成饼图
     * @param {string} containerId - 容器ID
     * @param {Object} data - 数据
     * @param {string} field - 字段名
     */
    pieChart(containerId, data, field) {
        const chart = this.initChart(containerId);
        if (!chart) return;
        
        const values = data[field];
        
        // 计算频数
        const frequency = {};
        values.forEach(value => {
            frequency[value] = (frequency[value] || 0) + 1;
        });
        
        const seriesData = Object.entries(frequency).map(([name, value]) => ({
            name,
            value
        }));
        
        const option = {
            title: {
                text: `Distribution of ${field}`
            },
            tooltip: {
                trigger: 'item',
                formatter: '{a} <br/>{b}: {c} ({d}%)'
            },
            legend: {
                orient: 'vertical',
                left: 'left'
            },
            series: [{
                name: field,
                type: 'pie',
                radius: '50%',
                data: seriesData,
                emphasis: {
                    itemStyle: {
                        shadowBlur: 10,
                        shadowOffsetX: 0,
                        shadowColor: 'rgba(0, 0, 0, 0.5)'
                    }
                }
            }]
        };
        
        chart.setOption(option);
    }
    
    /**
     * 生成箱线图
     * @param {string} containerId - 容器ID
     * @param {Object} data - 数据
     * @param {string} field - 字段名
     */
    boxChart(containerId, data, field) {
        const chart = this.initChart(containerId);
        if (!chart) return;
        
        const values = data[field].sort((a, b) => a - b);
        
        // 计算箱线图数据
        const q1 = this.calculatePercentile(values, 25);
        const q2 = this.calculatePercentile(values, 50);
        const q3 = this.calculatePercentile(values, 75);
        const iqr = q3 - q1;
        const lowerBound = Math.max(values[0], q1 - 1.5 * iqr);
        const upperBound = Math.min(values[values.length - 1], q3 + 1.5 * iqr);
        
        // 识别异常值
        const outliers = values.filter(value => value < lowerBound || value > upperBound);
        
        const option = {
            title: {
                text: `Box Plot of ${field}`
            },
            tooltip: {
                trigger: 'item',
                axisPointer: {
                    type: 'shadow'
                }
            },
            grid: {
                left: '10%',
                right: '10%',
                bottom: '15%'
            },
            xAxis: {
                type: 'category',
                data: [field],
                boundaryGap: true,
                nameGap: 30,
                splitArea: {
                    show: false
                },
                splitLine: {
                    show: false
                }
            },
            yAxis: {
                type: 'value',
                name: field,
                splitArea: {
                    show: true
                }
            },
            series: [{
                name: field,
                type: 'boxplot',
                data: [{
                    value: [lowerBound, q1, q2, q3, upperBound]
                }]
            }, {
                name: 'Outliers',
                type: 'scatter',
                data: outliers.map(value => [0, value]),
                itemStyle: {
                    color: '#ff4d4f'
                }
            }]
        };
        
        chart.setOption(option);
    }
    
    /**
     * 计算百分位数
     * @param {Array} values - 排序后的数组
     * @param {number} percentile - 百分位数（0-100）
     * @returns {number} 百分位数值
     */
    calculatePercentile(values, percentile) {
        const index = (percentile / 100) * (values.length - 1);
        const lower = Math.floor(index);
        const upper = Math.ceil(index);
        const weight = index - lower;
        
        if (upper === lower) return values[lower];
        return values[lower] * (1 - weight) + values[upper] * weight;
    }
    
    /**
     * 生成热力图
     * @param {string} containerId - 容器ID
     * @param {Object} data - 数据
     * @param {string} xField - X轴字段
     * @param {string} yField - Y轴字段
     * @param {string} valueField - 值字段
     */
    heatmapChart(containerId, data, xField, yField, valueField) {
        const chart = this.initChart(containerId);
        if (!chart) return;
        
        const xValues = [...new Set(data[xField])];
        const yValues = [...new Set(data[yField])];
        
        // 构建热力图数据
        const seriesData = [];
        for (let i = 0; i < data[xField].length; i++) {
            const xIndex = xValues.indexOf(data[xField][i]);
            const yIndex = yValues.indexOf(data[yField][i]);
            seriesData.push([xIndex, yIndex, data[valueField][i]]);
        }
        
        const option = {
            title: {
                text: `${valueField} Heatmap`
            },
            tooltip: {
                position: 'top'
            },
            grid: {
                height: '50%',
                top: '10%'
            },
            xAxis: {
                type: 'category',
                data: xValues,
                splitArea: {
                    show: true
                }
            },
            yAxis: {
                type: 'category',
                data: yValues,
                splitArea: {
                    show: true
                }
            },
            visualMap: {
                min: Math.min(...data[valueField]),
                max: Math.max(...data[valueField]),
                calculable: true,
                orient: 'horizontal',
                left: 'center',
                bottom: '5%'
            },
            series: [{
                name: valueField,
                type: 'heatmap',
                data: seriesData,
                label: {
                    show: true
                },
                emphasis: {
                    itemStyle: {
                        shadowBlur: 10,
                        shadowColor: 'rgba(0, 0, 0, 0.5)'
                    }
                }
            }]
        };
        
        chart.setOption(option);
    }
    
    /**
     * 销毁图表
     * @param {string} containerId - 容器ID
     */
    destroyChart(containerId) {
        if (this.charts[containerId]) {
            this.charts[containerId].dispose();
            delete this.charts[containerId];
        }
    }
}

// 导出ChartManager类
if (typeof module !== 'undefined' && module.exports) {
    module.exports = ChartManager;
} else if (typeof window !== 'undefined') {
    window.ChartManager = ChartManager;
}