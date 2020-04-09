acc_file = open('./only_entropy_1.txt', "r").readlines()
accs=[]
for i in acc_file:
    accs.append(float(i))
n=len(accs)
print(n)
avg=sum(accs)/n
print('avg',avg)
print('max(accs)',max(accs))
print('min(accs)',min(accs))
max_dis=max(accs)-avg
min_dis=min(accs)-avg
if max_dis>min_dis:
    print(max_dis)
else:
    print(min_dis)

#only entropy 8
# 20
# avg 0.8835489833641406
# max(accs) 0.8927911275415896
# min(accs) 0.8761552680221811
# 0.009242144177449063

#no entropy
# 20
# avg 0.8733826247689465
# max(accs) 0.88909426987061
# min(accs) 0.8539741219963032
# 0.015711645101663563

#only entropy 1
# 20
# avg 0.8703327171903883
# max(accs) 0.88909426987061
# min(accs) 0.8521256931608133
# 0.018761552680221727