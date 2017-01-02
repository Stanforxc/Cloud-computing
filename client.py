#!/usr/bin/python
# -*- coding: utf-8 -*-





import socket
import xmlrpclib
from util import const


proxy = xmlrpclib.ServerProxy("http://localhost:6000/")

addrs = proxy.put('df')

_file = open('/home/huang/Desktop/CentOS-7-x86_64-Minimal-1511.iso', 'rb')

sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)


def read_in_chunks(_file, chunk_size):
    """
    Lazy function (generator) to read a file piece by piece.
    Default chunk size: 1M
    You can set your own chunk size
    """

    while True:
        chunk_data = _file.read(chunk_size)
        if not chunk_data:
            break
        yield chunk_data

try:
    # Connect to server and send data
    chunk_size = 1024 * 1024 * 64
    sock.connect((addrs[0][0], addrs[0][1]))

    for chunk in read_in_chunks(_file, chunk_size):

        sock.sendall(chunk)



finally:
    sock.close()
