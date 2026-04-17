/**
 * 数据管理模块
 * 负责数据的导入、导出、清洗和变量管理
 */

class DataManager {
    constructor() {
        this.data = null;
        this.variables = [];
    }
    
    /**
     * 加载数据
     * @param {Object} data - 数据对象
     */
    loadData(data) {
        this.data = data;
        this.updateVariables();
    }
    
    /**
     * 更新变量列表
     */
    updateVariables() {
        if (!this.data) {
            this.variables = [];
            return;
        }
        
        this.variables = Object.keys(this.data).map(key => {
            const values = this.data[key];
            const type = this.detectVariableType(values);
            return {
                name: key,
                type: type,
                count: values.length,
                missing: this.countMissing(values)
            };
        });
    }
    
    /**
     * 检测变量类型
     * @param {Array} values - 变量值数组
     * @returns {string} 变量类型
     */
    detectVariableType(values) {
        if (!values || values.length === 0) return 'unknown';
        
        const nonNullValues = values.filter(v => v !== null && v !== undefined && v !== '');
        if (nonNullValues.length === 0) return 'unknown';
        
        const firstValue = nonNullValues[0];
        if (typeof firstValue === 'number') return 'numeric';
        if (typeof firstValue === 'string') {
            // 检查是否为日期
            if (!isNaN(Date.parse(firstValue))) return 'date';
            // 检查是否为分类变量（唯一值少于总长度的10%）
            const uniqueValues = new Set(nonNullValues);
            if (uniqueValues.size / nonNullValues.length < 0.1) return 'categorical';
            return 'string';
        }
        return 'unknown';
    }
    
    /**
     * 计算缺失值数量
     * @param {Array} values - 变量值数组
     * @returns {number} 缺失值数量
     */
    countMissing(values) {
        return values.filter(v => v === null || v === undefined || v === '').length;
    }
    
    /**
     * 导入CSV数据
     * @param {string} csvString - CSV字符串
     * @returns {Object} 导入的数据
     */
    importCSV(csvString) {
        const lines = csvString.split('\n').filter(line => line.trim() !== '');
        if (lines.length === 0) return null;
        
        const headers = lines[0].split(',').map(header => header.trim());
        const data = {};
        
        headers.forEach(header => {
            data[header] = [];
        });
        
        for (let i = 1; i < lines.length; i++) {
            const values = lines[i].split(',').map(value => {
                const trimmed = value.trim();
                if (trimmed === '') return null;
                if (!isNaN(trimmed) && trimmed !== '') return parseFloat(trimmed);
                return trimmed;
            });
            
            headers.forEach((header, index) => {
                data[header].push(values[index]);
            });
        }
        
        this.loadData(data);
        return data;
    }
    
    /**
     * 导出为CSV
     * @returns {string} CSV字符串
     */
    exportCSV() {
        if (!this.data) return '';
        
        const headers = Object.keys(this.data);
        const lines = [headers.join(',')];
        
        const rowCount = Object.values(this.data)[0].length;
        for (let i = 0; i < rowCount; i++) {
            const row = headers.map(header => {
                const value = this.data[header][i];
                if (value === null || value === undefined) return '';
                if (typeof value === 'string' && value.includes(',')) {
                    return `"${value}"`;
                }
                return value;
            });
            lines.push(row.join(','));
        }
        
        return lines.join('\n');
    }
    
    /**
     * 处理缺失值
     * @param {string} variable - 变量名
     * @param {string} method - 处理方法：mean, median, mode, remove
     * @returns {Object} 处理后的数据
     */
    handleMissing(variable, method) {
        if (!this.data || !this.data[variable]) return this.data;
        
        const values = this.data[variable];
        let fillValue;
        
        switch (method) {
            case 'mean':
                fillValue = this.calculateMean(values);
                break;
            case 'median':
                fillValue = this.calculateMedian(values);
                break;
            case 'mode':
                fillValue = this.calculateMode(values);
                break;
            case 'remove':
                // 移除包含缺失值的行
                this.removeRowsWithMissing(variable);
                return this.data;
            default:
                return this.data;
        }
        
        // 填充缺失值
        this.data[variable] = values.map(value => {
            return (value === null || value === undefined || value === '') ? fillValue : value;
        });
        
        return this.data;
    }
    
