#!/usr/bin/env python3

#info
#-name   : zhangruochi
#-email  : zrc720@gmail.com


import numpy as np
import pandas as pd
import os
import pickle
import random
import time
from functools import partial
import re
from operator import itemgetter
from collections import defaultdict
from random import shuffle

from scipy.stats import ttest_ind_from_stats
from sklearn.model_selection import StratifiedKFold
from sklearn.svm import SVC
from sklearn.naive_bayes import GaussianNB
from sklearn.neighbors import KNeighborsClassifier
from sklearn.tree import DecisionTreeClassifier
from sklearn.linear_model import LogisticRegression
from sklearn.ensemble import RandomForestClassifier
from sklearn.linear_model import LinearRegression
from sklearn.multiclass import OneVsOneClassifier

from scipy.stats import mannwhitneyu
from scipy import vectorize
from prepare import prepare_dataset_labels
from prepare import load_dataset
import copy



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
 

def prepare(dataset_filename,clinical_filename,criterion):
    dataset,labels = prepare_dataset_labels(dataset_filename,clinical_filename)
    raw_dataset = copy.deepcopy(dataset)

    name_index_dic = get_name_index(dataset)

    dataset.columns = list(range(dataset.shape[1]))
    dataset.index = list(range(dataset.shape[0]))
    dataset = rank_importance_value(dataset,labels)

    return raw_dataset,dataset,labels,name_index_dic



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


#四分类的准确性   
def four_class_acc(dataset,labels,estimator_list,skf):
    max_estimator_aac = 0
    for estimator in estimator_list:
        #estimator_aac = get_acc(OneVsOneClassifier(select_estimator(estimator)),dataset,labels,skf)
        estimator_aac = get_acc(select_estimator(estimator),dataset,labels,skf)
        #print("the acc for {}: {}".format(estimator,estimator_aac))

        if estimator_aac > max_estimator_aac:
            max_estimator_aac = estimator_aac   #记录对于 k 个 特征 用五个个estimator 得到的最大值
    #print("-"*20)        
    print("the macc is: {}".format(max_estimator_aac))     
    return max_estimator_aac 


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
        pattern = re.compile("\d+, \d+, 0\.\d+")
        matches = re.findall(pattern,content)
        candidate_features = processed_matches(matches) 

    return candidate_features

#删除重复特征
def delete_feature(union_feature):
    result = []
    for feature in union_feature:
        if not feature in result:
            result.append(feature)
    return result        

#得到特征并集
def generate_union_set(candidate_features,percent = 1):
    #print(candidate_features)
    union_feature = []
    for candidate in candidate_features:
        tmp = []
        for i in range(candidate[1]):
            tmp.append(candidate[0] + i)
        union_feature.extend(tmp)

    result = delete_feature(union_feature)    
    #print("\nget the union feature: " + str(result))
    result = result[:int(len(result) * percent )]
    return result


#循环删除时使用的 acc
def recursive_acc(dataset,labels,feature_list):
    max_estimator_aac = 0
    estimator_list = [0,1,2,3,4]
    skf = StratifiedKFold(n_splits = 10)
    
    for estimator in estimator_list:
        estimator_aac = get_acc(select_estimator(estimator),dataset[feature_list],labels,skf)
        if estimator_aac > max_estimator_aac:
            max_estimator_aac = estimator_aac   #记录对于 k 个 特征 用五个个estimator 得到的最大值
    #print("-"*20)        
    #print("the macc is: {}".format(max_estimator_aac))     
    return max_estimator_aac 



