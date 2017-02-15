# encoding=utf8
from __future__ import absolute_import
from __future__ import division
from __future__ import print_function
from __future__ import unicode_literals

__author__ = '1661'

from gen_code_for_structure_reader.gen_structure_from_c_code import *

def test():
    c_code = (
        "\n"
        "\t\tBYTE zizhi;\t\t\t//资质\n"
        "\t\tBYTE chengzhang;\t\t//成长\n"
        "\t\tBYTE lingxing;\t\t//灵性\n"
        "\t\tBYTE lingyun_star;\t//灵韵星级\n"
        "\t\tint modelid;\t\t//仙灵id\n"
        "\t\tchar name[16];\t\t//仙灵名字\n"
        "\t\tBYTE skill_num;\t\t//技能数\n"
        "\t\tBYTE version;\t\t//几代玄兽1:1代 2：2代 3：3代\n"
        "\t\tBYTE egg_type;\t\t//0:玄兽 1：蛋\n"
        "\t\tBYTE modelSize;\t\t//模型大小\n"
        "\t\tint type_id;\n"
    )

    sg = StructureGuess('XianLingInfo', c_code)
    sg.parse()
    py_code = sg.dumps(sg.structure)
    # print(py_code)
    assert py_code == """XianLingInfo = Structure('XianLingInfo')
XianLingInfo.namespace = ''
XianLingInfo.field_list.extend([
    Field(ctypes.c_ubyte, 'zizhi'),
    Field(ctypes.c_ubyte, 'chengzhang'),
    Field(ctypes.c_ubyte, 'lingxing'),
    Field(ctypes.c_ubyte, 'lingyun_star'),
    Field(ctypes.c_long, 'modelid'),
    Field((ctypes.c_char, 16), 'name'),
    Field(ctypes.c_ubyte, 'skill_num'),
    Field(ctypes.c_ubyte, 'version'),
    Field(ctypes.c_ubyte, 'egg_type'),
    Field(ctypes.c_ubyte, 'modelSize'),
    Field(ctypes.c_long, 'type_id'),
])
"""
