#!/usr/bin/python
# -*- coding: utf-8 -*-

t = [1, 2, 3, 4]

def fib(max):
    n, a, b = 0, 0, 1
    while n < max-2:
        yield b
        a, b = b, a + b
        n = n + 1

for t in fib(6):
    print t