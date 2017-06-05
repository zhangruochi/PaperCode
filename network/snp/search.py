import os
import pandas as pd
import sqlite3



DATABASE = {}

def process_vcf(filename):
    raw = pd.read_table(filename)
    dataset = raw[["#CHROM","POS","REF","ALT"]].dropna()
    print(dataset)



def creat_dict(database_filename):
    conn = sqlite3.connect(database_filename)
    c = conn.cursor()
    for row in c.execute("SELECT * FROM snp_disease"):
        print(row)


    



if __name__ == '__main__':
    filename = "SY.vcf"
    database_filename = "SNP.db"
    creat_dict(database_filename)
    #process_vcf(filename)    
