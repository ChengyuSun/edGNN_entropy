#encoding: utf-8
import copy

import numpy as np


def count_star(A,N,neiN,motif,edge_adj):
    n=0
    a=copy.copy(A)
    for i in range(N):
        if (np.sum(a[i])>neiN-1):
            #print('{} star center is {}'.format(motif,i))
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

def count_star_5and8(A,nodN,edge_adj):
    n_motif5=0
    n_motif8=0
    for i in range(nodN):
        x0 = np.nonzero(A[i])
        x=x0[0]
        degree=len(x)
        if degree<3:
            continue
        for a_3 in range(degree-2):
            for b_3 in range(a_3+1,degree-1):
                for c_3 in range(b_3+1,degree):
                    n_motif5+=1
                    #print('star 5 center {} to {} {} {}'.format(i,x[a_3],x[b_3],x[c_3]))
                    edge_adj[i][x[a_3]] += '5'
                    edge_adj[x[a_3]][i] += '5'
                    edge_adj[i][x[b_3]] += '5'
                    edge_adj[x[b_3]][i] += '5'
                    edge_adj[i][x[c_3]] += '5'
                    edge_adj[x[c_3]][i] += '5'
        if degree>=4:
            for a_4 in range(degree-3):
                for b_4 in range(a_4+1,degree-2):
                    for c_4 in range(b_4+1,degree-1):
                        for d_4 in range(c_4+1,degree):
                            n_motif8+=1
                            #print('star 8 center {} to {} {} {} {}'.format(i, x[a_4], x[b_4], x[c_4],x[d_4]))
                            edge_adj[i][x[a_4]] += '8'
                            edge_adj[x[a_4]][i] += '8'
                            edge_adj[i][x[b_4]] += '8'
                            edge_adj[x[b_4]][i] += '8'
                            edge_adj[i][x[c_4]] += '8'
                            edge_adj[x[c_4]][i] += '8'
                            edge_adj[i][x[d_4]] += '8'
                            edge_adj[x[d_4]][i] += '8'
    return n_motif5,n_motif8



def find_next_2(a,N,i,rest,stack,motif,edge_adj,n):
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
                    temp=find_next_2(a,N,next_Index,rest-1,stack,motif,edge_adj,temp)
                    stack.pop()
            return temp
        else:
            #print('弹出穷途节点：',p)
            return n


def count_chain_2(A,N,len,motif,edge_adj):
    #print('开始计算motif：',motif)
    n=0
    a = copy.copy(A)
    for i in range(N):
        #print('当前搜索起点：',i)
        stack = []
        stack.append(i)
        n=find_next_2(a,N,i,len-1,stack,motif,edge_adj,n)
    return n

def find_next(a,N,i,rest,stack):
    if rest==0:
        a[i].fill(0)
        for j in range(N):
            a[j][i] = 0
        return i
    else:
        if np.sum(a[i])>0:
            for j in range(N):
                a[j][i]=0
            x = np.nonzero(a[i])
            a[i].fill(0)
            next_Index=x[0][0]
            stack.append(next_Index)
            return find_next(a,N,next_Index,rest-1,stack)
        else:
            stack.pop()
            return -1

def count_chain(A,N,rest,motif,edge_adj):
    n=0
    a = copy.copy(A)
    for i in range(N):
        stack=[]
        stack.append(i)
        if find_next(a,N,i,rest-1,stack)>=0:
            #print('当前搜索完成！', stack)
            for j in range(len(stack) - 1):
                edge_adj[stack[j]][stack[j + 1]] += str(motif)
                edge_adj[stack[j + 1]][stack[j]] += str(motif)
            n+=1
    return n

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
                                edge_adj[l][k] += str(6)
                                edge_adj[i][l] += str(6)
                                edge_adj[l][i] += str(6)
    return n


def countEdge(A,nodN):
    edge_adj = [['0' for i in range(nodN)] for j in range(nodN)]
    for i in range(nodN):
        A[i][i] = 0
    print('start counting edges and motifs')
    Nm_1 = count_chain(A, nodN, 2, 1,edge_adj)
    Nm_2 = count_chain(A, nodN, 3, 2,edge_adj)
    Nm_3 = count_poly_edge(A, nodN,edge_adj)
    Nm_4 = count_chain(A, nodN, 4, 4,edge_adj)
    Nm_5= count_star(A, nodN,3,5,edge_adj)
    Nm_6 = count_poly_qua(A, nodN,edge_adj)
    Nm_7 = count_chain(A, nodN, 5, 7,edge_adj)
    Nm_8 = count_star(A,nodN,4,8,edge_adj)
    count_motifs=[Nm_1,Nm_2,Nm_3,Nm_4,Nm_5,Nm_6,Nm_7,Nm_8]
    # with open('../entropy/data/count_edge_club.txt', 'w') as file:
    #     for line in edge_adj:
    #         for item in line:
    #             file.write(item+',')
    #         file.write('\n')
    return edge_adj,count_motifs









