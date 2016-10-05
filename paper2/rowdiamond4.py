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
- date   : "2016.10.5"
- Version : 2.0.0

Description
    穷举法  每次选取两个特征
    使用 apply 函数迭代  取消双层 for 循环
    添加多进程机制
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
from sklearn.grid_search import GridSearchCV
from sklearn.cross_validation import KFold

# 加载数据集
def load_one_dataset(filename):
    full_path_name = os.path.join(
        "/Users/ZRC/Desktop/paper/dataset/data", filename)
    dataset = pd.read_csv(full_path_name).drop(' ',axis=1)

    return dataset


# 加载类标集
def load_one_labels(filename):
    full_path_name = os.path.join(
        "/Users/ZRC/Desktop/paper/dataset/class", filename)
    labelset = pd.read_csv(full_path_name).loc[:, "Class"]

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
        """
        paramters = {"kernel":["linear","rbf"],
                     "C": np.logspace(-4,4,10),
                    } 
        estimator = GridSearchCV(estimator,paramters)
        """
    elif case == 1:
        estimator = KNeighborsClassifier()
    elif case == 2:
        estimator = DecisionTreeClassifier()
    elif case == 3:
        estimator = GaussianNB()

    return estimator


# K-Fold生成器
def k_fold(y, k):
    kf = KFold(len(y), n_folds=k)
    for train_index, test_index in kf:
        yield train_index, test_index


#采用 K-Fold 交叉验证得到 aac  (注意这里存在问题)
def get_aac(estimator, X, y, k):
    scores = []
    for train_index, test_index in k_fold(y, k):
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



def cal(estimator_list,X,y,count_1,count_2):
    global max_i_aac
    global max_loc

    estimator_max_aac = 0
    for estimator in estimator_list:
        estimator_aac = get_aac(select_estimator(estimator), X, y, 3)   # k 折交叉验证的结果
        if estimator_aac > estimator_max_aac:
            estimator_max_aac = estimator_aac  


    if estimator_max_aac > max_i_aac.value:
        max_i_aac.value = estimator_max_aac
        del max_loc[:]
        max_loc.append((count_1,count_2,max_i_aac.value))

    elif estimator_max_aac == max_i_aac.value:
        max_loc.append((count_1,count_2,max_i_aac.value))
        estimator_max_aac = 0    
    
    

def worker():
    while True:
        try:
            X,y,count_1,count_2 = jobs.get()
            cal(estimator_list,X,y,count_1,count_2)
        finally:
            jobs.task_done()    

           

def layer_first(row):
    global count_1
    global count_2
    count_1 += 1
    count_2 = 0
    layer_second_dataset = dataset.drop(dataset.columns[0:count_1],axis=1,inplace=False) #第二层循环丢掉第一层循环之前的特征
    layer_second_dataset.apply(func=layer_second,axis=0,args=(row.values,)) 

def layer_second(row,layer_first_row):
    global count_2
    global jobs
    count_2 += 1
    X = np.vstack((layer_first_row,row.values)).T
    jobs.put((X,y,count_1,count_2))
    if count_2 == 7376:
        print(max_loc)
        exit()


estimator_list = [3]
dataset = load_one_dataset("Adenoma.csv").T
#filtered_dataset, feature_name_index = variance_filter(dataset)
y = load_one_labels("Adenomaclass.csv")
length = dataset.shape[1]
layer_first_dataset = dataset.drop(dataset.columns[-1],axis=1,inplace=False)  #第一层循环丢掉最后一个特征

jobs = multiprocessing.JoinableQueue(1000)
process_list = []
count_1 = 0
count_2 = 0
manager = multiprocessing.Manager()
max_loc = manager.list()
max_i_aac = manager.Value('d', 0.0)

for i in range(4):
    process = multiprocessing.Process(target= worker)
    process_list.append(process)

for process in process_list:
    process.daemon = True
    process.start()


layer_first_dataset.apply(func = layer_first)  #add_task  进程开始执行


for process in process_list:
    process.join()




    

    
