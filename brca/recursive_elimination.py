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
- date   : "2017.04.28"
- Version : 1.0.0

Description
    t-test
'''

import numpy as np
import pandas as pd
from single_main import single
import os
import pickle
from sklearn.linear_model import LogisticRegression
from sklearn.model_selection import StratifiedKFold
from sklearn.multiclass import OneVsOneClassifier
from sklearn.feature_selection import chi2
from prepare import load_dataset





def get_feature_set(dataset_filename,json_filename,feature_range = 20):
    if os.path.exists("result.txt"):
        os.remove("result.txt")

    classes_list = [[[1],[2]],[[1],[3]],[[2],[3]],[[1,2],[3]],[[1,3],[2]],[[1],[2,3]]]
    feature_set = set()
    for classes in classes_list:
        estimator_aic, feature_names = single(dataset_filename,json_filename,classes = classes,feature_range = feature_range)
        feature_set = feature_set.union(feature_names)

    with open("feature_set.pkl","wb") as f:
        pickle.dump(feature_set,f)

    print("the feature set is: ")    
    print(feature_set)
    print("the feature_set length is {}".format(len(feature_set)))

    return feature_set



def generate_mask(y_test):

    mask = []

    stage_mask = {
            1: [True,False,False],
            2: [False,True,False],
            3: [False,False,True]
    }

    for label in y_test:
        mask.append(stage_mask[label])

    return np.array(mask)    





#采用 K-Fold 交叉验证 得到 aac 
def get_residual_sum(estimator,X,y,skf):
    scores = []
    residual_sums = []
    for train_index,test_index in skf.split(X,y):
        X_train, X_test = X.iloc[train_index,:], X.iloc[test_index,:]
        y_train, y_test = y[train_index], y[test_index]
        estimator.fit(X_train,y_train)
        scores.append(estimator.score(X_test,y_test))
        all_proba = estimator.predict_proba(X_test)
        residual_sums.append(residual_sum_of_square(all_proba[generate_mask(y_test)]))

    score = np.mean(scores)
    residual_sum = np.mean(residual_sums) 
    print("acc is: " + str(score))
    print("residual_sum is: " + str(residual_sum))  
    
    return residual_sum



def main(dataset_filename,json_filename,feature_range = 20,n_splits = 10):
    filtered_dataset,labels = load_dataset(dataset_filename,json_filename)
    labels = np.array(labels)
    
    if os.path.exists("feature_set.pkl"):
        with open("feature_set.pkl","rb") as f:
            feature_set = pickle.load(f)
    else:
        feature_set = get_feature_set(dataset_filename,json_filename,feature_range = 20)

    dataset = filtered_dataset.loc[feature_set,:].T
    skf = StratifiedKFold(n_splits = 10)
    estimator = LogisticRegression()

    sample_num, feature_num = dataset.shape

    for first in range(feature_num-2):
        for second in range(first,feature_num-1):
            for third in range(second,feature_num):
                eliminate_feature = set([first,second,third])
                feature_list = list(range(feature_num)) - eliminate_feature
                


    




                





    


if __name__ == '__main__':
    #get_feature_set("matrix_data.tsv","clinical.project-TCGA-BRCA.2017-04-20T02_01_20.302397.json",feature_range = 20)    
    main("matrix_data.tsv","clinical.project-TCGA-BRCA.2017-04-20T02_01_20.302397.json",\
        feature_range = 20,n_splits = 10)















