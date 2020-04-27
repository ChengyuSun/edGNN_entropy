#-*- coding: utf-8
from decimal import Decimal
def bTod(n, pre=4):
    '''
    把一个带小数的二进制数n转换成十进制
    小数点后面保留pre位小数
    '''
    string_number1 = str(n) #number1 表示二进制数，number2表示十进制数
    decimal = 0  #小数部分化成二进制后的值
    flag = False
    for i in string_number1: #判断是否含小数部分
        if i == '.':
            flag = True
            break
    if flag: #若二进制数含有小数部分
        string_integer, string_decimal = string_number1.split('.') #分离整数部分和小数部分
        for i in range(len(string_decimal)):
            decimal += 2**(-i-1)*int(string_decimal[i])  #小数部分化成二进制
        number2 = int(str(int(string_integer, 2))) + decimal
        return round(number2, pre)
    else: #若二进制数只有整数部分
        return int(string_number1, 2)#若只有整数部分 直接一行代码二进制转十进制 python还是骚

def dTob(n):
    '''
    把一个带小数的十进制数n转换成二进制
    小数点后面保留pre位小数
    '''
    if n==0:
        return '0'
    string_number1 = str(n) #number1 表示十进制数，number2表示二进制数
    flag = False
    for i in string_number1: #判断是否含小数部分
        if i == '.':
            flag = True
            break
    if flag:
        string_integer, string_decimal = string_number1.split('.') #分离整数部分和小数部分
        integer = int(string_integer)
        decimal = Decimal(str(n)) - integer
        l1 = [0,1]
        l2 = []
        decimal_convert = ""
        while True:
           if integer == 0: break
           x,y = divmod(integer, 2)  #x为商，y为余数
           l2.append(y)
           integer = x
        string_integer = ''.join([str(j) for j in l2[::-1]])  #整数部分转换成二进制
        i=0
        while decimal != 0  and i<50:
            result = int(decimal * 2)
            decimal = decimal * 2 - result
            decimal_convert = decimal_convert + str(result)
            i+=1
        string_number2 = string_integer + '.' + decimal_convert
        return string_number2
    else: #若十进制只有整数部分
        l1 = [0,1]
        l2 = []
        while True:
           if n == 0: break
           x,y = divmod(n, 2)  #x为商，y为余数
           l2.append(y)
           n = x
        string_number = ''.join([str(j) for j in l2[::-1]])
        return string_number

def extend_to_50(s):
    zeros=''
    for i in range(50-len(s)):
        zeros+='0'
    return s+zeros
print(extend_to_50(dTob(0.12345)))