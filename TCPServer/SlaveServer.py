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



class UploadTCPHandler(SocketServer.BaseRequestHandler):
    def handle(self):
        file = open('pythonfile.blk', 'wb+')
        while True:
            print 'new send'
            self.data = self.request.recv(1024*1024*64)
            print sys.getsizeof(self.data)
            if sys.getsizeof(self.data) == 37:
                break
            file.write(self.data)
            file.flush()
        file.close()

if __name__ == "__main__":
    HOST, PORT = "localhost", 6001

    # Create the server, binding to localhost on port 9999
    server = SocketServer.TCPServer((HOST, PORT), UploadTCPHandler)

    # Activate the server; this will keep running until you
    # interrupt the program with Ctrl-C
    server.serve_forever()
