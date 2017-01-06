#!/usr/bin/python
# -*- coding: utf-8 -*-

import getpass
import os
from os.path import join, getsize
from util import const


user = getpass.getuser()
prefix_path = '/home/' + user + const.abs_path + '/block'


def create_block(index):
    _path = prefix_path + str(index)
    if not os.path.exists(_path):
        os.makedirs(_path)


def read_block(index):
    _path = prefix_path + str(index)
    return open(_path + '/' + os.listdir(_path)[0], 'rb')



def open_block(index, _timestamp):

    _path = prefix_path + str(index)
    return open(_path + '/' + str(_timestamp) + '.blk', 'wb+')


def inuse_block(index):
    _path = prefix_path + str(index)
    return len(os.listdir(_path)) != 0


def is_block(index, size):
    print index
    _path = prefix_path + str(index)

    # if len(os.listdir(_path)) != 0:
    #     print 'size' + str(getsize(_path + '/' +os.listdir(_path)[0]))
    return len(os.listdir(_path)) != 0 and getsize(_path + '/' + os.listdir(_path)[0]) + size > const.chunk_size

def delete_block(index):
    _path = prefix_path + str(index)
    os.removedirs(_path)