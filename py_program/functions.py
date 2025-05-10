'''
版本：0.1
数学相关的函数
'''

from math import *;

def sum(data):
	if len(data) == 0:
		return 0
	sum_a = 0
	for i in data:
		sum_a += i
	return sum_a

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
	average_a = average(data)
	sum = 0
	for i in data:
		sum += (i - average_a)**2
	return sum / len(data)