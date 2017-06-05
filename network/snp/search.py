#!/usr/bin/env python3

'''
python3

Required packages
- pandas
- sqlite3


Info
- name   : "zhangruochi"
- email  : "zrc720@gmail.com"
- date   : "2017.6.6"
- Version : 1.0.0

'''



import os
import pandas as pd
import sqlite3
import pickle
import sys



DATABASE = {}


def clean_vcf(filename):
    raw = pd.read_table(filename)
    dataset = raw[["#CHROM","POS","REF","ALT"]].dropna()
    return dataset






def main(database_filename,vcf_folder,vsersion):
    
    def func(row,c):
        nonlocal index
        nonlocal result

        #print(row.values.tolist())
        #exit()

        #if index % 1000 == 0:
        #    print("having been searching {}".format(index))


        for record in c.execute('SELECT * FROM snp_disease_{}  WHERE "#CHROM" = "{}" AND ("POS_START" <= {} AND "POS_END" >= {})'.format(vsersion,row["#CHROM"],int(row["POS"]) + 5,int(row["POS"]) - 5)):
            result.append([row.values.tolist(),record])


        index += 1    

    conn = sqlite3.connect(database_filename)
    c = conn.cursor()

    for vcf_filename in os.listdir(vcf_folder):
        if not vcf_filename.endswith(".vcf"):
            continue
        
        full_path_name = os.path.join(vcf_folder,vcf_filename)
    
        vcf_dataset = clean_vcf(full_path_name)
        print("precessing the {} which have {} entries..".format(vcf_filename,vcf_dataset.shape[0]))

        
        index = 0
        result = []

        #遍历样本的每条染色体的每个位点，看是否存在与 disease 数据库存在交叠的区域
        vcf_dataset.apply(func = func,axis = 1, args =(c,))


        """
        with open("result.pkl","wb") as f:
            pickle.dump(result,f)
            

        with open("result.pkl","rb") as f:
            records = pickle.load(f) 

               

        for record in result:
            print(record[0])
            print(record[1])
            print("\n")
        """
        
        if not os.path.exists("result"):
            os.mkdir("result")    

        name = vcf_filename.replace(".","_")
        with open("result/{}_result.txt".format(name),"w") as f:
            for record in result:
                f.write(str(record[0]))  
                f.write("\n")
                f.write(str(record[1]))
                f.write("\n\n")  

    c.close()
    conn.close()            
    print("finished.......")



if __name__ == '__main__':
    

    """
    命令行参数接口:

        database_filename:   数据库名称
        vcf_folder:          vcf文件所在的文件夹
        version:             选择测序版本号
    """    



    database_filename = sys.argv[1]
    vcf_folder = sys.argv[2]
    version = sys.argv[3]
    
    main(database_filename,vcf_folder,version)
    #clean_vcf(filename)    
