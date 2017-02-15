# encoding=utf8
from __future__ import absolute_import
from __future__ import division
from __future__ import print_function
from __future__ import unicode_literals

__author__ = '1661'
import six


from structure_reader.structure_reader import *


class StructureGuess(object):
    """it's NOT safe, use it at your risk

    """
    type_string_to_type_dict = dict()

    def __init__(self, name, code):
        self.name = name
        self.code = code
        self.structure = None

    @classmethod
    def remove_comments_and_spaces(cls, code):
        """
        if // in quotes , will error
        if \ at end of line(means line continue), will error
        :param code:
        :return:
        """
        new_code_list = list()
        for line in code.split('\n'):
            line = line.split('//', 1)[0]
            new_code_list.append(line)
        new_code = ''.join(new_code_list)
        new_code.replace('\t', ' ')
        new_code.replace('\n', ' ')
        new_code.replace('\r', ' ')
        while True:
            backup_code = new_code
            new_code = new_code.replace('  ', ' ')
            if new_code == backup_code:
                break
        return new_code

    @classmethod
    def guess_structure(cls, code, field_list):
        def split_one(str_, matcher_):
            piece_list_ = str_.split(matcher_, 1)
            if len(piece_list_) < 2:
                return piece_list_[0], ''
            else:
                return piece_list_

        for field_code in code.split(';'):
            field_code = field_code.strip()
            type_string, field_code = split_one(field_code, ' ')
            if not type_string and not field_code:
                continue
            type_ = cls.type_string_to_type(type_string)
            name_string, field_code = split_one(field_code, '[')
            if field_code:
                array_len_string, field_code = split_one(field_code, ']')
                try:
                    array_len_or_string = int(array_len_string)
                except ValueError:
                    array_len_or_string = array_len_string
            else:
                array_len_or_string = None

            if array_len_or_string is None:  # not array
                field_list.append(Field(type_, name_string))
            else:
                field_list.append(Field((type_, array_len_or_string), name_string))

    @classmethod
    def type_string_to_type(cls, type_string):
        if not cls.type_string_to_type_dict:
            for type_, string_list in valid_ctype_match_list:
                for string in string_list:
                    cls.type_string_to_type_dict[string] = type_
        try:
            return cls.type_string_to_type_dict[type_string]
        except KeyError:
            if type_string.startswith('ctypes.'):
                raise UntreatedError('type(%s) is ctypes but not support by structure_reader2' % type_string)

            return type_string


    def parse(self):
        new_code = self.remove_comments_and_spaces(self.code)
        self.structure = Structure(self.name)
        self.guess_structure(new_code, self.structure.field_list)

    @classmethod
    def dumps(cls, structure):
        def dump_name(obj):
            from structure_reader.py23 import str_type_list
            if isinstance(obj, str_type_list):
                    return """'%s'""" % obj
            elif obj in valid_ctype_list:
                return 'ctypes.%s' % obj.__name__
            else:
                return str(obj)

        def dump_field_type(field_type):
            if isinstance(field_type, tuple):
                base_type, number_string = field_type
                return '(%s, %s)' % (dump_name(base_type), dump_name(number_string))
            else:
                return dump_name(field_type)

        from six import StringIO
        s = StringIO()
        s.write("""%s = Structure('%s')\n""" % (structure.name, structure.name))
        s.write("""%s.namespace = %s\n""" % (structure.name, dump_name(structure.namespace)))
        s.write("""%s.field_list.extend([\n""" % (structure.name, ))
        tab = ' ' * 4

        for field in structure.field_list:
            s.write("""%sField(%s, %s),\n""" % (
                tab, dump_field_type(field.type), dump_name(field.name),
            ))

        s.write("""])\n""")

        s.seek(0)
        return s.read()
