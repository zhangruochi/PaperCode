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
- date   : "2017.5.11"
- Version : 1.0.0

Description
    RIFS2

'''


import numpy as np
import pandas as pd
import os
import pickle
import random
import time
from functools import partial
import re

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
    #print(dataset.shape)   #(7377, 36)
    #print(dataset.head())
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

    with open("p_rank.pkl","wb") as f:
        pickle.dump(sort_index,f)

    dataset = dataset.reindex(sort_index)
    return dataset.T


def prepare(datset_filename,class_filename):
    dataset = load_data(datset_filename)
    labels = load_class(class_filename)
    dataset = rank_t_value(dataset,labels)
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
def get_acc(estimator,X,y,skf):
    scores = []
    for train_index,test_index in skf.split(X,y):
        X_train, X_test = X.ix[train_index], X.ix[test_index]
        y_train, y_test = y[train_index], y[test_index]
        estimator.fit(X_train,y_train)
        scores.append(estimator.score(X_test,y_test))

    return np.mean(scores)    
        

#生成重启的位置
def random_num_generator(num_of_feature,seed_number, percent):
    random.seed(seed_number)
    result = random.sample(list(range(num_of_feature)),int(num_of_feature * percent -1))   # 重启的组数为所有特征的一半
    result.append(0)   #保证0在其中
    return result



#得到特定 threshold 过滤后的特征组合  [(442, 3), (2049, 3), (79, 6), (59, 9), (16, 6)]
def process_result(threshold = 0.7): 
    with open("result.txt","r") as f:
        content = f.read()
        #print(content)
        pattern = re.compile("\d+, \d, 0\.\d+")
        matches = re.findall(pattern,content)

        condidate_features = [(int(item.split(", ")[0]),int(item.split(", ")[1])) \
            for item in matches if float(item.split(", ")[2]) > threshold ]
    
    return condidate_features


#得到特征并集
def generate_union_set(condidate_features):
    union_set = set()
    for candidate in condidate_features:
        tmp = []
        for i in range(candidate[1]):
            tmp.append(candidate[0] + i)
        union_set = union_set.union(set(tmp))
    print("get the union feature: " + str(union_set))
    return union_set 



def get_macc(dataset,labels,feature_list):
    estimator_list = [0,1,2,3,4]
    skf = StratifiedKFold(n_splits = 3)
    max_estimator_aac = -1
    for index in estimator_list:
        estimator_aac = get_acc(select_estimator(index),dataset.iloc[:,feature_list],labels,skf)
        if estimator_aac > max_estimator_aac:
            max_estimator_aac = estimator_aac   #记录对于 k 个 特征 用四个estimator 得到的最大值
            
    return max_estimator_aac


def recursive_elimination(dataset,labels,feature_list):

    min_acc = get_macc(dataset,labels,list(feature_list))
    eliminate_feature = []

    while True:
        
        current_acc = 0
        feature_list = feature_list - set(eliminate_feature)
        print("current num of feature are: " + str(len(feature_list)))
    
        for first in feature_list:
            for second in feature_list:
                tmp_list = feature_list - set([first,second])
                macc = get_macc(dataset,labels,list(tmp_list))
                print(macc,first,second)
                if macc > current_acc:
                    current_acc = macc
                    eliminate_feature = [first,second]

        if current_acc < min_acc:
            break    
        else:
            min_acc = current_acc
            print("eliminate feature:  {}, the current acc is {}".format(str(eliminate_feature),str(min_acc)))            

    print("the final length of feature set is: "+ str(len(feature_list))) 
    print("the final feature are: " + str(feature_list))       
    return feature_list


    



#对每一个数据集进行运算
def single(dataset_filename,label_filename, seed = 7, percent = 0.4, stop = 3):
#------------参数接口---------------    
    seed_number = seed
    skf = StratifiedKFold(n_splits = 10)
    estimator_list = [0,1,2,3,4]
#----------------------------------    

    start = time.time()
    print("dealing the {}".format(dataset_filename))

    dataset,labels = prepare(dataset_filename,label_filename)

    """
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
                estimator_aac = get_acc(select_estimator(item),X,labels,skf)
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

    """
    
    condidate_features = process_result(threshold = 0.7)
    all_features = generate_union_set(condidate_features)

    #循环删除
    result = recursive_elimination(dataset,labels,all_features)

    
        

    return 
  






        

if __name__ == '__main__':
    single("t1d.csv","t1dclass.csv")
    #condidate_features = process_result(threshold = 0.7)
    #generate_union_set(condidate_features)



    
      

    
    
    

     
