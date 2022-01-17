import pandas as pd
import openpyxl as op

me = pd.read_excel('work.xlsx')
lat = me[:][0]
print(lat)
# me = op.load_workbook('work.xlsx')
# print(me)
# print(pd)

# myStr = "jiwadfnjiwoo"

# if "jiwoo" in myStr:
#     print(True)
# else:
#     print(False)

# if 'fqqq' in  myStr:
#     print("true" + "kk")
# else:
#     print("false"*2)