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
- date   : "2017.5.1"
- Version : 2.0.0

Description
    brac
'''

import numpy as np
import scipy as sp
import pandas as pd
from single_main import single
import os
import sys
import pickle
from sklearn.model_selection import StratifiedKFold
from sklearn.multiclass import OneVsOneClassifier
from prepare import load_dataset
from sklearn.linear_model import LassoLarsIC
from sklearn.svm import SVC
from sklearn.svm import LinearSVC
from sklearn.naive_bayes import GaussianNB
from sklearn.neighbors import KNeighborsClassifier
from sklearn.tree import DecisionTreeClassifier
from sklearn.linear_model import LogisticRegression
from sklearn.multiclass import OneVsOneClassifier
from sklearn.linear_model import Lasso
from sklearn.model_selection import GridSearchCV
from sklearn.metrics import make_scorer
from sklearn.metrics import r2_score
from sklearn.linear_model import LassoLarsCV
from sklearn.svm import SVR
from sklearn.linear_model import LinearRegression
from operator import itemgetter
from sklearn.linear_model import Ridge
from sklearn.metrics import confusion_matrix
import random

import warnings
warnings.filterwarnings(action="ignore", module="scipy", message="^internal gelsd")


    
#得到特征并集
def get_feature_set(dataset_filename,json_filename,alpha):
    if os.path.exists("result.txt"):
        os.remove("result.txt")

    """    
    classes_list = [[[1],[2]],[[1],[3]],[[1],[4]],[[2],[3]],[[2],[4]],[[3],[4]],\
        [[1,2],[3]],[[1,2],[4]],[[1,3],[2]],[[1,3],[4]],[[1,4],[2]],[[1,4],[3]],\
        [[2,3],[1]],[[2,3],[4]],[[2,4],[1]],[[2,4],[3]],[[3,4],[1]],[[3,4],[2]],\
        [[1],[2,3,4]],[[2],[1,3,4]],[[3],[1,2,4]],[[4],[1,2,3]],[[1,2],[3,4]],\
        [[1,3],[2,4]],[[1,4],[2,3]]]
    """
    classes_list = [[[1],[2]],[[1],[3]],[[2],[3]],[[1,2],[3]],[[1,3],[2]],[[2,3],[1]]]
        

    feature_set = set()
    for classes in classes_list:
        feature_names = single(dataset_filename,json_filename,alpha,classes = classes)
        feature_set = feature_set.union(feature_names)

    #print("the feature set is: ")    
    #print(feature_set)
    #print("the feature_set length is {}".format(len(feature_set)))

    return feature_set


#选择分类器 D-tree,SVM,NBayes,KNN
def select_estimator(case):

    if case == "SVM":
        estimator = SVC()
    elif case == "KNN":
        estimator = KNeighborsClassifier()
    elif case == "DT":
        estimator = DecisionTreeClassifier()
    elif case == "NB":
        estimator = GaussianNB()
    elif case == "LG":
        estimator = LogisticRegression() 
    elif case == "LSVM":
        estimator = LinearSVC()     

    return estimator         
  



#采用 K-Fold 交叉验证 得到 aac 
def get_acc(estimator,X,y,skf):
    scores = []
    cm = np.zeros((3,3))
    
    for train_index,test_index in skf.split(X,y):
        X_train, X_test = X.ix[train_index], X.ix[test_index]
        y_train, y_test = y[train_index], y[test_index]
        estimator.fit(X_train,y_train)
        scores.append(estimator.score(X_test,y_test))
        cm += confusion_matrix(y_test,estimator.predict(X_test))
    return np.mean(scores),cm 


    
#四分类的准确性   
def four_class_acc(dataset,labels,estimator_list,skf):
    max_estimator_aac = 0
    for estimator in estimator_list:
        estimator_aac,cm = get_acc(OneVsOneClassifier(select_estimator(estimator)),dataset,labels,skf)
        #print("the acc for {}: {}".format(estimator,estimator_aac))
        if estimator_aac > max_estimator_aac:
            max_estimator_aac = estimator_aac   #记录对于 k 个 特征 用五个个estimator 得到的最大值
    #print("-"*20)        
    #print("the macc is: {}\n".format(max_estimator_aac))
    #print(cm)  
    #print("\n")      
    return max_estimator_aac




#主函数
def main(dataset_filename,json_filename,n_splits = 10,\
    estimator_list = ["LG"]):
    
    #output_file = open("log_alpha.txt","w")
    #__console__ = sys.stdout
    #sys.stdout = output_file
    
    skf = StratifiedKFold(n_splits = n_splits)
    filtered_dataset,labels = load_dataset(dataset_filename,json_filename)
    labels = np.array(labels)

    for alpha in np.linspace(0,1,100):
        print("for alpha: {}".format(alpha))
        print("-"*40)
        try:
            feature_set = get_feature_set(dataset_filename,json_filename,alpha)
            dataset = filtered_dataset.loc[feature_set,:].T 
            feature_set = set(dataset.columns.tolist())
            print("the union set length: " +str(len(feature_set)))
            current_length = len(feature_set)
            macc = four_class_acc(dataset,labels, estimator_list, skf)
            print("the three class acc is : {}".format(macc))
            print("-" * 40)
            print("\n")
        except:
            print("can not get valid features for alpha = {}".format(alpha))  
            print("-" * 40) 
            print("\n") 



    #sys.stdout = __console__
    #output_file.close() 


if __name__ == '__main__':    
    main("matrix_data.tsv","clinical.project-TCGA-BRCA.2017-04-20T02_01_20.302397.json",n_splits = 10,\
        estimator_list = ["LG"])















