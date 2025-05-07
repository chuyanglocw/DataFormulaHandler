from math import *;

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