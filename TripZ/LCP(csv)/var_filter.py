
import pandas as pd
import numpy as np

#读取 csv 文件
def read_csv_file(filename):
    
    dataset = pd.read_csv(filename,header =None)
    print("the dataset shape is:  " + str(dataset.shape))
    #print(dataset.head())

    return dataset.T
    




#方差过滤
def var_filter(dataset,percent = 0.8):
    new_index_series = dataset.var(1)
    #首先过滤方差为0的
    dataset = dataset.loc[new_index_series != 0,:]

    new_index = new_index_series[new_index_series != 0].sort_values().index
    new_dataset = dataset.reindex(index = new_index)
    
    if percent > 0 and percent < 1:
        new_dataset = new_dataset.iloc[:int(new_dataset.shape[0]*percent),:].T
    else:
        print("the percent is error!")    

    print("the var filtered feature is: (feature, sample)" + str(new_dataset.shape))
    
    return new_dataset


def main():
    filename = "Gastritis_P.csv"
    dataset = read_csv_file(filename)
    new_dataset = var_filter(dataset,percent = 0.8)

    #save file
    new_dataset.to_csv("filtered_features.csv")





            
if __name__ == '__main__':
    main()
    




