'''
python3

Required packages
- pandas
- numpy
- sklearn
- multiprocessing

Info
- name   : "zhangruochi"
- email  : "zrc720@gmail.com"
- date   : "2016.12.01"
- Version : 5.0.0

Description
    穷举法  每次选取两个特征
    多进程机制
    最终版
'''

import pandas as pd
import numpy as np
import os
import pickle
from operator import itemgetter
import multiprocessing
from functools import partial

from sklearn.svm import SVC
from sklearn.naive_bayes import GaussianNB
from sklearn.neighbors import KNeighborsClassifier
from sklearn.tree import DecisionTreeClassifier
from sklearn.model_selection import StratifiedKFold

# 加载数据集
def load_one_dataset(filename):
    
    dataset = pd.read_csv(filename).iloc[:,1:]
    dataset.columns = list(range(dataset.shape[1]))
    print("successful loading the dataset, the shape is: ", dataset.shape)
    return dataset


# 加载类标集
def load_one_labels(filename):
    labelset = pd.read_csv(filename).loc[:, "Class"]  #series

    def to_numeric(lebel):
        if lebel == "P":
            return 1

        elif lebel == "N":
            return 0

        else:
            return np.nan

    labels = labelset.apply(to_numeric).values
    #[1 1 1 1 1 1 1 1 1 1 1 1 1 1 1 1 1 1 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0]
    return labels


#选择estimator
def select_estimator(case):

    if case == 0:
        estimator = SVC()
    elif case == 1:
        estimator = KNeighborsClassifier()
    elif case == 2:
        estimator = DecisionTreeClassifier()
    elif case == 3:
        estimator = GaussianNB()

    return estimator


#采用 K-Fold 交叉验证得到 aac  (注意这里存在问题)
def get_aac(estimator, X, y, skf):
    scores = []
    for train_index, test_index in skf.split(X, y):
        estimator.fit(X[train_index], y[train_index])
        scores.append(estimator.score(X[test_index], y[test_index]))
    return np.mean(scores)


# 根据方差进行过滤
def variance_filter(dataset, per=0.6):
    feature_name_index = {}
    if not os.path.exists("feature_name_index.txt"):
        with open("feature_name_index.pkl", "wb") as f:
            for index, name in enumerate(dataset.columns.tolist()):
                feature_name_index[name] = index
            pickle.dump(feature_name_index, f)

    else:
        with open("feature_name_index.pkl", "rb") as f:
            feature_name_index = pickle.load(f)

    dataset_var = dataset.apply(np.var, axis=0).sort_values()
    seleted_columns = dataset_var.iloc[0:int(dataset_var.shape[0] * per)].index
    filtered_dataset = dataset.loc[:, seleted_columns]

    return filtered_dataset, feature_name_index



def main():
#------------------接口-------------------------------
    k = 10
    skf = StratifiedKFold(n_splits=k)      #3折交叉验证 

    estimator_list = [0,1,2,3,4]

    dataset = load_one_dataset("t1d.csv").T #(36,7377)
    y = load_one_labels("t1dclass.csv")
    #dataset, feature_name_index = variance_filter(dataset)   #方差过滤一部分
#------------------接口-------------------------------
    
    jobs = multiprocessing.JoinableQueue(1000)    #创建容纳一千个任务的队列
    process_list = []
    count_1 = 0
    count_2 = 0
    manager = multiprocessing.Manager()
    max_loc = manager.list()
    max_i_aac = manager.Value('d', 0.0)


#-------------------定义辅助函数   利用闭包的特性传递共享变量------------------ 
    def cal(estimator_list,X,y,count_1,count_2):
        estimator_max_aac = 0
        for estimator in estimator_list:
            estimator_aac = get_aac(select_estimator(estimator), X, y, skf)   # k 折交叉验证的结果
            if estimator_aac > estimator_max_aac:
                estimator_max_aac = estimator_aac  

        if estimator_max_aac > max_i_aac.value:
            max_i_aac.value = estimator_max_aac
            del max_loc[:]
            max_loc.append((count_1,count_2,max_i_aac.value))


        elif estimator_max_aac == max_i_aac.value:
            max_loc.append((count_1,count_2,max_i_aac.value))
            estimator_max_aac = 0 

        print(count_2)    
        if count_2 == 54675:
            print(max_loc)
    

    #进程任务        
    def worker():
        while True:
            try:
                X,y,count_1,count_2 = jobs.get()
                cal(estimator_list,X,y,count_1,count_2)
            finally:
                jobs.task_done()    

    #第二层循环    
    def layer_second(row,layer_first_row):
        nonlocal count_1,count_2
        count_2 += 1
        X = np.vstack((layer_first_row,row.values)).T
        jobs.put((X,y,count_1,count_1+count_2))
            
    #第一层循环
    def layer_first(row):
        nonlocal count_1,count_2
        count_1 += 1
        count_2 = 0
        layer_second_dataset = dataset.drop(dataset.columns[0:count_1],axis=1,inplace=False) #第二层循环丢掉第一层循环之前的特征 
        layer_second_dataset.apply(func = layer_second,axis=0,args=(row.values,)) 

    
#-------------------辅助函数----------------------------


    #创建cpu_count个进程  
    for i in range(multiprocessing.cpu_count()):   
        process = multiprocessing.Process(target = worker)
        process.daemon = True    #设置为守护进程
        process_list.append(process)

    #所有进程开始执行 使其处于等待状态    
    for process in process_list:
        process.start()    

    layer_first_dataset = dataset.drop(dataset.columns[-1],axis=1,inplace=False)  #第一层循环丢掉最后一个特征
    layer_first_dataset.apply(func = layer_first)  #add_task  进程开始执行

    for process in process_list:
        process.join()    



if __name__ == '__main__':
    main()


    

    
