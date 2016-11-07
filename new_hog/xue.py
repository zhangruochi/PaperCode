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
- Version : 1.0.0

Description
    .....
'''


import numpy as np
import pandas as pd
import os
import pickle
from sklearn.svm import SVC
from sklearn.naive_bayes import GaussianNB
from sklearn.neighbors import KNeighborsClassifier
from sklearn.tree import DecisionTreeClassifier
from sklearn.linear_model import LogisticRegression
from sklearn.cross_validation import cross_val_score


def test_dataset():
    poly_dataset = pd.read_csv("Gastric_poly_Sub.csv",header = None)
    poly_shape = poly_dataset.shape                         #(158, 6480)
    poly_labels = [0 for i in range(poly_shape[0])] 

    ulcer_dataset = pd.read_csv("Gastric_ulcer_Sub.csv",header = None)
    ulcer_shape = ulcer_dataset.shape                        #(99, 6912)
    ulcer_labels = [1 for i in range(ulcer_shape[0])]


    sub_dataset = pd.read_csv("Gastritis_Sub.csv",header = None)
    sub_shape = sub_dataset.shape                            #(74, 3168)
    sub_labels = [2 for i in range(sub_shape[0])]

    normal_dataset = pd.read_csv("Normal_Sub.csv",header = None)
    normal_shape  = normal_dataset.shape                     #(243, 42336)
    sub_labels =  [3 for i in range(normal_shape[0])]

    dimension = min(min(poly_shape[1],ulcer_shape[1]),min(sub_shape[1],[normal_shape]))
   
def load_dataset_all():
    label_index = 0
    feature_range = list()
    labels = list()
    datasets = list()

    for file_name in os.listdir(os.getcwd()):
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
    with open("dataset.pkl","wb") as f:
        pickle.dump(new_dataset,f)
    with open("labels.pkl","wb")  as f:
        pickle.dump(labels,f)   

    return new_dataset,labels


#加载数据集
def load_data():
    with open("dataset.pkl","rb") as f:
        dataset = pickle.load(f)
    with open("labels.pkl","rb") as f:
        labels = pickle.load(f)

    print(dataset.shape)    
    print(labels.shape)        
    return dataset,labels


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


def classfier():
    dataset,labels = load_data()
    estimator_list = [0,1,2,3,4]

    for i in estimator_list:
        score = cross_val_score(select_estimator(i),dataset,labels,scoring = "accuracy").mean()
        print(score)
       

if __name__ == '__main__':
    test_dataset()

  