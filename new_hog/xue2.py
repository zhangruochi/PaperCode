'''
python3

Required packages
- pandas
- numpy
- sklearn

Info
- name   : "zhangruochi"
- email  : "zrc720@gmail.com"
- date   : "2016.10.31"
- Version : 2.0.0

Description
    加入特征提取
'''


import numpy as np
import pandas as pd
import os
import pickle

from sklearn.decomposition import PCA

from sklearn.svm import SVC
from sklearn.naive_bayes import GaussianNB
from sklearn.neighbors import KNeighborsClassifier
from sklearn.tree import DecisionTreeClassifier
from sklearn.linear_model import LogisticRegression
from sklearn.cross_validation import cross_val_score

#feature_seletion
from sklearn.feature_selection import VarianceThreshold
from sklearn.feature_selection import SelectKBest
from sklearn.linear_model import Lasso
from sklearn.linear_model import Ridge



def load_dataset_all():
    label_index = 0
    feature_range = list()
    labels = list()
    datasets = list()

    for file_name in sorted(os.listdir(os.getcwd())):
        if file_name.endswith(".csv"):
            dataset = pd.read_csv(file_name,header= None)
            labels = labels + [label_index for i in range(dataset.shape[0])]
            feature_range.append(dataset.shape[0])
            datasets.append(dataset)
            label_index += 1

    # 进行 pca 将维
    pca_datasets = list()
    pca = PCA(n_components = min(feature_range),random_state = 0)

    for dataset in datasets:
        pca_datasets.append(pca.fit_transform(dataset))


    for i in range(1,len(pca_datasets)):
        pca_datasets[0] = np.vstack((pca_datasets[0],pca_datasets[i]))

    new_dataset = pca_datasets[0]
    labels = np.array(labels)
    pca_datasets = []

    return new_dataset,labels


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


#filter: 根据方差进行过滤 默认为1
def feature_selection_variance(dataset,threshold = 1):
    transformer = VarianceThreshold(threshold = threshold)
    
    """
    transformer.fit(dataset)
    print(transformer.variances_.mean()) 平均方差竟然这么大 汗....5801492.33107
    """

    new_dataset = transformer.fit_transform(dataset)
    return new_dataset


#filter: 利用 f_classif 进行过滤 默认选择最好的10个特征
def feature_selection_selectKBest(dataset,labels,k=100):
    transformer = SelectKBest(k = "all")
   
    """
    transformer.fit(dataset,labels)
    print(transformer.scores_)
    """

    new_dataset = transformer.fit_transform(dataset,labels)
    return new_dataset


#wrapper: 利用lasso进行过滤
def feature_selection_lasso(dataset,labels,alpha=1.0):
    transformer = Lasso(alpha=alpha)
    coef_ = transformer.fit(dataset).coef_
    return dataset[coef_ != 0]

#wrapper:  利用ridge进行过滤
def feature_selection_ridge(dataset,alpha = 1.0):
    transformer = Ridge(alpha = alpha)
    coef_ = transformer.fit(dataset).coef_
    return dataset.loc[:,coef_ != 0]




def classfier():
    dataset,labels = load_dataset_all()
    #特征选择只需要更改这一句
    dataset = feature_selection_variance(dataset,threshold = 5801492)
    estimator_list = [0,1,2,3,4]

    for i in estimator_list:
        score = cross_val_score(select_estimator(i),dataset,labels,scoring = "accuracy").mean()
        print(score)
       

if __name__ == '__main__':
    classfier()


"""
方差过滤: 设定方差低于5801492 就过滤
output:
0.423355263158
0.761220760234
0.58918128655
0.365661549708
0.240259502924
"""



  