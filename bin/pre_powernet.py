import pymysql

def sqlexcu(sql,array):
    conn = pymysql.connect(
        host='106.75.24.29',
        user="S20190905_FC", passwd="S20190905_FC",
        db="S20190905_FC",
        port=3060,
        charset='utf8')
    cur = conn.cursor()
    try:
        cur.execute(sql)
        results = cur.fetchall()
        for row in results:
            array.append(row)
    except Exception as e:
        raise e
    finally:
        conn.close()

sql1 = "select * from neteco_instancenode_relation"
sql2 = "select * from neteco_energy"

nodes=[[-1] * 6 for i in range(253)]
relations=[]
attributes=[]

sqlexcu(sql1,relations)
sqlexcu(sql2,attributes)

for rel in relations:
    nodes[rel[1]-1][2]=rel[2]-1

graphLable=[0 for i in range(500)]
for i in range(500):
    count=0
    for j in range(253):
        if attributes[i*253+j][7]==1:
            count+=1
    graphLable[i]=count

print(graphLable)

def writefile():
    f = open("dataset/POWERNET/POWERNET.txt", "w")
    print('创建文件成功')

    f.write("500\n")
    for i in range(500):
        f.write("253 "+str(graphLable[i])+"\n")
        for j in range(253):
            nodesCopy = nodes[j].copy()
            nodesCopy[0] = attributes[i * 253 + j][7]
            nodesCopy[1] = 1
            nodesCopy[3] = attributes[i * 253 + j][3]
            nodesCopy[4] = attributes[i * 253 + j][4]
            nodesCopy[5] = attributes[i * 253 + j][5]
            if nodesCopy[2] == -1:
                nodesCopy[1] = 0
                nodesCopy[2] = ''
            f.write(" ".join(str(s) for s in nodesCopy) + "\n")
    f.close()

writefile()