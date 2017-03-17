import numpy as np
import pandas as pd
import pickle
import multiprocessing
from scipy.stats import ttest_ind_from_stats
from sklearn.feature_selection import SelectFdr
from sklearn.cluster import Birch
from scipy.stats import pearsonr
#import matplotlib.pyplot as plt


#加载数据集
def load_dataset(filename):
    dataset = pd.read_table(filename,index_col = "GeneID")
    GeneID = save_GeneID(dataset,filename)
    dataset_list = [dataset.iloc[:,index:index+5] for index in [0,5,10,15,20]]

    return dataset_list


def save_GeneID(dataset,filename):
    GeneID_dict = dict()
    GeneID = dataset.index.tolist()

    for index, ID in zip(range(dataset.shape[0]),GeneID):
        GeneID_dict[index] = ID

    with open("{}_GeneID.pkl".format(filename.split("_")[1]),"wb") as f:
        pickle.dump(GeneID_dict,f)        

    #print(GeneID_dict)    

"""
#利用 t_test 得到 p_value
def t_test(case,control):
    statistic,p_value = ttest_ind(case,control,axis=1,equal_var=False)
    #p_value = pd.Series(data=p_value,index=list(range(len(p_value))))
    print(p_value)
    return p_value
"""    

"""
#use formaular 
def formaular(case,control):
    abar = np.mean(case,1)
    avar = np.var(case,1)
    na = case.shape[1]
    adof = na - 1

    bbar = np.mean(control,1)
    bvar = np.var(control,1)
    nb = control.shape[1]
    bdof = nb - 1

    tf = (abar - bbar) / np.sqrt(avar/na + bvar/nb)
    dof = (avar/na + bvar/nb)**2 / (avar**2/(na**2*adof) + bvar**2/(nb**2*bdof))
    pf = 2*stdtr(dof, -np.abs(tf))    

    print(pf)
"""

#T-test 
def t_test(case,control):
    p_mean,n_mean = np.mean(case,1),np.mean(control,1)
    p_std,n_std = np.std(case,1),np.std(control,1)
    t_value,p_value = ttest_ind_from_stats(p_mean,p_std,case.shape[1],n_mean,n_std,control.shape[1],equal_var=False)
    return p_value


#根据 t 检验 然后和 fdr 的结果的过滤数据集
def fdr_t_value_filter(case,control,fdr=None):

    p_value = t_test(case,control)
    if not fdr:
        fdr = 0.01
    index_mask = p_value < 0.01

    filtered_dataset = case.loc[index_mask,:]
    print("t-test filtered dataset shape: " + str(filtered_dataset.shape))
    return filtered_dataset




#准备不同时间片的数据集
def prepare(case_filename, control_filename):
    case_dataset_list = load_dataset(case_filename)
    control_dataset_list = load_dataset(control_filename)
    print("raw dataset shape: " + str(case_dataset_list[0].shape) + "\n")
    #fdr = max(p_value)/control.shape[0]
    dataset_list = []
    for i in range(5):
        print("getting the {} period dataset....".format(i))
        dataset_list.append(fdr_t_value_filter(case_dataset_list[i],control_dataset_list[i],fdr = None))
    print("\n")
    return dataset_list,control_dataset_list    





#cluster the dataset, return labels and all candidate groups
def cluster_dataset(case,n_clusters = 50):
    cluster = Birch(n_clusters = n_clusters)
    cluster.fit(case)
    labels = cluster.labels_  #labels   

    all_condidate_clusters = []
    for i in range(50):
        case_cluster = case.iloc[labels == i,:]
        #自己改进的地方   如果聚类的结果中基因的个数小于等于三个，则放弃这个类
        if case_cluster.shape[0] <=10:
            continue 
        all_condidate_clusters.append(case_cluster)

    return all_condidate_clusters,labels


#normalize the data
def normalize(case,control):
    normalize_case = (case - control.mean().values) /  control.std().values
    return normalize_case


