#encoding: utf-8

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
from sklearn.linear_model import LogisticRegression
from sklearn.model_selection import StratifiedKFold
import operator
import copy
import sys

# 加载数据集
def load_dataset(filename):
    
    dataset = pd.read_csv(filename,index_col = 0)
    print("successful loading the dataset, the shape is: ", dataset.shape)
    #print(dataset.head())

    return dataset


# 加载类标集
def load_labels(filename):
    labelset = pd.read_csv(filename).loc[:, "Class"]  #series

    def to_numeric(lebel):
        if lebel == "P":
            return 1

        elif lebel == "N":
            return 0

        else:
            return np.nan

    labels = labelset.apply(to_numeric).values
    print("successful loading the labels, the length is: " + str(len(labels)))
    #[1 1 1 1 1 1 1 1 1 1 1 1 1 1 1 1 1 1 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0]
    return labels


#采用 K-Fold 交叉验证得到 aac  (注意这里存在问题)
def get_acc(estimator, X, y, skf):
    scores = []
    for train_index, test_index in skf.split(X, y):
        estimator.fit(X[train_index], y[train_index])
        scores.append(estimator.score(X[test_index], y[test_index]))
    return np.mean(scores)


# 根据方差进行过滤
def variance_filter(dataset, per=0.6):

    dataset_var = dataset.apply(np.var, axis=0).sort_values(ascending=False)#递减
    seleted_columns = dataset_var.iloc[0:int(dataset_var.shape[0] * per)].index
    filtered_dataset = dataset.loc[:, seleted_columns]
    print("-"*20)
    print("the var-filtered dataset shape is: "+ str(filtered_dataset.shape) +"\n")

    return filtered_dataset


#选择分类器 D-tree,SVM,NBayes,KNN
def select_estimator(case):

    if case == "SVM":
        estimator = SVC()
    elif case == "KNN":
        estimator = KNeighborsClassifier()
    elif case == "DT":
        estimator = DecisionTreeClassifier()
    elif case == "NB":
        estimator = GaussianNB()
    elif case == "LG":
        estimator = LogisticRegression()    

    return estimator       


def calculate_single(dataset,labels,estimator_name,skf):
    estimator = select_estimator(estimator_name)

    def acc(row,y,estimator,skf):
        scores = []
        row = row.values.reshape((len(row), 1))
        #print(row)
        for train_index, test_index in skf.split(row, y):
            estimator.fit(row[train_index], y[train_index])
            scores.append(estimator.score(row[test_index], y[test_index]))
        return np.mean(scores)

    scores = dataset.apply(func = acc , args=(labels,estimator,skf))

    result = dict()
    for key,value in scores.iteritems():
        result[key] = float(round(value,4))

    return result


#保存结点名字对应的索引
def get_name_index_dict(dataset):
    name_index_dict = {}
    index = 0
    for name in dataset.columns:
        name_index_dict[index] = name
        index += 1
   
    return name_index_dict    


def main(dataset_filename,class_filename,var_filter = False, k_fold = 10, estimator_name = "LG"):
#------------------接口-------------------------------
    k = k_fold
    skf = StratifiedKFold(n_splits=k)      #3折交叉验证 
    estimator_name = estimator_name
    dataset = load_dataset(dataset_filename).T #(samples,labels)
    y = load_labels(class_filename)
    
    if var_filter:
        dataset = variance_filter(dataset,per = var_filter)   #方差过滤一部分


    
    scores = calculate_single(dataset,y,estimator_name,skf) 

    with open("single_node.pkl","wb") as f:
        pickle.dump(scores,f)

 
    name_index_dict = get_name_index_dict(dataset)  

    with open("name_index_dict.pkl","wb") as f:
        pickle.dump(name_index_dict,f)   
  

#------------------接口-------------------------------
    jobs = multiprocessing.JoinableQueue(1000)    #创建容纳一千个任务的队列
    process_list = []
    count_1 = 0
    count_2 = 0
    manager = multiprocessing.Manager()
    max_loc = manager.list()

#-------------------定义辅助函数   利用闭包的特性传递共享变量------------------ 
    def cal(estimator_name,X,y,position_first,position_second):
        estimator_acc = get_acc(select_estimator(estimator_name), X, y, skf)   # k 折交叉验证的结果
        max_loc.append((position_first,position_second,float(round(estimator_acc,4))))


        
        
    #进程任务        
    def worker():
        while True:
            try:
                X,y,position_first,position_second = jobs.get()
                cal(estimator_name,X,y,position_first,position_second)
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

        print(count_1)

        """
        if count_1 == 5:
            print("hello world!")
            nodes = copy.deepcopy(max_loc)
            with open("all_nodes.pkl","wb") as f:
                pickle.dump(nodes,f)
         
            sys.exit(0)     
        """      
        
                
        
    
#-------------------辅助函数----------------------------


    #创建cpu_count个进程  
    for i in range(multiprocessing.cpu_count()):   
        process = multiprocessing.Process(target = worker)
        process.daemon = True    #设置为守护进程
        process_list.append(process)

    #所有进程开始执行 使其处于等待状态(jobs为空)   
    for process in process_list:
        process.start()    

    layer_first_dataset = dataset.drop(dataset.columns[-1],axis=1,inplace=False)  #第一层循环丢掉最后一个特征
    layer_first_dataset.apply(func = layer_first)  #add_task  进程开始执行

    jobs.join()
    print("all task finished.......")

    #通过p.join()方法来使得子进程运行结束后再执行父进程    
    
    all_nodes = copy.deepcopy(max_loc)

    with open("all_nodes.pkl","wb") as f:
        pickle.dump(all_nodes,f)    

    print("finished save all nodes.......")    

if __name__ == '__main__':
    main("Adenoma.csv","Adenomaclass.csv", var_filter = 0.02, k_fold = 10, estimator_name = "LG")


    

    
