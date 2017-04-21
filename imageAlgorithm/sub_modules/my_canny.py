import os
from skimage.feature import canny
from PIL import Image

try:
    import ConfigParser
except ImportError:
    import configparser as ConfigParser 

import numpy as np

#from matplotlib import pyplot as plt


class CANNY(object):

    def __str__(self):
        return "\nUsing the algorithm Canny.....\n"


    def get_options(self):
        cf = ConfigParser.ConfigParser()
        cf.read("config.cof")
        
        option_dict = dict()

        for key,value in cf.items("CANNY"):

            option_dict[key] = eval(value)

        #print(option_dict)    
        return option_dict
    

    def bool_num_converter(self,bool_feature):
        num_matrix = np.zeros((bool_feature.shape[0],bool_feature.shape[1]))
        num_matrix[bool_feature == False] = 0
        num_matrix[bool_feature == True] = 1
        return num_matrix


    def read_image(self,image_name,size = None):
        options = self.get_options()

        if size:    
            im = np.array(Image.open(image_name).convert("L").resize(size))
        else:
            im = np.array(Image.open(image_name).convert("L"))
   
        options["image"] = im  
        bool_feature = canny(**options)
        feature = self.bool_num_converter(bool_feature)
        #plt.imshow(feature)
        #plt.show()


        return feature.reshape((1,feature.shape[0]*feature.shape[1]))[0]     

if __name__ == '__main__':
    feature = CANNY().read_image("../img_SUB/Gastric_polyp_sub/Erosionscromatosc_1_s.jpg")
    #print(feature.shape)
    #get_options()
