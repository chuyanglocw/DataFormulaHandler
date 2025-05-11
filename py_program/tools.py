'''
版本：0.1
作者：初阳LOCW
时间：2025.5.9
更新时间：2025.5.11
描述：Context Queue类 及其 标识符定义
'''

# 更新日志：
# * 将主体代码移动到 dfh_core.py

#--------------------------
# 默认开始和结束的设定
# Begin
variable_begin_line = "<variables>"
begin_line = "<formulas>"
data_begin_line = "<data>"
py_begin_line = "<py>"
data_file = "<dataf>"
py_file = "<pyf>"
excel_file = "<excel>"

# End
variable_end_line = "</variables>"
end_line ="</formulas>"
data_end_line = "</data>"
py_end_line = "</py>"
data_file_end = "</dataf>"
py_file_end = "</pyf>"
excel_file_end = "</excel>"
#--------------------------

funcuse = "f-"

temp_variable = "="

datalabel = ";"

#--------------------------

pattern = r'\".*?\"|\(.*?\)|\[[^\[\]]*\]|[a-zA-Z0-9]+'

#--------------------------

output_format = "{formula}={_ans_}"
float_output_format = "{formula}={_ans_:.%df}"

#--------------------------

class Context:
	def __init__(self):
		self.variables = []
		self.formulas = []
		self.prec = 12
		self.py_self_define = {}
		self.define = {}

	def setprec(self, prec):
		self.prec = prec

	def setpyselfdefine(self,p):
		self.py_self_define = p

class Queue:
	def __init__(self, array: list):
		self.data = array

	def enqueue(self,value):
		self.data.append(value)

	def peek(self):
		if not self.empty():
			return self.data[0]

	def append_queue(self,queue):
		self.data = self.data + queue.data

	def append_list(self, o_list):
		self.data = self.data + o_list

	def put_queue_front(self,queue):
		self.data = queue.data + self.data

	def put_list_front(self, o_list):
		self.data = o_list + self.data

	def __len__(self):
		return len(self.data)

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

	def __str__(self):
		return "head|" + str(self.data) + "|tail"

def excel_col_transfrom(col: int) -> str:
	'''
	版本：0.1
	作用：将Excel的列号转换为列名
	参数：col: int 列号
	返回：str 列名
	'''
	col_r = ""
	while col > 0:
		col_r = chr(65 + (col - 1) % 26) + col_r
		col = (col - 1) // 26
	return col_r

def read_value_from_excel(dfh_namespace : dict, row: int, col: int):
	'''
	版本：0.1
	作用：从Excel文件中读取值
	参数：excel_file: str Excel文件路径, row: int 行号, col: int 列号
	返回：str 值
	'''
	sheet = dfh_namespace["excel_file_instance"].active
	return sheet[excel_col_transfrom(col) + str(row)].value

# 测试代码
if __name__ == "__main__":
	context = Context()
	context.variables = ["a","b","c"]
	context.formulas = ["a+b","a+c","b+c"]
	print(context.variables)
	print(context.formulas)
	context.setprec(10)
	print(context.prec)
	context.setpyselfdefine({"a":1,"b":2,"c":3})
	print(context.py_self_define)
	queue = Queue([1,2,3,4,5])
	print(queue.empty())
	print(queue.peek())
	for i in queue:
		print(i)
	print(queue.empty())