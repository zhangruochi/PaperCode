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
- date   : "2016.10.12"
- Version : 2.0.0

Description
    RIFS
    multiprocessing
'''


import numpy as np
import pandas as pd
import os
import pickle
import random
import time
import multiprocessing
from functools import partial
import re

from scipy.stats import ttest_ind_from_stats

from sklearn.cross_validation import KFold
from sklearn.svm import SVC
from sklearn.naive_bayes import GaussianNB
from sklearn.neighbors import KNeighborsClassifier
from sklearn.tree import DecisionTreeClassifier
from sklearn.grid_search import GridSearchCV
from sklearn.linear_model import LogisticRegression



#加载数据集
def load_data(filename):
    full_path_name = os.path.join("dataset/data",filename)
    dataset = pd.read_csv(full_path_name,index_col=0)
    name_index_dic = get_name_index(dataset)
    dataset.columns = list(range(dataset.shape[1]))
    dataset = dataset.rename(index = name_index_dic)
    return dataset

#加载标签
def load_class(filename):
    full_path_name = os.path.join("dataset/class",filename)
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


#创造特征索引和特征名字对应的字典 
def get_name_index(dataset):
    name_index_dic = {}
    index = 0
    for name in dataset.index:
        name_index_dic[name] = index
        index += 1 
    return name_index_dic 


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
def save_t_value(dataset,labels):
    p_feature_data,n_feature_data,p_value = t_test(dataset,labels)
    sort_index = p_value.sort_values(ascending=True).index

    return sort_index    



#得到特征子集的其实位置和特征子集的个数
def get_ranked_subfeature():
    with open("output.txt","r") as f:
        ranked_subfeature = []
        for line in f.readlines():
            temp_list = []
            for number in line.split(", ")[0:2]:
                temp_list.append(number)
            ranked_subfeature.append(temp_list)
        
    return ranked_subfeature        



#得到实际位置和 t 检验排序后的位置对应的词典
def get_rank_dict(dataset,labels):
    rank_list = save_t_value(dataset,labels)
    rank_dict = {}
    for index,rank in enumerate(rank_list):
        rank_dict[index] = rank
    return rank_dict    
     

#得到实际 feature 的位置
def deal_output(dataset,labels,ranked_subfeature):
    rank_dict = get_rank_dict(dataset,labels)          
    feature_list = []
    start = int(ranked_subfeature[0])

    for i in range(int(ranked_subfeature[1])):
        feature_list.append(rank_dict[start+i])
    return feature_list         



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
def single(dataset,labels,feature_list,all_results,seed_number):
    estimator_list = [0,1,2,3,4]

    extracted_p_dataset = dataset.T.iloc[labels == 1,feature_list]
    extracted_n_dataset = dataset.T.iloc[labels == 0,feature_list]

    max_estimator_aac = -1
    for index in estimator_list:
        estimator_aac = get_aac(select_estimator(index),extracted_p_dataset,extracted_n_dataset,labels,seed_number)
        if estimator_aac > max_estimator_aac:
            max_estimator_aac = estimator_aac   #记录对于 k 个 特征 用四个estimator 得到的最大值
            

    all_results.append(max_estimator_aac)       
    with open("{}_rifs_results.txt".format(seed_number),"a") as f:
        f.write("{0}\n".format(max_estimator_aac))



#对17个数据集进行一次运行
def all_dataset():
    dataset_list = os.listdir('dataset/data')
    label_list = os.listdir('dataset/class')

    try:
        dataset_list.remove('.DS_Store')
        label_list.remove('.DS_Store')
    except:
        pass

    ranked_subfeature_list = get_ranked_subfeature() 
      
    all_seeds_result = []
    for seed_number in list(range(0,20)):
        index = 0
        all_results = []
        for dataset_filename,label_filename in zip(dataset_list,label_list):
            dataset = load_data(dataset_filename)
            labels = load_class(label_filename)
            feature_list = deal_output(dataset,labels,ranked_subfeature_list[index])  

            print(seed_number,dataset_filename)
            single(dataset,labels,feature_list,all_results,seed_number)
            index += 1
        all_seeds_result.append(all_results)
    matrix_result = np.array(all_seeds_result).mean(0)
    with open("20_seed_mean.pkl","wb") as f:
        pickle.dump(matrix_result,f)
        
    print(matrix_result)


def ultimate():
    matrix = np.array([[1.0, 1.0, 0.77941176470588225, 0.83991482771970583, 0.91323924731182793, 0.81666666666666676, 0.92121212121212126, 0.95999999999999996, 0.97222222222222221, 0.99206349206349209, 0.96969696969696972, 1.0, 1.0, 0.85561605162331122, 0.94084542908072322, 1.0, 0.84165181224004748], [1.0, 1.0, 0.72916666666666663, 0.83217189314750284, 0.91323924731182793, 0.86666666666666659, 0.88939393939393929, 0.96098765432098754, 0.97222222222222232, 1.0, 0.96897546897546893, 0.98666666666666669, 1.0, 0.86146400483968544, 0.93133859604447844, 0.97619047619047628, 0.84135472370766484], [1.0, 1.0, 0.80269607843137258, 0.81610530391018188, 0.91563620071684593, 0.8666666666666667, 0.91969696969696957, 0.95999999999999996, 0.96527777777777779, 0.99206349206349209, 0.98412698412698418, 0.98611111111111116, 1.0, 0.84956644484775146, 0.93133859604447844, 0.97619047619047628, 0.84194890077243023], [1.0, 1.0, 0.78737745098039225, 0.84765776229190859, 0.91323924731182793, 0.80000000000000016, 0.90454545454545465, 0.96197530864197534, 0.97222222222222221, 1.0, 0.95382395382395391, 0.98550724637681153, 1.0, 0.83222423875781404, 0.94142262965792378, 1.0, 0.84135472370766484], [1.0, 1.0, 0.75, 0.84030197444831589, 0.92399193548387093, 0.8833333333333333, 0.90454545454545465, 0.96098765432098754, 0.96527777777777768, 0.99206349206349209, 0.95454545454545459, 1.0, 1.0, 0.86680782415809643, 0.91344537815126048, 0.97619047619047628, 0.83184789067142006], [1.0, 1.0, 0.80208333333333337, 0.84785133565621373, 0.90313620071684586, 0.84999999999999998, 0.85303030303030292, 0.97432098765432096, 0.96527777777777768, 1.0, 0.96897546897546893, 0.98666666666666669, 1.0, 0.86700947771728176, 0.93133859604447844, 0.97222222222222221, 0.8223410576351754], [1.0, 1.0, 0.74019607843137258, 0.81629887727448702, 0.93510304659498222, 0.76666666666666661, 0.91969696969696957, 0.97432098765432096, 0.97222222222222232, 1.0, 1.0, 1.0, 1.0, 0.85571687840290389, 0.93219590866649682, 1.0, 0.83095662507427226], [1.0, 1.0, 0.80085784313725483, 0.85636856368563674, 0.92535842293906823, 0.88333333333333341, 0.93787878787878787, 0.98666666666666669, 0.97222222222222221, 1.0, 1.0, 1.0, 1.0, 0.89614841701956038, 0.95126050420168073, 1.0, 0.84194890077243023], [1.0, 1.0, 0.77022058823529405, 0.82462253193960511, 0.9135752688172043, 0.8833333333333333, 0.92121212121212126, 0.98666666666666669, 0.96527777777777779, 1.0, 0.95382395382395391, 0.98611111111111116, 1.0, 0.8669086509376891, 0.93076139546727787, 0.97222222222222221, 0.84224598930481287], [1.0, 1.0, 0.7898284313725491, 0.83236546651180798, 0.89482526881720437, 0.81666666666666676, 0.91666666666666663, 0.97432098765432096, 0.97222222222222232, 1.0, 0.96897546897546893, 1.0, 1.0, 0.83817301875378103, 0.94084542908072322, 0.97619047619047628, 0.83125371360665479], [1.0, 1.0, 0.79901960784313719, 0.83972125435540068, 0.9135752688172043, 0.8833333333333333, 0.92121212121212126, 0.96197530864197534, 0.96527777777777779, 1.0, 0.96969696969696972, 0.98611111111111116, 1.0, 0.84966727162734423, 0.94115949410067057, 1.0, 0.84194890077243023], [1.0, 1.0, 0.71017156862745112, 0.83952768099109554, 0.91494175627240149, 0.83333333333333337, 0.88484848484848488, 0.97432098765432096, 0.96527777777777768, 1.0, 0.98484848484848486, 0.98666666666666669, 1.0, 0.86711030449687432, 0.92036329683388507, 0.94841269841269848, 0.84194890077243023], [1.0, 1.0, 0.7591911764705882, 0.83178474641889277, 0.90351702508960585, 0.84999999999999998, 0.90151515151515149, 0.98765432098765427, 0.97222222222222232, 1.0, 0.98484848484848486, 1.0, 1.0, 0.85561605162331122, 0.93133859604447844, 0.94841269841269848, 0.83184789067142006], [1.0, 1.0, 0.75980392156862742, 0.81571815718157181, 0.90418906810035848, 0.78333333333333333, 0.88939393939393929, 0.94666666666666666, 0.97222222222222232, 1.0, 0.96969696969696972, 1.0, 1.0, 0.83202258519862882, 0.94143960614548849, 0.97619047619047628, 0.84046345811051693], [1.0, 1.0, 0.74938725490196079, 0.83972125435540068, 0.9135752688172043, 0.8666666666666667, 0.9363636363636364, 0.98666666666666669, 0.96527777777777779, 1.0, 0.95454545454545459, 0.98550724637681153, 1.0, 0.85551522484371845, 0.92179781003310424, 0.95238095238095244, 0.84135472370766484], [0.91666666666666663, 1.0, 0.70894607843137258, 0.84804490902051877, 0.90313620071684586, 0.83333333333333337, 0.91969696969696957, 0.95999999999999996, 0.96527777777777768, 1.0, 0.96897546897546893, 0.98611111111111116, 1.0, 0.84402097197015513, 0.92094049741108563, 0.95238095238095244, 0.84194890077243023], [1.0, 1.0, 0.74877450980392146, 0.84010840108401075, 0.9135528673835126, 0.8833333333333333, 0.93636363636363618, 0.94765432098765423, 0.97222222222222221, 1.0, 0.98412698412698418, 0.98611111111111116, 1.0, 0.8669086509376891, 0.94143960614548849, 0.97619047619047628, 0.83184789067142006], [1.0, 1.0, 0.74938725490196079, 0.8393341076267905, 0.90349462365591393, 0.76666666666666661, 0.93787878787878787, 0.96197530864197534, 0.97222222222222221, 1.0, 0.98412698412698418, 0.98611111111111116, 1.0, 0.85501109094575511, 0.94114251761310586, 0.97619047619047628, 0.83155080213903743], [1.0, 1.0, 0.77941176470588225, 0.83991482771970583, 0.90418906810035848, 0.81666666666666654, 0.91666666666666663, 0.97432098765432096, 0.97222222222222232, 0.99206349206349209, 0.96969696969696972, 0.98550724637681153, 1.0, 0.86700947771728165, 0.93189882013411429, 0.97619047619047628, 0.84076054664289968], [1.0, 1.0, 0.78982843137254888, 0.84804490902051877, 0.89413082437275992, 0.84999999999999998, 0.86969696969696964, 0.96197530864197534, 0.97222222222222221, 1.0, 0.96897546897546893, 0.98550724637681153, 1.0, 0.86146400483968544, 0.95064935064935063, 0.97619047619047628, 0.84105763517528231]])
    print(matrix.mean(0))


if __name__ == '__main__':
    #single("Adenoma.csv","Adenomaclass.csv",[3068],7)
    all_dataset()

    
    
    

     