#calculate inner pcc
def calculate_inner_pcc(normalize_cluster):
    pearsons = []
    for gene_id_i, value_i in normalize_cluster.iterrows():
        for gene_id_j, value_j in normalize_cluster.iterrows():
            if gene_id_i == gene_id_j:
                continue
            else:
                pearson_coeffient,p_value = pearsonr(value_i,value_j)
                #print(pearson_coeffient)
                pearsons.append(pearson_coeffient)  

    average_pearsons = abs(np.mean(pearsons))
    #print("the average inner pcc: " + str(average_pearsons))
    return average_pearsons


def calculate_std(normalize_cluster):
    stds = []
    for gene_id,value in normalize_cluster.iterrows():
        std = value.std()
        #print(std)
        stds.append(std)
    average_stds = np.mean(stds)    
    #print("the average std is: "+ str(average_stds))    
    return average_stds   


def calculate_outer_pcc(normalize_cluster,case):
    pearsons = []
    for gene_id_inner, value_inner in normalize_cluster.iterrows():
        for gene_id_outer, value_outer in case.iterrows():
            if gene_id_inner == gene_id_outer:
                continue
            else:    
                pearson_coeffient,p_value = pearsonr(value_inner,value_outer)
                #print(pearson_coeffient)
                pearsons.append(pearson_coeffient)

    average_pearsons = abs(np.mean(pearsons))
    #print("the average outer pcc: "+ str(average_pearsons))

    return average_pearsons            


#计算 CI 值  SD*PCC(inner)/PCC(outter)
def calculate_ci(case_cluster,control_cluster):
    normalize_cluster = normalize(case_cluster,control_cluster)
    #print(normalize_cluster)
    inner_pear = calculate_inner_pcc(normalize_cluster)
    outer_pear = calculate_outer_pcc(normalize_cluster,case_cluster)
    std = calculate_std(normalize_cluster)
    return inner_pear * std / outer_pear


#[(case_cluster, control_cluster),.........]
def get_cluster_pair(all_case_clusters,control_dataset):
    cluster_pair = []
    for i in range(len(all_case_clusters)):
        id_index = all_case_clusters[i].index
        #print(id_index)
        #print(control_dataset)
        control_cluster = control_dataset.loc[id_index,:]
        #print(all_case_clusters[i].head())
        #print(control_cluster.head())
        cluster_pair.append((all_case_clusters[i],control_cluster))
    return cluster_pair    


#封装一个work函数， 包含对每一个 cluster 的所有运算， 同时提供给进程池
def work(cluster_pair):
    case_cluster,control_cluster = cluster_pair
    #print(case_cluster.shape)
    #print(case_cluster)
    #print(control_cluster)
    case_ci = calculate_ci(case_cluster,control_cluster)
    control_ci = calculate_ci(control_cluster,control_cluster)

    #print("the case ci is: " + str(case_ci))
    #print("the control ci is " + str(control_ci))
    #print("")
    return case_ci,control_ci


    
#multiprocessing the cluster
def multiprocessing_clusetr(cluster_pair_list):
    pool = multiprocessing.Pool(multiprocessing.cpu_count())
    result = pool.map(work,cluster_pair_list)
    
    case_ci_list = []
    control_ci_list = []

    for item in result:
        case_ci_list.append(item[0])
        control_ci_list.append(item[1])

    return case_ci_list,control_ci_list


    
def main(case_filename,control_filename):
    case_dataset_list,control_dataset_list = prepare(case_filename,control_filename)
    
    for i in range(len(case_dataset_list)):
        all_case_clusters, case_labels = cluster_dataset(case_dataset_list[i])
        cluster_pair_list = get_cluster_pair(all_case_clusters,control_dataset_list[i])
        
        case_ci_list,control_ci_list = multiprocessing_clusetr(cluster_pair_list[10:15])
        print("")
        print("the {} of time period: ".format(i))
        print("case result: " + str(case_ci_list))
        print("control result: " + str(control_ci_list))
                
        
if __name__ == '__main__':
    main("liver_case_data.txt","liver_control_data.txt")
    


       

