'''
python3

Required packages
- pandas
- scipy
- numpy
- sklearn
- scipy
- PIL


Info
- name   : "zhangruochi"
- email  : "zrc720@gmail.com"
- date   : "2017.02.19"
- Version : 3.0.0

Description
    lcp 
'''


import os
from PIL import Image
import numpy as np
from scipy.ndimage import filters
from math import ceil
from math import pi
from collections import defaultdict
from operator import itemgetter
import pickle
import pandas as pd

from sklearn.svm import SVC
from sklearn.naive_bayes import GaussianNB
from sklearn.neighbors import KNeighborsClassifier
from sklearn.tree import DecisionTreeClassifier
from sklearn.ensemble import RandomForestClassifier
from sklearn.linear_model import LogisticRegression
from sklearn.model_selection import cross_val_score
from sklearn.model_selection import StratifiedKFold

from sklearn.metrics import precision_recall_fscore_support


#读取 csv 文件
def read_csv_file(p_filename,n_filename):
    
    p_dataset = pd.read_csv(p_filename)
    n_dataset = pd.read_csv(n_filename)

    dataset = np.vstack((p_dataset,n_dataset))

    #print(p_dataset.shape)
    #print(n_dataset.shape)
    #print(dataset.shape)

    #生成类标
    labels = []
    for i in range(n_dataset.shape[0]):
        labels.append(0)
    for i in range(p_dataset.shape[0]):
        labels.append(1)

    return dataset,labels


#选择分类器 D-tree,SVM,NBayes,KNN
def select_estimator(case):

    if case == 0:
        estimator = SVC()
    elif case == 1:
        estimator = RandomForestClassifier(random_state = 7)
    elif case == 2:
        estimator = DecisionTreeClassifier(random_state = 7)
    elif case == 3:
        estimator = GaussianNB()
    elif case == 4:
        estimator = LogisticRegression()
    elif case == 5:
        estimator = KNeighborsClassifier()        

    return estimator


#主函数
def main():
#-------------参数------------------    
    n = 5    #采用 n 折交叉验证
    p_filename = "Gastirc_polyp_P.csv"
    n_filename = "Gastirc_polyp_N.csv"
#-------------参数------------------       

    dataset,labels = read_csv_file(p_filename,n_filename)   
    print("dataset shape:",dataset.shape)  
    
    estimator_list = [0,1,2,3,4,5]
    skf = StratifiedKFold(n_splits= n,random_state = 7)

    score_func_list = ["accuracy","recall","roc_auc"]
    for score_func in score_func_list:
        print(score_func+": ")
        for i in estimator_list:
            score = cross_val_score(select_estimator(i),dataset,labels,scoring = score_func ,cv=skf).mean()
            print(score)  



            
if __name__ == '__main__':
    main()



