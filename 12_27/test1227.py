from openpyxl import load_workbook

myExcel = load_workbook('work.xlsx')

m1 = myExcel.worksheets[0]
m2 = myExcel.worksheets[1]

gp1 = m1['L']
gp2 = m2['L']
    
print(len(gp1))
print(len(gp2))
