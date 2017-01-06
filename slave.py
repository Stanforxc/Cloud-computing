#!/usr/bin/python
# -*- coding: utf-8 -*-
import os
from util import const
#import util.const as const

from util import *
# from util import dcf

# print util.abc
# print dcf
print dir()
#
if not os.listdir(const.abs_path + '/block' + str(1)):
    print 'in'
