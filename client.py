#!/usr/bin/python
# -*- coding: utf-8 -*-

import socket
import xmlrpclib
import os, sys
from util import const
from util import file_ope


_file = open('/home/huang/Downloads/VMware-Workstation-Full-12.5.2-4638234.x86_64.bundle', 'rb')

size = os.path.getsize('/home/huang/Downloads/VMware-Workstation-Full-12.5.2-4638234.x86_64.bundle')

proxy = xmlrpclib.ServerProxy("http://localhost:%d" % const.rpc_port)
addrs = proxy._put('df', size)
print tuple(addrs)

proxy2 = xmlrpclib.ServerProxy("http://localhost:%d" % 10000)


#
#     # Connect to server and send data


# for addr in addrs:
#     try:
#         i = 0
#         for chunk in file_chunk.read_in_chunks(_file, const.chunk_size):
#             if i == len(addr[1]):
#                 break
#             sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
#             print addr[1][i]
#             port = proxy2._write(addr[1][i])
#             i += 1
#             print port
#             sock.connect((addr[0], port))
#             print _file.tell()
#             sock.sendall(chunk)
#     finally:
#         sock.close()



addrs = proxy._get('df', size)
_file2 = open('/home/huang/Downloads/test.bundle', 'wb+')


for addr in addrs:
    try:
        for i in addr[1]:
            sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
            print i
            size = 0
            port = proxy2._read(i)
            sock.connect((addr[0], port))
            sock.send('daf')
            while True:
                try:
                    data = sock.recv(const.chunk_size)
                    size = sys.getsizeof(data)
                    print size
                    if size == 37:
                        break
                    _file2.write(data)
                    _file2.flush()
                except:
                    #sock.shutdown(socket.SHUT_WR)
                    sock.close()
                    print size
                    break
            #sock.shutdown(socket.SHUT_WR)
            sock.close()
    finally:
        _file2.close()
