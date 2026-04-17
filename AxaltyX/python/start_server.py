#!/usr/bin/env python3
# 启动Python服务器的脚本

import subprocess
import sys
import os
import time

# 启动Flask服务器
print("启动Python统计服务器...")
server_process = subprocess.Popen([
    sys.executable, 
    os.path.join(os.path.dirname(__file__), 'server.py')
])

print(f"服务器进程ID: {server_process.pid}")

# 等待服务器启动
time.sleep(2)

print("服务器启动完成，可以开始使用AxaltyX了！")

# 保持脚本运行，直到被终止
try:
    while True:
        time.sleep(1)
except KeyboardInterrupt:
    print("正在停止服务器...")
    server_process.terminate()
    server_process.wait()
    print("服务器已停止")
