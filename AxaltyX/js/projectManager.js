/**
 * 项目管理和报告生成模块
 * 负责项目的创建、打开、保存和报告生成
 */

class ProjectManager {
    constructor() {
        this.currentProject = null;
        this.projects = [];
    }
    
    /**
     * 新建项目
     * @param {string} name - 项目名称
     * @param {string} description - 项目描述
     * @returns {Object} 新项目
     */
    createProject(name, description) {
        const project = {
            id: Date.now().toString(),
            name: name || `项目 ${this.projects.length + 1}`,
            description: description || '',
            createdAt: new Date().toISOString(),
            lastModified: new Date().toISOString(),
            data: null,
            analyses: [],
            charts: []
        };
        
        this.currentProject = project;
        this.projects.push(project);
        
        return project;
    }
    
    /**
     * 打开项目
     * @param {string} projectId - 项目ID
     * @returns {Object} 打开的项目
     */
    openProject(projectId) {
        const project = this.projects.find(p => p.id === projectId);
        if (project) {
            this.currentProject = project;
            return project;
        }
        return null;
    }
    
    /**
     * 保存项目
     * @param {Object} project - 项目对象
     * @returns {boolean} 保存成功与否
     */
    saveProject(project) {
        if (!project) project = this.currentProject;
        if (!project) return false;
        
        project.lastModified = new Date().toISOString();
        
        // 这里可以添加实际的保存逻辑，例如保存到本地文件系统
        console.log('保存项目:', project.name);
        
        return true;
    }
    
    /**
     * 保存项目为
     * @param {string} name - 新项目名称
     * @param {Object} project - 项目对象
     * @returns {Object} 新保存的项目
     */
    saveProjectAs(name, project) {
        if (!project) project = this.currentProject;
        if (!project) return null;
        
        const newProject = {
            ...project,
            id: Date.now().toString(),
            name: name,
            createdAt: new Date().toISOString(),
            lastModified: new Date().toISOString()
        };
        
        this.projects.push(newProject);
        this.currentProject = newProject;
        
        return newProject;
    }
    
    /**
     * 删除项目
     * @param {string} projectId - 项目ID
     * @returns {boolean} 删除成功与否
     */
    deleteProject(projectId) {
        const index = this.projects.findIndex(p => p.id === projectId);
        if (index !== -1) {
            this.projects.splice(index, 1);
            if (this.currentProject && this.currentProject.id === projectId) {
                this.currentProject = this.projects.length > 0 ? this.projects[0] : null;
            }
            return true;
        }
        return false;
    }
    
    /**
     * 获取所有项目
     * @returns {Array} 项目列表
     */
    getProjects() {
        return this.projects;
    }
    
    /**
     * 获取当前项目
     * @returns {Object} 当前项目
     */
    getCurrentProject() {
        return this.currentProject;
    }
    
    /**
     * 更新项目数据
     * @param {Object} data - 数据对象
     */
    updateProjectData(data) {
        if (this.currentProject) {
            this.currentProject.data = data;
            this.currentProject.lastModified = new Date().toISOString();
        }
    }
    
    /**
     * 添加分析结果到项目
     * @param {Object} analysis - 分析结果
     */
    addAnalysis(analysis) {
        if (this.currentProject) {
            this.currentProject.analyses.push({
                id: Date.now().toString(),
                timestamp: new Date().toISOString(),
                ...analysis
            });
            this.currentProject.lastModified = new Date().toISOString();
        }
    }
    
    /**
     * 添加图表到项目
     * @param {Object} chart - 图表配置
     */
    addChart(chart) {
        if (this.currentProject) {
            this.currentProject.charts.push({
                id: Date.now().toString(),
                timestamp: new Date().toISOString(),
                ...chart
            });
            this.currentProject.lastModified = new Date().toISOString();
        }
    }
    
