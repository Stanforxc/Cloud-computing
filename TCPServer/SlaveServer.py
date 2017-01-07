#!/usr/bin/python
# -*- coding: utf-8 -*-


import SocketServer, threading, time
from util import const
import os, socket, sys
from util import block_ope, config_ope
from SimpleXMLRPCServer import SimpleXMLRPCServer


global slaveServer


class SlaveServer:
    def __init__(self):
        self.num_blocks = 20
        self.bitmap = [0] * self.num_blocks
        for i in range(1, self.num_blocks + 1):
            if block_ope.inuse_block(i):
                self.bitmap[i] = 1




def get_socket():
    s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    i = 0
    for i in range(7010, 65535):
        try:
            s.bind(('localhost', i))
            print i
            return i
        except:
            continue
    return -1


def upload(sock, blk_num):
    print 'in'
    _timestamp = int(time.time())
    _file = block_ope.open_block(blk_num, _timestamp)
    while True:
        data = sock.recv(const.chunk_size)
        size = sys.getsizeof(data)
        print size
        if size == 37:
            break
        _file.write(data)
        _file.flush()
    _file.close()
    sock.close()


def download(sock, blk_num):
    print 'blk_num:'+ str(blk_num)
    _file = block_ope.read_block(blk_num)
    data = _file.read(const.chunk_size)
    sock.sendall(data)
    _file.close()
    print socket.SHUT_WR
    sock.shutdown(socket.SHUT_WR)
    while True:
        res = sock.recv(const.chunk_size)
        if sys.getsizeof(res) == 0:
            break
    sock.close()


def upload_listen(s, blk_num):
    while True:
        sock, addr = s.accept()
        t = threading.Thread(target=upload, args=(sock, blk_num))
        t.start()


def download_listen(s, blk_num):
    while True:
        sock, addr = s.accept()
        t = threading.Thread(target=download, args=(sock, blk_num))
        t.start()


def _write(blk_num):
    port = get_socket()
    s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    if port == -1:
        return -1
    s.bind(('localhost', port))
    s.listen(5)
    socket_thread = threading.Thread(target=upload_listen, args=(s, blk_num))
    socket_thread.start()
    return port


def _read(blk_num):
    port = get_socket()
    s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    if port == -1:
        return -1
    s.bind(('localhost', port))
    s.listen(5)
    socket_thread = threading.Thread(target=download_listen, args=(s, blk_num))
    socket_thread.start()
    return port


def get_meta():
    return slaveServer.bitmap


if __name__ == "__main__":
    config_ope.create_config()
    slaveServer = SlaveServer()
    for i in range(1, 21):
        block_ope.create_block(i)
    server = SimpleXMLRPCServer(('localhost', 10000))
    server.register_function(_write, '_write')
    server.register_function(_read, '_read')
    server.serve_forever()


