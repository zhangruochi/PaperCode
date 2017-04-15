#encoding: utf-8
import os
from skimage.feature import CENSURE
from PIL import Image
import ConfigParser 
import numpy as np




class MYCENSURE(object):

    def get_options(self):
        cf = ConfigParser.ConfigParser()
        cf.read('config.cof')
        
        option_dict = dict()

        for key,value in cf.items("CENSURE"):
            option_dict[key] = eval(value)

        #print(option_dict)    
        return option_dict
    


    def read_image(self,image_name,size):
        #读取配置文件
        options = self.get_options()
        eps = 1e-7

        if size:    
            im = np.array(Image.open(image_name).convert("L").resize(size))
        else:
            im = np.array(Image.open(image_name).convert("L"))
        
        
        censure = CENSURE(**options)
        censure.detect(im)
        censure_feature = censure.scales 
        feature = censure_feature / (sum(censure_feature) + eps ) 
        
        print(feature.shape)


        return feature        

         

if __name__ == '__main__':
    MYCENSURE().read_image("1.jpg",(200,200))
    #get_options()
