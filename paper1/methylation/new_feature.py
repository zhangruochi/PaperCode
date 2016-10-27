import pandas as pd
import re
import numpy as np
import math
import csv
import os
import pickle

#得到原始的特征与特征所在染色体的位置  eg:{'cg00000292': ['16', '28797486', '28797825']}
def get_feature():
    dataset = pd.read_csv("for_trans.csv",sep='\t',index_col='ID')
    dataset_index  = dataset.index     #20006
    feature_dict = dict()
    for index, row in dataset.iterrows():
      feature_dict[index] = [item for item in row.values[0].split(" ")]
    return dataset_index,feature_dict


def remove_n(data):
    return data.strip("\n")

#初步处理数据 生成临时文件  得到mRNA及其数据的列表
def get_mRNA(chr_fileanme):
    with open(chr_fileanme) as f:
        if not os.path.exists("temp_output"):
            os.mkdir("temp_output")
        with open("temp_output/{}.txt".format(os.path.split(chr_fileanme)[1]),"a") as result_file:
            while True:
                data = f.readline().strip(" ")
                if data:
                    if len(data) == 0:
                        pass
                    elif data.startswith("mRNA"):
                        every_mRNA_data = []
                        every_mRNA_data.append(data)
                        next_line = f.readline().strip(" ")
                        while next_line[0].isdigit() or next_line[0] == "<":
                            every_mRNA_data.append(next_line)
                            next_line = f.readline().strip(" ")    
                        while True:
                            data = f.readline().strip(" ")
                            if data.startswith('/db_xref="GeneID'): 
                                every_mRNA_data.append(" "+data)   
                                result_file.write("".join(list(map(remove_n,every_mRNA_data))) +"\n")  
                                break
                else:
                    break

def get_id(string):
    return string[string.find("GeneID"):].split(":")[-1].strip('"')

def get_loc(string):
    string_list = string.split("..")
    start = int(string_list[0].split("(")[-1].strip(">").strip("<"))  #not find  return -1
    end = int(string_list[-1].strip(")").strip("<").strip(">"))
    return start,end

#根据临时文件得到mRNA最终的数据结构  
def get_id_loc(temp_file):
    result_dict = {}
    all_dataset = []
    with open(os.path.join("temp_output",temp_file),"r") as f:
        for line in f.readlines():
            data = [item.strip() for item in line.split(" ") if len(item) != 0]
            all_dataset.append(data)

    gene_id = get_id(all_dataset[0][-1])
    start,end = get_loc(all_dataset[0][1])
    start_list=[start]
    end_list = [end]

    for mRNA in all_dataset[1:]:
        temp_gene_id = get_id(mRNA[-1])
        
        if temp_gene_id in result_dict:
            start_list =[get_loc(mRNA[1])[0]]
            end_list = [get_loc(mRNA[1])[1]]
            result_dict[temp_gene_id] = [min([start_list[0],result_dict[temp_gene_id][0]]),max([end_list[0],result_dict[temp_gene_id][1]])]
            continue

        if temp_gene_id != gene_id:
            result_dict[gene_id]=[min(start_list),max(end_list)]
            gene_id = temp_gene_id
            start_list = []
            end_list = []
            start_list.append(get_loc(mRNA[1])[0])
            end_list.append(get_loc(mRNA[1])[1])
        else:
            start_list.append(get_loc(mRNA[1])[0])
            end_list.append(get_loc(mRNA[1])[1])
      
    return result_dict   



#初步清晰所有染色体的文件 保存到临时文件夹
def save_temp_file():    
    dirname = os.path.join("Autism","GRCh")
    for filename in os.listdir(dirname):
        if filename == ".DS_Store":
            continue
        full_filename = os.path.join("Autism","GRCh",filename)
        get_mRNA(full_filename)
            
#根据所有染色体的临时文件 生成字典 
def get_all_chr_dic():
    all_chr = dict()
    for filename in os.listdir("temp_output"):   
        if filename == ".DS_Store":
            pass
        print(filename)    
        chr_index = filename.split(".")[1][filename.split(".")[1].find("r")+1:]
        all_chr[chr_index] =  get_id_loc(filename)


    with open("feature_index.pkl","wb") as f:
        pickle.dump(all_chr,f)


def get_feature_relation():
    
    with open("feature_index.pkl","rb") as f:
        chr_dict = pickle.load(f)
    #{1:{'126695': [26949556, 26960484],...},.....}

    dataset_index,feature_dict = get_feature()    #{'cg13277160': ['2', '208197158', '208200384']....}
    cg_ge_relation = []
    for feature,infor in feature_dict.items():
        for gene_id,loc_list in chr_dict[infor[0]].items():
            if int(infor[1]) >= loc_list[0] and int(infor[2]) <= loc_list[1]:
                cg_ge_relation.append((gene_id,feature))
                print(feature,gene_id)

    print(len(cg_ge_relation))
    with open("cg_ge_relation.pkl","wb") as f:
        pickle.dump(cg_ge_relation,f)       #10333

def deal_relation():
    with open("cg_ge_relation.pkl","rb") as f:
        infor_list = pickle.load(f)
    from collections import defaultdict   
    result_dict = defaultdict(list)
    
    for item in infor_list:
        result_dict[item[0]].append(item[1])  #{'653583': ['cg01594262', 'cg15844609', 'cg08980578', 'cg24968336'.....
    
    with open("relation_ultimate.pkl","wb") as f:    
        pickle.dump(result_dict,f)
    return result_dict
                









if __name__ == '__main__':
    deal_relation()
