
'''
版本:0.1
作者:ChuYangLOCW
时间:2025.05.06
'''

from tools import *

#TODO 添加 执行 脚本的功能
#TODO 添加 读取 数据文件的功能
#TODO 添加 读取 Excle文件的功能

#-----------------------------------
variable_begine_line = "<variables>"

begine_line = "<formulas>"

data_begine_line = "<data>"

py_begine_line = "<py>"

data_file = "<dataf>"

#------------------------------------

def printh():
	print("Hello")

context = Context()

file  = open(input("输入文件路径:"),"r")
qs = file.readlines()
file.close()

variables	 = []
formulas = []
qeue = Qeue(qs)

while not qeue.empty():
	line = qeue.deqeue()
	if not line == None:
		if line.startswith(variable_begine_line):
			variables = collect_variables(qeue)
		# elif line.startswith(py_begine_line):
		# 	exec_py(qeue)
		elif line.startswith(begine_line):
			formulas = collect_formulas(qeue)
		elif line.startswith(data_begine_line):
			handle_data(qeue,variables,formulas,context)


input("按下任意按键退出...")

