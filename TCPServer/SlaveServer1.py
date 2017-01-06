# import SocketServer
#
# class MasterServer(SocketServer.ThreadingMixIn, SocketServer.TCPServer):
# import socket
# import threading
# import SocketServer
# from TCPHandler import UploadTCPHandler
#
#
# class ThreadedTCPServer(SocketServer.ThreadingMixIn, SocketServer.TCPServer):
#     pass
#
#
# def client(_ip, _port, message):
#     sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
#     sock.connect((_ip, _port))
#     try:
#         sock.sendall(message)
#         response = sock.recv(1024)
#         print "Received: {}".format(response)
#     finally:
#         sock.close()
#
# if __name__ == "__main__":
#     # Port 0 means to select an arbitrary unused port
#     HOST, PORT = "localhost", 0
#
#     server = ThreadedTCPServer((HOST, PORT), UploadTCPHandler)
#     ip, port = server.server_address  # Start a thread with the server -- that thread will then start one
#     # more thread for each request
#     server_thread = threading.Thread(target=server.serve_forever)
#     # Exit the server thread when the main thread terminates
#     server_thread.daemon = True
#     server_thread.start()
#     print "Server loop running in thread:", server_thread.name
#
#     client(ip, port, "Hello World 1")
#     client(ip, port, "Hello World 2")
#     client(ip, port, "Hello World 3")
#
#     server.shutdown()

import SocketServer, threading, time
from util import file_chunk, const
import os, socket, sys

from TCPHandler.UploadTCPHandler import UploadTCPHandler
from util import block_ope
from SimpleXMLRPCServer import SimpleXMLRPCServer
# def read_in_chunks(_file, chunk_size):
#
#     while True:
#         chunk_data = _file.read(chunk_size)
#
#         # if not chunk_data:
#         #     break
#         yield chunk_data

absPath = '/hadoop1'
blks = []

# class UploadTCPHandler(SocketServer.BaseRequestHandler):
#     def handle(self):
#         for i in range(1, 10):
#             _path = absPath + '/block' + str(i)
#             if not os.path.exists(_path):
#                 os.makedirs(_path)
#                 break
#         _timestamp = int(time.time())
#         print _path
#         _fileName = _path + '/' + str(_timestamp) + '.blk'
#         file = open(_fileName, 'wb+')
#         while True:
#             print 'new send1'
#             self.data = self.request.recv(const.chunk_size)
#             print sys.getsizeof(self.data)
#             if sys.getsizeof(self.data) == 37:
#                 break
#             file.write(self.data)
#             file.flush()
#         file.close()

        # proxy = xmlrpclib.ServerProxy("http://localhost:6000/")
        # proxy._sendMeta([])
# class UploadTCPHandler(SocketServer.BaseRequestHandler):
#     def handle(self):
#         i = -1
#         while True:
#             print 'in'
#             for i in range(i+1, 21):
#                 if not block_ope.inuse_block(i):
#                     break
#
#             print 'new send1'
#             self.data = self.request.recv(const.chunk_size)
#             print sys.getsizeof(self.data)
#             if sys.getsizeof(self.data) == 37:
#                 break
#             block_ope.write_block(i, self.data)
#         # proxy = xmlrpclib.ServerProxy("http://localhost:6000/")
#         # proxy._sendMeta([])


socket_pool = {}


def get_socket():
    s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    i = 0
    for i in range(7010, 65535):
        try:
            s.bind(('localhost', i))
            print i
            return i
        except:
            continue
    return -1


def upload(sock, blk_num):
    print 'in'
    _timestamp = int(time.time())
    _file = block_ope.open_block(blk_num, _timestamp)
    while True:
        data = sock.recv(const.chunk_size)
        size = sys.getsizeof(data)
        print size
        if size == 37:
            break
        _file.write(data)
        _file.flush()
    _file.close()
    sock.close()


def download(sock, blk_num):
    print 'd'
    _file = block_ope.read_block(blk_num)
    data = _file.read(const.chunk_size)
    size = sys.getsizeof(data)
    print size
    sock.sendall(data)
    _file.close()
    time.sleep(1)
    sock.close()


def upload_listen(s, blk_num):
    while True:
        sock, addr = s.accept()
        t = threading.Thread(target=upload, args=(sock, blk_num))
        t.start()


def download_listen(s, blk_num):
    while True:
        sock, addr = s.accept()
        t = threading.Thread(target=download, args=(sock, blk_num))
        t.start()


def _write(blk_num):
    port = get_socket()
    s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    if port == -1:
        return -1
    s.bind(('localhost', port))
    s.listen(5)
    socket_thread = threading.Thread(target=upload_listen, args=(s, blk_num))
    socket_thread.start()
    return port


def _read(blk_num):
    port = get_socket()
    s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    if port == -1:
        return -1
    s.bind(('localhost', port))
    s.listen(5)
    socket_thread = threading.Thread(target=download_listen, args=(s, blk_num))
    socket_thread.start()
    return port


if __name__ == "__main__":
    for i in range(1, 21):
        block_ope.create_block(i)
    server = SimpleXMLRPCServer(('localhost', 10000))
    server.register_function(_write, '_write')
    server.register_function(_read, '_read')
    server.serve_forever()


    #down_server.close()
    # SocketServer.TCPServer.allow_reuse_address = True
    #
    # server = SocketServer.TCPServer((HOST, PORT), UploadTCPHandler)
    #
    # server.serve_forever()
    # server.socket.close()

    # HOST2, PORT2 = "localhost", const.download_port
    # server2 = SocketServer.TCPServer((HOST2, PORT2), DownloadTCPHandler)
    # server2.serve_forever()
