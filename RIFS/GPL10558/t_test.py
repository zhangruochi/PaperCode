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
- date   : "2016.10.21"
- Version : 1.0.0

Description
    other algorithms compared to RIFS
'''



import numpy as np
import pandas as pd
import os
import pickle
import random
import multiprocessing
from functools import partial

from scipy.stats import ttest_ind_from_stats

from sklearn.model_selection import StratifiedKFold
from sklearn.svm import SVC
from sklearn.naive_bayes import GaussianNB
from sklearn.neighbors import KNeighborsClassifier
from sklearn.tree import DecisionTreeClassifier
from sklearn.linear_model import LogisticRegression
import re
from sklearn.preprocessing import MinMaxScaler
from sklearn import metrics



def load_label(filename):
    with open(filename) as f:
        content = f.read()
  
    label_list = re.split("\"\s+\"",content)
    label_list = [label.replace("malignacy type: ","") for label in label_list]
    
    label_array = []
    for label in label_list:
        if label.startswith("benign prostatic hyperplasia"):
            label_array.append(0)
        elif label.startswith("Prostate carcinoma"):
            label_array.append(1)

    #exit()

    mask = [True if label.startswith("benign prostatic hyperplasia") or\
            label.startswith("Prostate carcinoma") else False for label in label_list]
    
    return np.array(label_array),mask

def get_name_index(dataset):
    name_index_dic = {}
    index = 0
    for name in dataset.index:
        name_index_dic[name] = index
        index += 1 
    return name_index_dic 


def load_dataset(filename,mask):
    dataset = pd.read_table(filename,index_col=0, header=None)
    name_index_dic = get_name_index(dataset)
    with open("name_index.pkl","wb") as f:
        pickle.dump(name_index_dic,f)

    dataset.columns = list(range(dataset.shape[1]))
    dataset = dataset.rename(index = name_index_dic)
    dataset = dataset.fillna(dataset.mean())

    dataset = dataset.loc[:,mask]
    return dataset




# t_检验  得到每个特征的 t 值
def t_test(dataset,labels):
    p_feature_data = dataset.loc[:,labels == 1]  #得到正类数据集
    n_feature_data = dataset.loc[:,labels == 0]  #得到负类数据集

    p_mean,n_mean = np.mean(p_feature_data,1),np.mean(n_feature_data,1)
    p_std,n_std = np.std(p_feature_data,1),np.std(n_feature_data,1)

    t_value,p_value = ttest_ind_from_stats(p_mean,p_std,p_feature_data.shape[1],n_mean,n_std,n_feature_data.shape[1])
    p_value = pd.Series(data=p_value,index=list(range(len(p_value))))


    return p_value
 
#normalize
def normalize_dataset(dataset):
    minimize = MinMaxScaler()
    dataset = pd.DataFrame(data = minimize.fit_transform(dataset),index = range(dataset.shape[0]),columns = range(dataset.shape[1]))
    return dataset


#根据 t 检验的结果的大小重新构造特征集
def rank_t_value(dataset,labels):
    p_value = t_test(dataset,labels)
    sort_index = p_value.sort_values(ascending=True).index
    dataset = dataset.reindex(sort_index)
    
    return dataset.T


def prepare(datset_filename,class_filename):
    labels,mask = load_label(class_filename)
    dataset = load_dataset(datset_filename,mask)
    dataset = rank_t_value(dataset,labels)
    #数据归一化
    dataset = normalize_dataset(dataset)
    return dataset,labels

#选择分类器 D-tree,SVM,NBayes,KNN
def select_estimator(case):

    if case == 0:
        estimator = SVC(probability=True)
    elif case == 1:
        estimator = KNeighborsClassifier()
    elif case == 2:
        estimator = DecisionTreeClassifier(random_state = 7)
    elif case == 3:
        estimator = GaussianNB()
    elif case == 4:
        estimator = LogisticRegression()    

    return estimator            

#采用 K-Fold 交叉验证 得到 aac 
def get_aac(estimator,X,y,seed_number,skf):
    scores = []
    aucs = []
    for train_index,test_index in skf.split(X,y):
        X_train, X_test = X.ix[train_index], X.ix[test_index]
        y_train, y_test = y[train_index], y[test_index]
        estimator.fit(X_train,y_train)
        y_predict = estimator.predict(X_test)

        predict_prob_y = estimator.predict_proba(X_test)

        test_auc = metrics.roc_auc_score(y_test,predict_prob_y[:,1])
        #print(test_auc)
        aucs.append(test_auc)

        scores.append(np.mean(y_test == y_predict))

    return np.mean(scores),np.mean(aucs)    


#对每一个数据集进行运算
def single(datset_filename,class_filename,feature_range,seed_number):
    estimator_list = [0,1,2,3,4]
    skf = StratifiedKFold(n_splits = 10)
    dataset,labels = prepare(datset_filename,class_filename)
    
    max_estimator_aac = 0
    max_auc_score = 0
    for estimator in estimator_list:
        estimator_aac,auc = get_aac(select_estimator(estimator),dataset.iloc[:,1:feature_range],labels,seed_number,skf)
        print(auc)
        if estimator_aac > max_estimator_aac:
            max_estimator_aac = estimator_aac   #记录对于 k 个 特征 用四个estimator 得到的最大值

        if auc > max_auc_score:
            max_auc_score = auc   #记录对于 k 个 特征 用四个estimator 得到的最大值    

    return max_estimator_aac,auc









if __name__ == '__main__':
    print(single("GSE55599-GPL10558_series_matrix.txt","label.txt",2,7))


    
    
    

     
