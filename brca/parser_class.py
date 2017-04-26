import json
import pandas as pd
from collections import defaultdict

#TCGA-A8-A07E 


#解析 json 文件， 得到样本和样本stage的对应dict
def get_name_sample_dict(json_filename):
    with open(json_filename,"r") as f:
        dataset = json.load(f)
        #print(type(dataset))

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


#测试是不是存在名称相同的样本
def test_exist(samples):
    exist_sample = defaultdict(int)
    for sample in samples:
        exist_sample[sample] += 1

    for sample, num in exist_sample.items():
        if num != 1:
            print(sample)  


#加载需要训练数据集的类标
def load_sample(dataset_filename):
    with open(dataset_filename) as f:
        samples = f.readline().split()     
        #test_exist(samples)

        samples = [sample[0:12] for sample in samples]

        return samples



#得到有用的样本及其类标
def get_labels(dataset_filename,json_filename):
    labels = []
    name_sample_dict = get_name_sample_dict(json_filename)
    samples = load_sample(dataset_filename)
    sample_mask = []   #正确样本的 mask

    index = 0
    for sample_name in samples:
        if sample_name in name_sample_dict:
            sample_mask.append(index)
            labels.append(name_sample_dict[sample_name])
        #不存在 stage 的样本
        #else:
        #    print(sample_name)  
        index += 1

    #print("the num of samples: " + str(len(sample_mask)))    
    #print("the valid num of samples: " + str(len(labels)))

    return sample_mask,labels







if __name__ == '__main__':
    get_labels("matrix_data.tsv","clinical.project-TCGA-BRCA.2017-04-20T02_01_20.302397.json")

                    





                 