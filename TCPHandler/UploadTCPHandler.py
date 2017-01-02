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
