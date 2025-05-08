
'''
版本:0.1
作者:ChuYangLOCW
时间:2025.05.08
'''

from tools import *

#TODO 添加 读取 数据文件的功能
#TODO 添加 读取 Excel文件的功能

#-----------------------------------
variable_begine_line = "<variables>"

begine_line = "<formulas>"

data_begine_line = "<data>"

py_begine_line = "<py>"

data_file = "<dataf>"

py_file = "<pyf>"

excle_file = "<excel>"

#------------------------------------

context = Context()

file  = open(input("输入文件路径:"),"r")
qs = file.readlines()
file.close()

variables	 = []
formulas = []
queue = Queue(qs)

while not queue.empty():
	line = queue.dequeue()
	if not line == None:
		if line.startswith(variable_begine_line):
			variables = collect_variables(queue)
		elif line.startswith(py_begine_line):
			exec_py(queue,context)
		elif line.startswith(begine_line):
			formulas = collect_formulas(queue)
		elif line.startswith(data_begine_line):
			handle_data(queue,variables,formulas,context)


input("按下任意按键退出...")

