Nn=20000
def devide(N):
    n = [[0] * N for i in range(0, N)]
    for i in range(N):
        for j in range((i+1)//2):
            if i==0:
                n[i][j]=1
            else:
                if j ==0:
                    n[i][j]=sum(n[i-1])
                else :
                    if i+1==2*(j+1):
                        n[i][j] = n[i - j - 1][j]
                    else:
                       n[i][j]=n[i-j-1][j]+1
        n[i][i]=1
    return n
dN_matrix=devide(Nn)
with open("./data2/devide_"+str(Nn)+"_Nodes.csv","w") as fc:
    for i in range(Nn):
        fc.write(str(sum(dN_matrix[i]))+'\n')


