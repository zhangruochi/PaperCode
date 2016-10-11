import numpy as np
import pandas as pd
import os
import pickle
import random

from sklearn.svm import SVC
from sklearn.naive_bayes import GaussianNB
from sklearn.neighbors import KNeighborsClassifier
from sklearn.tree import DecisionTreeClassifier
from sklearn.grid_search import GridSearchCV

#加载数据集
def load_data(filename):
    full_path_name = os.path.join("/Users/ZRC/Desktop/HLab/dataset/data",filename)
    dataset = pd.read_csv(full_path_name,index_col=0)
    name_index_dic = get_name_index(dataset)
    with open("name_index.pkl","wb") as f:
        pickle.dump(name_index_dic,f)
    
    dataset = dataset.rename(index = name_index_dic)

    return dataset


#创造特征索引和特征名字对应的字典 
def get_name_index(dataset):
    name_index_dic = {}
    index = 0
    for name in dataset.index:
        name_index_dic[name] = index
        index += 1
    return name_index_dic 


#加载标签
def load_class(filename):
    full_path_name = os.path.join("/Users/ZRC/Desktop/HLab/dataset/class",filename)
    class_set = pd.read_csv(full_path_name,index_col = 0)
    labels = class_set["Class"]
    result = []
    
    def convert(label):
        if label == 'N':
            result.append(0)
        if label == 'P':
            result.append(1)    

    labels.apply(func = convert)        

    return np.array(result)



# t_检验  得到每个特征的 t 值
def t_test(dataset,labels):
    
    p_num = np.sum(labels)
    n_num = len(labels) - p_num  #  计算正负类各自标签的数量

    t_value = []
    
    def t_test_row(row):
        p_feature_data,n_feature_data = [],[]

        for index,label in enumerate(labels):
            if label == 0:
                n_feature_data.append(row[index])  
            elif label == 1:
                p_feature_data.append(row[index])
                
        p_mean,n_mean = np.mean(p_feature_data),np.mean(n_feature_data)
        p_std,n_std = np.std(p_feature_data),np.std(n_feature_data)
        

        t_value.append(t_test_algo(p_mean,n_mean,p_std,n_std,p_num,n_num))  #t 检验
    
    dataset.apply(func = t_test_row,axis = 1)

    return t_value
 
#t 检验算法           
def t_test_algo(p_mean,n_mean,p_std,n_std,p_num,n_num):
    return abs(p_mean - n_mean) / ( ( (p_std ** 2 ) / p_num + (n_std ** 2) / n_num ) ** 0.5 )


#根据 t 检验的结果的大小重新构造特征集
def rank_t_value(dataset,labels):
    t_value = t_test(dataset,labels)
    list_t_value = []

    for index,value in enumerate(t_value):
        list_t_value.append((index,value))

    from operator import itemgetter
    sorted_tuple = sorted(list_t_value,key = itemgetter(1),reverse = True)
    sorted_list = [item[0] for item in sorted_tuple]
    dataset = dataset.reindex(sorted_list)

    return dataset.T


def prepare(datset_filename,class_filename):
    dataset = load_data(datset_filename)
    labels = load_class(class_filename)
    dataset = rank_t_value(dataset,labels)
    return dataset,labels



#选择分类器 D-tree,SVM,NBayes,KNN 
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

#采用 K-Fold 交叉验证 得到 aac 
def get_aac(estimator,X,y):
    scores = []
    k = 3 
    for train_index,test_index in k_fold(y,k):
        estimator.fit(X[train_index],y[train_index])
        scores.append(estimator.score(X[test_index],y[test_index]))
    return np.mean(scores)    

# K-Fold  生成器
def k_fold(y,k):
    from sklearn.cross_validation import KFold
    kf = KFold(len(y),n_folds = k)
    for train_index,test_index in kf:
        yield train_index,test_index
        

#生成重启的位置
def random_num_generator(num_of_feature):
    random.seed(7)
    return [random.randint(0,num_of_feature) for i in range(num_of_feature // 2 )]   # 重启的组数为所有特征的一半



def main():
    dataset,labels = prepare("Adenoma.csv","Adenomaclass.csv")
    loc_of_first_feature = random_num_generator(t_dataset.shape[1]) # 重启的位置

    max_aac = 0
    max_aac_list = []
    max_loc_aac = 0
    max_k_aac = 0

    feature_range = t_dataset.shape[1]
    for loc in loc_of_first_feature:
        for k in range(feature_range - loc - 2):  # 从 loc位置 开始选取k个特征   -3的原因是停止的条件是增加后面三个特征 aac 不增加
            locs = [i for i in range(loc,loc+k+1)]
            X = t_dataset[:,locs]
            for i in range(4):
                estimator = select_estimator(i)
                max_estimator_aac = get_aac(estimator,X,labels)
                if max_estimator_aac > max_k_aac:
                    max_k_aac = max_estimator_aac   #记录对于 k 个 特征 用四个estimator 得到的最大值

            if max_k_aac > max_loc_aac:
                max_loc_aac = max_k_aac   #得到的是从 loc 开始重启的最大值
                continue

            
            max_k_aac_next = 0
            max_k_aac_next_list = [] #记录加入后面三个特征后aac 的值
            new_locs = locs
            for i in range(2):
                new_locs = new_locs + [new_locs[-1] + 1]
                X = t_dataset[:,new_locs]
                for e in range(4):
                    estimator = select_estimator(e)
                    max_estimator_aac = get_aac(estimator,X,labels)
                    if max_estimator_aac > max_k_aac_next:
                        max_k_aac_next = max_estimator_aac   #记录对于 k 个 特征 用四个estimator 得到的最大值
                max_k_aac_next_list.append(max_k_aac_next)        

            if max_k_aac_next_list[0] <= max_loc_aac and max_k_aac_next_list[1] <= max_loc_aac:
                break   
            max_k_aac = 0    


        if max_loc_aac > max_aac:
            max_aac = max_loc_aac
                
        max_loc_aac = 0


    print(max_aac,loc,k)        
    return max_aac,loc,k         

"""
def svc_test(X,y):
    estimator = SVC()
    from sklearn.cross_validation import cross_val_score
    from sklearn.grid_search import GridSearchCV

    paramters = {"kernel":["linear","rbf"],
                 "C": np.logspace(-4,4,10),
                }
    grid = GridSearchCV(estimator,paramters)
    grid.fit(X,y)

    print(grid.best_estimator_)
"""

if __name__ == '__main__':
    dataset,labels = prepare("Adenoma.csv","Adenomaclass.csv")
    print(dataset)
    print(labels)

    
    
    

     
