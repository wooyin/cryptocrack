#!/usr/bin/env python3
# -*- coding: utf-8 -*-
import random
import argparse
from io import StringIO
from functools import partial
import sys

__github__ = 'https://github.com/feng409/core-values-encoder/'
__author__ = 'https://github.com/sym233/core-values-encoder'

core_value = ('富强', '民主', '文明', '和谐',
              '自由', '平等', '公正', '法治',
              '爱国', '敬业', '诚信', '友善')


is_py3 = sys.version_info[0] == 3


def str2hex(unicode_str):
    """
    转换字符串为16进制生成器
    :param unicode_str:
    :return:
    """
    for _ in unicode_str:
        hexs = is_py3 and _.encode('utf-8').hex() or _.encode('hex')
        for h in hexs:
            yield h


def hex2twelve(hex_gen):
    """
    转换16进制为12进制
    其中，对于大于10的十六进制数字，
    采取随机两种方式：
    10 + hex_num - 10 表示，即 a -> 100, f -> 105
    11 + hex_num - 6 表示， 即 a -> 114, f -> 119
    :param hex_gen:
    :return: generator()
    """
    for h in hex_gen:
        h = int(h, 16)
        if h < 10:
            yield h
        elif random.randint(0, 1):
            yield 10
            yield h - 10
        else:
            yield 11
            yield h - 6


def twelve_2_core_value(twelve_iter):
    """
    根据12进制下标转换
    :param twelve_iter:
    :return:
    """
    for index in twelve_iter:
        yield core_value[index]


def core_value_2_twelve(core_value_str):
    """
    将社会主义核心价值观转换为12进制
    :param core_value_str:
    :return:
    """
    for word in iter(partial(StringIO(core_value_str).read, 2), ''):
        yield core_value.index(word)


def twelve2hex(twelve_iter):
    """
    将12进制转换为16进制
    :param twelve_iter:
    :return:
    """
    for twelve in twelve_iter:
        if twelve < 10:
            yield twelve
        elif twelve == 10:
            yield 10 + next(twelve_iter)
        else:
            yield 6 + next(twelve_iter)


def hex2bytes(hex_iter):
    """
    将十六进制转换为bytes对象
    :param hex_iter:
    :return:
    """
    for h in hex_iter:
        b = '{:x}{:x}'.format(h, next(hex_iter))
        yield bytes.fromhex(b)


def encode(origin):
    """
    转换utf-8编码为社会主义核心价值观编码
    :param origin:
    :return:
    """
    hex_str = str2hex(origin)
    twelve = hex2twelve(hex_str)
    core_value_iter = twelve_2_core_value(twelve)
    return ''.join(core_value_iter)


def decode(origin):
    """
    将社会主义核心价值观编码转换为utf-8编码
    :param origin:
    :return:
    """
    twelve_iter = core_value_2_twelve(origin)
    hex_iter = twelve2hex(twelve_iter)
    bytes_iter = hex2bytes(hex_iter)
    return (b''.join(bytes_iter)).decode('utf-8')

