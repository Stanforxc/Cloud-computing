#!/usr/bin/python

class entry(object):
    def __init__(self, name, blk_num, *blks):
        self.name = name
        self.blk_num = blk_num
        self.blks = blks