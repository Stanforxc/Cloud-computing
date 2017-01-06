import SocketServer
import sys


class DownloadTCPHandler(SocketServer.BaseRequestHandler):
    def handle(self):
        while True:
            print 'new send'
            self.request.sendall()
