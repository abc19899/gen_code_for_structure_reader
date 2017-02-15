# encoding=utf8
from __future__ import absolute_import
from __future__ import division
from __future__ import print_function
from __future__ import unicode_literals

__author__ = '1661'

from structure_reader.structure_reader import *


global ggdefs


def setup_module(self):
    from gen_code_for_structure_reader.ggdefs_parser import main
    from six import StringIO
    # try:
    #     from cStringIO import StringIO
    # except ImportError:
    #     from StringIO import StringIO

    file_ = StringIO()
    main(
        ggdefs_h_file_path_name=r"D:\netgame\MZT_server\netgame\gamegate\operate\ggdefs.h",
        out_file_path_name_or_file=file_
    )
    file_.seek(0)
    code = file_.read()
    file_.close()

    # load ggdefs module from code
    import imp
    global ggdefs
    ggdefs = imp.new_module('ggdefs')
    # exec code in ggdefs.__dict__
    from six import exec_
    from gen_code_for_structure_reader.py23 import to_builtin_str
    exec_(to_builtin_str(code), ggdefs.__dict__)
    file_.close()


def build_csr():
    root_namespace = Namespace()
    root_namespace.root_namespace = root_namespace
    ctx = Ctx(namespace=root_namespace)
    csr = ComplexStructureReader(ctx=ctx)

    for structure in ggdefs.all_structure_list:
        csr.add_structure(structure)
    return csr


def get_structure_def(csr, structure_name):
    return csr.ctx.namespace.sub_namespace[structure_name].class_


def parse_and_check_len(csr, sample_structure, bytes_data):
    ret_structure, len_ = csr.parse(sample_structure=sample_structure, bytes_data=bytes_data)
    assert len_ == len(bytes_data)
    return ret_structure


def check_extra_buf(parser):
    if len(parser.data) > parser.pos:
        print('剩余%d/%d未解析' % (len(parser.data) - parser.pos, len(parser.data)))
        return True

    return False


def assert_ctype(ctype_instance, ctype, value):
    assert isinstance(ctype_instance, ctype)
    assert ctype_instance.value == value


import binascii


def test_short():
    csr = build_csr()
    award_one = get_structure_def(csr, 'award_one')
    ret = parse_and_check_len(csr, award_one, binascii.a2b_hex('01000000020003'))
    assert_ctype(ret.get_field_value('itemid'), ctypes.c_int, 1)
    assert_ctype(ret.get_field_value('number'), ctypes.c_short, 2)
    assert_ctype(ret.get_field_value('quality'), ctypes.c_ubyte, 3)


def test_array():
    csr = build_csr()
    sample_structure = get_structure_def(csr, 'news_info')
    ret = parse_and_check_len(csr, sample_structure, binascii.a2b_hex('0102'))
    length = ret.get_field_value('length')
    assert len(length) == 2
    assert_ctype(length[0], ctypes.c_ubyte, 1)
    assert_ctype(length[1], ctypes.c_ubyte, 2)


# todo: not implemented
# def test_mutable_array():


