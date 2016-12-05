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
- date   : "2016.12.02"
- Version : 1.0.0

Description
    RIFS
    single file
'''


import numpy as np
import pandas as pd
import os
import pickle
import random
import time
from functools import partial

from scipy.stats import ttest_ind_from_stats
from sklearn.model_selection import StratifiedKFold
from sklearn.svm import SVC
from sklearn.naive_bayes import GaussianNB
from sklearn.neighbors import KNeighborsClassifier
from sklearn.tree import DecisionTreeClassifier
from sklearn.linear_model import LogisticRegression



#加载数据集
def load_data(filename):
    dataset = pd.read_csv(filename,index_col=0)
    name_index_dic = get_name_index(dataset)
    
    with open("name_index.pkl","wb") as f:
        pickle.dump(name_index_dic,f)

    dataset.columns = list(range(dataset.shape[1]))
    dataset = dataset.rename(index = name_index_dic)
    print(dataset.shape)   #(7377, 36)
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
    #with open("p_rank.pkl","wb") as f:
    #    pickle.dump(sort_index,f)
    dataset = dataset.reindex(sort_index)
    return dataset.T

#根据 t 检验的结果的大小重新构造特征集
def save_t_value(dataset,labels):
    p_value = t_test(dataset,labels)
    sort_index = p_value.sort_values(ascending=True).index

    return sort_index   

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

#得到特征子集的起始位置和特征子集的个数
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

#采用 K-Fold 交叉验证 得到 aac 
def get_aac(estimator,X,y,skf):
    for train_index,test_index in skf.split(X,y):
        X_train, X_test = X.ix[train_index], X.ix[test_index]
        y_train, y_test = y[train_index], y[test_index]
        estimator.fit(X_train,y_train)
        scores = estimator.score(X_test,y_test)

    return estimator,np.mean(scores)    
        

#生成重启的位置
def random_num_generator(num_of_feature,seed_number, percent):
    random.seed(seed_number)
    result = random.sample(list(range(num_of_feature)),int(num_of_feature * percent -1))   # 重启的组数为所有特征的一半
    result.append(0)   #保证0在其中
    return result


#得到实际 feature 的位置
def deal_output(dataset,labels,ranked_subfeature):
    rank_dict = get_rank_dict(dataset,labels)     
    feature_list = []
    start = int(ranked_subfeature[0])
    for i in range(int(ranked_subfeature[1])):
        feature_list.append(rank_dict[start+i]) 
    return feature_list         


"""
def find_best_subfeature(feature_list):  #[(950, 6, 0.8125, 1), (2702, 3, 0.8125, 1)]
    return sorted(feature_list,key = lambda x:x[1])
"""    


if __name__ == '__main__':
    dataset = load_data("Adenoma.csv")
    labels = load_class("Adenomaclass.csv")
    estimator_list = [0,1,2,3,4]
    skf = StratifiedKFold(n_splits = 3)
    ranked_subfeature_list = [381,1]
    print(ranked_subfeature_list)
    feature_list = deal_output(dataset,labels,ranked_subfeature_list)
    print(feature_list)
    names = ["SVM","KNeighbors","DecisionTree","NaiveBayes","LogisticRegression"]
    index = 0
    for index in estimator_list:
        clf,estimator_aac = get_aac(select_estimator(index),dataset.iloc[feature_list,:].T,labels,skf)
        print("for {}: {} \n".format(names[index],estimator_aac))
        index += 1
                
    

    
      

    
    
    

     
