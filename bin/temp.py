acc_file = open('', "r").readlines()
accs=[]
for i in acc_file:
    accs.append(float(i))
n=len(accs)
max_acc=max(accs)
min_acc=min(accs)


