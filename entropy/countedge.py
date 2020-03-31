#encoding: utf-8
import copy

import numpy as np

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
def find_next(a,N,i,rest,stack,motif,edge_adj,n):
    if rest==0:
        #print('当前搜索完成！',stack)
        for j in range(len(stack)-1):
            edge_adj[stack[j]][stack[j+1]]+=str(motif)
            edge_adj[stack[j+1]][stack[j]] += str(motif)
        return n+1
    else:
        if np.sum(a[i])>0:
            x = np.nonzero(a[i])
            temp=n
            #print('x for :',x)
            for next_Index in x[0]:
                #排除已经找过的节点
                if  next_Index not in stack:
                    #print('next_Index:',next_Index)
                    stack.append(next_Index)
                    temp=find_next(a,N,next_Index,rest-1,stack,motif,edge_adj,temp)
                    stack.pop()
            return temp
        else:
            #print('弹出穷途节点：',p)
            return n


def count_chain(A,N,len,motif,edge_adj):
    #print('开始计算motif：',motif)
    n=0
    a = copy.copy(A)
    for i in range(N):
        #print('当前搜索起点：',i)
        stack = []
        stack.append(i)
        n=find_next(a,N,i,len-1,stack,motif,edge_adj,n)
    #print('chain: {}  has {}'.format(motif,n))
    #chain都被计算了两次，头尾各一次
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
    n=0
    a = copy.copy(A)
    for i in range(N):
        for j in range(i,N):
            if a[i][j]>0:
                for k in range(j,N):
                    if a[j][k]>0 and a[k][i] >0:
                        n+=1
                        edge_adj[i][j] += str(3)
                        edge_adj[j][i] += str(3)
                        edge_adj[j][k] += str(3)
                        edge_adj[k][j] += str(3)
                        edge_adj[i][k] += str(3)
                        edge_adj[k][i] += str(3)
    return n

def count_poly_qua(A, N,edge_adj):
    n=0
    a = copy.copy(A)
    for i in range(N):
        for j in range(i,N):
            if a[i][j]>0:
                for k in range(j,N):
                    if a[j][k]>0:
                        for l in range(k,N):
                            if a[k][l]>0 and a[l][i]>0:
                                n+=1
                                edge_adj[i][j] += str(6)
                                edge_adj[j][i] += str(6)
                                edge_adj[j][k] += str(6)
                                edge_adj[k][j] += str(6)
                                edge_adj[k][l] += str(6)
                                edge_adj[k][k] += str(6)
                                edge_adj[i][l] += str(6)
                                edge_adj[l][i] += str(6)
    return n




# with open("CountMotif_web.csv", "wb") as fc:
#      csvWriter = csv.writer(fc)
#      for i in range(Ng):
#         if i%10==0:
#             print i
#         csvWriter.writerow(count_Motifs(i+1))
#         fc.close

def countEdge(A,nodN):
    edge_adj = [['0' for i in range(nodN)] for j in range(nodN)]
    # rd = np.argsort(sum(np.transpose(A)))
    # rdA = A[rd]
    # rdA[:, ] = rdA[:, rd]
    for i in range(nodN):
        A[i][i] = 0
    # print  "graph %d number of nodes:"% i,nodN
    print('start counting edges and motifs')
    Nm_1 = count_chain(A, nodN, 2, 1,edge_adj)
    print(1)
    Nm_2 = count_chain(A, nodN, 3, 2,edge_adj)
    print(2)
    Nm_3 = count_poly_edge(A, nodN,edge_adj)
    print(3)
    Nm_4 = count_chain(A, nodN, 4, 4,edge_adj)
    print(4)
    Nm_5 = count_star(A, nodN, 3, 5,edge_adj)
    print(5)
    Nm_6 = count_poly_qua(A, nodN,edge_adj)
    print(6)
    Nm_7 = count_chain(A, nodN, 5, 7,edge_adj)
    print(7)
    Nm_8 = count_star(A, nodN, 4, 8,edge_adj)
    print(8)
    count_motifs=[Nm_1,Nm_2,Nm_3,Nm_4,Nm_5,Nm_6,Nm_7,Nm_8]
    # rd2=np.argsort(rd)
    with open('./data/count_edge.txt', 'w') as file:
        for line in edge_adj:
            for item in line:
                file.write(item+',')
            file.write('\n')
    # edge_adj=np.array(edge_adj)
    # edge_adj=edge_adj[rd2]
    #np.savetxt('./data2/count_edge.csv', edge_adj_matrix, delimiter=",", fmt='%s')
    #return np.transpose(np.transpose(edge_adj)[rd2])
    return edge_adj,count_motifs