    /**
     * 计算均值
     * @param {Array} values - 数值数组
     * @returns {number} 均值
     */
    calculateMean(values) {
        const numericValues = values.filter(v => typeof v === 'number' && !isNaN(v));
        if (numericValues.length === 0) return 0;
        return numericValues.reduce((sum, v) => sum + v, 0) / numericValues.length;
    }
    
    /**
     * 计算中位数
     * @param {Array} values - 数值数组
     * @returns {number} 中位数
     */
    calculateMedian(values) {
        const numericValues = values.filter(v => typeof v === 'number' && !isNaN(v)).sort((a, b) => a - b);
        if (numericValues.length === 0) return 0;
        const mid = Math.floor(numericValues.length / 2);
        return numericValues.length % 2 === 0 ? (numericValues[mid - 1] + numericValues[mid]) / 2 : numericValues[mid];
    }
    
    /**
     * 计算众数
     * @param {Array} values - 数组
     * @returns {any} 众数
     */
    calculateMode(values) {
        const nonNullValues = values.filter(v => v !== null && v !== undefined && v !== '');
        if (nonNullValues.length === 0) return null;
        
        const frequency = {};
        nonNullValues.forEach(value => {
            frequency[value] = (frequency[value] || 0) + 1;
        });
        
        let maxFreq = 0;
        let mode = null;
        Object.entries(frequency).forEach(([value, freq]) => {
            if (freq > maxFreq) {
                maxFreq = freq;
                mode = value;
            }
        });
        
        return mode;
    }
    
    /**
     * 移除包含缺失值的行
     * @param {string} variable - 变量名
     */
    removeRowsWithMissing(variable) {
        if (!this.data || !this.data[variable]) return;
        
        const indicesToKeep = [];
        const values = this.data[variable];
        
        values.forEach((value, index) => {
            if (value !== null && value !== undefined && value !== '') {
                indicesToKeep.push(index);
            }
        });
        
        // 保留有效行
        Object.keys(this.data).forEach(key => {
            this.data[key] = indicesToKeep.map(index => this.data[key][index]);
        });
    }
    
    /**
     * 添加新变量
     * @param {string} name - 变量名
     * @param {Array} values - 变量值
     */
    addVariable(name, values) {
        if (!this.data) {
            this.data = { [name]: values };
        } else {
            // 确保值的长度与其他变量一致
            const rowCount = Object.values(this.data)[0].length;
            if (values.length !== rowCount) {
                throw new Error('变量值长度与数据集不一致');
            }
            this.data[name] = values;
        }
        this.updateVariables();
    }
    
    /**
     * 删除变量
     * @param {string} name - 变量名
     */
    deleteVariable(name) {
        if (this.data && this.data[name]) {
            delete this.data[name];
            this.updateVariables();
        }
    }
    
    /**
     * 重命名变量
     * @param {string} oldName - 旧变量名
     * @param {string} newName - 新变量名
     */
    renameVariable(oldName, newName) {
        if (this.data && this.data[oldName]) {
            this.data[newName] = this.data[oldName];
            delete this.data[oldName];
            this.updateVariables();
        }
    }
    
    /**
     * 转换变量类型
     * @param {string} variable - 变量名
     * @param {string} type - 目标类型：numeric, string, date
     */
    convertVariableType(variable, type) {
        if (!this.data || !this.data[variable]) return;
        
        this.data[variable] = this.data[variable].map(value => {
            if (value === null || value === undefined || value === '') return value;
            
            switch (type) {
                case 'numeric':
                    return parseFloat(value);
                case 'string':
                    return String(value);
                case 'date':
                    return new Date(value).toISOString();
                default:
                    return value;
            }
        });
        
        this.updateVariables();
    }
}

// 导出DataManager类
if (typeof module !== 'undefined' && module.exports) {
    module.exports = DataManager;
} else if (typeof window !== 'undefined') {
    window.DataManager = DataManager;
}