# encoding=utf8
"""把征途GgDefs.h中的结构体转成structure_reader格式的三条structure
"""
from __future__ import absolute_import
from __future__ import division
from __future__ import print_function
from __future__ import unicode_literals

__author__ = '1661'

import CppHeaderParser
from structure_reader.structure_reader import *
import ctypes


class Converter(object):
    @classmethod
    def convert_type(cls, chp_structure):
        if 'ctypes_type' in chp_structure:
            ctypes_type = chp_structure['ctypes_type']

            if not ctypes_type.startswith('ctypes.'):
                raise UntreatedError('unknown ctypes_type(%s)' % ctypes_type)

            if ctypes_type == 'ctypes.c_uchar':  # ctypes have no type c_uchar, wrong from CppHeaderParser
                type_ = ctypes.c_ubyte
            elif ctypes_type == 'ctypes.c_void_p':  # this is wrong from CppHeaderParser?
                type_ = chp_structure['type']
            else:
                type_ = eval(ctypes_type)
        else:
            type_ = chp_structure['type']

        return type_


def deal_structure_specialize_addons(structure):
    from gen_code_for_structure_reader.ggdefs_h_specialize import structure_addons

    structure_full_name = add_route(structure.namespace, '.' + structure.name)
    structure_addon = structure_addons.get(structure_full_name, None)

    if structure_addon:
        if isinstance(structure_addon, list):
            structure_addon_list = structure_addon
        else:
            structure_addon_list = [structure_addon]

        for structure_addon in structure_addon_list:
            field, add_after = structure_addon
            if add_after is None:
                add_pos = 0
            else:
                def find_pos():
                    for index, this_field in enumerate(structure.field_list):
                        if this_field.name == add_after:
                            return index + 1
                    raise UntreatedError('not find add_after(%s) in structure(%s)' % (
                        add_after, structure_full_name))
                add_pos = find_pos()

            structure.field_list.insert(add_pos, field)


class CreateAndClosingFile(object):
    def __init__(self, file_, file_path_name):
        if file_ is None:
            import codecs
            self.open_file = codecs.open(file_path_name, mode='wb', encoding='utf8')
            self.close_on_exit = True
        else:
            self.open_file = file_
            self.close_on_exit = False

    def __enter__(self):
        return self.open_file

    def __exit__(self, *exc_info):
        if self.close_on_exit:
            self.open_file.close()


def main(ggdefs_h_file_path_name, out_file_path_name_or_file):
    if hasattr(out_file_path_name_or_file, 'write'):
        out_file = out_file_path_name_or_file
        out_file_path_name = None
    else:
        out_file = None
        out_file_path_name = out_file_path_name_or_file

    from gen_code_for_structure_reader.ggdefs_h_specialize import macro_dict

    def unmacro(str_):
        return macro_dict.get(str_, str_)

    try:
        cppHeader = CppHeaderParser.CppHeader(ggdefs_h_file_path_name)
    except CppHeaderParser.CppParseError as e:
        print(e)
        sys.exit(1)

    csr = ComplexStructureReader()
    all_structure_list = list()
    for class_name, class_ in cppHeader.classes.items():
        structure = Structure(class_['name'])

        # trans
        # todo: deal with the leading ::
        structure.namespace = '.'.join(class_['namespace'].lstrip(':').split('::'))

        for i in class_['properties']['public']:
            if i['name'] == 'result_item' and structure.name == 'ret_quality_compose_special':
                pass
            type_ = Converter.convert_type(i)
            if i['array']:
                array_size = int(unmacro(i['array_size']))
                field = Field((type_, array_size), i['name'])
            else:
                if type_ in (ctypes.c_char, ):
                    type_ = ctypes.c_byte
                field = Field(type_, i['name'])
            structure.field_list.append(field)

        deal_structure_specialize_addons(structure)

        csr.add_structure(structure)
        all_structure_list.append(structure)

    from gen_code_for_structure_reader import gen_structure_from_c_code

    with CreateAndClosingFile(out_file, out_file_path_name) as f:
        file_header = (
            "# encoding=utf-8\n"
            "from __future__ import absolute_import\n"
            "from __future__ import division\n"
            "from __future__ import print_function\n"
            "from __future__ import unicode_literals\n"
            "from structure_reader.structure_reader import *"
            "\n"
            "\n"
            "all_structure_list = list()\n"
            "\n"
            "\n"
        )
        f.write(file_header)
        for structure in all_structure_list:
            f.write(gen_structure_from_c_code.StructureGuess.dumps(structure))
            f.write("""all_structure_list.append(%s)\n""" % structure.name)
    #
    # for i in csr.ctx.namespace.sub_namespace.values():
    #     if i.route == 'ret_nationwar_jifen_detail':
    #         for ii in i.sub_namespace.values():
    #             print(ii.route)
