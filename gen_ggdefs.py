# encoding=utf-8
from __future__ import absolute_import
from __future__ import division
from __future__ import print_function
from __future__ import unicode_literals

__author__ = '1661'
import sys

PY3 = sys.version_info[0] == 3

_zsq_scripts_path = '/data/zsq_scripts/'
if _zsq_scripts_path not in sys.path:
    sys.path.insert(0, _zsq_scripts_path)

from gen_code_for_structure_reader import ggdefs_parser

ggdefs_parser.main(
    ggdefs_h_file_path_name=r"D:\netgame\MZT_server\netgame\gamegate\operate\ggdefs.h",
    out_file_path_name_or_file='ggdefs.py'
)
