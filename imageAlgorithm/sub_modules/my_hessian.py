import os
from skimage.feature import hessian_matrix_det
from PIL import Image

try:
    import ConfigParser
except ImportError:
    import configparser as ConfigParser 

import numpy as np

#from matplotlib import pyplot as plt


class HESSIAN(object):

    def __str__(self):
        return "\nUsing the algorithm Hessian Matrix.....\n"


    def get_options(self):
        cf = ConfigParser.ConfigParser()
        cf.read("../config.cof")
        
        option_dict = dict()

        for key,value in cf.items("HESSIAN"):

            option_dict[key] = eval(value)

        #print(option_dict)    
        return option_dict

    def normalize(self,feature):
        
        normalizer = MinMaxScaler()
        normalized_feature = normalizer.fit_transform(feature)

        return normalized_feature    
    


    def read_image(self,image_name,size = None):
        options = self.get_options()

        if size:    
            im = np.array(Image.open(image_name).convert("L").resize(size))
        else:
            im = np.array(Image.open(image_name).convert("L"))

        options["image"] = im    
        feature = hessian_matrix_det(**options)

        if options["normalize"]:
            feature = self.normalize(feature)

        #plt.imshow(feature)
        #plt.show()


        return feature.reshape((1,feature.shape[0]*feature.shape[1]))[0]        


if __name__ == '__main__':
    feature = HESSIAN().read_image("../img_SUB/Gastric_polyp_sub/Erosionscromatosc_1_s.jpg")
    print(feature)
    #get_options()
