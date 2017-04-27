from parser_class import get_labels
import pandas as pd


#valid_samples,labels = get_labels()
#print(valid_samples)
#print(labels)

def load_dataset(dataset_filename,json_filename):
    dataset = pd.read_csv(dataset_filename,"\t",index_col = 0)
    print("raw_dataset: ",str(dataset.shape))

    mask,labels = get_labels(dataset_filename,json_filename)
    filtered_dataset = dataset.iloc[:,mask].fillna(method = "backfill")
    
    print("filtered_dataset: " + str(filtered_dataset.shape))
    print("raw filtered_labels: "+ str(len(labels)))

    return filtered_dataset,labels


if __name__ == '__main__':
    load_dataset("matrix_data.tsv","clinical.project-TCGA-BRCA.2017-04-20T02_01_20.302397.json")    
