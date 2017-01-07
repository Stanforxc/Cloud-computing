#!/usr/bin/python
# -*- coding: utf-8 -*-


import getpass
import os
from os.path import join, getsize
from util import const, file_ope


user = getpass.getuser()
prefix_path = '/home/' + user + const.abs_path + '/config'


def create_config():
    if not os.path.exists(prefix_path):
        os.makedirs(prefix_path)

def read_master():
    _path = prefix_path + '/master'
    return open(_path, 'rb')


def read_slaves():
    _path = prefix_path + '/slaves'
    return open(_path, 'rb')


