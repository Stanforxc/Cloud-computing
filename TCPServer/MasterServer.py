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

import Queue
from util import const
from SimpleXMLRPCServer import SimpleXMLRPCServer
from multiprocessing.managers import BaseManager
from util import const


def _put(name, size):
    #TODO add entry

    return [['localhost', [1, 2, 3, 4, 5, 6]]]


def _get(name, size):

    return [['localhost', [1, 2, 3, 4, 5, 6]]]


def _update():
    pass


def _sendMeta():
    pass

task_queue = Queue.Queue()


class QueueManager(BaseManager):
    pass

QueueManager.register('get_task_queue', callable=lambda: task_queue)
manager = QueueManager(address=('', const.task_port), authkey='abc')
manager.start()

task = manager.get_task_queue()


server = SimpleXMLRPCServer(('localhost', const.rpc_port))
print "Listening on port 6000..."
server.register_multicall_functions()
server.register_function(_put, '_put')
server.register_function(_get, '_get')
server.register_function(_update, '_update')
server.register_function(_sendMeta, '_sendMeta')
server.serve_forever()
