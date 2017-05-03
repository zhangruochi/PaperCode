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
from sklearn.linear_model import LogisticRegression

from prepare import prepare_dataset_labels


#创造特征索引和特征名字对应的字典 
def get_name_index(dataset):
    name_index_dic = {}
    index = 0
    for name in dataset.index:
        name_index_dic[index] = name
        index += 1    
    return name_index_dic 




# t_检验  得到每个特征的 t 值
def t_test(dataset,labels):
    p_feature_data = dataset.loc[:,labels == 1]  #得到正类数据集
    n_feature_data = dataset.loc[:,labels == 0]  #得到负类数据集

    p_mean,n_mean = np.mean(p_feature_data,1),np.mean(n_feature_data,1)
    p_std,n_std = np.std(p_feature_data,1),np.std(n_feature_data,1)

    t_value,p_value = ttest_ind_from_stats(p_mean,p_std,p_feature_data.shape[1],n_mean,n_std,n_feature_data.shape[1])
    p_value = pd.Series(data=p_value,index=list(range(len(p_value))))

    return p_value
 


#根据 t 检验的结果的大小重新构造特征集
def rank_t_value(dataset,labels):
    p_value = t_test(dataset,labels)
    sort_index = p_value.sort_values(ascending=True).index
    dataset = dataset.reindex(sort_index)

    return dataset.T


def prepare(dataset_filename,json_filename,criterion): 
    dataset,labels = prepare_dataset_labels(dataset_filename,json_filename,criterion)

    name_index_dic = get_name_index(dataset)
    dataset.columns = list(range(dataset.shape[1]))
    dataset.index = list(range(dataset.shape[0]))
    dataset = rank_t_value(dataset,labels)

    return dataset,labels,name_index_dic



def cal_aic(prob,y_true,k):


    sum_1 = sum(prob[y_true == 1,0] ** 2)
    sum_0 = sum(prob[y_true == 0,1] ** 2)

    deviation = sum_1 + sum_0

    n = len(y_true)
    k = k
    l = -(2/n)*math.log(2*math.pi) - n/2 * math.log(deviation / n) - n/2
    aic = -2 * l + 2 * (k + 1)

    return aic

 
def get_aic(estimator,X,y,k):
    estimator.fit(X,y)
    prob = estimator.predict_proba(X)
    acc = estimator.score(X,y)
    aic = cal_aic(prob,y,k)

    return aic,acc


def get_name(name_index_dic, feature_list):

    result = []
    for num in feature_list:
        result.append(name_index_dic[num])

    return result    




#对每一个数据集进行运算
def single(dataset_filename,json_filename,classes = [[1],[2,3]],feature_range = 20):
    estimator = LogisticRegression()

    dataset,labels,name_index_dic = prepare(dataset_filename,json_filename,classes)

    feature_list = dataset.columns[:feature_range].tolist()
    feature_names = get_name(name_index_dic,feature_list)

    print("the dataset shape is(samples,features): {}".format(str(dataset.shape)))
    print("-"*20)



    estimator_aic,estimator_acc = get_aic(estimator,dataset.iloc[:,:feature_range],labels,feature_range)
    print("for different classes: {}\n".format(str(classes)))
    print("the features name is: ")
    print(feature_names)
    print("the aic is: {}".format(estimator_aic))
    print("the acc is: {}\n".format(estimator_acc))

    with open("result.txt","a") as f:
        f.write("for different classes: {}\n".format(str(classes)))
        f.write("the feature name is: {}\n".format(str(feature_names)))
        f.write("the aic is: {}\n".format(estimator_aic))
        f.write("the acc is: {}\n\n".format(estimator_acc))
        
        
    return estimator_aic, feature_names
        

if __name__ == '__main__':
    """
    参数接口:
        dataset_filename  数据文件
        class_filename    类标签文件
        classes           分类标准
        feature_range     选择前 n 个特征
    """
    single("matrix_data.tsv","clinical.project-TCGA-BRCA.2017-04-20T02_01_20.302397.json",\
        classes = [[1],[2,3]],feature_range = 10)


    
    
    

     
