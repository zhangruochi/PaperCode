#encoding: utf-8
import os
from skimage.feature import ORB, match_descriptors
from PIL import Image
import ConfigParser 
import numpy as np




class MYORB(object):

    def get_options(self):
        cf = ConfigParser.ConfigParser()
        cf.read('config.cof')
        
        option_dict = dict()

        for key,value in cf.items("ORB"):
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

        detector_extractor = ORB(**options)
        detector_extractor.detect_and_extract(im)
        orb_feature = detector_extractor.scales

        feature = orb_feature / (sum(orb_feature) + eps) 
        print(feature)
        
        return feature        

         

if __name__ == '__main__':
    MYORB().read_image("2.jpg",(500,500))
    #get_options()
