"""
提取每个甲基化的数据对应在染色体上的坐标
16 28797486 28797825
3 57716811 57718675
7 15691512 15693551
7 148453584 148455804
11 93501124 93502564
14 92883203 92883973
"""


import pandas as pd
import re
import numpy as np
import math

def load_data():
    dataset = pd.read_table("GPL8490-65.txt",index_col = 'ID')
    print(dataset.shape)  #(27578, 38)

    used_dataset = dataset.loc[:,['CPG_ISLAND_LOCATIONS']]
    print(used_dataset.iloc[0,0])
    print(type(used_dataset.iloc[0,0]))

    for index,row in used_dataset.iterrows():
      try:
        used_dataset.loc[index,"CPG_ISLAND_LOCATIONS"] = " ".join(re.split('[:-]',row.values[0]))
      except:
        used_dataset.loc[index,"CPG_ISLAND_LOCATIONS"] = np.NaN  

    used_dataset.dropna(axis = 0,how='any',inplace = True)
    used_dataset.to_csv("for_trans.csv",sep='\t')   

def get_unfransformed_dataset():
    dataset = pd.read_csv("for_trans.csv",sep='\t',index_col='ID')
    dataset_index  = dataset.index     #20006

    with open("location.txt","w") as f:
      for index, row in dataset.iterrows():
          f.write(row.values[0] + "\n")


if __name__ == '__main__':
    load_data()
    get_unfransformed_dataset()

