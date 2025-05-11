

'''
版本：0.1
作者：初阳LOCW
时间：2025.5.11
更新时间：2025.5.11
描述：这是DFH的主体内核
'''

# 更新日志：
# * 主体部分 由tools.py 移动到 dfh_core.py
# * 添加 读取 Excel文件的功能

from tools import *
import functions
import os
import re

class DFH:
	def __init__(self, file_path: str, queue: Queue = None):
		'''
		版本：0.1
		作用：集合处理，方便主类做别的操作
		'''
		self.used_excel = False
		self.file_path = file_path
		self.path_folder = os.path.dirname(file_path)
		self.queue = queue
		if queue == None:
			file  = open(file_path,"r")
			qs = file.readlines()
			file.close()
			self.queue = Queue(qs)
		self.context = Context()
		self.handled_data = False

	def is_active(self) -> bool:
		return not self.queue.empty()

	def handle(self):
		'''
		版本：0.1
		作用：处理一条命令
		'''
		collect_variables(self)
		exec_py(self)
		exec_py_file(self)
		collect_formulas(self)
		handle_data(self)
		handle_data_file(self)
		handle_excel_file(self)
		if not self.handled_data:
			print(self.queue.dequeue())
		else:
			self.handled_data = False

	def use_excel(self):
		'''
		版本：0.1
		作用：要求openpyxl用于使用Excel，这样是为了如果不用Excel而无法使用本程序
		'''
		if self.used_excel :
			return
		extension = {}
		exec("import openpyxl as excel",None,extension)
		self.context.setpyselfdefine(self.context.py_self_define | extension)
		self.used_excel = True

def print_begin_collect_variables():
	print("------------------- 开始 输入变量 -------------------")
def print_end_collect_variables():
	print("------------------- 结束 输入变量 -------------------")
def collect_variables(dfh: DFH, begin_line: str = variable_begin_line, end_line: str = variable_end_line):
	'''
	版本：0.1
	作用：获得变量表
	'''
	if dfh.queue.empty() or not dfh.queue.peek().startswith(begin_line):
		return
	dfh.handled_data = True
	dfh.queue.dequeue()
	print_begin_collect_variables()
	variables = []
	for v_line in dfh.queue:
		v_line = v_line.replace("\n","")
		if v_line == None or v_line.startswith(end_line):
			break
		v_list = v_line.split(" ")
		for v in v_list:
			variables.append(v)
	dfh.context.variables = variables
	print(f"变量顺序:{variables}")
	print_end_collect_variables()

def print_begin_exec_py():
	print("------------------- 开始 执行脚本 -------------------")
def print_end_exec_py():
	print("------------------- 结束 执行脚本 -------------------")
def exec_py(dfh: DFH, begin_line: str = py_begin_line, end_line: str = py_end_line):
	'''
	版本：0.1
	作用：获得脚本来执行
	'''
	if dfh.queue.empty() or not dfh.queue.peek().startswith(begin_line):
		return
	dfh.handled_data = True
	dfh.queue.dequeue()
	print_begin_exec_py()
	cmd = ""
	for cmd_line in dfh.queue:
		if cmd_line == None or cmd_line.startswith(end_line):
			break
		cmd = f"{cmd}{cmd_line}"
	print_end_exec_py()
	py_self_define = {}
	exec(cmd, None, py_self_define)
	dfh.context.setpyselfdefine(py_self_define)

def print_begin_handle_py_file():
	print("----------------- 开始 处理脚本文件 -----------------")
def print_end_handle_py_file():
	print("----------------- 结束 处理脚本文件 -----------------")
def exec_py_file(dfh : DFH, begin_line : str = py_file, end_line : str = py_file_end):
	'''
	版本：0.1
	描述：执行脚本文件
	'''
	if dfh.queue.empty() or not dfh.queue.peek().startswith(begin_line):
		return
	dfh.handled_data = True
	dfh.queue.dequeue()
	print_begin_handle_py_file()
	for py_line in dfh.queue:
		if py_line == None or py_line.startswith(end_line):
			break
		py_line = py_line.replace("\n","")
		py_file_path = os.path.join(dfh.path_folder,py_line)
		py_file = open(py_file_path,"r")
		py_cmd = py_file.read()
		py_file.close()
		exec(py_cmd, None, dfh.context.py_self_define)
	print_end_handle_py_file()



def print_begin_collect_formulas():
	print("------------------- 开始 输入公式 -------------------")
def print_end_collect_formulas():
	print("------------------- 结束 输入公式 -------------------")
def collect_formulas(dfh: DFH, begin_line: str = begin_line, end_line: str = end_line):
	'''
	版本：0.1
	作用：获得公式表
	'''
	if dfh.queue.empty() or not dfh.queue.peek().startswith(begin_line):
		return
	dfh.handled_data = True
	dfh.queue.dequeue()
	print_begin_collect_formulas()
	formulas = []
	for f_line in dfh.queue:
		if f_line == None or f_line.startswith(end_line):
			break
		f_line = f_line.replace("\n","")
		formulas.append(f_line)
	print_end_collect_formulas()
	dfh.context.formulas = formulas


def print_data_title():
	print("-----------------------------------------------------")
def print_handle_data():
	print("--------------------- 处理数据 ----------------------")
