import pandas as pd
import numpy as np
from collections import defaultdict


NAME_LEVEL = {
    "DM":   5,
    "DFP":  4,
    "DM?":  3,
    "FP":   2,
    "DP":   1,
}

DISEASE_NAMES = {
    "myelogenous":      "myeloid",
    "nonlymphocytic":   "myeloid",
    "myeloblastic":     "myeloid",
    "myelocytic":       "myeloid",
    "granulocytic":     "myeloid",
    "leukaemia":        "leukemia",
    "lymphoblastic":    "lymphocytic",
    "lymphoid":         "lymphocytic",
    "oesophageal":      "oesophagus",
    "endometrial":      "Endometrioid",
    "Oesophageal":      "Endometrioid",
    "Tumour":           "Tumor",
    "tumors":           "Tumor",
    "tumours":          "Tumor" ,
    "Phaeochromocytoma":"Pheochromocytoma",
    "malformations":    "malformation",
    "defect":           "disease",
    "defects":          "disease",
    "diseases":         "disease",
    "disorder":         "disease",
    "disorders":        "disease",
    "hemorrhage":       "haemorrhage",
    "Alzheimer's":      "Alzheimer",
    "Parkinson's":      "Parkinson"
}



#清洗不需要的数据，保存为新的 database
def process_HGMD(filename):
    raw = pd.read_csv(filename)
    dataset = raw[["Variant_class","disease","genomic_coordinates_hg38","sequence_context_hg38"]]


#处理 Variant_class
def map_the_level(name):
    
    if name in NAME_LEVEL:
        return NAME_LEVEL[name]
    else:
        return 1

#处理 disease
def map_the_disease(name):
    name = name.lower()
    for disease in DISEASE_NAMES:
        if disease in name:
            name = name.replace(disease,DISEASE_NAMES[disease])
    return name


#创造疾病与 HITag 和 Group 的字典
def create_hitag_dic(HItage_file,other_HItage_file):
    tag_group_dict = dict()
    other_tag_group_dict = dict()

    HItag_dataset = pd.read_csv(HItage_file)
    other_HItage_dataset = pd.read_csv(other_HItage_file)

    def func_1(row):
        tag_group_dict[row["#Disease"].strip().lower()] = [row["#HITag"],row["Group"]]

    def func_2(row):
        other_tag_group_dict[row["#Disease"].strip().lower()] = [row["#HITag"],row["Group"]]    

    HItag_dataset.apply(func_1,axis = 1)
    other_HItage_dataset.apply(func_2,axis = 1)

    return tag_group_dict,other_tag_group_dict


#判断疾病属于哪个 tag 以及 group， 并添加这两项
def add_tag_group(row,tag_group_dict,other_tag_group_dict):
    for name,attrs in tag_group_dict.items():
        if name in row["disease"]:
            row["HITag"] = attrs[0]
            row["Group"] = attrs[1]
            return 

    for name,attrs in other_tag_group_dict.items():
        for _ in name.split(" "):
            if _ in row["disease"]:
                row["HITag"] = attrs[0]
                row["Group"] = attrs[1]
                return

    #print("can not find tag and group for: {}".format(row["disease"]))        
    return None

def main(database_file,HItage_file,other_HItage_file):
    
    dataset = pd.read_csv(database_file,index_col = 0)
    tag_group_dict,other_tag_group_dict = create_hitag_dic(HItage_file,other_HItage_file)
          
    #处理"Variant_class"
    dataset.loc[:,"Variant_class"] = dataset.loc[:,"Variant_class"].apply(map_the_level)
    #处理"disease"
    dataset.loc[:,"disease"] = dataset.loc[:,"disease"].apply(map_the_disease)

    dataset.loc[:,"HITag"] = None
    dataset.loc[:,"Group"] = None

    dataset.apply(func = add_tag_group,axis = 1,args = (tag_group_dict,other_tag_group_dict,))

    dataset.to_csv("new_database.csv")

        
    



if __name__ == '__main__':
    #filename = "HGMD_Advanced_Substitutions.csv"
    database_file = "database.csv"
    HItage_file = "HITAG.csv"
    other_HItage_file = "other_HITAG.csv"

    main(database_file,HItage_file,other_HItage_file)


       