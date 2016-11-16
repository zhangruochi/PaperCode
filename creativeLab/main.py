from scipy import io
import matplotlib.pyplot as plt 
import os
import numpy as np
import pandas as pd

from sklearn.svm import SVC
from sklearn.naive_bayes import GaussianNB
from sklearn.neighbors import KNeighborsClassifier
from sklearn.tree import DecisionTreeClassifier
from sklearn.linear_model import LogisticRegression
from sklearn.model_selection import StratifiedKFold


def load_dataset(filename):
    full_path_name = os.path.join("iData",filename)
    dataset_mat = io.loadmat(full_path_name)
    dataset_struct = dataset_mat['dataStruct']
    #print(dataset_struct[0][0][0].shape)       #(240000, 16)

    dataset = pd.DataFrame(data = dataset_struct[0][0][0])
    
    if filename.startswith("P"):
        label = [1 for i in range(16)]
    elif filename.startswith("N"):
        label = [0 for i in range(16)]

    return dataset,label

def graph_initial_dataset(dataset):
    fig = plt.figure(figsize=(8.0, 5.0))
    fig.add_subplot(111).plot(dataset[0])
    fig.savefig("fig1.png")
    plt.show()

def graph_trans_dataset(dataset):
    transformed = np.fft.fft(dataset[0])
    fig = plt.figure(figsize=(8.0, 5.0))
    fig.add_subplot(111).plot(transformed)
    fig.savefig("fig2.png")
    plt.show()




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



def get_freq(columns):
    return np.fft.fftfreq(len(columns))




def classfier():
    p_dataset,p_labels = load_dataset("P.mat")
    n_dataset,n_labels = load_dataset("N.mat")
    labels = np.array(p_labels + n_labels)
    print(labels)
    #进行傅里叶转换
    p_dataset = p_dataset.apply(func = np.fft.fft, axis = 0)
    n_dataset = n_dataset.apply(func = np.fft.fft, axis = 0)
    
    p_dataset = p_dataset.apply(func = get_freq,axis = 0)
    n_dataset = n_dataset.apply(func = get_freq,axis = 0)

    dataset = np.hstack((p_dataset,n_dataset)).T
    print(dataset.shape)

    estimator_list = [0,1,2,3,4]
    skf = StratifiedKFold(n_splits = 5)

    for train_index, test_index in skf.split(dataset,labels):
        for estimator_index in estimator_list:
            estimator = select_estimator(estimator_index)
            estimator.fit(dataset[train_index],labels[train_index])
            print(estimator.predict(dataset[test_index]))


    
        
if __name__ == '__main__': 
    classfier()
    

