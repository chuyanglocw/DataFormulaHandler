
'''
版本:0.1
作者:ChuYangLOCW
时间:2025.05.06
'''

from math import *

#TODO 将列表修改成队列 删除已处理语句
#TODO 添加 py 脚本功能
#TODO 添加 读取 数据文件的功能
#TODO 添加 读取 Excle文件的功能

#-----------------------------------
variable_begine_line = "<variables>"
variable_end_line = "</variables>"

begine_line = "<formulas>"
end_line ="</formulas>"

data_begine_line = "<data>"
data_end_line = "</data>"

funcuse = "f-"

#TODO 编写相应处理方法
mapfunc = "-m"
filfunc = "-f"

#TODO 编写数据片段声明
datatitle = ";"

_prec = 12
def setprec(prec):
	global _prec
	_prec = prec

def sum(data):
	if len(data) == 0:
		return 0
	suma = 0
	for i in data:
		suma += i
	return suma

def average(data):
	if len(data) == 0:
		return 0
	sum = 0
	for i in data:
		sum += i
	return sum / len(data)

def variance(data):
	if len(data) == 0:
		return 0
	averagea = average(data)
	sum = 0
	for i in data:
		sum += (i - averagea)**2
	return sum / len(data)

def map_collect(p: list, relation) -> list:
	return list(map(p,relation))

def filter_collect(p: list, relation) -> list:
	return list(map(p,relation))


file  = open(input("输入文件路径:"),"r")
lista = file.readlines()
file.close()

variables	 = []
calculations = []
v_b = False
c_b = False
d_b = False

for i in lista:
	i = i.replace("\n","")


	if i.startswith(variable_begine_line):
		print("------------------- 开始 输入变量 -------------------")
		v_b = True
		variables = []
		continue
	elif i.startswith(variable_end_line):
		print("------------------- 结束 输入变量 -------------------")
		v_b = False
		continue
	if v_b:
		vs = i.split(" ")
		for j in vs:
			variables.append(j)
		continue


	if i.startswith(begine_line):
		print("------------------- 开始 输入公式 -------------------")
		c_b = True
		calculations = []
		continue
	elif i.startswith(end_line):
		print("------------------- 结束 输入公式 -------------------")
		c_b = False
		continue
	if c_b:
		calculations.append(i)
		continue


	if i.startswith(data_begine_line):
		d_b = True
		continue
	elif i.startswith(data_end_line):
		d_b = False
		continue
	if d_b:
		print("--------------------- 处理数据 ---------------------")
		vs = i.split(" ")
		for index in range(0,len(variables)):
			ex = f"{variables[index]}={vs[index]}"
			exec(ex)
		print(f"{i}:")
		for calc in calculations:
			if (calc.startswith(funcuse)):
				exec(calc.replace(funcuse,""))
				continue
			_ans = eval(calc.replace("^","**"))
			output_format = "{calc}={_ans}"
			if type(_ans) == float:
				output_format = "{calc}={_ans:.%df}" % _prec
			exec(f"print(f\"{output_format}\")",locals={"calc":calc,"_ans":_ans})


input("按下任意按键退出...")

