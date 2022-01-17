array = [0,1,2,3,4,5,6,7]
array1 = array[0:4]
array2 = array[4:8]

matrix  = [array1, array2]
print(matrix)
col = matrix[0][:]
print("col: ")
print(col)

row = matrix[:][0]
print("row: ")
print(row)