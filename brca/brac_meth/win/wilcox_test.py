'''
python3

Required packages
- pandas
- numpy
- sklearn
- scipy


Info
- name   : "zhangruochi"
- email  : "zrc720@gmail.com"
- date   : "2017.04.28"
- Version : 1.0.0

Description
    wilcox test 
'''


import numpy as np
import pandas as pd
import os
import pickle
import random
import multiprocessing
from functools import partial

from scipy.stats import wilcoxon

from sklearn.model_selection import StratifiedKFold
from sklearn.svm import SVC
from sklearn.naive_bayes import GaussianNB
from sklearn.neighbors import KNeighborsClassifier
from sklearn.tree import DecisionTreeClassifier
from sklearn.linear_model import LogisticRegression


#加载数据集
def load_data(filename):
    dataset = pd.read_csv(filename,header = None)
    name_index_dic = get_name_index(dataset)
    with open("name_index.pkl","wb") as f:
        pickle.dump(name_index_dic,f)

    dataset.columns = list(range(dataset.shape[1]))
    dataset = dataset.rename(index = name_index_dic)
    return dataset


#创造特征索引和特征名字对应的字典 
def get_name_index(dataset):
    name_index_dic = {}
    index = 0
    for name in dataset.index:
        name_index_dic[name] = index
        index += 1 
    return name_index_dic 


#加载标签
def load_class(filename):
    class_set = pd.read_csv(filename,index_col = 0)
    labels = class_set["Class"]
    result = []
    
    def convert(label):
        if label == 'N':
            result.append(0)
        if label == 'P':
            result.append(1)    

    labels.apply(func = convert)     
    return np.array(result)



# t_检验  得到每个特征的 t 值
def wilcoxon_test(dataset,labels):
    p_value = dataset.apply(func = wilcoxon,axis=1,args=(None,"wilcox",))
    return p_value
 


#根据 t 检验的结果的大小重新构造特征集
def rank_p_value(dataset,labels):
    p_value = wilcoxon_test(dataset,labels)
    sort_index = p_value.sort_values(ascending=True).index
    dataset = dataset.reindex(sort_index)
    return dataset.T


def prepare(datset_filename,class_filename):
    dataset = load_data(datset_filename)
    labels = load_class(class_filename)
    dataset = rank_p_value(dataset,labels)
    #将样本的顺序打乱  防止在交叉验证的时候出错
    return dataset,labels


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

#采用 K-Fold 交叉验证 得到 aac 
def get_aac(estimator,X,y,seed_number,skf):
    scores = []
    for train_index,test_index in skf.split(X,y):
        X_train, X_test = X.ix[train_index], X.ix[test_index]
        y_train, y_test = y[train_index], y[test_index]
        estimator.fit(X_train,y_train)
        scores.append(estimator.score(X_test,y_test))

    return np.mean(scores)    


#对每一个数据集进行运算
def w_test_main(dataset_filename,class_filename,estimator = ["SVM","KNN","DT","NB","LG"],feature_range = 10,k_fold = 10,seed_number = 7):
    estimator_list = estimator
    skf = StratifiedKFold(n_splits = k_fold)
    dataset,labels = prepare(dataset_filename,class_filename)
    print("the dataset shape is(samples,features): {}".format(str(dataset.shape)))
    print("-"*20)
    acc_list = []
    max_estimator_aac = 0
    for estimator in estimator_list:
        estimator_aac = get_aac(select_estimator(estimator),dataset.iloc[:,:feature_range],labels,seed_number,skf)
        print("the acc for {}: {}".format(estimator,estimator_aac))
        acc_list.append(estimator_aac)
        
        if estimator_aac > max_estimator_aac:
            max_estimator_aac = estimator_aac   #记录对于 k 个 特征 用五个个estimator 得到的最大值
    
    acc_list.append(max_estimator_aac)
    print("-"*20)        
    print("the macc is: {}\n".format(max_estimator_aac))        
    return acc_list




if __name__ == '__main__':
    """
    参数接口:
        dataset_filename  数据文件
        class_filename    类标签文件
        estimator         选择的分类器 （可选一个或者多个，默认五个全部选择）  
        feature_range     选择前 n 个特征
        k_fold            k 倍交叉验证， 默认10倍
        seed_number       随机种子

    """
    single(dataset_filename = "Adenoma.csv",class_filename = "Adenomaclass.csv",\
        estimator = ["SVM","KNN","DT","NB","LG"],feature_range = 50, k_fold = 10,seed_number = 7)


    
    
    

     
