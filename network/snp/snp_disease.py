import pandas as pd
import numpy as np
from collections import defaultdict
import os
import re
import sqlite3


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
    dataset = raw[["Variant_class","disease","genomic_coordinates_hg19","sequence_context_hg19"]]
    dataset.to_csv("database.csv")


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

    line = row["genomic_coordinates_hg19"].split(":")

    for name,attrs in tag_group_dict.items():
        if name in row["disease"]:
            return [row["genomic_coordinates_hg19"],name,line[0],int(line[1]),attrs[0],attrs[1]]

    for name,attrs in other_tag_group_dict.items():
        for _ in name.split(" "):
            if _ in row["disease"]:
                return [row["genomic_coordinates_hg19"],_,line[0],int(line[1]),attrs[0],attrs[1]]


    #print("can not find tag and group for: {}".format(row["disease"])) 
    return [np.nan,np.nan,np.nan,-1,np.nan,np.nan]  


def add_variance(row,pattern):
    ref_alt = re.search(pattern,row["sequence_context_hg19"]).group().strip("[").strip("]").split("/")
    return [row["sequence_context_hg19"],ref_alt[0],ref_alt[1]]




def data_cleaning(database_file,HItage_file,other_HItage_file):

    if not os.path.exists("snp_disease.sql"):
    
        if not os.path.exists("new_database.csv"):
            dataset = pd.read_csv(database_file,index_col = 0).dropna()
            tag_group_dict,other_tag_group_dict = create_hitag_dic(HItage_file,other_HItage_file)
                  
            #处理"Variant_class"
            dataset.loc[:,"Variant_class"] = dataset.loc[:,"Variant_class"].apply(map_the_level)
            #处理"disease"
            dataset.loc[:,"disease"] = dataset.loc[:,"disease"].apply(map_the_disease)


            dataset.loc[:,"#CHROM"] = np.nan
            dataset.loc[:,"POS"] = np.nan
            dataset.loc[:,"HITag"] = np.nan
            dataset.loc[:,"Group"] = np.nan

            dataset.loc[:,["genomic_coordinates_hg19","disease","#CHROM","POS","HITag","Group"]] = dataset.loc[:,["genomic_coordinates_hg19","disease","#CHROM","POS","HITag","Group"]].apply(func = add_tag_group,axis = 1, args = (tag_group_dict,other_tag_group_dict,))
            dataset.to_csv("new_database.csv")

        else:
            dataset = pd.read_csv("new_database.csv",index_col = 0).dropna().reset_index(drop = True)
            pattern = re.compile("\[\w+\/\w+\]")
            dataset.loc[:,"REF"] = np.nan
            dataset.loc[:,"ALT"] = np.nan
            dataset.loc[:,["sequence_context_hg19","REF","ALT"]] = dataset.loc[:,["sequence_context_hg19","REF","ALT"]].apply(func = add_variance, axis = 1, args = (pattern,))
            dataset = dataset.drop(labels = ["genomic_coordinates_hg19","sequence_context_hg19"],axis = 1)
            dataset = dataset[['disease', '#CHROM', 'POS', 'REF','ALT','Variant_class', 'HITag', 'Group']]
            dataset.to_csv("snp_disease.csv")

            conn = sqlite3.connect('SNP.db')
            conn.execute("DROP TABLE IF EXISTS snp_disease")
            
            dataset.to_sql("snp_disease",con = conn)
    else:       
        pass     



if __name__ == '__main__':
    #filename = "HGMD_Advanced_Substitutions.csv"
    #process_HGMD(filename)
    #exit()
    database_file = "database.csv"
    HItage_file = "HITAG.csv"
    other_HItage_file = "other_HITAG.csv"

    data_cleaning(database_file,HItage_file,other_HItage_file)


       