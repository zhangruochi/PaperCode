'''
Required packages
- pandas
- numpy
- sklearn

Info
- name   : "zhangruochi"
- email  : "zrc720@gmail.com"
- date   : "2016.09.05"
- Version : 2.0.0

Description
    穷举法  每次选取两个特征
    加入多线程进行并行计算  提高效率
'''

import pandas as pd
import numpy as np
import os

from sklearn.svm import SVC
from sklearn.naive_bayes import GaussianNB
from sklearn.neighbors import KNeighborsClassifier
from sklearn.tree import DecisionTreeClassifier
from sklearn.grid_search import GridSearchCV
from sklearn.cross_validation import KFold

#加载数据集
def load_one_dataset(filename):
    full_path_name = os.path.join("data",filename)
    dataset = pd.read_csv(full_path_name,index_col = 0)
    return dataset


#加载类标集
def load_one_labels(filename):
    full_path_name = os.path.join("label",filename)
    labelset = pd.read_csv(full_path_name).loc[:,"Class"]

    def to_numeric(lebel):
        if lebel == "P":
            return 1
         
        elif lebel == "N":
            return 0
        
        else:
            return np.nan     

    labels = labelset.apply(to_numeric).values
    #[1 1 1 1 1 1 1 1 1 1 1 1 1 1 1 1 1 1 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0]
    return labels


#选择 estimator
def select_estimator(case):
    
    if case == 0:
        estimator = SVC()
        """
        paramters = {"kernel":["linear","rbf"],
                     "C": np.logspace(-4,4,10),
                    } 
        estimator = GridSearchCV(estimator,paramters)
        """
    elif case == 1:
        estimator = KNeighborsClassifier()
    elif case == 2:
        estimator = DecisionTreeClassifier()
    elif case == 3:
        estimator = GaussianNB()

    return estimator


#K-Fold 生成器
def k_fold(y,k):
    kf = KFold(len(y),n_folds = k)
    for train_index,test_index in kf:
        yield train_index,test_index

 
#采用 K-Fold 交叉验证得到 aac  (注意这里存在问题)
def get_aac(estimator,X,y,k):
    scores = []
    for train_index,test_index in k_fold(y,k):
        estimator.fit(X.iloc[train_index],y[train_index])
        scores.append(estimator.score(X.iloc[test_index],y[test_index]))
    return np.mean(scores)    






