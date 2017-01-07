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

from SimpleXMLRPCServer import SimpleXMLRPCServer
from util import const, config_ope, file_ope, meta_ope
import cPickle as pickle
from SlaveServer import SlaveServer
import xmlrpclib

global masterServer


class MasterServer:
    def __init__(self):
        self.num_slaves = 4
        self.replication = 2
        self.entries = []
        self.slaves = []
        self.bitmap = []
        s_f = config_ope.read_slaves()
        for slave in file_ope.read_in_lines(s_f):
            self.slaves.append(slave)
            proxy = xmlrpclib.ServerProxy("http://%s:%d" % (slave, const.rpc_port))
            self.bitmap.append(proxy.get_meta())


def get_unuse(_blks, _num):
    res = []
    for i in range(0, len(_blks)):
        if _blks[i] == 0:
            res.append(i)
            if len(res) == _num:
                break
    return res


def _put(name, size):
    result = []
    blk_num = size / const.chunk_size if size % const.chunk_size == 0 else size / const.chunk_size + 1
    temp = blk_num / masterServer.num_slaves
    delt = 0
    for i in range(0, masterServer.num_slaves):
        if delt == 0:
            res = get_unuse(masterServer.bitmap[i], temp)
            delt = temp - len(res)
        else:
            res = get_unuse(masterServer.bitmap[i], temp + delt)
            delt = temp + delt - len(res)

        result.append([masterServer.slaves[i], res])
    if delt > 0:
        return -1

    else:
        masterServer.entries.append({name: result})
        return result


def _get(name):
    return masterServer.entries[name]


def _update():
    pass


def _send_meta():
    pass


if __name__ == "__main__":
    config_ope.create_config()
    meta_ope.create_meta()
    try:
        f = open('fsimage', 'rb')
        masterServer = pickle.load(f)
    except:
        masterServer = MasterServer()
    server = SimpleXMLRPCServer(('localhost', const.rpc_port))
    print "Listening on port 6000..."
    server.register_multicall_functions()
    server.register_function(_put, '_put')
    server.register_function(_get, '_get')
    server.register_function(_update, '_update')
    server.register_function(_send_meta, '_send_meta')
    server.serve_forever()
