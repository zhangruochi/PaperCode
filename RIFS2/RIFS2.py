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
from operator import itemgetter

from scipy.stats import ttest_ind_from_stats
from sklearn.model_selection import StratifiedKFold
from sklearn.svm import SVC
from sklearn.naive_bayes import GaussianNB
from sklearn.neighbors import KNeighborsClassifier
from sklearn.tree import DecisionTreeClassifier
from sklearn.linear_model import LogisticRegression
from sklearn.ensemble import RandomForestClassifier
from sklearn.linear_model import LinearRegression

from scipy.stats import mannwhitneyu
from scipy import vectorize
from prepare import prepare_dataset_labels



#创造特征索引和特征名字对应的字典 
def get_name_index(dataset):
    name_index_dic = {}
    index = 0
    for name in dataset.index:
        name_index_dic[index] = name
        index += 1    
    return name_index_dic 


#根据排名得到特征的名字
def get_name(name_index_dic, column_index, feature_list):
    result = []
    for index in feature_list:
        result.append(name_index_dic[column_index[index]])
    return result  


#根据特征排序
def resort_features(feature_importances,dataset):
    feature_dict = dict()
    for index,feature in enumerate(feature_importances):
        feature_dict[index] = feature

    feature_dict = sorted(feature_dict.items(),key =  itemgetter(1))
    feature_index = [tuple_[0] for tuple_ in feature_dict]


    dataset = dataset.reindex(feature_index).T

    return dataset
    

# 根据 U 检验排序
def rank_importance_value(dataset,labels):
    p_feature_data = dataset.loc[:,labels == 1]  #得到正类数据集
    n_feature_data = dataset.loc[:,labels == 0]  #得到负类数据集

    feature_importances = []
    for index in range(dataset.shape[0]):
        statistic,p = mannwhitneyu(p_feature_data.iloc[index,:],n_feature_data.iloc[index,:])
        feature_importances.append(p)

    dataset = resort_features(feature_importances,dataset)

    return dataset
 

def prepare(datset_filename,clinical_filename,criterion):
    dataset,labels = prepare_dataset_labels(dataset_filename,clinical_filename)

    name_index_dic = get_name_index(dataset)

    dataset.columns = list(range(dataset.shape[1]))
    dataset.index = list(range(dataset.shape[0]))
    dataset = rank_importance_value(dataset,labels)

    return dataset,labels,name_index_dic



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



#处理 matches
def processed_matches(matches):
    match_list = []
    result = []

    for item in matches:
        match_list.append(list(map(float,item.split(", "))))

    sorted_match_list = sorted(match_list,key = itemgetter(2),reverse = True) 
    result = [(int(match[0]),int(match[1])) for match in sorted_match_list]

    return result    



#得到特定 threshold 过滤后的特征组合  [(442, 3), (2049, 3), (79, 6), (59, 9), (16, 6)]
def process_result(result_filename): 
    with open(result_filename,"r") as f:
        content = f.read()
        #print(content)
        pattern = re.compile("\d+, \d, 0\.\d+")
        matches = re.findall(pattern,content)
        candidate_features = processed_matches(matches) 

    return candidate_features


#得到特征并集
def generate_union_set(candidate_features,max_union_set):
    union_set = set()
    for candidate in candidate_features:
        tmp = []
        for i in range(candidate[1]):
            tmp.append(candidate[0] + i)
        union_set = union_set.union(set(tmp))
        if len(union_set) >= max_union_set:
            break

    all_features = list(union_set)
    all_features.reverse()

    print("\nget the union feature: " + str(all_features))

    return set(all_features)



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
        print("\ncurrent num of feature are: " + str(len(feature_list)))
    
        for first in feature_list:
            for second in feature_list:
                tmp_list = feature_list - set([first,second])
                macc = get_macc(dataset,labels,list(tmp_list))
                #print(macc,first,second)
                if macc > current_acc:
                    current_acc = macc
                    eliminate_feature = [first,second]

        if current_acc < min_acc:
            break    
        else:
            min_acc = current_acc
            print("eliminate feature:  {}, the current acc is {}".format(str(eliminate_feature),str(min_acc)))            

    print("\nthe final length of feature set is: "+ str(len(feature_list))) 
    print("the final feature are: " + str(feature_list))       
    return feature_list


    



#对每一个数据集进行运算
def single(dataset_filename,clinical_filename, seed = 7, threshold = 0.8, percent = 0.5, stop = 4, criterion = [[1,2],[3,4]],max_union_set = 250):
#------------参数接口---------------    

    seed_number = seed
    skf = StratifiedKFold(n_splits = 10)
    estimator_list = [0,1,2,3,4]
#-----------------------------------    

    start = time.time()
    print("dealing the {}".format(dataset_filename))
    result_filename = "result_{}.txt".format(dataset_filename[-8:-4])
    feature_filename = "feature_{}.txt".format(dataset_filename[-8:-4])


    #此时的 dataset 已经是给特征排名后的dataset
    dataset,labels,name_index_dic = prepare(dataset_filename,clinical_filename,criterion)  

    loc_of_first_feature = random_num_generator(dataset.shape[1], seed_number, percent) # 重启的位置

    
   #------------------------RIFS1----------------------------------- 
    max_loc_aac = 0
    max_acc_list = []
    feature_range = dataset.shape[1]


    for loc in loc_of_first_feature:  #该 loc 是 u-test 排名后的 loc
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
   
        if max_k_aac > threshold:
            max_acc_list.append((loc,num,max_k_aac,best_estimator))
            print(max_acc_list)
            print("")
            
    with open(result_filename,"w") as infor_file:
        infor_file.write("=: {}\n".format(max_acc_list))
    
    end = time.time()            
    with open(result_filename,"a") as infor_file:
        infor_file.write("using time: {}".format(end-start))  
    

#-----------------------RIFS2------------------------------
   
    candidate_features = process_result(result_filename)
    all_features = generate_union_set(candidate_features,max_union_set)

    #循环删除
    feature_list = recursive_elimination(dataset,labels,all_features)

    #得到 dataset 的 column name，  根据排名的 loc 找到对应的 column name，然后再找到实际的 name
    column_index = dataset.columns.tolist()    

    #得到最终特征的名字
    feature_names = get_name(name_index_dic, column_index, feature_list)
    print("\nthe final feature name: "+ str(feature_names))

    with open(feature_filename,"w") as f:
        f.write(str(feature_names))
    
    return feature_names
  






        

if __name__ == '__main__':
    """
    输入参数是:
        matrix_data     文件
        clinical        数据文件
        seed            随机种子
        threshold       RIFS1 所要保存特征组合的最低准确率
        percent         随机重启的组数
        stop            停止条件，向后搜索的个数
        criterion       分类标准，如 [[1],[2,3]] 表示stage i为一类， stage ii，iii 为第二类
                                    [[1,2],[3,4]] 表示stage i,ii为一类， stage iii,iv 为第二类

        max_union_set   特征并集的最大规模(也就是需要做循环删除的特征量)                           
    """


    dataset_filename = "KIRC/matrix_data_kirc.tsv"
    clinical_filename = "KIRC/clinical_KIRC.json"

    feature_names = single(dataset_filename,clinical_filename, seed = 7, threshold = 0.8, \
        percent = 0.5, stop = 4, criterion = [[1,2],[3,4]], max_union_set = 200)
    

    
      

    
    
    

     
