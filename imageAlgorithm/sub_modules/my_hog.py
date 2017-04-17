import os
from skimage.feature import hog
from PIL import Image

try:
    import ConfigParser
except ImportError:
    import configparser as ConfigParser 

import numpy as np


class HOG(object):

    def __str__(self):
        return "\nUsing the algorithm HOG.....\n"


    def get_options(self):
        cf = ConfigParser.ConfigParser()
        cf.read("config.cof")
        
        option_dict = dict()

        for key,value in cf.items("HOG"):

            option_dict[key] = eval(value)

        #print(option_dict)    
        return option_dict
    


    def read_image(self,image_name,size = None):
        options = self.get_options()

        if size:    
            im = np.array(Image.open(image_name).convert("L").resize(size))
        else:
            im = np.array(Image.open(image_name).convert("L"))

        options["image"] = im    
        feature = hog(**options)

        return feature        


if __name__ == '__main__':
    feature = HOG().read_image("../img_SUB/Gastric_polyp_sub/Erosionscromatosc_1_s.jpg")
    print(feature.shape)
    #get_options()
