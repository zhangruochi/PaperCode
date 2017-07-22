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
import copy


FEATURES = {
    "LUAD": ['TGFB3', 'KIAA0513', 'LOC283514'],
    "COAD": ['FLJ22222', 'RBM3', 'BET1', 'TBXA2R', 'CXCL2', 'SLC25A15', 'C18orf37','TNFRSF10C', 'PIGL', 'MGC16385', 'ADCY2', 'HMGCL', 'RTTN', 'HS3ST5', 'HIG2','NECAP2', 'AQP1', 'NHN1', 'XPNPEP1', 'DCDC1', 'LMAN1', 'SLC27A6', 'ATP6V1F','TBX4', 'FAM118A', 'MYH13', 'LTC4S', 'NEO1', 'BCL2A1', 'GATA4', 'PEX19', 'KCNMB3','EDEM1', 'KIR2DL4', 'PCM1'],
    "LUSC": ['PCDHGB6', 'BCMO1', 'PIGC', 'C9orf105', 'EFCAB2', 'HSD17B7', 'SLC39A4', 'SYPL2', 'TMEM141', 'SHOX2', 'MGST3', 'MYD88', 'DPF3', 'OR51D1', 'TMEM170', 'GOSR2', 'C1orf156', 'DMC1', 'DLL3', 'APOL6', 'C1D', 'GPR180', 'KRT77', 'MGC13057', 'FAM116A', 'ZNF608', 'CCDC67', 'NDUFA8', 'MRPS14', 'RAN', 'ACP2', 'CGA', 'PLXNB2', 'DEFB4', 'C14orf140', 'TOMM40L', 'EBAG9', 'SMUG1', 'KLK2', 'SLC35D3', 'LOC90826', 'PINK1', 'TMEM1', 'PCDHGC3', 'PRDX4', 'SKI', 'ZSCAN12', 'NHS', 'C14orf142', 'ERF', 'FBXL10', 'HINT2', 'SLC1A6', 'WRB', 'SULT6B1', 'USP8', 'URG4', 'GNAO1', 'STXBP2', 'CDC2L2', 'ANAPC10', 'POU4F3', 'SC5DL', 'UHMK1', 'SNAPAP'],
    "KIRC": ['CLSPN', 'BLNK', 'ATP10A', 'PTGIR', 'CYP39A1', 'COBLL1', 'FLJ25006', 'GPBAR1', 'HIST1H2BA', 'IFT140', 'LILRB4'],    
    "BRAC": ['GYPA', 'RNF19A', 'FGG', 'FAM122C', 'HSPB1', 'SSH1', 'OR2W3', 'LDLRAD3', 'C1RL', 'GUK1', 'METTL1', 'HELB', 'TYW3', 'TBXA2R', 'FLJ20160', 'RNF5', 'MTF1', 'SLC25A15', 'TTC32', 'HIPK3', 'DDX20', 'C9orf39', 'PKP2', 'MMP15', 'TMEM150', 'DNAJC5', 'TIFA', 'GRHL2', 'SPDEF', 'PMAIP1', 'EIF2C4', 'LTBP2', 'KLHDC8B', 'FLJ25439', 'PMS1', 'C10orf63', 'FNTB', 'ZNF546', 'CORO2B', 'BDH2', 'EIF3M', 'GATA4', 'PARP3', 'OR51B6', 'GTF2B', 'CTTNBP2NL', 'GATA1', 'DPEP1', 'FLJ90757', 'IBSP', 'SCGB1D1', 'MPN2', 'PAGE5', 'VAC14', 'RSL1D1', 'CNOT6L', 'ZNF558', 'PRKRA', 'LPP', 'ZNF493', 'GPR82', 'LMOD1', 'IL1F6', 'CDK5RAP1', 'NOC3L']
}



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



#处理 matches( 按照准确率排序)
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
    print("length: " + str(len(union_set)))

    return union_set



