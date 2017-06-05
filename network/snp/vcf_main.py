import pandas as pd

def process_vcf(filename):
    raw = pd.read_table(filename)
    dataset = raw[["#CHROM","POS","REF","ALT"]].dropna()
    print(dataset)



if __name__ == '__main__':
    filename = "SY.vcf"
    process_vcf(filename)    
