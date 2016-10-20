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
- date   : "2016.10.12"
- Version : 2.0.0

Description
    RIFS
    multiprocessing
'''


import numpy as np
import pandas as pd
import os
import pickle
import random
import time
import multiprocessing
from functools import partial
import re

from scipy.stats import ttest_ind_from_stats

from sklearn.cross_validation import KFold
from sklearn.svm import SVC
from sklearn.naive_bayes import GaussianNB
from sklearn.neighbors import KNeighborsClassifier
from sklearn.tree import DecisionTreeClassifier
from sklearn.grid_search import GridSearchCV
from sklearn.linear_model import LogisticRegression



#加载数据集
def load_data(filename):
    full_path_name = os.path.join("dataset/data",filename)
    dataset = pd.read_csv(full_path_name,index_col=0)
    name_index_dic = get_name_index(dataset)
    dataset.columns = list(range(dataset.shape[1]))
    dataset = dataset.rename(index = name_index_dic)
    return dataset

#加载标签
def load_class(filename):
    full_path_name = os.path.join("dataset/class",filename)
    class_set = pd.read_csv(full_path_name,index_col = 0)
    labels = class_set["Class"]
    result = []
    
    def convert(label):
        if label == 'N':
            result.append(0)
        if label == 'P':
            result.append(1)    

    labels.apply(func = convert)     
    return np.array(result)


#创造特征索引和特征名字对应的字典 
def get_name_index(dataset):
    name_index_dic = {}
    index = 0
    for name in dataset.index:
        name_index_dic[name] = index
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


    return p_feature_data, n_feature_data, p_value
 


#根据 t 检验的结果的大小重新构造特征集
def save_t_value(dataset,labels):
    p_feature_data,n_feature_data,p_value = t_test(dataset,labels)
    sort_index = p_value.sort_values(ascending=True).index

    return sort_index    



#得到特征子集的其实位置和特征子集的个数
def get_ranked_subfeature():
    with open("output.txt","r") as f:
        ranked_subfeature = []
        for line in f.readlines():
            temp_list = []
            for number in line.split(", ")[0:2]:
                temp_list.append(number)
            ranked_subfeature.append(temp_list)
        
    return ranked_subfeature        



#得到实际位置和 t 检验排序后的位置对应的词典
def get_rank_dict(dataset,labels):
    rank_list = save_t_value(dataset,labels)
    rank_dict = {}
    for index,rank in enumerate(rank_list):
        rank_dict[index] = rank
    return rank_dict    
     

#得到实际 feature 的位置
def deal_output(dataset,labels,ranked_subfeature):
    rank_dict = get_rank_dict(dataset,labels)          
    feature_list = []
    start = int(ranked_subfeature[0])

    for i in range(int(ranked_subfeature[1])):
        feature_list.append(rank_dict[start+i])
    return feature_list         



#选择分类器 D-tree,SVM,NBayes,KNN
def select_estimator(case):

    if case == 0:
        estimator = SVC()
    elif case == 1:
        estimator = KNeighborsClassifier()
    elif case == 2:
        estimator = DecisionTreeClassifier()
    elif case == 3:
        estimator = GaussianNB()
    elif case == 4:
        estimator = LogisticRegression()    

    return estimator            

#采用 K-Fold 交叉验证 得到 aac 
def get_aac(estimator,p_feature_data,n_feature_data,y,seed_number):
    scores = []
    k = 3
    p_kf = KFold(p_feature_data.shape[0],n_folds = k,shuffle = True,random_state = seed_number)
    n_kf = KFold(n_feature_data.shape[0],n_folds = k,shuffle = True,random_state = seed_number)
    
    for i in range(k):

        p_train_data = p_feature_data.iloc[list(p_kf)[i][0],:]
        p_test_data = p_feature_data.iloc[list(p_kf)[i][1],:]

        n_train_data = n_feature_data.iloc[list(n_kf)[i][0],:]
        n_test_data = n_feature_data.iloc[list(n_kf)[i][1],:]

        X_train = p_train_data.append(n_train_data)
        y_train = y[X_train.index]
        estimator.fit(X_train,y_train)

                
        X_test = p_test_data.append(n_test_data)
        y_test = y[X_test.index]
        scores.append(estimator.score(X_test,y_test))

    return np.mean(scores)    


#对每一个数据集进行运算
def single(dataset,labels,feature_list,seed_number):
    estimator_list = [0,1,2,3,4]

    extracted_p_dataset = dataset.T.iloc[labels == 1,feature_list]
    extracted_n_dataset = dataset.T.iloc[labels == 0,feature_list]

    max_estimator_aac = -1
    for index in estimator_list:
        estimator_aac = get_aac(select_estimator(index),extracted_p_dataset,extracted_n_dataset,labels,seed_number)
        if estimator_aac > max_estimator_aac:
            max_estimator_aac = estimator_aac   #记录对于 k 个 特征 用四个estimator 得到的最大值
            

    print("{0}".format(max_estimator_aac))        
    with open("rifs_results.txt","a") as f:
        f.write("{0}\n".format(max_estimator_aac))



#对17个数据集进行一次运行
def all_dataset():
    dataset_list = os.listdir('dataset/data')
    label_list = os.listdir('dataset/class')

    try:
        dataset_list.remove('.DS_Store')
        label_list.remove('.DS_Store')
    except:
        pass

    ranked_subfeature_list = get_ranked_subfeature() 
    print(ranked_subfeature_list)   
    
    seed_number = 7
    index = 0
    for dataset_filename,label_filename in zip(dataset_list,label_list):
        dataset = load_data(dataset_filename)
        labels = load_class(label_filename)
        feature_list = deal_output(dataset,labels,ranked_subfeature_list[index])  

        print(dataset_filename,label_filename,feature_list)
        single(dataset,labels,feature_list,seed_number)
        index += 1

if __name__ == '__main__':
    #single("Adenoma.csv","Adenomaclass.csv",[3068],7)
    all_dataset()
      

    
    
    

     
