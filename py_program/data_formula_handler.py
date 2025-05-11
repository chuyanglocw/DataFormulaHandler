'''
版本:0.1
作者:ChuYangLOCW
时间:2025.05.08
描述:启动文件
'''


#TIP: 如果你需要自定义可以重写DFH类的handle方法, 并在handle方法中调用你自定义的方法

from dfh_core import DFH
import sys;

dfh = None

if len(sys.argv) > 2:
	dfh = DFH(sys.argv[1])
	sys.stdout = open(sys.argv[2],"w")
else:
	dfh = DFH(input("输入文件路径:"))
while dfh.is_active():
	dfh.handle()
if len(sys.argv) > 2:
	sys.stdout.close()
else:
	input("按下任意按键退出...")
sys.stdout = sys.__stdout__
print("完成Data处理!")