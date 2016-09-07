'''
Required packages
- pandas
- numpy
- sklearn

Info
- name   : "zhangruochi"
- email  : "zrc720@gmail.com"
- date   : "2016.09.04"
- Version : 1.0

Description

    这个版本的穷举法只是初步封装对某个数据集的检验
    exhaustion_mathod() 是算法的主函数

    参数设定(可手动修改)： 
    window_size （窗口大小）
    step  （步长）
    k  （k 折交叉验证）
    estimator_list （分类器选择  可选择一个和多个） 
    stop_accuracy  （算法停止所必须的准确率）

    运行结果
    以 Adenoma.csv 数据集为例子 
    window_size = 5 
    step = 3    
    k = 4 
    estimator_list = [1]  决策树
    stop_accuracy = 0.98  
        
        输出
        1.0 [3306]         
        [Finished in 21.8s]
    
    1.0 为准确率  3306 为最高准确率的特征子集的起始位置
'''




import pandas as pd
import numpy as np
import os

from sklearn.svm import SVC
from sklearn.naive_bayes import GaussianNB
from sklearn.neighbors import KNeighborsClassifier
from sklearn.tree import DecisionTreeClassifier
from sklearn.grid_search import GridSearchCV
from sklearn.cross_validation import KFold


#加载数据集
def load_one_dataset(filename):
    full_path_name = os.path.join("data",filename)
    dataset = pd.read_csv(full_path_name,index_col = 0)
    return dataset


#加载类标集
def load_one_labels(filename):
    full_path_name = os.path.join("label",filename)
    labelset = pd.read_csv(full_path_name).loc[:,"Class"]

    def to_numeric(lebel):
        if lebel == "P":
            return 1
         
        elif lebel == "N":
            return 0
        
        else:
            return np.nan     

    labels = labelset.apply(to_numeric).values
    #[1 1 1 1 1 1 1 1 1 1 1 1 1 1 1 1 1 1 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0]
    return labels


#选择 estimator
def select_estimator(case):
    
    if case == 0:
        estimator = SVC()
        """
        paramters = {"kernel":["linear","rbf"],
                     "C": np.logspace(-4,4,10),
                    } 
        estimator = GridSearchCV(estimator,paramters)
        """
    elif case == 1:
        estimator = KNeighborsClassifier()
    elif case == 2:
        estimator = DecisionTreeClassifier()
    elif case == 3:
        estimator = GaussianNB()

    return estimator       


#K-Fold 生成器
def k_fold(y,k):
    kf = KFold(len(y),n_folds = k)
    for train_index,test_index in kf:
        yield train_index,test_index


#采用 K-Fold 交叉验证得到 aac
def get_aac(estimator,X,y,k):
    scores = []
    for train_index,test_index in k_fold(y,k):
        estimator.fit(X.iloc[train_index],y[train_index])
        scores.append(estimator.score(X.iloc[test_index],y[test_index]))
    return np.mean(scores)    


def get_rate_of_progress(i,length):
    return (str( i/length * 100) + " %")



#穷举法 主程序
def exhaustion_mathod():
    
    window_size = 5 #window_size
    step = 3    #step =< window_size
    k = 4  #k cross validation
    estimator_list = [1]  #estimator
    stop_accuracy = 0.98   #算法停止的最低准确率

    dataset = load_one_dataset("Adenoma.csv").T
    y = load_one_labels("Adenomaclass.csv")
    length = dataset.shape[1]

    estimator_max_aac = 0
    window_max_aac = 0
    max_loc = []

    for i in range(0,length):
        #print(get_rate_of_progress(i,length))   显示进度
        for j in range(i,length,step):     
            if j + window_size > length:
                break
            
            X = dataset.iloc[:,j:j+window_size]
            for estimator in estimator_list:
                estimator_aac = get_aac(select_estimator(estimator),X,y,k)   # k 折交叉验证的结果
                if estimator_aac > estimator_max_aac:
                    estimator_max_aac = estimator_aac
            if estimator_max_aac == window_max_aac:  
                max_loc.append(j)

            if estimator_max_aac > window_max_aac:
                window_max_aac = estimator_max_aac
                max_loc = []
                max_loc.append(j)

            estimator_max_aac = 0         
        if  window_max_aac >= stop_accuracy:
            return window_max_aac,max_loc

    return window_max_aac,max_loc        
                      

if __name__ == '__main__':
    window_max_aac,max_loc  = exhaustion_mathod()
    print(window_max_aac,max_loc)
    

