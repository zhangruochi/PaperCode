from scipy import io
#import matplotlib.pyplot as plt 
import os
import numpy as np
import pandas as pd
import pickle


from sklearn.svm import SVC
from sklearn.naive_bayes import GaussianNB
from sklearn.neighbors import KNeighborsClassifier
from sklearn.tree import DecisionTreeClassifier
from sklearn.linear_model import LogisticRegression
from sklearn.ensemble import RandomForestClassifier
from sklearn.model_selection import StratifiedKFold



"""
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
"""

 
#加载单个文件
def load_dataset(Folder_name,filename):
    dataset_mat = io.loadmat(os.path.join(Folder_name,filename))
    data_struct = dataset_mat['dataStruct']
    #print(dataset_struct[0][0][0].shape)       #(16, 240000)
    dataset = data = data_struct[0][0][0].T
    return dataset

#对每个文件16个信道进行傅里叶变换（16，240000）
def change_one_file(dataset):
    vector = ff_change(dataset[0])
    for row in dataset[1:]:
        row_vector = ff_change(row)
        vector = np.hstack((vector,row_vector))
    return vector    

#对每一列数据进行傅里叶变换
def ff_change(row):
    changed_row = np.fft.fft(row,n = 10)    
    return changed_row       



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



#分类函数
def classfier(dataset,labels):    
    estimator_list = [0,1,2,3,4]
    skf = StratifiedKFold(n_splits = 3)
    names = ["SVM","KNeighbors","DecisionTree","Naives_Bayes","LogisticRegression"]
    index = 0
   
    for estimator_index in estimator_list:
        scores = []
        estimator = select_estimator(estimator_index)
        for train_index, test_index in skf.split(dataset,labels):
            estimator.fit(dataset[train_index],labels[train_index])
            score = estimator.score(dataset[test_index],labels[test_index])
            scores.append(score)
        print("{}: {}".format(names[index],np.mean(scores)))
        index += 1


#主函数
def main():
    #虚拟起始的向量  
    result_vector = np.zeros(160)

    # Negtive  dataset 和 labels
    N_labels = []
    N_folder_name = "N_Folder"
    for filename in os.listdir(N_folder_name):
        if filename == ".DS_Store":
            continue
        print(filename)    
        dataset = load_dataset(N_folder_name,filename)
        vector = change_one_file(dataset)
        result_vector = np.vstack((result_vector,vector))
        N_labels.append(0)    

    print(result_vector.shape)    
    #Positive  dataset 和 labels
    P_labels = []
    P_folder_name = "P_Folder"
    for filename in os.listdir(P_folder_name):
        if filename == ".DS_Store":
            continue
        print(filename)      
        dataset = load_dataset(P_folder_name,filename)
        vector = change_one_file(dataset)
        P_labels.append(1)
        result_vector = np.vstack((result_vector,vector))

    labels = np.hstack((N_labels,P_labels))
    dataset = result_vector[1:]

    print(labels.shape)
    print(dataset.shape)
    with open("dataset.pkl","wb") as f:
        pickle.dump(dataset,f)

    with open("labels.pkl","wb") as f:
        pickle.dump(labels,f)   

    #分类
    classfier(np.angle(dataset),labels)



#测试
def test_acc():
    with open("dataset.pkl","rb") as f:
        dataset = pickle.load(f)

    with open("labels.pkl","rb") as f:
        labels = pickle.load(f)

    dataset = np.angle(dataset)
    print(dataset.shape)
    

    estimator = RandomForestClassifier()
    estimator.fit(dataset,labels)
    new_dataset = dataset[:,estimator.feature_importances_ != 0]
    print(new_dataset.shape)
    
    from sklearn.model_selection import cross_val_score
    print(cross_val_score(estimator,new_dataset,labels))


    #[ 0.66666667  0.56565657  0.48979592]
    


    






            

        
if __name__ == '__main__': 
    #main()
    test_acc()
    