def handle_data(dfh: DFH, begin_line: str = data_begin_line, end_line : str = data_end_line) -> bool:
	'''
	版本：0.1
	作用：处理数据
	'''
	if dfh.queue.empty() or not dfh.queue.peek().startswith(begin_line):
		return False
	dfh.handled_data = True
	dfh.queue.dequeue()

	context = dfh.context
	variables = context.variables
	formulas = context.formulas


	if len(variables) == 0 or len(formulas) == 0:
		return False
	for data in dfh.queue:
		if data == None or data.startswith(end_line):
			break

		if data.startswith(datalabel):
			print_data_title()
			print(f"处理 {data.replace(";","").replace("\n","")} :")
			continue
		print_handle_data()
		data = data.replace("\n","")
		data = re.findall(pattern, data)
		data_dict = {"func":functions, "context":context, "pi":functions.pi, "e":functions.e} | context.py_self_define
		for i in range(0,len(variables)):
			data_dict[variables[i]] = eval(data[i], globals(),locals=data_dict)
		for formula in formulas:
			if formula.startswith(funcuse):

				exec(formula.replace(funcuse,""), globals(),locals=data_dict)
				continue
			_ans_ = "Err"
			if temp_variable in formula:
				l_and_r = formula.split("=")
				l = l_and_r[0].replace(" ","")
				r = l_and_r[1]
				r = eval(r.replace("^","**"),globals(), locals=data_dict)
				data_dict[l] = r
				_ans_ = r
			else :
				_ans_ = eval(formula.replace("^","**"),globals(), locals=data_dict)
			out_f = output_format
			if type(_ans_) == float:
				out_f = float_output_format % data_dict["context"].prec
			exec(f"print(f\"{out_f}\")",locals={"formula":formula,"_ans_":_ans_})
	return True


def print_begin_handle_data_file():
	print("----------------- 开始 处理数据文件 -----------------")
def print_end_handle_data_file():
	print("----------------- 结束 处理数据文件 -----------------")
def handle_data_file(dfh: DFH, begin_line: str = data_file, end_line : str = data_file_end):
	'''
	版本：0.1
	作用：处理数据文件
	'''
	if dfh.queue.empty() or not dfh.queue.peek().startswith(begin_line):
		return False
	dfh.handled_data = True
	dfh.queue.dequeue()
	print_begin_handle_data_file()
	for data_file in dfh.queue:
		if data_file == None or data_file.startswith(end_line):
			break
		file = open(f"{dfh.path_folder}/{data_file.replace("\n","")}","r")
		qs = file.readlines()
		file.close()
		qs.insert(0,data_begin_line)
		qs.append(data_end_line)
		queue = Queue(qs)
		dfh.queue.put_queue_front(queue)

		print_data_title()
		print(f"处理 {data_file.replace("\n","")} :")
		handle_data(dfh)

	print_end_handle_data_file()

def print_begin_excel_file():
	print("----------------- 开始 处理excel文件 ----------------")
def print_end_excel_file():
	print("----------------- 结束 处理excel文件 ----------------")
'''
思路：
1. 读取Excel文件
2. 读取1行的变量名称
3. 从2行开始读取数据
4. 处理数据
5. 输出数据
'''
def handle_excel_file(dfh: DFH, begin_line: str = excel_file, end_line : str = excel_file_end):
	'''
	版本：0.1
	描述：处理Excel文件
	'''
	if dfh.queue.empty() or not dfh.queue.peek().startswith(begin_line):
		return
	dfh.handled_data = True
	dfh.queue.dequeue()
	dfh.use_excel()
	xl = dfh.context.py_self_define["excel"]
	print_begin_excel_file()
	for excel_file_a in dfh.queue:
		if excel_file_a == None or excel_file_a.startswith(end_line):
			break
		excel_file_path = os.path.join(dfh.path_folder,excel_file_a.replace("\n",""))
		print("开始处理Excel文件:"+excel_file_path)
		excel_file = xl.load_workbook(excel_file_path)
		dfh.context.define["excel_file_instance"] = excel_file
		input_excel_file_data_and_handle(dfh,excel_file_a.replace("\n",""))
		dfh.context.define["excel_file_instance"] = None
		excel_file.close()
	print_end_excel_file()

def input_excel_file_data_and_handle(dfh: DFH, name: str):
	'''
	版本：0.1
	描述：输入Excel文件的数据
	'''

	data_length = 0
	variables = []
	while True:
		value = read_value_from_excel(dfh.context.define,1,data_length+1)
		if value == None or value == "":
			break
		variables.append(value)
		data_length += 1
	dfh.context.variables = variables
	if data_length == 0:
		return
	else :
		dfh.queue.enqueue(data_begin_line)
		dfh.queue.enqueue(";"+name)

	data_deep = 0
	while True:
		value = read_value_from_excel(dfh.context.define,data_deep+2,1)
		if value == None or value == "":
			break
		data_line = ""
		for i in range(0,data_length):
			value = read_value_from_excel(dfh.context.define,data_deep+2,i+1)
			if value == None or value == "":
				break
			data_line = f"{data_line}{value} "
		dfh.queue.enqueue(data_line)
		data_deep += 1
	dfh.queue.enqueue(data_end_line)
	handle_data(dfh)


if __name__ == '__main__':
	queue = Queue(["a b", "</variables>","a+b","a*b","</formulas>",";Rect1","2 4",";Rect2","6 7.0","</data>"])
	dfh = DFH(None,queue)
	v_l = collect_variables(dfh)
	f_l = collect_formulas(dfh)
	handle_data(dfh)