    /**
     * 生成分析报告
     * @param {Object} options - 报告选项
     * @returns {string} 报告HTML
     */
    generateReport(options = {}) {
        if (!this.currentProject) return '';
        
        const { title, includeData = true, includeAnalyses = true, includeCharts = true } = options;
        
        let report = `
<!DOCTYPE html>
<html lang="zh-CN">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>${title || this.currentProject.name} - 分析报告</title>
    <style>
        body {
            font-family: -apple-system, BlinkMacSystemFont, 'Segoe UI', Roboto, 'Helvetica Neue', Arial, sans-serif;
            line-height: 1.6;
            color: #333;
            max-width: 800px;
            margin: 0 auto;
            padding: 20px;
        }
        h1, h2, h3, h4 {
            color: #1890ff;
        }
        table {
            width: 100%;
            border-collapse: collapse;
            margin: 20px 0;
        }
        th, td {
            padding: 8px;
            text-align: left;
            border-bottom: 1px solid #e8e8e8;
        }
        th {
            background-color: #fafafa;
            font-weight: 600;
        }
        .section {
            margin-bottom: 30px;
        }
        .meta-info {
            background-color: #f6ffed;
            padding: 15px;
            border-radius: 4px;
            margin-bottom: 20px;
        }
        .chart-container {
            margin: 20px 0;
            padding: 20px;
            background-color: #fafafa;
            border-radius: 4px;
        }
    </style>
</head>
<body>
    <h1>${title || this.currentProject.name}</h1>
    <div class="meta-info">
        <p><strong>项目描述:</strong> ${this.currentProject.description}</p>
        <p><strong>创建时间:</strong> ${new Date(this.currentProject.createdAt).toLocaleString()}</p>
        <p><strong>最后修改:</strong> ${new Date(this.currentProject.lastModified).toLocaleString()}</p>
    </div>`;
        
        // 包含数据
        if (includeData && this.currentProject.data) {
            report += `
    <div class="section">
        <h2>数据概览</h2>
        <table>
            <thead>
                <tr>`;
            
            const columns = Object.keys(this.currentProject.data);
            columns.forEach(col => {
                report += `<th>${col}</th>`;
            });
            
            report += `
                </tr>
            </thead>
            <tbody>`;
            
            const rowCount = Object.values(this.currentProject.data)[0].length;
            for (let i = 0; i < Math.min(rowCount, 10); i++) { // 只显示前10行
                report += `<tr>`;
                columns.forEach(col => {
                    report += `<td>${this.currentProject.data[col][i]}</td>`;
                });
                report += `</tr>`;
            }
            
            if (rowCount > 10) {
                report += `<tr><td colspan="${columns.length}"><em>... 共 ${rowCount} 行数据，仅显示前 10 行</em></td></tr>`;
            }
            
            report += `
            </tbody>
        </table>
    </div>`;
        }
        
        // 包含分析结果
        if (includeAnalyses && this.currentProject.analyses.length > 0) {
            report += `
    <div class="section">
        <h2>分析结果</h2>`;
            
            this.currentProject.analyses.forEach(analysis => {
                report += `
        <div style="margin-bottom: 20px;">
            <h3>${analysis.type || '分析'}</h3>
            <p><em>分析时间: ${new Date(analysis.timestamp).toLocaleString()}</em></p>`;
                
                if (analysis.result) {
                    report += `<pre>${JSON.stringify(analysis.result, null, 2)}</pre>`;
                }
                
                report += `
        </div>`;
            });
            
            report += `
    </div>`;
        }
        
        // 包含图表
        if (includeCharts && this.currentProject.charts.length > 0) {
            report += `
    <div class="section">
        <h2>图表</h2>`;
            
            this.currentProject.charts.forEach(chart => {
                report += `
        <div class="chart-container">
            <h3>${chart.title || '图表'}</h3>
            <p><em>创建时间: ${new Date(chart.timestamp).toLocaleString()}</em></p>
            <div style="height: 400px; background-color: #fff; border: 1px solid #e8e8e8; border-radius: 4px;">
                <p style="text-align: center; line-height: 400px;">图表: ${chart.type}</p>
            </div>
        </div>`;
            });
            
            report += `
    </div>`;
        }
        
        report += `
</body>
</html>`;
        
        return report;
    }
    
    /**
     * 导出报告
     * @param {string} format - 导出格式 (html, pdf, docx)
     * @param {Object} options - 报告选项
     * @returns {string} 导出文件路径
     */
    exportReport(format, options = {}) {
        const report = this.generateReport(options);
        
        // 这里可以添加实际的导出逻辑
        console.log(`导出报告为 ${format} 格式`);
        
        // 返回模拟的文件路径
        return `report.${format}`;
    }
}

// 导出ProjectManager类
if (typeof module !== 'undefined' && module.exports) {
    module.exports = ProjectManager;
} else if (typeof window !== 'undefined') {
    window.ProjectManager = ProjectManager;
}