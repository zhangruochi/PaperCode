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
from sklearn.model_selection import StratifiedKFold
from sklearn.multiclass import OneVsOneClassifier
from prepare import load_dataset
from sklearn.linear_model import LassoLarsIC



    
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

  

def main(dataset_filename,json_filename,feature_range = 10,n_splits = 10,criterion = "aic"):
    estimator = LassoLarsIC(criterion = criterion,max_iter = 100)

    filtered_dataset,labels = load_dataset(dataset_filename,json_filename)
    labels = np.array(labels)
    
    if os.path.exists("feature_set.pkl"):
        with open("feature_set.pkl","rb") as f:
            feature_set = pickle.load(f)
    else:
        feature_set = get_feature_set(dataset_filename,json_filename,feature_range = feature_range)

    dataset = filtered_dataset.loc[feature_set,:].T
    sample_num, feature_num = dataset.shape

    feature_list = set(range(feature_num))

    current_aic = min(estimator.fit(dataset,labels).criterion_)

    min_aic = current_aic - 1
    eliminate_feature = []

    while min_aic < current_aic:
        min_aic = current_aic
        feature_list = feature_list - set(eliminate_feature)

        print(min_aic,len(feature_list))


        for first in range(len(feature_list)-1):
            for second in range(first,len(feature_list)):
                tmp_list = feature_list - set([first,second])
                estimator.fit(dataset.iloc[:,list(tmp_list)],labels)
                aic = min(estimator.criterion_)
                print(first,second,current_aic)
                if aic < current_aic:
                    current_aic = aic
                    eliminate_feature = [first,second]


if __name__ == '__main__':
    #get_feature_set("matrix_data.tsv","clinical.project-TCGA-BRCA.2017-04-20T02_01_20.302397.json",feature_range = 20)    
    main("matrix_data.tsv","clinical.project-TCGA-BRCA.2017-04-20T02_01_20.302397.json",\
        feature_range = 5,n_splits = 10,criterion = "aic")















