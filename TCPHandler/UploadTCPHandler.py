import SocketServer
import sys
import xmlrpclib
from util import const, block_ope
import time


class UploadTCPHandler(SocketServer.BaseRequestHandler):
    def handle(self):
        i = 1
        j = 0
        _timestamp = int(time.time())
        _file = block_ope.open_block(i, j, _timestamp)
        while True:
            self.data = self.request.recv(const.chunk_size)
            size = sys.getsizeof(self.data)
            if size == 37:
                break
            if block_ope.is_block(i, size):
                _file.close()
                j += 1
                _timestamp = int(time.time())
                print '======================================================================================'
                for i in range(i+1, 21):
                    if not block_ope.inuse_block(i):
                        _file = block_ope.open_block(i, j, _timestamp)
                        break
            print i

            _file.write(self.data)
            _file.flush()
            self.server._shutdown_request = True
        # proxy = xmlrpclib.ServerProxy("http://localhost:6000/")
        # proxy._sendMeta([])