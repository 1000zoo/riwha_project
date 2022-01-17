from haversine import haversine
from openpyxl import Workbook

midPoints = []
pointStack =[]

pointStack.append(3)
pointStack.append(2)

print(pointStack)

while not not pointStack:
    k = pointStack.pop()
    print(k)
    
    
print(len(pointStack))