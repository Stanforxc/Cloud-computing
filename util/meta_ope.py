#!/usr/bin/python
# -*- coding: utf-8 -*-


import getpass
import os
from os.path import join, getsize
from util import const, file_ope


user = getpass.getuser()
prefix_path = '/home/' + user + const.abs_path + '/name'


def create_meta():
    if not os.path.exists(prefix_path):
        os.makedirs(prefix_path)


def read_fsimage():
    _path = prefix_path + '/fsimage'
    return open(_path, 'rb')

def write_fsimage():
    _path = prefix_path + '/fsimage'
    return open(_path, 'wb')