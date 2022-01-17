
def nothing(unit, *some):
    result = 0
    for i in some:
        result = result + i
        
    if unit == 'm':
        return str(result) + unit
    elif unit == 'km':
        return str(result / 1000) + unit
    elif unit == 'mm':
        return str(result * 1000) + unit
    else:
        return 'error'
    
print(nothing('m', 1,2,3,4,5))
print(nothing('mm', 2,3,4,5))


def returnTwo(a, b):
    return a+b, a*b

result1, result2 = returnTwo(3,5)
print(result1)
print(result2)
print(returnTwo(3,2))
