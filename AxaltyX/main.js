const { app, BrowserWindow, Menu } = require('electron');
const path = require('path');
const { spawn } = require('child_process');

// 保持窗口对象的全局引用，避免被垃圾回收
let mainWindow;
// 保持Python服务器进程的引用
let pythonServer;

function createWindow() {
  // 启动Python服务器
  console.log('启动Python统计服务器...');
  const pythonExecutable = process.platform === 'win32' ? 'python' : 'python3';
  pythonServer = spawn(pythonExecutable, [path.join(__dirname, 'python', 'server.py')]);
  
  pythonServer.stdout.on('data', (data) => {
    console.log(`Python服务器输出: ${data}`);
  });
  
  pythonServer.stderr.on('data', (data) => {
    console.error(`Python服务器错误: ${data}`);
  });
  
  pythonServer.on('close', (code) => {
    console.log(`Python服务器进程退出，代码: ${code}`);
  });
  
  // 创建浏览器窗口
  mainWindow = new BrowserWindow({
    width: 1200,
    height: 800,
    minWidth: 1024,
    minHeight: 768,
    webPreferences: {
      preload: path.join(__dirname, 'preload.js'),
      nodeIntegration: true,
      contextIsolation: false
    },
    title: 'AxaltyX - 专业统计分析软件'
  });

  // 加载应用的 index.html
  mainWindow.loadFile('index.html');

  // 打开开发者工具
  // mainWindow.webContents.openDevTools();

  // 窗口关闭时触发
  mainWindow.on('closed', function () {
    mainWindow = null;
  });

  // 创建菜单
  createMenu();
}

function createMenu() {
  const template = [
    {
      label: '文件',
      submenu: [
        {
          label: '新建项目',
          accelerator: 'CmdOrCtrl+N',
          click: () => {
            mainWindow.webContents.send('menu-action', 'new-project');
          }
        },
        {
          label: '打开项目',
          accelerator: 'CmdOrCtrl+O',
          click: () => {
            mainWindow.webContents.send('menu-action', 'open-project');
          }
        },
        {
          label: '保存项目',
          accelerator: 'CmdOrCtrl+S',
          click: () => {
            mainWindow.webContents.send('menu-action', 'save-project');
          }
        },
        { type: 'separator' },
        {
          label: '退出',
          accelerator: 'CmdOrCtrl+Q',
          click: () => app.quit()
        }
      ]
    },
    {
      label: '编辑',
      submenu: [
        { label: '撤销', accelerator: 'CmdOrCtrl+Z', role: 'undo' },
        { label: '重做', accelerator: 'CmdOrCtrl+Y', role: 'redo' },
        { type: 'separator' },
        { label: '剪切', accelerator: 'CmdOrCtrl+X', role: 'cut' },
        { label: '复制', accelerator: 'CmdOrCtrl+C', role: 'copy' },
        { label: '粘贴', accelerator: 'CmdOrCtrl+V', role: 'paste' },
        { label: '全选', accelerator: 'CmdOrCtrl+A', role: 'selectAll' }
      ]
    },
    {
      label: '分析',
      submenu: [
        {
          label: '描述性统计',
          submenu: [
            { label: '频数分析' },
            { label: '描述性统计量' },
            { label: '交叉表与卡方检验' }
          ]
        },
        {
          label: '假设检验',
          submenu: [
            { label: '单样本 t 检验' },
            { label: '独立样本 t 检验' },
            { label: '配对样本 t 检验' },
            { label: '方差分析' }
          ]
        },
        {
          label: '回归分析',
          submenu: [
            { label: '线性回归' },
            { label: 'Logistic 回归' },
            { label: '非线性回归' }
          ]
        }
      ]
    },
    {
      label: '绘图',
      submenu: [
        { label: '基础图表' },
        { label: '高级图表' },
        { label: '交互式可视化' }
      ]
    },
    {
      label: '工具',
      submenu: [
        { label: '数据导入' },
        { label: '数据清洗' },
        { label: '变量管理' }
      ]
    },
    {
      label: '帮助',
      submenu: [
        { label: '文档' },
        { label: '教程' },
        { label: '关于' }
      ]
    }
  ];

  const menu = Menu.buildFromTemplate(template);
  Menu.setApplicationMenu(menu);
}

// Electron 完成初始化后创建窗口
app.on('ready', createWindow);

// 关闭所有窗口时退出应用
app.on('window-all-closed', function () {
  if (pythonServer) {
    console.log('停止Python服务器...');
    pythonServer.kill();
  }
  if (process.platform !== 'darwin') app.quit();
});

// 激活应用时创建窗口（Mac）
app.on('activate', function () {
  if (mainWindow === null) createWindow();
  // 确保Python服务器正在运行
  if (!pythonServer || pythonServer.killed) {
    console.log('重新启动Python服务器...');
    const pythonExecutable = process.platform === 'win32' ? 'python' : 'python3';
    pythonServer = spawn(pythonExecutable, [path.join(__dirname, 'python', 'server.py')]);
    
    pythonServer.stdout.on('data', (data) => {
      console.log(`Python服务器输出: ${data}`);
    });
    
    pythonServer.stderr.on('data', (data) => {
      console.error(`Python服务器错误: ${data}`);
    });
    
    pythonServer.on('close', (code) => {
      console.log(`Python服务器进程退出，代码: ${code}`);
    });
  }
});