#!/usr/bin/python
# -*- coding: utf-8 -*-
import socket
import xmlrpclib
import os




_file = open('/home/huang/Desktop/CentOS-7-x86_64-Minimal-1511.iso', 'rb')

size = os.path.getsize('/home/huang/Desktop/CentOS-7-x86_64-Minimal-1511.iso')

proxy = xmlrpclib.ServerProxy("http://localhost:6000/")

addrs = proxy._put('df', size)
print tuple(addrs)


def read_in_chunks(_file, chunk_size):

    while True:
        chunk_data = _file.read(chunk_size)

        # if not chunk_data:
        #     break
        yield chunk_data


    # Connect to server and send data


for addr in addrs:
    chunk_data = 0
    chunk_size = 1024 * 1024 * 64
    try:
        sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        sock.connect((addr[0], addr[1]))
        i = 0
        for chunk in read_in_chunks(_file, chunk_size):
            print _file.tell()
            if i == addr[2]-1:
                chunk_data = chunk
                break
            i = i + 1
            sock.sendall(chunk)
        sock.sendall(chunk_data)
    finally:
        sock.close()

addrs = proxy._get('df', size)

for addr in addrs:
    chunk_data = 0
    chunk_size = 1024 * 1024 * 64
    try:
        sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        sock.connect((addr[0], addr[1]))

        sock.recv()
    finally:
        sock.close()
