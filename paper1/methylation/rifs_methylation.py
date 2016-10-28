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
def load_data(filename):
    full_path_name = os.path.join("dataset/data",filename)
    dataset = pd.read_table(full_path_name,index_col = 0)  #(27578, 1128) ->  [27578 rows x 970 columns]
    dataset.fillna(method="bfill",axis = 0,inplace =True)
    labels,mask = processing_label(dataset)
    dataset = dataset.iloc[:,mask]
    print(dataset.shape)
    """
    with open("relation_ultimate.pkl","rb") as f:
        relation = pickle.load(f)

    result_dict = {}    
    for new_feature, raw_feature_list in relation.items():
        result_dict[new_feature] = dataset.loc[raw_feature_list,:].mean()

    dataset = pd.DataFrame(data=result_dict).T

    name_index_dic = get_name_index(dataset)
    dataset.columns = list(range(dataset.shape[1]))
    dataset = dataset.rename(index = name_index_dic)
    return dataset,labels
    """
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
    dataset,labels = load_data(datset_filename)
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
    result = random.sample(list(range(num_of_feature)),num_of_feature)   # 重启全部的位置
    return result


#对每一个数据集进行运算
def single(dataset_filename):
    seed_number = 7
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
                if count == 3:
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
    load_data("GSE27044_Matrix_Normalized_AllSampleBetaPrime.txt")
    #single("GSE27044_Matrix_Normalized_AllSampleBetaPrime.txt")

    """
                EBSC_CTL1.Avg_Beta  11299.s1.Avg_Beta  11596.s1.Avg_Beta  \
TargetID                                                               
cg00000292             0.83445            0.82689            0.90273   
cg00002426             0.81105            0.87160            0.87480   
cg00003994             0.09169            0.04863            0.05136   
cg00005847             0.16712            0.10359            0.12377   
cg00006414             0.05613            0.05347            0.04305   

            11031.p1.Avg_Beta  11077.p1.Avg_Beta  11093.p1.Avg_Beta  \
TargetID                                                              
cg00000292            0.87100            0.82592            0.84602   
cg00002426            0.88310            0.91067            0.83902   
cg00003994            0.03462            0.03135            0.04831   
cg00005847            0.12953            0.11839            0.14722   
cg00006414            0.05901            0.05398            0.02422   

            11094.s1.Avg_Beta  11557.s1.1.Avg_Beta  11077.s1.Avg_Beta  \
TargetID                                                                
cg00000292            0.82479              0.86973            0.88127   
cg00002426            0.89546              0.89960            0.85116   
cg00003994            0.03554              0.06368            0.05727   
cg00005847            0.10715              0.11490            0.18365   
cg00006414            0.05182              0.02531            0.07893   

            11597.s1.Avg_Beta        ...          13340.p1.Avg_Beta  \
TargetID                             ...                              
cg00000292            0.84240        ...                    0.85840   
cg00002426            0.83261        ...                    0.78484   
cg00003994            0.07004        ...                    0.06454   
cg00005847            0.08533        ...                    0.22056   
cg00006414            0.02208        ...                    0.14369   

            13333.p1.Avg_Beta  13333.s1.Avg_Beta  13341.s1.Avg_Beta  \
TargetID                                                              
cg00000292            0.82105            0.77858            0.86424   
cg00002426            0.87201            0.80646            0.83743   
cg00003994            0.09299            0.14999            0.08606   
cg00005847            0.19703            0.25209            0.21091   
cg00006414            0.08543            0.14874            0.14270   

            13381.s2.Avg_Beta  HG_CTL88.Avg_Beta  13358.s1.Avg_Beta  \
TargetID                                                              
cg00000292            0.87527            0.86466            0.86232   
cg00002426            0.82739            0.84684            0.87421   
cg00003994            0.09698            0.16562            0.10124   
cg00005847            0.19630            0.23495            0.18734   
cg00006414            0.12818            0.14033            0.13212   

            13381.p1.Avg_Beta  13341.p1.Avg_Beta  13358.p1.Avg_Beta  
TargetID                                                             
cg00000292            0.82824            0.81397            0.88834  
cg00002426            0.85569            0.80672            0.81903  
cg00003994            0.10649            0.12787            0.12966  
cg00005847            0.23563            0.30499            0.31832  
cg00006414            0.16127            0.21358            0.17410  
"""
    

    
    
    

     
