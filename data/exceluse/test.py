from openpyxl import Workbook,load_workbook

wokbook = load_workbook(filename="data/exceluse/data.xlsx")
sheet = wokbook.active

print(sheet["C1"].value)