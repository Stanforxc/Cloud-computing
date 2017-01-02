#!/usr/bin/python
# -*- coding: utf-8 -*-

# import socket
# import threading
# import time


import Queue
import SocketServer
import time

import QueueManager
from TCPHandler import UploadTCPHandler

if __name__ == "__main__":
    HOST, PORT = "localhost", 9999

    # Create the server, binding to localhost on port 9999
    server = SocketServer.TCPServer((HOST, PORT), UploadTCPHandler)

    # Activate the server; this will keep running until you
    # interrupt the program with Ctrl-C
    server.serve_forever()


# s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
#
# s.bind(('127.0.0.1', 9999))
#
# s.listen(5)
# print 'Waiting for connection...'
#
# def tcplink(sock, addr):
#     print 'Accept new connection from %s:%s...' % addr
#     sock.send('Welcome!')
#     while True:
#         data = sock.recv(1024*1024*64)
#         time.sleep(1)
#         if data == 'exit' or not data:
#             break
#         sock.send('Hello, %s!' % data)
#     sock.close()
#     print 'Connection from %s:%s closed.' % addr
#
# while True:
#     # 接受一个新连接:
#     sock, addr = s.accept()
#     # 创建新线程来处理TCP连接:
#     t = threading.Thread(target=tcplink, args=(sock, addr))
#     t.start()
#


QueueManager.register('get_task_queue')
QueueManager.register('get_result_queue')

# 连接到服务器，也就是运行taskmanager.py的机器:
server_addr = '127.0.0.1'
print('Connect to server %s...' % server_addr)
# 端口和验证码注意保持与taskmanager.py设置的完全一致:
m = QueueManager(address=(server_addr, 5000), authkey='abc')
# 从网络连接:
m.connect()
# 获取Queue的对象:
task = m.get_task_queue()
result = m.get_result_queue()
# 从task队列取任务,并把结果写入result队列:
for i in range(10):
    try:
        n = task.get(timeout=1)
        print('run task %d * %d...' % (n, n))
        r = '%d * %d = %d' % (n, n, n*n)
        time.sleep(1)
        result.put(r)
    except Queue.Empty:
        print('task queue is empty.')
# 处理结束:
print('worker exit.')