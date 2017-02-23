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
from sklearn.metrics import matthews_corrcoef
import warnings



#读取 csv 文件
def read_csv_file(p_filename,n_filename):
    
    p_dataset = pd.read_csv(p_filename,header =None)
    n_dataset = pd.read_csv(n_filename, header = None)
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


def evaluate(estimator,X,y,skf):
    warnings.filterwarnings("ignore")
    acc_list,sn_list,sp_list,mcc_list = [],[],[],[]
    for train_index, test_index in skf.split(X, y):
        estimator.fit(X[train_index],y[train_index])
        y_predict = estimator.predict(X[test_index])
        y_true = y[test_index]

        #索引
        predict_index_p = (y_predict == 1)  #预测为正类的
        predict_index_n = (y_predict == 0)  #预测为负类

        index_p = (y_true==1)  #实际为正类
        index_n = (y_true==0)  #实际为负类

        Tp = sum(y_true[predict_index_p])       #正确预测的正类  （实际为正类 预测为正类）
        Tn = sum([1 for x in list(y_true[predict_index_n]) if x == 0]) #正确预测的负类   (实际为负类 预测为负类)
        Fn = sum(y_predict[index_n])       #错误预测的负类  （实际为负类 预测为正类）
        Fp = sum(y_true[predict_index_n])       #错误预测的正类   (实际为正类 预测为负类)

        acc = (Tp+Tn)/(Tp+Tn+Fp+Fn)
        sn = Tp/(Tp+Fn)
        sp = Tn/(Tn+Fp)
        mcc = matthews_corrcoef(y_true,y_predict)

        acc_list.append(acc)
        sn_list.append(sn)
        sp_list.append(sp)
        mcc_list.append(mcc)

    return np.mean(acc_list),np.mean(sn_list),np.mean(sp_list),np.mean(mcc_list)


#主函数
def main():
#-------------参数------------------    
    n = 5    #采用 n 折交叉验证
    p_filename = "Gastirc_polyp_P.csv"
    n_filename = "Gastirc_polyp_N.csv"
#-------------参数------------------       

    dataset,labels = read_csv_file(p_filename,n_filename)   
    print("dataset shape:",dataset.shape)  
    
    labels = np.array(labels)    
    estimator_list = [0,1,2,3,4,5]
    skf = StratifiedKFold(n_splits= n,random_state = 7)

    for i in estimator_list:    
        acc,sn,sp,mcc = evaluate(select_estimator(i),dataset,labels,skf)
        print("Acc: ",acc)
        print("Sn: ",sn)
        print("Sp: ",sp)
        print("Mcc: ",mcc)
        print("\n")



            
if __name__ == '__main__':
    main()
    