#采用 K-Fold 交叉验证 得到 aac 
def get_aac(estimator,X,y,seed_number,skf):
    scores = []
    for train_index,test_index in skf.split(X,y):
        X_train, X_test = X.ix[train_index], X.ix[test_index]
        y_train, y_test = y[train_index], y[test_index]
        estimator.fit(X_train,y_train)
        scores.append(estimator.score(X_test,y_test))
        
    return np.mean(scores)   


def recursive_elimination(dataset,labels,feature_list):

    min_acc = get_macc(dataset,labels,list(feature_list))
    print("for the union set, the acc is : "+str(min_acc))

    eliminate_feature = []

    while True:
        
        current_acc = 0
        feature_list = feature_list - set(eliminate_feature)
        print("\ncurrent num of feature are: " + str(len(feature_list)))
        origin = copy.copy(feature_list)
    
        for item in feature_list:
            tmp_list = feature_list.remove(first)
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

    print("\nthe final length of feature set is: "+ str(len(feature_list))) 
    print("the final feature are: " + str(feature_list))       
    return feature_list



#对每一个数据集进行运算
def single(dataset_filename_list,clinical_filename_list, seed = 7, criterion = [[1,2],[3,4]],max_union_set_list =  [200,300,400,500,600,700,800,900,1000]):
#------------参数接口---------------    
    seed_number = seed
    skf = StratifiedKFold(n_splits = 3)
    estimator_list = [0,1,2,3,4]
#-----------------------------------   

    union_list = []
    for item in FEATURES.keys():
        union_list.extend(FEATURES[item]) 
    union_set =   list(set(union_list))
    print("the union set length is: " +str(len(union_set)) + "\n") 


    #此时的 dataset 已经是给特征排名后的dataset
    for dataset_filename,clinical_filename in zip(dataset_filename_list,clinical_filename_list):
        dataset,labels = prepare_dataset_labels(dataset_filename,clinical_filename)
        dataset = dataset.T
        disease_name = dataset_filename[-8:-4].upper()

        print("for dataset : {}".format(disease_name))
        max_estimator_aac = 0

        for estimator in estimator_list:
            estimator_aac = get_aac(select_estimator(estimator),dataset[FEATURES[disease_name]],labels,seed_number,skf)
            #print("the acc for {}: {}".format(estimator,estimator_aac))       
            if estimator_aac > max_estimator_aac:
                max_estimator_aac = estimator_aac   #记录对于 k 个 特征 用五个个estimator 得到的最大值       
        print("the macc is: {}".format(max_estimator_aac))
        print("-"*30) 
    print("\n")

    print("\nfor the union features......\n")

    for dataset_filename,clinical_filename in zip(dataset_filename_list,clinical_filename_list):
        dataset,labels = prepare_dataset_labels(dataset_filename,clinical_filename)
        dataset = dataset.T
        disease_name = dataset_filename[-8:-4].upper()

        print("for dataset : {}".format(disease_name))
        max_estimator_aac = 0

        for estimator in estimator_list:
            estimator_aac = get_aac(select_estimator(estimator),dataset[union_set],labels,seed_number,skf)
            #print("the acc for {}: {}".format(estimator,estimator_aac))       
            if estimator_aac > max_estimator_aac:
                max_estimator_aac = estimator_aac   #记录对于 k 个 特征 用五个个estimator 得到的最大值       
        print("the macc is: {}".format(max_estimator_aac))
        print("-"*30) 
    print("\n")

    
      

                
        
"""
        #得到 dataset 的 column name，  根据排名的 loc 找到对应的 column name，然后再找到实际的 name
        column_index = dataset.columns.tolist()    
        feature_names = get_name(name_index_dic, column_index, list(union_set))
        print("\nthe final feature name: "+ str(feature_names))

        with open(feature_filename,"w") as f:
            f.write(str(feature_names))
        
        return feature_names
"""


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

    feature_names = single(dataset_filename_list,clinical_filename_list, seed = 7, criterion = [[1,2],[3,4]], max_union_set_list = [200,250,300,350,400,450,500,550,600,650,700,750,800,850,900,950,1000])

