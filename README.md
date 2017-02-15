从C/C++代码中解析结构体,并生成用于structure_reader的structure定义文件

用法:
	例如gen_ggdefs.py, 输入源C/C++文件和目的文件, 即可输出

注意:
	由于C/C++结构体定义中没有定义复合结构, 比如
	struct A
	{
		int a;
		// 后跟a个B结构体
	};
	struct B
	{
		int b;
	};

	像这种A结构体是包含了A::a个B结构体, 在C/C++代码中是无法体现出来的,因此默认的解析也无法完成. 需要在gen_code_for_structure_reader/ggdefs_h_specialize.py中的structure_addons手动对这些结构体加上特殊处理

	另外C/C++文件的宏定义, 也要再gen_code_for_structure_reader/ggdefs_h_specialize.py中的macro_dict里定义好


Resolve the structure from the C / C ++ code and generate the structure definition file for the structure_reader

usage:
         In the main function of gen_ggdefs.py, input source C / C ++ files and destination files, run the script then you can get output file.

note:
         Since the C / C ++ structure definition does not define a composite structure, for example
         Struct A
         {
                 Int a;
                 // followed by some B structures. the number of structures is in variable "a".
         };
         Struct B
         {
                 Int b;
         };

         Like this A structure contains A::a B structures. In C / C + + code this can not be reflected. So the default resolution can not be completed. You need add some code in gen_code_for_structure_reader/ggdefs_h_specialize.py manually to deal with these addons.

         In addition, the macro definition of the C / C ++ file is also need to be defined in macro_dict in file gen_code_for_structure_reader/ggdefs_h_specialize.py

