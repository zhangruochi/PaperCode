import warnings
warnings.filterwarnings("ignore")

from sklearn.decomposition import PCA

try:
    import ConfigParser
except ImportError:
    import configparser as ConfigParser   
  
import os
import numpy as np
import time
from functools import partial
import multiprocessing
import pandas as pd
import gzip 


try:
    import cPickle as pickle
except ImportError:
    import pickle


from sub_modules import my_hog
from sub_modules import my_lbp



def proxy(cls_instance,algorithm,size,image_path):
    return cls_instance.work(algorithm,size,image_path)


class ImageProcess(object):
    def __init__(self):
        self.option_dict = self.get_options()
        #print(self.option_dict)     

    #configure file 
    def get_options(self):
        cf = ConfigParser.ConfigParser()
        cf.read('config.cof')
        
        option_dict = dict()
        for key,value in cf.items("main"):
            option_dict[key] = eval(value)

        return option_dict

    #select algorithm
    def get_algorithm(self):
        algorithms = []
        for algorithm in self.option_dict["algorithm"]:
            if algorithm == "HOG":
                algorithms.append(my_hog.HOG())
            if algorithm == "LBP":
                algorithms.append(my_lbp.LBP())    
            
        return algorithms          

    #image read function
    def image_read(self,algorithm):
        print("using single process to dealing with pictures.......\n")
        feature_list = []
        name_list = []

        if self.option_dict["image_size"]:
            size = self.option_dict["image_size"]
            #print(size);exit()
        else:
            size = None
            
        for file in os.listdir(self.option_dict["folder"]):
            if file.split(".")[-1] in self.option_dict["image_format"]:  
                print("read image: {}".format(file))
                name_list.append(file)     
                feature = algorithm.read_image(os.path.join(self.option_dict["folder"],file),size)
                feature_list.append(feature)

        feature_list = np.array(feature_list)    
                
        return feature_list,name_list


    #merge the features from different algorithms
    def merge_dataset(self):

        dataset_index = 0 
        algorithm_list = self.get_algorithm()

        if self.option_dict["njob"] == 1:
            for algorithm in algorithm_list:
                print(algorithm)
                if dataset_index == 0:
                    left,name_list = self.image_read(algorithm)
                    dataset_index += 1    
                    #print(left.shape)
                else:
                    left = np.hstack((left,self.image_read(algorithm)[0]))
                    #print(left.shape)

        elif self.option_dict["njob"] > 1:
            for algorithm in algorithm_list:
                dataset = self.multiprocessing_read(algorithm)
                if dataset_index == 0:
                    left,name_list = self.image_read(algorithm)
                    dataset_index += 1    
                else:
                    left = np.hstack((left,self.image_read(algorithm)[0]))
        else:
            print("you should write the true value of njob")     


        if self.option_dict["pca"]:
            left = implement_pca(left)               

        dataset = pd.DataFrame(data = left,index= name_list,columns= list(range(left.shape[1])))  
        
        return dataset  
            

    def work(self,algorithm,size,image_path):
        feature = algorithm.read_image(image_path,size)
        image_name = os.path.split(image_path)[-1]
        
        return (feature,image_name)


    #multiprocessing the images   
    def multiprocessing_read(self,algorithm):
        print("using multiprocesses to deal with pictures......\n")
        
        feature_list = []
        if self.option_dict["image_size"]:
            size = self.option_dict["image_size"]
            #print(size);exit()
        else:
            size = None

        work = partial(proxy,self,algorithm,size)
           
        pool = multiprocessing.Pool(self.option_dict["njob"])
        image_path_list = [os.path.join(self.option_dict["folder"],name) for name \
                in os.listdir(self.option_dict["folder"]) if name.split(".")[-1] in self.option_dict["image_format"]]
        result = pool.map(work,image_path_list) 

        feature_list = np.array([item[0] for item in result])
        name_list = np.array([item[1] for item in result])

        dataset = pd.DataFrame(data = feature_list.T,index = list(range(feature_list.shape[1])), columns = name_list)


        return dataset

    
    def save_dataset(self,saving_name,dataset):
        format_list = self.option_dict["save_format"]

        if "csv" in format_list:
            dataset.to_csv("{}.csv".format(saving_name))

        if "pickle" in format_list:
            dataset.to_pickle("{}.pkl".format(saving_name))

        if "json" in format_list:
            dataset.to_json("{}.json".format(saving_name))        

        if "gzip" in format_list:
            file = gzip.GzipFile("{}.pkl.zip".format(saving_name), 'wb')
            pickle.dump(dataset, file, -1)
            file.close()       

        print("\nSaving features file successful!\n")         
        

    def run(self):
        dataset = self.merge_dataset()
        print("\nGetting {} samples, every sample has {} features".format(dataset.shape[0],dataset.shape[1]))
        #print(dataset.shape)   #"[sample,feature]"
        saving_name = os.path.split(self.option_dict["folder"])[-1]
        self.save_dataset(saving_name,dataset) 



if __name__ == '__main__':
    processor = ImageProcess() 
    processor.run()       



