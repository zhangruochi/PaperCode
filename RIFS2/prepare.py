#!/usr/bin/env python3

#info
#-name   : zhangruochi
#-email  : zrc720@gmail.com

"""
根据 parser_class 文件，做一些准备工作，返回最终需要处理的dataset 和 label
"""


import numpy as np
import pandas as pd
import os
import pickle
import random
from functools import partial
from parser_class import get_labels
import csv

def load_dataset(dataset_filename,json_filename):
    dataset = pd.read_csv(dataset_filename,"\t",index_col = 0)
    #print("raw_dataset: ",str(dataset.shape))

    mask,labels = get_labels(dataset_filename,json_filename)
    filtered_dataset = dataset.iloc[:,mask].fillna(method = "backfill")
    
    #print("filtered_dataset: " + str(filtered_dataset.shape))
    #print("raw filtered_labels: "+ str(len(labels)))
    
    names = filtered_dataset.columns.tolist()
    """
    with open('lables.csv', 'w') as csvfile:
        writer = csv.writer(csvfile)
        writer.writerow(names)
        writer.writerow(labels)
    """ 
    return filtered_dataset,labels


#加载标签
def processing_class(labels,criterion):
    #print(labels)
    p_class = criterion[0]
    n_class = criterion[1]
    result = []
    mask = []
    
    for label in labels:
        if label in p_class:
            result.append(1)
            mask.append(True)
        elif label in n_class:
            result.append(0) 
            mask.append(True)
        else:
            mask.append(False)    
    return np.array(result),mask




def prepare_dataset_labels(dataset_filename,json_filename,criterion = [[1,2],[3,4]]):
    dataset,labels = load_dataset(dataset_filename,json_filename)
    labels,mask = processing_class(labels,criterion)
    #print(dataset)
    dataset = dataset.loc[:,mask]
    """
    print("-"*20)
    print("using label to filter....")
    print("-"*20)
    print("ultimate dataset: " + str(dataset.shape))
    print("ultimate laabel length: " + str(len(labels)))
    print("\n")
    """
    return dataset,labels

         
if __name__ == '__main__':
    #标准输出是: 经过数据清洗后的dataset 及其对应的类标

    """
    输入参数是:
        matrix_data 文件
        clinical 数据文件
        分类标准    如 [[1],[2,3]] 表示stage i为一类， stage ii，iii 为第二类
                     [[1,2],[3]] 表示stage i,ii为一类， stage iii 为第二类
    """

    dataset_filename = "COAD/matrix_data_coad.tsv"
    clinical_filename = "COAD/clinical_COAD.json"

    dataset,labels = prepare_dataset_labels(dataset_filename,clinical_filename)

    print(dataset)     
    
    
    

     
