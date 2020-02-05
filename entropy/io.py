import numpy as np
import pandas as pd
import xlrd


def read_adjMatrix_csv(graphfile_csv):
    array = open(graphfile_csv).readlines()
    N = len(array)
    matrix = []
    for line in array:
        line = line.strip('\r\n').split(',')
        line = [int(float(x)) for x in line]
        matrix.append(line)
    matrix = np.array(matrix)
    return matrix,N


def translata_xlsx_to_csv(graphfile_xlsx):
    data_xls = pd.read_excel(io=graphfile_xlsx,sheet_name=0,header=None,index_col=None)
    data_xls.to_csv('./data2/graphfile.csv', sep=',', index=0,header=0,encoding='utf-8')
    return './data2/graphfile.csv'