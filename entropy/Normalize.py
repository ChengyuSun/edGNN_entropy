import numpy as np
import csv
import math
Ng=5976

def transfer(arr,N):
    print(N)

    Nm = 8
    narr=[]
    for i in range(Nm):
        narr.append(math.log(arr[i],10))

   # narr = []
   # narr.append(math.log(arr[0],10))
    return narr
def readData(filename):
    array=open(filename).readlines()
    matrix=[]
    for line in array:
        line=line.strip('\r\n').split(',')
        line=[float(x) for x in line]
        matrix.append(line)
    matrix=np.array(matrix)
    return matrix
#with open("dN_Eco_3.csv","wb") as fc:
with open("log10E_256_27_1000.csv", "wb") as fc:
    csvWriter=csv.writer(fc)
    e=readData('./E_256_27_1000.csv')
    NodeNum =347
    for i in range(Ng):
        e[i]=transfer(e[i],NodeNum)
        csvWriter.writerow(e[i])
    fc.close
