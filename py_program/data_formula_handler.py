'''
版本:0.1
作者:ChuYangLOCW
时间:2025.05.08
描述:启动文件
'''

from tools import DFH

dfh = DFH(input("输入文件路径:"))
while dfh.is_active():
	dfh.handle()
input("按下任意按键退出...")


#------------------------------------
# 自定义示例
#------------------------------------
#
# from tools import *
#
# file  = open(input("输入文件路径:"),"r")
# qs = file.readlines()
# file.close()
# context = Context()
# queue = Queue(qs)
# while not queue.empty():
# 	line = queue.dequeue()
# 	if not line == None:
# 		if line.startswith(variable_begine_line):
# 			collect_variables(queue,context)
# 		elif line.startswith(py_begine_line):
# 			exec_py(queue,context)
# 		elif line.startswith(begine_line):
# 			collect_formulas(queue,context)
# 		elif line.startswith(data_begine_line):
# 			handle_data(queue,context)
# input("按下任意按键退出...")
#-------------------------------------