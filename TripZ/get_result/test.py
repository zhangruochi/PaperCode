import re
import numpy as np

content = ""
with open("acc.txt","r") as f:
    content = f.read()
    print(content)

pattern = re.compile("ulcer_acc:  \d\.\d+") 
result = re.findall(pattern,content)
#print(result)   

result_number = [float(item.strip("ulcer_acc:  ")) for item in result]
print(result_number)


rf = []
dt = []
nb = []
lr = []
knn = []

for index, number in enumerate(result_number) :
    if index % 5 == 0:
        rf.append(number)
    elif index % 5 == 1:
        dt.append(number)
    elif index % 5 == 2:
        nb.append(number)
    elif index % 5 == 3:
        lr.append(number)
    elif index % 5 == 4:
        knn.append(number)



print(len(rf))
print(len(dt))
print(len(nb))
print(len(lr))
print(len(knn))            
                

result_list = [rf,dt,nb,lr,knn]

for estimator_result in result_list:
    print(np.mean(estimator_result))
    print(np.var(estimator_result))
    print("")