def test_sub_structure():
    csr = build_csr()
    sample_structure = get_structure_def(csr, 'RetJjcChallengeRecord')

    one_record = '0100000000000000' + '02000000' + '32333300000000000000000000000000' + '01' + '02'
    tow_record = '0200000000000000' + '02000000' + '32333300000000000000000000000000' + '01' + '02'
    thr_record = '0300000000000000' + '02000000' + '32333300000000000000000000000000' + '01' + '02'
    fou_record = '0400000000000000' + '02000000' + '32333300000000000000000000000000' + '01' + '02'
    ret = parse_and_check_len(csr, sample_structure, binascii.a2b_hex(
        '01000000' + one_record + tow_record + thr_record + fou_record
    ))
    assert_ctype(ret.get_field_value('num_'), ctypes.c_uint, 1)
    one, tow, three, four = ret.get_field_value('record_')
    assert_ctype(one.get_field_value('time'), ctypes.c_longlong, 1)
    assert_ctype(tow.get_field_value('time'), ctypes.c_longlong, 2)
    assert_ctype(three.get_field_value('time'), ctypes.c_longlong, 3)
    assert_ctype(four.get_field_value('time'), ctypes.c_longlong, 4)

    def assert_record(record):
        assert_ctype(record.get_field_value('userid'), ctypes.c_int, 2)
        adversaryName = record.get_field_value('adversaryName')
        assert len(adversaryName) == 16
        for i, v in zip(adversaryName, ['2', '3', '3', '\x00', '\x00', '\x00', '\x00', '\x00', '\x00', '\x00', '\x00', '\x00', '\x00', '\x00', '\x00', '\x00', ]):
            assert_ctype(i, ctypes.c_char, v)
        assert_ctype(record.get_field_value('isWin'), ctypes.c_byte, 1)
        assert_ctype(record.get_field_value('isAttack'), ctypes.c_byte, 2)

    assert_record(one)
    assert_record(tow)
    assert_record(three)
    assert_record(four)


