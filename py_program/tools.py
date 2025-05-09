'''
版本：0.1
作者：初阳LOCW
时间：2025.5.9
描述：这是DFH的主体内核
	 之所以将 Context Queue 还有处理方法分离出 DFH类 是为了可以自定义处理
'''

#TODO 将个函数改回原本 传入 Queue Context 对象 方便自定义 并且在末尾添加 自定义开始、结束标识 默认为设定的常量

import functions

#TODO 添加 读取 数据文件的功能
#TODO 添加 读取 Excel文件的功能

#--------------------------
# 默认开始和结束的设定
# Begine
variable_begine_line = "<variables>"
begine_line = "<formulas>"
data_begine_line = "<data>"
py_begine_line = "<py>"
data_file = "<dataf>"
py_file = "<pyf>"
excle_file = "<excel>"

# End
variable_end_line = "</variables>"
end_line ="</formulas>"
data_end_line = "</data>"
py_end_line = "</py>"
data_file_end = "</dataf>"
py_file_end = "</pyf>"
excle_file_end = "</excel>"
#--------------------------

funcuse = "f-"

temp_variable = "="

datalabel = ";"

#--------------------------

class Context:
	def __init__(self):
		self.variables = []
		self.formulas = []
		self.prec = 12
		self.py_self_define = {}

	def setprec(self, prec):
		self.prec = prec

	def setpyselfdefine(self,p):
		self.py_self_define = p

class Queue:
	def __init__(self, array: list):
		self.data = array

	def enqueue(self,value):
		self.data.append(value)

	def dequeue(self):
		if not self.empty():
			return self.data.pop(0)
		else :
			return None

	def empty(self) -> bool:
		return len(self.data) == 0

	def __iter__(self):
		return self

	def __next__(self):
		return self.dequeue()

class DFH:
	def __init__(self, file_path: str, queue: Queue = None):
		'''
		版本：0.1
		作用：集合处理，方便主类做别的操作
		'''
		self.queue = queue
		if queue == None:
			file  = open(file_path,"r")
			qs = file.readlines()
			file.close()
			self.queue = Queue(qs)
		self.context = Context()

	def is_active(self) -> bool:
		return not self.queue.empty()

	def handle(self):
		'''
		版本：0.1
		作用：处理一条命令
		'''
		line = self.queue.dequeue()
		if not line == None:
			if line.startswith(variable_begine_line):
				collect_variables(self)
			elif line.startswith(py_begine_line):
				exec_py(self)
			elif line.startswith(begine_line):
				self.formulas = collect_formulas(self)
			elif line.startswith(data_begine_line):
				handle_data(self)

	def use_excel(self):
		'''
		版本：0.1
		作用：要求openpyxl用于使用Excel，这样是为了如果不用Excel而无法使用本程序
		'''
		extension = {}
		exec("import openpyxl as excel",None,extension)
		self.context.setpyselfdefine(self.context.py_self_define | extension)

def print_begine_collect_variables():
	print("------------------- 开始 输入变量 -------------------")
def print_end_collect_variables():
	print("------------------- 结束 输入变量 -------------------")
def collect_variables(dfh: DFH):
	'''
	版本：0.1
	作用：获得变量表
	'''
	print_begine_collect_variables()
	variables = []
	for v_line in dfh.queue:
		v_line = v_line.replace("\n","")
		if v_line == None or v_line.startswith(variable_end_line):
			break
		v_list = v_line.split(" ")
		for v in v_list:
			variables.append(v)
	dfh.context.variables = variables


def print_begine_exec_py():
	print("------------------- 开始 执行脚本 -------------------")
def print_end_exec_py():
	print("------------------- 结束 执行脚本 -------------------")
def exec_py(dfh: DFH):
	'''
	版本：0.1
	作用：获得脚本来执行
	'''
	print_begine_exec_py()
	cmd = ""
	for cmd_line in dfh.queue:
		if cmd_line == None or cmd_line.startswith(py_end_line):
			break
		cmd = f"{cmd}{cmd_line}"
	print_end_exec_py()
	py_self_define = {}
	exec(cmd, None, py_self_define)
	dfh.context.setpyselfdefine(py_self_define)

def print_begine_collect_formulas():
	print("------------------- 开始 输入公式 -------------------")
def print_end_collect_formulas():
	print("------------------- 结束 输入公式 -------------------")
def collect_formulas(dfh: DFH):
	'''
	版本：0.1
	作用：获得公式表
	'''
	print_begine_collect_formulas()
	formulas = []
	for f_line in dfh.queue:
		if f_line == None or f_line.startswith(end_line):
			break
		f_line = f_line.replace("\n","")
		formulas.append(f_line)
	print_end_collect_formulas()
	dfh.context.formulas = formulas

output_format = "{formula}={_ans_}"
float_output_format = "{formula}={_ans_:.%df}"
def print_data_title():
	print("-----------------------------------------------------")
def print_hanle_data():
	print("--------------------- 处理数据 ----------------------")
def handle_data(dfh: DFH) -> bool:
	'''
	版本：0.1
	作用：处理数据
	'''
	context = dfh.context
	variables = context.variables
	formulas = context.formulas


	if len(variables) == 0 or len(formulas) == 0:
		return False
	for data in dfh.queue:
		if data == None or data.startswith(data_end_line):
			break

		if data.startswith(datalabel):
			print_data_title()
			print(f"处理 {data.replace(";","").replace("\n","")} :")
			continue
		print_hanle_data()
		print(data)
		data = data.replace("\n","").split(" ")
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


if __name__ == '__main__':
	queue = Queue(["a b", "</variables>","a+b","a*b","</formulas>",";Rect1","2 4",";Rect2","6 7.0","</data>"])
	dfh = DFH(None,queue)
	v_l = collect_variables(dfh)
	f_l = collect_formulas(dfh)
	handle_data(dfh)