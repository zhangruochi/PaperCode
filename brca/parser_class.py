import json
import pandas as pd

#TCGA-A8-A07E 

def get_name_sample_dict():
    with open("clinical.project-TCGA-BRCA.2017-04-20T02_01_20.302397.json","r") as f:
        dataset = json.load(f)
        print(type(dataset))

        names_classes = dict()

        for _ in dataset:
            for key,value in _.items():
                if key == "diagnoses":
                    sample_id = value[0]["submitter_id"].strip("_diagnosis")
                    stage = value[0]["tumor_stage"].replace("stage ","")
                    if not "i" in stage:
                        continue

                    if stage[-1] != "i":
                        stage = stage[:-1]

                    if len(stage) > 4 or len(stage) < 1:
                        continue

                    names_classes[sample_id] = len(stage) 
                    continue      
        
        #print(names_classes)    
    return names_classes


def load_sample():
    with open("matrix_data.tsv") as f:
        samples = f.readline().split()     
        #print(samples)  
        samples = [sample[0:12] for sample in samples]
        #print(samples)
        return samples




def get_labels():
    labels = []
    name_sample_dict = get_name_sample_dict()
    samples = load_sample()
    print("the num of samples: " + str(len(samples)))
    valid_samples = []

    for sample_name in samples:
        if sample_name in name_sample_dict:
            valid_samples.append(sample_name)
            labels.append(name_sample_dict[sample_name])
        else:
            print(sample_name)    
        
    print("the valid num of samples: " + str(len(labels)))

    return valid_samples,labels







if __name__ == '__main__':
    get_labels()
                    





                 