def test_complex_structure_reader():
    # [gg][65604] 2017/01/19 16:26:07
    # json_string = """{"gg_block_x":4,"gg_block_y":3,"gg_map_index":7,"players":[{"VIPLevel":0,"bonus_buff":[{"type":101,"value":9598}],"chenghao":255,"chengzhang":0,"country":0,"egg_type":0,"equip_info":{"equip_1":0,"equip_2":0,"equip_3":0,"num_1":0,"num_2":0,"num_3":0},"guild_index":0,"hp":1779,"hp_max":1779,"last_act_time":1484814367,"lingxing":0,"lingyun_star":0,"major":0,"major_plus":0,"model":500,"modelSize":10,"modelid":-1,"mp":0,"mp_max":0,"sex":1,"skill_num":0,"string_bonus_buff":null,"target_building_id":0,"teamnum":0,"type_id":-1,"user_id":2147482064,"username":"步兵","usertype":1,"version":4,"weapon":-1,"x":1831,"xianling_name":"","y":1031,"zizhi":0}]}"""
    origin_data = "01 00 00 00 D0 F9 FF 7F 27 07 00 00 07 04 00 00 1F 78 80 58 01 00 00 00 00 E6 AD A5 E5 85 B5 00 00 00 00 00 90 D0 8F 44 20 01 F3 06 00 00 F3 06 00 00 00 00 00 00 00 00 00 00 00 FF FF FF FF 00 00 00 FF F4 01 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 FF FF FF FF 00 00 20 D0 8F 44 20 7F 00 00 3B 45 6F 00 00 00 00 04 00 0A FF FF FF FF 01 00 65 7E 25 00 00"
    hex_data = ''.join(x for x in origin_data.split(' '))
    bytes_data = binascii.a2b_hex(hex_data)
    csr = ComplexStructureReader()

    # PushChangeMap = Structure('PushChangeMap')
    # PushChangeMap.field_list.extend([
    #     Field(ctypes.c_int, 'num'),
    #     Field(('OtherPlayer', 'num'), 'other_player'),
    # ])
    # csr.add_structure(PushChangeMap)
    #
    # OtherPlayer = Structure('OtherPlayer')
    # OtherPlayer.field_list.extend([
    #     Field(ctypes.c_int, 'user_id'),
    #     Field(ctypes.c_int, 'x'),
    #     Field(ctypes.c_int, 'y'),
    #     Field(ctypes.c_int, 'last_act_time'),
    #     Field(ctypes.c_byte, 'usertype'),
    #     Field(ctypes.c_int, 'target_building_id'),
    #     Field((ctypes.c_char, 16), 'username'),
    #     Field(ctypes.c_char, 'sex'),
    #     Field(ctypes.c_int, 'hp'),
    #     Field(ctypes.c_int, 'hp_max'),
    #     Field(ctypes.c_int, 'mp'),
    #     Field(ctypes.c_int, 'mp_max'),
    #     Field(ctypes.c_char, 'country'),
    #     Field(ctypes.c_int, 'weapon'),
    #     Field(ctypes.c_byte, 'major'),
    #     Field(ctypes.c_byte, 'major_plus'),
    #     Field(ctypes.c_byte, 'VIPLevel'),
    #     Field(ctypes.c_byte, 'chenghao'),
    #     Field(ctypes.c_int, 'model'),
    #     Field(ctypes.c_byte, 'teamnum'),
    #     Field(ctypes.c_int, 'guild_index'),
    #     Field('EquipInfos', 'equip_infos'),
    #     Field((ctypes.c_char, 40), 'guild_name'),
    #     Field('XianLingInfo', 'm_xianling'),
    #     Field(ctypes.c_byte, 'bonus_buff_num'),
    #     Field(ctypes.c_byte, 'string_bonus_buf_num'),
    #     Field(('BonusBuff', 'bonus_buff_num'), 'bonus_buff'),
    #     Field(('StringBonusBuff', 'string_bonus_buf_num'), 'string_bonus_buf'),
    # ])
    # csr.add_structure(OtherPlayer)
    #
    # BonusBuff = Structure('BonusBuff')
    # BonusBuff.field_list.extend([
    #     Field(ctypes.c_byte, 'type'),
    #     Field(ctypes.c_int, 'value'),
    # ])
    # csr.add_structure(BonusBuff)
    #
    # StringBonusBuff = Structure('StringBonusBuff')
    # StringBonusBuff.field_list.extend([
    #     Field(ctypes.c_byte, 'type'),
    #     Field(ctypes.c_byte, 'value_len'),
    #     Field((ctypes.c_char, 'value_len'), 'value'),
    # ])
    # csr.add_structure(StringBonusBuff)
    #
    # EquipInfos = Structure('EquipInfos')
    # EquipInfos.field_list.extend([
    #     Field(ctypes.c_byte, 'equip_1'),
    #     Field(ctypes.c_byte, 'num_1'),
    #     Field(ctypes.c_byte, 'equip_2'),
    #     Field(ctypes.c_byte, 'num_2'),
    #     Field(ctypes.c_byte, 'equip_3'),
    #     Field(ctypes.c_byte, 'num_3'),
    # ])
    # csr.add_structure(EquipInfos)
    #
    # XianLingInfo = Structure('XianLingInfo')
    # XianLingInfo.field_list.extend([
    #     Field(ctypes.c_byte, 'zizhi'),
    #     Field(ctypes.c_byte, 'chengzhang'),
    #     Field(ctypes.c_byte, 'lingxing'),
    #     Field(ctypes.c_byte, 'lingyun_star'),
    #     Field(ctypes.c_int, 'modelid'),
    #     Field((ctypes.c_char, 16), 'name'),
    #     Field(ctypes.c_byte, 'skill_num'),
    #     Field(ctypes.c_byte, 'version'),
    #     Field(ctypes.c_byte, 'egg_type'),
    #     Field(ctypes.c_byte, 'modelSize'),
    #     Field(ctypes.c_int, 'type_id'),
    # ])
    # csr.add_structure(XianLingInfo)

    PushChangeMap = get_structure_def(csr, 'PushChangeMap')

    push_change_map, read_len = csr.parse(PushChangeMap, bytes_data=bytes_data)
    assert read_len == len(bytes_data)
    assert push_change_map.get_value('num') == 1
    other_player = push_change_map.get_field_value('other_player')
    assert len(other_player) == 1
    player = other_player[0]
    assert_ctype(player.get_field_value('VIPLevel'), ctypes.c_ubyte, 0)
    assert len(player.get_field_value('string_bonus_buf')) == 0
    bonus_buf = player.get_field_value('bonus_buff')
    assert len(bonus_buf) == player.get_value('bonus_buff_num') == 1
    # {"type":101,"value":9598}
    assert_ctype(bonus_buf[0].get_field_value('type'), ctypes.c_ubyte, 101)
    assert_ctype(bonus_buf[0].get_field_value('value'), ctypes.c_int, 9598)
