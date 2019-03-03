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
- date   : "2017.05.10"
- Version : 2.0.0

Description
    t-test
'''



import numpy as np
import pandas as pd
import os
import pickle
import random
import multiprocessing
from functools import partial
import math

from scipy.stats import ttest_ind_from_stats
from sklearn.model_selection import StratifiedKFold
from prepare import prepare_dataset_labels
from sklearn.linear_model import Lasso
from sklearn.linear_model import LogisticRegression
from sklearn.multiclass import OneVsOneClassifier
from sklearn.model_selection import StratifiedKFold
from sklearn.linear_model import Ridge
import csv



#创造特征索引和特征名字对应的字典 
def get_name_index(dataset):
    name_index_dic = {}
    index = 0
    for name in dataset.index:
        name_index_dic[index] = name
        index += 1    
    return name_index_dic 


# 选择重要性程度大的特征
def rank_importance_value(dataset,labels,alpha = 0.01):
    t_dataset = dataset.T
    selector = Lasso(alpha = alpha,random_state=7)
    selector.fit(t_dataset,labels)
    dataset = t_dataset.iloc[:, abs(selector.coef_) != 0]
    
    return dataset





def prepare(dataset_filename,json_filename,criterion,alpha): 
    dataset,labels = prepare_dataset_labels(dataset_filename,json_filename,criterion)

    name_index_dic = get_name_index(dataset)
    dataset.columns = list(range(dataset.shape[1]))
    dataset.index = list(range(dataset.shape[0]))
    dataset = rank_importance_value(dataset,labels,alpha)

    return dataset,labels,name_index_dic


def get_name(name_index_dic, feature_list):

    result = []
    for num in feature_list:
        result.append(name_index_dic[num])

    return result    


def test_acc(X,y):
    """
    df = pd.read_csv("eggs.csv")
    y = df.values[0]
    estimator = OneVsOneClassifier(LogisticRegression())
    """
            
    skf = StratifiedKFold(n_splits = 10)
    estimator = LogisticRegression()
    scores = []
    for train_index,test_index in skf.split(X,y):
        X_train, X_test = X.ix[train_index], X.ix[test_index]
        y_train, y_test = y[train_index], y[test_index]
        estimator.fit(X_train,y_train)
        scores.append(estimator.score(X_test,y_test))

    return np.mean(scores) 


#对每一个数据集进行运算
def single(dataset_filename,json_filename,alpha = 0.01,classes = [[1,2],[3,4]]):

    dataset,labels,name_index_dic = prepare(dataset_filename,json_filename,classes,alpha)
    
    scores = test_acc(dataset,labels)
    print("for classes {}, the acc is: {}".format(classes,scores))

    feature_list = dataset.columns.tolist()
    feature_names = get_name(name_index_dic,feature_list)

    """
    print("the dataset shape is(samples,features): {}".format(str(dataset.shape)))
    print("-"*30)

    print("for different classes: {}\n".format(str(classes)))
    print("the features name is: ")
    print(feature_names)

    
    with open("result.txt","a") as f:
        f.write("for classes: {}\n".format(str(classes)))
        f.write("the dataset shape is(samples,features): {}\n".format(str(dataset.shape)))
        f.write("the acc is: {}\n".format(scores))
        f.write("the feature name is: {}\n\n".format(str(feature_names)))
    """
    return feature_names    


        

if __name__ == '__main__':
    """
    参数接口:
        dataset_filename  数据文件
        class_filename    类标签文件
        classes           分类标准
        feature_range     选择前 n 个特征
    """
    single("matrix_data.tsv","clinical.project-TCGA-BRCA.2017-04-20T02_01_20.302397.json")


    
    
    

     
