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
- Version : 2.0.0

Description
    RIFS
    检验17个数据集
    ultimate
'''


import numpy as np
import pandas as pd
import os
import pickle
import random
import multiprocessing
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
    full_path_name = os.path.join("dataset","data",filename)
    dataset = pd.read_csv(full_path_name,index_col=0)
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
    full_path_name = os.path.join("dataset","class",filename)
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
    #print(dataset)  //根据 p值的排序

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
        estimator = DecisionTreeClassifier()
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
        

#生成重启的位置
def random_num_generator(num_of_feature,seed_number, percent):
    random.seed(seed_number)
    result = random.sample(list(range(num_of_feature)),int(num_of_feature * percent -1))   # 重启的组数为所有特征的一半
    result.append(0)   #保证0在其中
    return result


#对每一个数据集进行运算
def single(dataset_filename,label_filename, seed = 0, percent = 0.5, stop = 4):
#------------参数接口---------------    
    seed_number = seed
    skf = StratifiedKFold(n_splits = 10)
    estimator_list = [0,1,2,3,4]
#----------------------------------    

    start = time.time()
    print("dealing the {}".format(dataset_filename))


    dataset,labels = prepare(dataset_filename,label_filename)
    loc_of_first_feature = random_num_generator(dataset.shape[1], seed_number, percent) # 重启的位置

    max_loc_aac = 0
    max_aac_list = []
    feature_range = dataset.shape[1]

    if not os.path.exists("{}".format(seed)):
        os.mkdir("{}".format(seed))

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

            infor_file = open("{}/{}_result.txt".format(seed_number,dataset_filename.split(".")[0]),"a")
            infor_file.write(">: {}\n".format(max_aac_list))
            infor_file.close()
            

        elif max_k_aac == max_loc_aac:
            max_aac_list.append((loc,num,max_loc_aac,best_estimator))
            print("=: {}\n".format(max_aac_list))
            
            infor_file = open("{}/{}_result.txt".format(seed_number,dataset_filename.split(".")[0]),"a")
            infor_file.write("=: {}\n".format(max_aac_list))
            infor_file.close()
    
    end = time.time()            
    infor_file = open("{}/{}_result.txt".format(seed_number,dataset_filename.split(".")[0]),"a")
    infor_file.write("using time: {}".format(end-start))  
    infor_file.close() 

    return max_aac_list         


#对17个数据集进行一次运行
def all_dataset():
    dataset_list = os.listdir('dataset/data')
    label_list = os.listdir('dataset/class')
    try:
        dataset_list.remove('.DS_Store')
        label_list.remove('.DS_Store')
    except:
        pass

    seed_list = [17,18]
    for seed in seed_list:
        print(seed)
        for dataset_filename,labels_filename in zip(sorted(dataset_list),sorted(label_list)):
            single(dataset_filename,labels_filename,seed = seed)
            

if __name__ == '__main__':
    all_dataset()
    
      

    
    
    

     
