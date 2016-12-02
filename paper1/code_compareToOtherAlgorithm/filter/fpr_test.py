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
    fpr test algorithms compared to RIFS
'''


import numpy as np
import pandas as pd
import os
import pickle
import random
import multiprocessing
from functools import partial

from sklearn.feature_selection import SelectFpr

from sklearn.cross_validation import KFold
from sklearn.svm import SVC
from sklearn.naive_bayes import GaussianNB
from sklearn.neighbors import KNeighborsClassifier
from sklearn.tree import DecisionTreeClassifier
from sklearn.grid_search import GridSearchCV
from sklearn.linear_model import LogisticRegression



#加载数据集
def load_data(filename):
    full_path_name = os.path.join("/Users/ZRC/Desktop/HLab/dataset/data",filename)
    dataset = pd.read_csv(full_path_name,index_col=0)
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
    full_path_name = os.path.join("/Users/ZRC/Desktop/HLab/dataset/class",filename)
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



# t_检验  得到每个特征的 t 值
def fpr_test(dataset,labels):
    p_feature_data = dataset.loc[:,labels == 1]  #得到正类数据集
    n_feature_data = dataset.loc[:,labels == 0]  #得到负类数据集

    t_dataset = dataset.T
    selector = SelectFpr()
    selector.fit(t_dataset,labels)
    p_value = pd.Series(data=selector.pvalues_,index= list(range(len(selector.pvalues_))))

    return p_feature_data, n_feature_data, p_value
 


#根据 t 检验的结果的大小重新构造特征集
def rank_p_value(dataset,labels):
    p_feature_data,n_feature_data,p_value = fpr_test(dataset,labels)
    sort_index = p_value.sort_values(ascending=True).index

    p_feature_data = p_feature_data.reindex(sort_index)
    n_feature_data = n_feature_data.reindex(sort_index)

    return p_feature_data.T,n_feature_data.T


def prepare(datset_filename,class_filename):
    dataset = load_data(datset_filename)
    labels = load_class(class_filename)
    p_feature_data,n_feature_data = rank_p_value(dataset,labels)
    #将样本的顺序打乱  防止在交叉验证的时候出错
    return p_feature_data,n_feature_data,labels


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
    k = 5
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
def single(datset_filename,class_filename,feature_range,seed_number):
    estimator_list = [0,1,2,3,4]
    p_feature_data,n_feature_data,labels = prepare(datset_filename,class_filename)
    
    max_estimator_aac = 0
    for estimator in estimator_list:
        estimator_aac = get_aac(select_estimator(estimator),p_feature_data.iloc[:,:feature_range],n_feature_data.iloc[:,:feature_range],labels,seed_number)
        if estimator_aac > max_estimator_aac:
            max_estimator_aac = estimator_aac   #记录对于 k 个 特征 用四个estimator 得到的最大值

    return max_estimator_aac


#得到特征子集的其实位置和特征子集的个数
def get_ranked_subfeature():
    with open("output.txt","r") as f:
        ranked_subfeature = []
        for line in f.readlines():
            ranked_subfeature.append(int(line.split(", ")[1]))
    return ranked_subfeature  


def all_dataset():
    dataset_list = os.listdir('dataset/data')
    label_list = os.listdir('dataset/class')

    try:
        dataset_list.remove('.DS_Store')
        label_list.remove('.DS_Store')
    except:
        pass

    ranked_subfeature = get_ranked_subfeature()  #['1', '1', '7', '3', '3', '8', '2', '0', '6', '6', '9', '6', '6', '4', '2', '1', '3', '9', '4']

    all_seed_output = []
    for seed_number in range(20): 
        print(seed_number)
        index = 0
        output_list = []
        for dataset_filename,label_filename in zip(dataset_list,label_list):
            acc = single(dataset_filename,label_filename,ranked_subfeature[index],seed_number)
            print(dataset_filename,acc)
            index += 1
            output_list.append(acc)
        all_seed_output.append(output_list)
    
    print(np.array(all_seed_output).mean(0))  
    with open("wilcon_out.pkl","wb") as f:
        pickle.dump(np.array(all_seed_output).mean(0),f)
              


if __name__ == '__main__':
    all_dataset()


    
    
    

     