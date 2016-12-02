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
- date   : "2016.10.22"
- Version : 2.0.0

Description
    RIFS methylation
'''


import numpy as np
import pandas as pd
import os
import pickle
import random
import time
import multiprocessing
from functools import partial


from scipy.stats import ttest_ind_from_stats

from sklearn.cross_validation import KFold
from sklearn.svm import SVC
from sklearn.naive_bayes import GaussianNB
from sklearn.neighbors import KNeighborsClassifier
from sklearn.tree import DecisionTreeClassifier
from sklearn.linear_model import LogisticRegression



#加载数据集
def load_data():
    with open("Gastric_polyp_Sub.pkl","rb") as f:
        n_feature  = pickle.load(f)

    with open("Normal_Sub.pkl","rb") as f:
        p_feature  = pickle.load(f)    

    dataset = np.vstack((n_feature,p_feature))
    print("dataset shape:",dataset.shape)
    #生成类标
    labels = []
    for i in range(n_feature.shape[0]):
        labels.append(0)
    for i in range(p_feature.shape[0]):
        labels.append(1)

    labels = np.array(labels)    
    dataset = pd.DataFrame(data = dataset)

    return dataset,labels
    
def processing_label(dataset):
    labels = []
    raw_labels = dataset.columns.tolist()
    split_raw_labels = [label.split(".")[1] for label in raw_labels]
    mask = [True if label in ["s1","p1"] else False for label in split_raw_labels]
    for label in [label for label in split_raw_labels if label in ["s1","p1"]]:
        if label == "p1":
            labels.append(1)
        else:
            labels.append(0)
            
    return np.array(labels),mask



#创造特征索引和特征名字对应的字典 
def get_name_index(dataset):
    name_index_dic = {}
    index = 0
    for name in dataset.index:
        name_index_dic[name] = index
        index += 1 
    return name_index_dic 


""" 
# 根据方差进行过滤
def variance_filter(dataset, per=0.6):
    feature_name_index = {}
    if not os.path.exists("feature_name_index.txt"):
        with open("feature_name_index.pkl", "wb") as f:
            for index, name in enumerate(dataset.columns.tolist()):
                feature_name_index[name] = index
            pickle.dump(feature_name_index, f)

    else:
        with open("feature_name_index.pkl", "rb") as f:
            feature_name_index = pickle.load(f)

    dataset_var = dataset.apply(np.var, axis=0).sort_values()
    seleted_columns = dataset_var.iloc[0:int(dataset_var.shape[0] * per)].index
    filtered_dataset = dataset.loc[:, seleted_columns]

    return filtered_dataset, feature_name_index   
"""


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
def rank_t_value(dataset,labels):
    p_feature_data,n_feature_data,p_value = t_test(dataset,labels)
    sort_index = p_value.sort_values(ascending=True).index

    with open("p_rank.pkl","wb") as f:
        pickle.dump(sort_index,f)

    p_feature_data = p_feature_data.reindex(sort_index)
    #print(p_feature_data)  //根据 p值的排序
    n_feature_data = n_feature_data.reindex(sort_index)

    return p_feature_data.T,n_feature_data.T


def prepare(datset_filename):
    dataset,labels = load_data()
    p_feature_data,n_feature_data = rank_t_value(dataset,labels)
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

# K-Fold  生成器
def k_fold(y,k):

    kf = KFold(len(y),n_folds = k)
    for train_index,test_index in kf:
        yield train_index,test_index
        

#生成重启的位置
def random_num_generator(num_of_feature,seed_number):
    random.seed(seed_number)
    result = random.sample(list(range(num_of_feature)),int(num_of_feature*0.4 -1))   # 重启全部的位置
    result.append(1)
    return result


#对每一个数据集进行运算
def single(dataset_filename):
    seed_number = 0
    start = time.time()

    print("dealing the {}".format(dataset_filename))
    p_feature_data,n_feature_data,labels = prepare(dataset_filename)
    loc_of_first_feature = random_num_generator(p_feature_data.shape[1],seed_number) # 重启的位置

    max_loc_aac = 0
    max_aac_list = []
    estimator_list = [0,1,2,3,4]
    feature_range = p_feature_data.shape[1]


    if not os.path.exists("{}".format(seed_number)):
        os.mkdir("{}".format(seed_number))

    for loc in loc_of_first_feature:
        num = 0
        max_k_aac = 0 
        count = 0  #记录相等的次数
        best_estimator = -1   
        
        for k in range(feature_range - loc):  # 从 loc位置 开始选取k个特征
            max_estimator_aac = 0
            locs = [i for i in range(loc,loc+k+1)]

            p_data = p_feature_data.iloc[:,locs]
            n_data = n_feature_data.iloc[:,locs]

            for item in estimator_list:
                estimator_aac = get_aac(select_estimator(item),p_data,n_data,labels,seed_number)
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
                if count == 5:
                    break
   
        if max_k_aac > max_loc_aac:
            max_loc_aac = max_k_aac
            max_aac_list = []
            max_aac_list.append((loc,num,max_loc_aac,best_estimator))
            print(">: {}\n".format(max_aac_list))
            
            with open("{}/{}_outpot.txt".format(seed_number,dataset_filename.split(".")[0]),"a") as infor_file:
                infor_file.write(">: {}\n".format(max_aac_list))
                infor_file.close()
            

        elif max_k_aac == max_loc_aac:
            max_aac_list.append((loc,num,max_loc_aac,best_estimator))
            print("=: {}\n".format(max_aac_list))
            with open("{}/{}_outpot.txt".format(seed_number,dataset_filename.split(".")[0]),"a") as infor_file:
                infor_file.write("=: {}\n".format(max_aac_list))
                infor_file.close()
    
    end = time.time()            
    with open("{}/{}_outpot.txt".format(seed_number,dataset_filename.split(".")[0]),"a") as infor_file:
        infor_file.write("using time: {}".format(end-start))  
        infor_file.close()              
    return max_aac_list         

        

if __name__ == '__main__':
    pass

  