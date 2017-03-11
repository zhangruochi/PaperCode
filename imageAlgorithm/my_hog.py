import os
from skimage.feature import hog
from PIL import Image
import configparser
import numpy as np


class HOG(object):

    def get_options(self):
        cf = configparser.ConfigParser()
        cf.read('config.cof')
        
        option_dict = dict()
        for key,value in cf.items("HOG"):
            option_dict[key] = eval(value)

        #print(option_dict)    
        return option_dict    
     

    def read_image(self,image_name,size):
        #读取配置文件
        options = self.get_options()

        if size:    
            im = np.array(Image.open(image_name).convert("L").resize(size))
        else:
            im = np.array(Image.open(image_name).convert("L"))

        options["image"] = im    
    
        feature = hog(**options)
        return feature        

         

if __name__ == '__main__':
    HOG().read_image("2.jpg",(500,500))
    #get_options()
