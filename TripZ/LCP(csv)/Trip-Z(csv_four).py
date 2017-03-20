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
- date   : "2017.03.20"
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
from sklearn.multiclass import OneVsOneClassifier



#读取 csv 文件
def read_csv_file(p_filename,n_filename_1,n_filename_2,n_filename_3):
    
    p_feature = pd.read_csv(p_filename,header =None)
    n_feature_1 = pd.read_csv(n_filename_1, header = None)
    n_feature_2 = pd.read_csv(n_filename_2, header = None)
    n_feature_3 = pd.read_csv(n_filename_3, header = None)

    dataset = np.vstack((n_feature_1,n_feature_2)) 
    dataset = np.vstack((dataset,n_feature_3))   
    dataset = np.vstack((dataset,p_feature))   

    print("\ndataset shape:",dataset.shape)  
    #生成类标
    labels = []
    for i in range(n_feature_1.shape[0]):
        labels.append(0)
    for i in range(n_feature_2.shape[0]):
        labels.append(1)
    for i in range(n_feature_3.shape[0]):
        labels.append(2)        
    for i in range(p_feature.shape[0]):
        labels.append(3)

    labels = np.array(labels)    

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


def get_single_score(y_true,y_predict,class_):
    #某个类别的个数 
    sum_count = 0
    for label in y_predict:
        if label == class_:
            sum_count += 1

    true_count = 0         
    #这个类别预测准确的个数        
    for i in range(len(y_true)):
        if y_predict[i] == class_ and y_predict[i] == y_true[i]:
            true_count += 1

    if sum_count == 0:  
        single_score = 0
    else:          
        single_score = true_count/sum_count        
    #print("   subclass{} acc: ".format(str(class_)) + str(single_score))
    
    return single_score

#采用 K-Fold 交叉验证 得到 aac 
def get_aac(estimator,X,y,skf):
    all_scores, ulcer_scores, polyp_socres, Gastritis_socres,normal_scores = [],[],[],[],[]

    for train_index,test_index in skf.split(X,y):
        X_train, X_test = X[train_index], X[test_index]
        y_train, y_test = y[train_index], y[test_index]
        estimator.fit(X_train,y_train)

        y_true = y[test_index]
        y_predict = estimator.predict(X_test)

        #print(y_true)
        #print(y_predict)
        #print(np.mean(y_true == y_predict))
        all_scores.append(np.mean(y_true == y_predict))

        for class_ in range(4):
            if class_ == 0:
               ulcer_scores.append(get_single_score(y_true,y_predict,class_))
            elif class_ == 1:
                polyp_socres.append(get_single_score(y_true,y_predict,class_))
            elif class_ == 2:
                Gastritis_socres.append(get_single_score(y_true,y_predict,class_))
            elif class_ == 3:
                normal_scores.append(get_single_score(y_true,y_predict,class_))        
                   
    return np.mean(all_scores),np.mean(ulcer_scores),np.mean(polyp_socres),np.mean(Gastritis_socres),np.mean(normal_scores)


#主函数
def main():
#-------------参数------------------    
    n = 10    #采用 n 折交叉验证
    n_filename_1 = "Gastric_ucler_P.csv"
    n_filename_2 = "Gastirc_polyp_P.csv"
    n_filename_3 = "Gastritis_P.csv"
    p_filename   = "Normal_P.csv"
#-------------参数------------------  

        

    dataset,labels = read_csv_file(p_filename,n_filename_1,n_filename_2,n_filename_3)   
 
      
    estimator_list = [0,1,2,3,4,5]
    skf = StratifiedKFold(n_splits= n,random_state = 7)

    for i in estimator_list:    
        four_acc,ulcer_acc, polyp_acc, Gastritis_acc,normal_acc = get_aac(OneVsOneClassifier(select_estimator(i)),dataset,labels,skf)
        print("Four acc: ",four_acc)
        print("    ulcer_acc: ",ulcer_acc)
        print("    polyp_acc: ",polyp_acc)
        print("    Gastritis_acc: ",Gastritis_acc)
        print("    normal_acc: ",normal_acc)
        print("")



            
if __name__ == '__main__':
    main()
    




