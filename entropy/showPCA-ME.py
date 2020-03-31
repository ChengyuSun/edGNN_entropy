#encoding:utf-8
import numpy as np
import matplotlib as mpl
import matplotlib.pyplot as plt
from mpl_toolkits.mplot3d import Axes3D
from scipy.spatial.distance import pdist, squareform
label_font = {
    'color': [0,0,0],
    'size': 10,
    'weight':'bold'
}


def randrange(n, vmin, vmax):

    r = np.random.rand(n)  # 随机生成n个介于0~1之间的数
    array=(vmax - vmin) * r + vmin  # 得到n个[vmin,vmax]之间的随机数
    array=[[i]for i in array]
    #print "x:",array
    return array

def loadDataSet(filename):
    Entropy=[]
    f = open(filename, 'r')  # num=count_Motifs(i)
    for line in f.readlines():
        line = line.strip('\r\n').split(',')
        line = [float(x) for x in line]
        Entropy.append(line)
    Entropy=np.array(Entropy)
    return Entropy
kE=loadDataSet('.\\result\kPCA_VNE_u.csv')


fig = plt.figure(figsize=(11.5,7))
ax = fig.add_subplot(111, projection="3d")  # 添加子坐标轴，111表示1行1列的第一个子图

y=[]
for i in range(len(kE)):
    if i>=86 and i<=92:
        y.append(1)
    elif i>=4021 and i <=4028:
        y.append(3)
    elif i>=5204 and i <=5212:
        y.append(4)
    elif i>=5378 and i <=5388:
        y.append(5)
    else:
        y.append(0)
y=np.array(y)

ax.scatter(kE[y==1, 0], kE[y==1, 1], kE[y==1, 2], c='k', marker='^', label='Black Monday',s=40)

ax.scatter(kE[y==3, 0], kE[y==3, 1], kE[y==3, 2], c='b', marker='^', label='Irac War',s=40)
ax.scatter(kE[y==4, 0], kE[y==4, 1], kE[y==4, 2], c='r', marker='^', label='Subprime Mortgage Crisis',s=40)
ax.scatter(kE[y==5, 0], kE[y==5, 1], kE[y==5, 2], c='m', marker='^', label='Bankrauptcy of Lehman Brothers',s=40)

ax.scatter(kE[y==0, 0], kE[y==0, 1], kE[y==0, 2], c='c', marker='o', label='background', s=5,alpha=.1)

#ax.scatter(kE2[:, 0], kE2[:, 1], kE2[:, 2], c='r', marker='*', label='OV', s=40)

#ax.scatter(kE3[:, 0], kE3[:, 1], kE3[:, 2], c='k', marker='*', label='UCEC', s=40)

#ax.set_xlabel("PC1", fontdict=label_font)
#ax.set_ylabel("PC2", fontdict=label_font)
#ax.set_zlabel("PC3", fontdict=label_font)

#plt.zticks(fontsize=8)
ax.set_title("PCA for log(Von Neumann Entropy)", alpha=0.6, color=[0,0.1,0.1], size=12, weight='bold', backgroundcolor="w")   #子图的title
ax.legend(loc="upper left",borderaxespad=-0.2)    #legend的位置左上

ax.set_xlabel(xlabel="1st principle component")
ax.set_ylabel(ylabel="2nd principle component")
ax.set_zlabel(zlabel="3rd principle component")


plt.show()