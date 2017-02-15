# encoding=utf-8
""" common wrapper for python2/3
"""
from __future__ import absolute_import
from __future__ import division
from __future__ import print_function
from __future__ import unicode_literals

__author__ = '1661'
import sys
import six

PY3 = sys.version_info[0] == 3


def change_string_encoding(str_, encoding='utf8'):
    """ 把str | unicode转成指定的encoding, 非str或unicode格式不转换
    :param str_: 要转换的str | unicode
    :param encoding: 要转成的encoding, 如果不需要任何encoding, 请传入unicode. (和标准库
    :rtype : str | unicode
    """

    if isinstance(str_, six.binary_type):
        if encoding == 'utf8':
            return str_
        else:
            str_ = str_.decode('utf8')

    if isinstance(str_, six.string_types):
        if encoding == 'unicode':
            return str_
        else:
            return str_.encode(encoding)

    return str_


def to_builtin_str(str_):
    """ bytes/unicode 根据编码转换成内置str
    py2: unicode to str
    py3: bytes to str
    :param str_:
    :return:
    """
    import sys
    if sys.version_info[0] == 2:
        return change_string_encoding(str_, 'utf8')
    else:
        return change_string_encoding(str_, 'unicode')
