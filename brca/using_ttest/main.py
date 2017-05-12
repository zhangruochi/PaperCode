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
- date   : "2017._5.1"
- Version : 2.0.0

Description
    brac
'''

import numpy as np
import pandas as pd
from single_main import single
import os
import pickle
from sklearn.model_selection import StratifiedKFold
from sklearn.multiclass import OneVsOneClassifier
from prepare import load_dataset
from sklearn.linear_model import LassoLarsIC
from sklearn.svm import SVC
from sklearn.naive_bayes import GaussianNB
from sklearn.neighbors import KNeighborsClassifier
from sklearn.tree import DecisionTreeClassifier
from sklearn.linear_model import LogisticRegression
from sklearn.multiclass import OneVsOneClassifier



    
#得到特征并集
def get_feature_set(dataset_filename,json_filename,feature_range = 10):
    if os.path.exists("result.txt"):
        os.remove("result.txt")

    classes_list = [[[1],[2]],[[1],[3]],[[1],[4]],[[2],[3]],[[2],[4]],[[3],[4]],\
        [[1,2],[3]],[[1,2],[4]],[[1,3],[2]],[[1,3],[4]],[[1,4],[2]],[[1,4],[3]],\
        [[2,3],[1]],[[2,3],[4]],[[2,4],[1]],[[2,4],[3]],[[3,4],[1]],[[3,4],[2]],\
        [[1],[2,3,4]],[[2],[1,3,4]],[[3],[1,2,4]],[[4],[1,2,3]],[[1,2],[3,4]],\
        [[1,3],[2,4]],[[1,4],[2,3]]]

    feature_set = set()
    for classes in classes_list:
        feature_names = single(dataset_filename,json_filename,classes = classes,feature_range = feature_range)
        feature_set = feature_set.union(feature_names)

    with open("feature_set.pkl","wb") as f:
        pickle.dump(feature_set,f)

    print("the feature set is: ")    
    print(feature_set)
    print("the feature_set length is {}".format(len(feature_set)))

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

    return estimator         
  

def recursive_elimination(dataset,labels,criterion):
    estimator = LassoLarsIC(criterion = criterion,max_iter = 100)
    sample_num, feature_num = dataset.shape
    feature_list = set(range(feature_num))

    min_aic = min(estimator.fit(dataset,labels).criterion_)
    print("the first aic(bic) is : " + str(min_aic))
    eliminate_feature = []

    while True:
        
        current_aic = 0
        feature_list = feature_list - set(eliminate_feature)
        
    
        for first in range(len(feature_list)-1):
            for second in range(first+1,len(feature_list)):
                tmp_list = feature_list - set([first,second])
                estimator.fit(dataset.iloc[:,list(tmp_list)],labels)
                aic = min(estimator.criterion_)

                if aic < current_aic:
                    current_aic = aic
                    print(current_aic,first,second)
                    eliminate_feature = [first,second]

        if current_aic >= min_aic:
            break    
        else:
            min_aic = current_aic
            print("eliminate feature:  {}, the current aic(bic) is {}".format(str(eliminate_feature),str(min_aic)))            

    print("the final length of feature set is: "+ str(len(feature_list)))        
    return list(feature_list)



#采用 K-Fold 交叉验证 得到 aac 
def get_aac(estimator,X,y,skf):
    scores = []
    for train_index,test_index in skf.split(X,y):
        X_train, X_test = X.ix[train_index], X.ix[test_index]
        y_train, y_test = y[train_index], y[test_index]
        estimator.fit(X_train,y_train)
        scores.append(estimator.score(X_test,y_test))

    return np.mean(scores)    

    
#四分类的准确性   
def four_class_acc(dataset,labels,estimator_list,skf):
    max_estimator_aac = 0
    for estimator in estimator_list:
        estimator_aac = get_aac(OneVsOneClassifier(select_estimator(estimator)),dataset,labels,skf)
        print("the acc for {}: {}".format(estimator,estimator_aac))
        if estimator_aac > max_estimator_aac:
            max_estimator_aac = estimator_aac   #记录对于 k 个 特征 用五个个estimator 得到的最大值
    print("-"*20)        
    print("the macc is: {}\n".format(max_estimator_aac))        
    return max_estimator_aac



#主函数
def main(dataset_filename,json_filename,feature_range = 20,n_splits = 10,criterion = "aic",\
    estimator_list = [0,1,2,3,4],seed_number = 7):
    
    skf = StratifiedKFold(n_splits = n_splits)
    filtered_dataset,labels = load_dataset(dataset_filename,json_filename)
    labels = np.array(labels)
    
    if os.path.exists("feature_set.pkl"):
        with open("feature_set.pkl","rb") as f:
            feature_set = pickle.load(f)
    else:
        feature_set = get_feature_set(dataset_filename,json_filename,feature_range = feature_range)

    dataset = filtered_dataset.loc[feature_set,:].T  

    macc = four_class_acc(dataset,labels, estimator_list, skf)

    if os.path.exists("feature_list.pkl"):
        with open("feature_list.pkl","rb") as f:
            feature_list = pickle.load(f)
    else:        
        feature_list =  recursive_elimination(dataset,labels,criterion)
        with open("feature_list.pkl","wb") as f:
            pickle.dump(feature_list,f)
    


    skf = StratifiedKFold(n_splits = n_splits) 
    macc = four_class_acc(dataset.iloc[:,feature_list] ,labels,estimator_list,skf)

    return macc


    




    


if __name__ == '__main__':
    #get_feature_set("matrix_data.tsv","clinical.project-TCGA-BRCA.2017-04-20T02_01_20.302397.json",feature_range = 20)    
    main("matrix_data.tsv","clinical.project-TCGA-BRCA.2017-04-20T02_01_20.302397.json",feature_range = 20,n_splits = 10,\
        criterion = "aic",estimator_list = ["SVM","KNN","DT","NB","LG"],seed_number = 7)















