import os
import random
f = open('data/cow_jpg.lst')#上一步生成的图片路径文件
list = f.readlines()
print(len(list))
random.shuffle(list)
print(list)
set_num = int(float(len(list))*0.2)
#0.2为拆分阈值，0.2则是前20%为测试集，剩下的是训练集
test_list = list[:set_num]
train_list = list[set_num:]
print('=======================================================================================')
print(len(test_list))
print(len(train_list))
print(test_list and train_list)

f2 = open('data/cow_jpg_train.lst','w')
for i in train_list:
    f2.write(i)
f3 = open('data/cow_jpg_test.lst','w')
for i in test_list:
    f3.write(i)
# new_list = [x1-x2 for x1, x2 in zip(list, de_list)]
# print(new_list)
# print(len(new_list))
f.close()
f2.close()
f3.close()