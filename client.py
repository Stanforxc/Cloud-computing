#!/usr/bin/python
# -*- coding: utf-8 -*-

import socket
import xmlrpclib
import os, sys
from util import const
from util import file_ope


_file = open('/home/huang/Downloads/VMware-Workstation-Full-12.5.2-4638234.x86_64.bundle', 'rb')

size = os.path.getsize('/home/huang/Downloads/VMware-Workstation-Full-12.5.2-4638234.x86_64.bundle')
#proxy = xmlrpclib.ServerProxy("http://localhost:%d" % const.rpc_port)
proxy = xmlrpclib.ServerProxy("http://192.168.1.9:%d" % const.rpc_port)
addrs = proxy._put('df', size)
print tuple(addrs)



#
# for addr in addrs:
#     try:
#         i = 0
#         for chunk in file_ope.read_in_chunks(_file, const.chunk_size):
#             sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
#             print addr[0]
#             print addr[1][i]
#             slave_proxy = xmlrpclib.ServerProxy("http://%s:%d" % (addr[0], const.rpc_port))
#             port = slave_proxy._write(addr[1][i])
#             i += 1
#             print port
#             sock.connect((addr[0], port))
#             print _file.tell()
#             sock.sendall(chunk)
#             if i == len(addr[1]):
#                 break
#     finally:
#         sock.close()



addrs = proxy._get('df')
_file2 = open('/home/huang/Downloads/test.bundle', 'wb+')


for addr in addrs:
    slave_proxy = xmlrpclib.ServerProxy("http://%s:%d" % (addr[0], const.rpc_port))
    try:
        for i in addr[1]:
            sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
            print i
            size = 0
            port = slave_proxy._read(i)
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
                    sock.close()
                    print size
                    break

    finally:
        sock.close()

_file2.close()