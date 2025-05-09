/**
 * 版本：0.1
 * 作者：初阳LOCW
 * 描述：这是一个用于生成终端使用的exe文件，但是其具有缺陷，只能打开软件文件夹下的文件夹作为工作空间。
 * 局限：仅仅 Windows 可用。
 */

#include <iostream>
#include <string>
#include <sstream>

// 用于 拼接 启动路径
const char launch_path[] = "cd \"..\\..\\";
const char launch[] = "\" && start python ..\\py_program\\data_formula_handler.py";

int main(int argc, char** argv){
	// 切换 UTF-8 避免乱码
	system("chcp 65001");
	if (argc == 1){
		std::stringstream ss;
		ss << launch_path << "data" << launch;
		system(ss.str().c_str());
	}else if (argc == 2){
		std::stringstream ss;
		ss << launch_path << argv[1] << launch;
		system(ss.str().c_str());
	}else {
		std::cout << "使用方法：\n(1)直接打开 \n(2)输入一个参数（为软件文件夹下的文件夹名称）" << std::endl;
	}
	return 0;
}