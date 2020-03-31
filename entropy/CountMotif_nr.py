#encoding: utf-8
import copy
import csv

import numpy as np

# number of motif

Nm = 8

def countMotifs(A,nodN):
    rd=np.argsort(sum(np.transpose(A)))
    rdA=A[rd]
    rdA[:,]=rdA[:,rd]
    A2=np.array(np.matrix(A)**2)
    A3=np.array(np.matrix(A)**3)
    A4=np.array(np.matrix(A)**4)
    num_triangle=count_triangle(A3,nodN)
    num_quads=count_quads(A2,A4,nodN)
    Nm_1=count_chain(rdA,nodN,2)
    Nm_2=count_chain(rdA,nodN,3)
    Nm_3=count_polygon0(num_triangle,3)
    Nm_4=count_chain(rdA,nodN,4)
    Nm_5=count_star(rdA,nodN,3)
    Nm_6=count_polygon0(num_quads,4)
    Nm_7=count_chain(rdA,nodN,5)
    Nm_8=count_star(rdA,nodN,4)
    num=[Nm_1,Nm_2,Nm_3,Nm_4,Nm_5,Nm_6,Nm_7,Nm_8]
    #print ('count_motifs: '+str(num))
    return num

def count_star(A,N,neiN):
    n=0
    a=copy.copy(A)
    for i in range(N):
        if (np.sum(a[i])>neiN-1):
            n+=1
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
def find_next(a,N,i,rest):
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
            return find_next(a,N,next_Index,rest-1)
        else:
            return -1
def count_chain(A,N,len):
    n=0
    a = copy.copy(A)
    for i in range(N):
        if find_next(a,N,i,len-1)>=0:
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
    n=num//edges
    return n

def writeMotifNumber(graphfile):
    with open("CountMotif.csv", "w") as fc:
        csvWriter = csv.writer(fc)
        csvWriter.writerow(countMotifs(graphfile))
        fc.close
        return




