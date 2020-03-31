## Intro
edgnn需要的数据集：邻接矩阵、节点属性/边属性、图标签/点标签 （带/表示二者至少要存在一个）

数据格式：参见bin/preprocessed_data/.../unzipped

程序入口：
1. preprocess（对数据预处理）
   
    标准流程从下载数据的压缩包开始（我改成了从解压开始），系统判别数据集类型（也就是分析任务是图分类or点分类），判别之后进入core/data/dortmund(或dglrgcn)把文本数据整合成真正的graph。以dortmund（图分类 ）为例，我在系统读取数据属性的同时，加了熵进去，作为边的一维属性，此后系统将完整的graph和一些参数save成pickle，方便使用时进行读取。

2. run_model:

    流程从分析数据集类型开始（同上文），确定任务后，进入上述两种模型之一读取pickle，同时读取我们写好的配置文件（包括数据属性、激活函数、网络类型、网络层数等，参见core/models/config_file）。然后主程序把load到的pickle传给core/app.py，app负责具体的前向传播、反向传播（自动）和测试。其中前向传播过程确定了我们的模型model，model的任务比较复杂，它通过查看配置文件，构造出一定数量、一定类型的layer（我只使用过core/models/layers/edgnn）。紧接着，model把app传给它的batch数据（分批训练）稍做处理，发给各层layer。至于edgnn这个layer，就是整合了邻居+自己+领边的属性。model的这几层layer跑完之后就输出了最后的结果。


边熵的计算分为两大过程
（参见[entropy/interface.py](entropy/interface.py)的line42）：
1. 熵的计算：CountMotif.py把graph的motif数出来（motif可以理解成某种拓扑结构，这里我们数了8种），用entropy中的那个复杂公式计算出熵（graph的8维向量）
2. 边的计算：countege.py从起点出发，遍历整张图，数出图中的边在哪种motif中出现过
3. edge_entropy.py计算边熵时，需要把2中出现过多少次都加起来，最终得到每条边分摊多少的熵，作为边的1维属性（因为8维在这里都加起来了）

## How to run

part1:
```powershell
preprocess
    dortmund(alternative)
    --dataset
        MUTAG(alternative)
    --out_folder
        ./preprocessed_data/MUTAG(alternative)
```

part2:
```powershell
run_model
    --dataset
        ptc_fr(alternative)
    --config_fpath
        ../core/models/config_files/config_edGNN_graph_class_mutag.json(alternative)
    --data_path
        ./preprocessed_data/MUTAG/(alternative)
    --n-epochs
        40
    --gpu(alternative)
        0
```

if you want more details,please read [README_original.md](README_original.md).