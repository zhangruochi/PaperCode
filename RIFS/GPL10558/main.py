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
- date   : "2017.2.22"
- Version : 1.0.0

Description
    test randomly re-start the IFS strategy
'''

import re
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
from sklearn.preprocessing import MinMaxScaler


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
    
    print(label_array)
    #exit()

    mask = [True if label.startswith("benign prostatic hyperplasia") or\
            label.startswith("Prostate carcinoma") else False for label in label_list]
    
    print(mask)
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

    return t_value
 

#根据 t 检验的结果的大小重新构造特征集
def rank_t_value(dataset,labels):
    p_value = t_test(dataset,labels)
    #print(p_value)
    sort_index = p_value.sort_values(ascending=True).index
    with open("p_rank.pkl","wb") as f:
        pickle.dump(sort_index,f)

    dataset = dataset.reindex(sort_index)
    #print(dataset)
    return dataset.T

#normalize
def normalize_dataset(dataset):
    minimize = MinMaxScaler()
    dataset = pd.DataFrame(data = minimize.fit_transform(dataset),index = range(dataset.shape[0]),columns = range(dataset.shape[1]))
    return dataset

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
        estimator = SVC()
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
def get_aac(estimator,X,y,skf):
    scores = []
    for train_index,test_index in skf.split(X,y):
        X_train, X_test = X.ix[train_index], X.ix[test_index]
        y_train, y_test = y[train_index], y[test_index]
        estimator.fit(X_train,y_train)
        scores.append(estimator.score(X_test,y_test))
    return np.mean(scores) 

"""        
#采用 K-Fold 交叉验证 得到 aac  sn sp mcc
def evaluate(estimator,X,y,skf):
    acc_list,sn_list,sp_list,mcc_list = [],[],[],[]
    for train_index, test_index in skf.split(X, y):
        estimator.fit(X[train_index],y[train_index])
        y_predict = estimator.predict(X[test_index])
        y_true = y[test_index]

        #索引
        predict_index_p = (y_predict == 1)  #预测为正类的
        predict_index_n = (y_predict == 0)  #预测为负类

        index_p = (y_true==1)  #实际为正类
        index_n = (y_true==0)  #实际为负类

        Tp = sum(y_true[predict_index_p])       #正确预测的正类  （实际为正类 预测为正类）
        Tn = sum([1 for x in list(y_true[predict_index_n]) if x == 0]) #正确预测的负类   (实际为负类 预测为负类)
        Fn = sum(y_predict[index_n])       #错误预测的负类  （实际为负类 预测为正类）
        Fp = sum(y_true[predict_index_n])       #错误预测的正类   (实际为正类 预测为负类)

        acc = (Tp+Tn)/(Tp+Tn+Fp+Fn)
        sn = Tp/(Tp+Fn)
        sp = Tn/(Tn+Fp)
        mcc = matthews_corrcoef(y_true,y_predict)

        acc_list.append(acc)
        sn_list.append(sn)
        sp_list.append(sp)
        mcc_list.append(mcc)

    return np.mean(acc_list),np.mean(sn_list),np.mean(sp_list),np.mean(mcc_list)
"""

#生成重启的位置
def random_num_generator(num_of_feature,seed_number, percent):
    random.seed(seed_number)
    result = random.sample(list(range(num_of_feature)),int(num_of_feature * percent -1))   # 重启的组数为所有特征的一半
    result.append(0)   #保证0在其中
    return result


#对每一个数据集进行运算
def single(dataset_filename,label_filename, seed = 7, percent = 0.5, stop = 4):
#------------参数接口---------------    
    seed_number = seed
    skf = StratifiedKFold(n_splits = 10)
    estimator_list = [0,1,2,3,4]
#----------------------------------    

    start = time.time()
    print("dealing the {}".format(dataset_filename))

    dataset,labels = prepare(dataset_filename,label_filename)
    print(dataset.shape)
    print(labels)
    exit()
    loc_of_first_feature = random_num_generator(dataset.shape[1], seed_number, percent) # 重启的位置

    max_loc_aac = 0
    max_aac_list = []
    feature_range = dataset.shape[1]


    for loc in loc_of_first_feature:
        num = 0
        max_k_aac = 0 
        count = 0  #记录相等的次数
        best_estimator = -1   
        
        for k in range(feature_range - loc):  # 从 loc位置 开始选取k个特征
            max_estimator_aac = 0
            locs = [i for i in range(loc,loc+k+1)]
            X = dataset.iloc[:,locs]

            for item in estimator_list:
                estimator_aac = get_aac(select_estimator(item),X,labels,skf)
                if estimator_aac > max_estimator_aac:
                    max_estimator_aac = estimator_aac   #记录对于 k 个 特征 用四个estimator 得到的最大值
                    best_temp_estimator = item
     
            if max_estimator_aac > max_k_aac:
                count = 0 
                max_k_aac = max_estimator_aac   #得到的是从 loc 开始重启的最大值
                num = k+1
                best_estimator = best_temp_estimator
            
            else:
                count += 1
                if count == stop:
                    break
   
        if max_k_aac > max_loc_aac:
            max_loc_aac = max_k_aac
            max_aac_list = []
            max_aac_list.append((loc,num,max_loc_aac,best_estimator))
            print(">: {}\n".format(max_aac_list))

            with open("result.txt","a") as infor_file:
                infor_file.write(">: {}\n".format(max_aac_list))

        elif max_k_aac == max_loc_aac:
            max_aac_list.append((loc,num,max_loc_aac,best_estimator))
            print("=: {}\n".format(max_aac_list))
            
            with open("result.txt","a") as infor_file:
                infor_file.write("=: {}\n".format(max_aac_list))
    
    end = time.time()            
    with open("result.txt","a") as infor_file:
        infor_file.write("using time: {}".format(end-start))  

    return max_aac_list         




 


if __name__ == '__main__':
    #single("GSE29315_series_matrix.txt","label1.txt")  #[(12613, 3, 0.87714285714285722, 1)]
    #load_label("label1.txt")
    #load_dataset("GSE55599-GPL10558_series_matrix.txt")
    single("GSE55599-GPL10558_series_matrix.txt","label.txt")
