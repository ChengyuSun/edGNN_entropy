#encoding: utf-8
import numpy as np
import csv
import copy
# number of motif

Nm = 8
Node_num = 23


# for i in range(Node_num):
#     for j in range(Node_num):
#         print type(i)
#         edge_adj[i][j] += str(Nm)


def read_adjMatrix():
    array = open('./data2/graphfile.csv').readlines()
    N = len(array)
    matrix = []
    for line in array:
        line = line.strip('\r\n').split(',')
        line = [int(float(x)) for x in line]
        matrix.append(line)
    matrix = np.array(matrix)
    return matrix,N


def count_star(A,N,neiN,motif,edge_adj):
    n=0
    a=copy.copy(A)
    for i in range(N):

        if (np.sum(a[i])>neiN-1):
            n+=1

            edge_num = neiN
            while edge_num > 0:
                for k in range(len(a[i])):
                    if a[i][k] >0:
                        edge_adj[i][k] += str(motif)
                        edge_adj[k][i] += str(motif)
                        edge_num -= 1

            for j in range(i):
                a[N-j-1][i]=0
            x=np.nonzero(a[i])
            nei_Index=x[0][:neiN]
            a[i].fill(0)
            for j in nei_Index:
                a[j].fill(0)
                for k in range(N):
                    a[k][j]=0
    return n
def find_next(a,N,i,rest,motif,edge_adj):
    if rest==0:
        a[i].fill(0)
        for j in range(N):
            a[j][i] = 0
        return i
    else:
        if np.sum(a[i])>0:
            for j in range(N):
                a[j][i]=0
            #print i
            x = np.nonzero(a[i])
            a[i].fill(0)
            next_Index = x[0][0]
            "存在边，边属于哪个模体"
            m = int(next_Index)
            edge_adj[i][m] += str(motif)
            edge_adj[m][i] += str(motif)
            return find_next(a,N,next_Index,rest-1,motif,edge_adj)
        else:
            return -1
def count_chain(A,N,len,motif,edge_adj):
    n=0
    a = copy.copy(A)
    for i in range(N):
        if find_next(a,N,i,len-1,motif,edge_adj)>=0:
            n+=1
    return n
"""
def circle_find_next(a,N,i,rest):
    if rest==0:
        return i
    else:
        if np.sum(a[i])>0:
            for j in range(N):
                a[j][i]=0
            x = np.nonzero(a[i])
            a[i].fill(0)
            next_Index=x[0]
            for k in next_Index:
                return circle_find_next(a,N,k,rest-1)
        else:
            return -1
def count_polygon(A,N,edges):
    n=0
    a=copy.copy(A)
    for i in range(N):
        if circle_find_next(a,N,i,edges)==i:
            n+=1
    return n
"""

def count_quads(A2,A4,N):
    re=0
    n=0
    for i in range(N):
        for j in range(N):
            if j==i:
                re+=A2[i][j]**2
            else: re+=A2[i][j]
        if(A4[i][i]-re)>=2:n+=1
        re=0
    return n
def count_triangle(A3,N):
    n=0
    for i in range(N):
        if A3[i][i]>=2: n+=1
    return n

def count_polygon0(num,edges):
    n=num/edges
    return n

def count_poly_edge(A, N,edge_adj):
    a = copy.copy(A)
    for i in range(N):
        for j in range(i,N):
            if a[i][j]>0:
                for k in range(j,N):
                    if a[j][k]>0 and a[k][i] >0:
                        edge_adj[i][j] += str(3)
                        edge_adj[j][i] += str(3)
                        edge_adj[j][k] += str(3)
                        edge_adj[k][j] += str(3)
                        edge_adj[i][k] += str(3)
                        edge_adj[k][i] += str(3)
    return 0

def count_poly_qua(A, N,edge_adj):
    a = copy.copy(A)
    for i in range(N):
        for j in range(i,N):
            if a[i][j]>0:
                for k in range(j,N):
                    if a[j][k]>0:
                        for l in range(k,N):
                            if a[k][l]>0 and a[l][i]>0:
                                edge_adj[i][j] += str(6)
                                edge_adj[j][i] += str(6)
                                edge_adj[j][k] += str(6)
                                edge_adj[k][j] += str(6)
                                edge_adj[k][l] += str(6)
                                edge_adj[k][k] += str(6)
                                edge_adj[i][l] += str(6)
                                edge_adj[l][i] += str(6)
    return 0




# with open("CountMotif_web.csv", "wb") as fc:
#      csvWriter = csv.writer(fc)
#      for i in range(Ng):
#         if i%10==0:
#             print i
#         csvWriter.writerow(count_Motifs(i+1))
#         fc.close

def countEdge(A,nodN):
    edge_adj = [['0' for i in range(nodN)] for j in range(nodN)]
    rd = np.argsort(sum(np.transpose(A)))
    rdA = A[rd]
    rdA[:, ] = rdA[:, rd]
    for i in range(nodN):
        rdA[i][i] = 0
    # print  "graph %d number of nodes:"% i,nodN

    Nm_1 = count_chain(rdA, nodN, 2, 1,edge_adj)
    #print(1)
    Nm_2 = count_chain(rdA, nodN, 3, 2,edge_adj)
    #print(2)
    Nm_3 = count_poly_edge(rdA, nodN,edge_adj)
    #print(3)
    Nm_4 = count_chain(rdA, nodN, 4, 4,edge_adj)
    #print(4)
    Nm_5 = count_star(rdA, nodN, 3, 5,edge_adj)
    #print(5)
    Nm_6 = count_poly_qua(rdA, nodN,edge_adj)
    #print(6)
    Nm_7 = count_chain(rdA, nodN, 5, 7,edge_adj)
    #print(7)
    Nm_8 = count_star(rdA, nodN, 4, 8,edge_adj)
    #print(8)

    rd2=np.argsort(rd)
    edge_adj=np.array(edge_adj)
    edge_adj=edge_adj[rd2]
    #np.savetxt('./data2/count_edge.csv', edge_adj_matrix, delimiter=",", fmt='%s')
    return np.transpose(np.transpose(edge_adj)[rd2])









