# encoding: utf-8
from sympy import *
import numpy as np
import csv
import math

Nm = 8
Nn = 347
# number of graph
Ng = 5976


def get_Amount_of_Motif():
    array = open('./data2/CountMotif_nr1.csv').readlines()
    matrix = []
    for line in array:
        line = line.strip('\r\n').split(',')
        line = [int(x) for x in line]
        matrix.append(line)
    matrix = np.array(matrix)
    return matrix


def read_data(i, filename):
    array = open(filename).readlines()
    N = int(array[i])
    return N

def calEntropy(n, N, dN):
    l = [2, 3, 3, 4, 4, 4, 5, 5]
    e = [1, 2, 3, 3, 3, 4, 4, 4]
    iso = [1, 3, 1, 12, 4, 1, 20, 5]
    K = 1.0 / 100000
    T = 100.0
    DELTA = 256

    beta = symbols('BETA')
    pi = 3.1415926
    Integral = sqrt(beta) * sqrt(pi) * DELTA
    Entropy = []
    r = 27.0
    global Nm
    for i in range(Nm):
        m_integral = iso[i] * (Integral ** e[i]) * r ** (l[i] - e[i])
        if N - l[i] * n[i] > 0:
            logZ = n[i] * (log(m_integral) - math.log(n[i]) - l[i] * math.log(l[i]) + 1) + (N - l[i] * n[i]) * (
                    math.log(r) - math.log(N - l[i] * n[i]) + 1)
        else:
            logZ = n[i] * (-math.log(n[i]) + 1 + log(m_integral) - math.log(factorial(l[i])))
        logZ += math.log(dN)
        U = diff(logZ, beta)
        E = logZ + U * beta
        E = E.subs(beta, 1.0 / (K * T))
        Entropy.append(E)
    return Entropy


#motif_num_matrix = get_Amount_of_Motif()

dN = read_data(Nn - 1, './data2/devide_347_Nodes.csv')

# with open("./files/E_256_27_1000.csv", "wb") as fc:
#     csvWriter = csv.writer(fc)
#     for i in range(Ng):
#         n = motif_num_matrix[i]
#         csvWriter.writerow(calEntropy(n, Nn, dN))
#         print i
#     fc.close()
n=[173, 115, 115, 86, 100, 86, 69, 77]
print(calEntropy(n, Nn, dN))