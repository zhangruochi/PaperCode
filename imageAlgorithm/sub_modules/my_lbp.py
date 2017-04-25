#encoding: utf-8
import os
from skimage.feature import local_binary_pattern
from PIL import Image
try:
    import ConfigParser
except ImportError:
    import configparser as ConfigParser   
    
import numpy as np
from sklearn.preprocessing import MinMaxScaler

#from matplotlib import pyplot as plt


class LBP(object):

    def get_options(self):
        cf = ConfigParser.ConfigParser()
        cf.read('config.cof')
        
        option_dict = dict()
        for key,value in cf.items("LBP"):
            option_dict[key] = eval(value)

        #print(option_dict)    
        return option_dict    
    
    def normalize(self,feature):
        
        normalizer = MinMaxScaler()
        normalized_feature = normalizer.fit_transform(feature)

        return normalized_feature

     

    def read_image(self,image_name,size = None):
        #读取配置文件
        option_dict = self.get_options()

        if size:    
            im = np.array(Image.open(image_name).convert("L").resize(size))
        else:
            im = np.array(Image.open(image_name).convert("L"))

        
        lbp = local_binary_pattern(im, option_dict["p"],
            option_dict["r"], option_dict["method"])

        if options["normalize"]:
            lbp = self.normalize(lbp)
        #plt.imshow(lbp)
        #plt.show()
        
        
        # return the histogram of Local Binary Patterns
        return normalized_lbp.reshape((1,lbp.shape[0]*lbp.shape[1]))[0]
       

         
if __name__ == '__main__':
    feature = LBP().read_image("../img_SUB/Gastric_polyp_sub/Erosionscromatosc_1_s.jpg")
    print(feature)
    #get_options()
