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



    


if __name__ == '__main__':
    get_feature_set("matrix_data.tsv","clinical.project-TCGA-BRCA.2017-04-20T02_01_20.302397.json",feature_range = 20)    
















