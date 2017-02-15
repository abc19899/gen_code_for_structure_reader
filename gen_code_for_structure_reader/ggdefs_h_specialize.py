# encoding=utf-8
""" ggdefs.h有一些逻辑不能通过代码分析来获得, 这里手动处理
"""
from __future__ import absolute_import
from __future__ import division
from __future__ import print_function
from __future__ import unicode_literals

macro_dict = {
    'MAX_PLAYER_NAME_LEN': 16,
    'MAX_INSET_JEWEL_NUM': 4,
    'MAX_SUBATTR_NUM': 15,
    'MAX_EQUIP_NUM': 15,
    'MAX_MERIDIAN_TYPE': 7,
    'MAX_EXTRA_ATTR_NUM': 4,
    'MAX_SERVER_NAME_LEN': 16,
    'MAX_XIANLING_ZIZHI_NUM': 5,
    'QIN_COUNTRY_ID': 0,
    'CHU_COUNTRY_ID': 2,
    'LOGIN_AWARD_NUM': 7,
    'num_size': 999999999,

    'MAX_PLAYER_RANK_NUM': 25,
}

from structure_reader.structure_reader import *
from ctypes import *

structure_addons = {
    # key: structure_name, value: tuple(add_field, add_after_with_column),
    # add_field is Field type, add_after_with_column is string type. if add_after_with_column is None,
    # it means add at beginning
    # TIPS: if exist multiple value, value should be a type like [value0, value1]

    'ret_get_black_list': (Field(('BlackRoleData', 'mSize'), 'black_role_data'), 'mSize'),
    'ReqUpdateTask': (Field((c_byte, 'size'), 'script'), 'size'),
    'ReqEquipSkill': (Field(('_Equip_Skill_', 'change_num'), 'equipskill'), 'change_num'),
    'TeamRev': (Field(('TeamItem', 'num'), 'team_item'), 'num'),
    'RetRaid': [
        (Field((c_byte, 'contentSize'), 'battle_content'), 'contentSize'),
        (Field(('Package_item', 'loot_item_num'), 'loot_item'), 'battle_content'),
        (Field(('Package_item', 'complete_raid_item_num'), 'complete_raid_item'), 'loot_item'),
    ],

    'RetJjcChallengeList': (Field((c_int, 'luck_rank_num'), 'luck_rank'), 'luck_rank_num'),
    'RetJjcChallengeRank': (Field((c_byte, 'battleSize'), 'battle_content'), 'rongyu'),
    'RetJjcFightReplay': (Field((c_byte, 'contentSize'), 'battle_content'), 'contentSize'),

    # todo: complete it. (hard work...)

    # todo: can use A::B in Field?
    'PushChangeMap': (Field(('RetScenePlayerlist::OtherPlayer', 'num'), 'other_player'), 'num'),
    'RetScenePlayerlist.OtherPlayer': [
        (Field(('RetScenePlayerlist::BonusBuff', 'bonus_buff_num'), 'bonus_buff'), 'string_bonus_buf_num'),
        (Field(('RetScenePlayerlist::StringBonusBuff', 'string_bonus_buf_num'), 'string_bonus_buf'), 'bonus_buff'),
    ],
    'RetScenePlayerlist.StringBonusBuff': (Field((c_char, 'value_len'), 'value'), 'value_len'),

    'RetScenePlayerlist': (Field(('OtherPlayer', 'player_num'), 'other_player'), 'player_num'),
}