#循环删除
def recursive_elimination(datasets_dict,labels_dict,feature_list,acc_list):
    min_acc = min(acc_list)
    print("initial: {}".format(min_acc))
    eliminate_feature = ""

    while True:

        print("\ncurrent num of feature are: " + str(len(feature_list)))        
        current_acc = 0  
               
        for first in feature_list:

            tmp_list = copy.deepcopy(feature_list)
            tmp_list.remove( first)

            worst = 1
            #删除一个特征后，求出四个数据集中准确率的最小值
            for key,dataset in datasets_dict.items():
                macc = recursive_acc(dataset,labels_dict[key],tmp_list)
                if macc < worst:
                    worst = macc
        
            #任意删除一个特征后，求出删除后四分类平均准确率最大的值      
            if worst > current_acc:
                current_acc = worst
                eliminate_feature = first
                print(current_acc,eliminate_feature)
                

        #如果最低的四分类准确率降低了，则没有特征可以删除了           
        if current_acc < min_acc:
            break    
        else:
            min_acc = current_acc
            feature_list.remove(eliminate_feature)
            print("eliminate feature:  {}, the current acc is {}".format(str(eliminate_feature),str(min_acc)))            

    print("\nthe final length of feature set is: "+ str(len(feature_list))) 
    print("the final feature are: " + str(feature_list))       
    return feature_list


def main():
    percent = 1
    estimator_list = [0,1,2,3,4]
    seed_number = 7
    skf = StratifiedKFold(n_splits = 10)

    dataset_filename_list = [   "COAD/matrix_data_coad.tsv",
                                "BRAC/matrix_data_brac.tsv",
                                "LUSC/matrix_data_lusc.tsv",
                                "KIRC/matrix_data_kirc.tsv",
                                "LUAD/matrix_data_luad.tsv",
                            ]

    clinical_filename_list = [  "COAD/clinical_COAD.json",
                                "BRAC/clinical_BRAC.json",
                                "LUSC/clinical_LUSC.json",
                                "KIRC/clinical_KIRC.json",
                                "LUAD/clinical_LUAD.json",
                            ]
    """
    disease_features = set()   
    datasets_dict = {}
    labels_dict = {}                

    index = 0

    for dataset_filename,clinical_filename in zip(dataset_filename_list,clinical_filename_list):                        
        
        for file in os.listdir("result"):
            if not file.endswith(".txt"):
                continue

            names = file.strip(".txt").split("_")
            disease_name = names[1]
            criterion = eval(names[2])
            
            if disease_name in dataset_filename:
                print(disease_name,dataset_filename,criterion)

                candidate_features = process_result(os.path.join("result",file))
                all_features = generate_union_set(candidate_features,percent = percent)
                raw_dataset,dataset,labels,name_index_dic = prepare(dataset_filename,clinical_filename,criterion = criterion) 
                
                datasets_dict[disease_name] = raw_dataset.T
                labels_dict[disease_name] = np.array(labels)    

                #得到 dataset 的 column name，  根据排名的 loc 找到对应的 column name，然后再找到实际的 name
                column_index = dataset.columns.tolist()  
                
                feature_names = get_name(name_index_dic, column_index, all_features)
                print("features num: {}".format(len(feature_names)))
                
                if index == 0:
                    disease_features = disease_features.union(set(feature_names))
                else:
                    disease_features = disease_features.intersection(set(feature_names))     
                
                index += 1
                print("union: {}\n".format(len(disease_features)))


    features = sorted(list(disease_features))
    with open("cache.pkl","wb") as f:
        pickle.dump([features,datasets_dict,labels_dict],f)
    """
     


    with open("cache.pkl","rb") as f:
        features,datasets_dict,labels_dict  = pickle.load(f)
        features = (features)
   
    acc_list = []
    for key,dataset in datasets_dict.items():
        print("for dataset : {},the shape is: {}".format(key,dataset.shape))
        print("")
        dataset = dataset[features]
        acc = four_class_acc(dataset,labels_dict[key],estimator_list,skf) 
        acc_list.append(acc)           
    print("\n") 


    print("starting recursive elimination.......\n")

    #test
    #features = features[:10]
    
    #进行循环删除
    features = recursive_elimination(datasets_dict,labels_dict,features,acc_list)

    with open("ultimate.pkl","wb") as f:
        pickle.dump(features,f)

    
    print("\n\n")
    for key,dataset in datasets_dict.items():
        macc = four_class_acc(dataset[features],labels_dict[key],estimator_list,skf)

        






if __name__ == '__main__':
    main()




