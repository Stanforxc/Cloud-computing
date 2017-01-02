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

import SocketServer
import sys
import time
import xmlrpclib
import os

chunk_size = 1024*1024*64
def read_in_chunks(_file, chunk_size):

    while True:
        chunk_data = _file.read(chunk_size)

        # if not chunk_data:
        #     break
        yield chunk_data

absPath = '/hadoop1'
blks = []

class UploadTCPHandler(SocketServer.BaseRequestHandler):
    def handle(self):
        for i in range(1, 10):
            _path = absPath + '/block' + str(i)
            if not os.path.exists(_path):
                os.makedirs(_path)
                break
        _timestamp = int(time.time())
        print _path
        _fileName = _path + '/' + str(_timestamp) + '.blk'
        file = open(_fileName, 'wb+')
        while True:
            print 'new send1'
            self.data = self.request.recv(chunk_size)
            print sys.getsizeof(self.data)
            if sys.getsizeof(self.data) == 37:
                break
            file.write(self.data)
            file.flush()
        file.close()

        # proxy = xmlrpclib.ServerProxy("http://localhost:6000/")
        # proxy._sendMeta([])


class DownloadTCPHandler(SocketServer.BaseRequestHandler):
    def handle(self):

        for blk in blks:
            _path = absPath + '/block' + str(blk)
            files = os.listdir(_path)
            file = open(absPath + '/block' + str(blk) + '/' + files[0], 'wb+')

            for chunk in read_in_chunks(file, chunk_size):
                self.request.sendall(chunk)

            file.close()

if __name__ == "__main__":
    HOST, PORT = "localhost", 6001

    # Create the server, binding to localhost on port 9999
    server = SocketServer.TCPServer((HOST, PORT), UploadTCPHandler)
    if not os.path.exists(absPath):
        os.makedirs(absPath)
    # Activate the server; this will keep running until you
    # interrupt the program with Ctrl-C
    server.serve_forever()

    HOST2, PORT2 = "localhost", 6003

    # Create the server, binding to localhost on port 9999
    server2 = SocketServer.TCPServer((HOST2, PORT2), DownloadTCPHandler)
    # Activate the server; this will keep running until you
    # interrupt the program with Ctrl-C
    server2.serve_forever()
