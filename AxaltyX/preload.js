// preload.js
const { contextBridge, ipcRenderer } = require('electron');

// 向渲染进程暴露API
contextBridge.exposeInMainWorld('electronAPI', {
  // 接收来自主进程的消息
  onMenuAction: (callback) => ipcRenderer.on('menu-action', callback),
  // 向主进程发送消息
  sendMessage: (channel, data) => ipcRenderer.send(channel, data)
});