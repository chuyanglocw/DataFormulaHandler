import functions
variable_end_line = "</variables>"

# py_end_line = "</py>"

end_line ="</formulas>"

data_end_line = "</data>"

py_end_line = "</py>"

data_file_end = "</dataf>"

py_file_end = "</pyf>"

excle_file_end = "</excel>"

funcuse = "f-"

temp_variable = "="

datalabel = ";"

class Context:
	def __init__(self):
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

def print_begine_collect_variables():
	print("------------------- 开始 输入变量 -------------------")
def print_end_collect_variables():
	print("------------------- 结束 输入变量 -------------------")
def collect_variables(queue: Queue) -> list:
	'''
	版本：0.1
	作用：获得变量表
	'''
	print_begine_collect_variables()
	variables = []
	for v_line in queue:
		v_line = v_line.replace("\n","")
		if v_line == None or v_line.startswith(variable_end_line):
			break
		v_list = v_line.split(" ")
		for v in v_list:
			variables.append(v)
	print_end_collect_variables()
	return variables


def print_begine_exec_py():
	print("------------------- 开始 执行脚本 -------------------")
def print_end_exec_py():
	print("------------------- 结束 执行脚本 -------------------")
def exec_py(queue: Queue, context: Context):
	'''
	版本：0.1
	作用：获得脚本来执行
	'''
	print_begine_exec_py()
	cmd = ""
	for cmd_line in queue:
		if cmd_line == None or cmd_line.startswith(py_end_line):
			break
		cmd = f"{cmd}{cmd_line}"
	print_end_exec_py()
	py_self_define = {}
	exec(cmd, None, py_self_define)
	context.setpyselfdefine(py_self_define)

def print_begine_collect_formulas():
	print("------------------- 开始 输入公式 -------------------")
def print_end_collect_formulas():
	print("------------------- 结束 输入公式 -------------------")
def collect_formulas(queue: Queue) -> list:
	'''
	版本：0.1
	作用：获得公式表
	'''
	print_begine_collect_formulas()
	formulas = []
	for f_line in queue:
		if f_line == None or f_line.startswith(end_line):
			break
		f_line = f_line.replace("\n","")
		formulas.append(f_line)
	print_end_collect_formulas()
	return formulas

output_format = "{formula}={_ans_}"
float_output_format = "{formula}={_ans_:.%df}"
def print_data_title():
	print("-----------------------------------------------------")
def print_hanle_data():
	print("--------------------- 处理数据 ----------------------")
def handle_data(queue: Queue, variables: list, formulas: list, context: Context) -> bool:
	'''
	版本：0.1
	作用：处理数据
	'''
	if len(variables) == 0 or len(formulas) == 0:
		return False
	for data in queue:
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
	context = Context()
	v_l = collect_variables(queue)
	f_l = collect_formulas(queue)
	handle_data(queue,v_l,f_l,context)