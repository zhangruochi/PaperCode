#encoding: utf-8
import os
from skimage.feature import local_binary_pattern
from PIL import Image
import ConfigParser 
import numpy as np


class LBP(object):

    def get_options(self):
        cf = ConfigParser.ConfigParser()
        cf.read('config.cof')
        
        option_dict = dict()
        for key,value in cf.items("LBP"):
            option_dict[key] = eval(value)

        #print(option_dict)    
        return option_dict    
     

     

    def read_image(self,image_name,size):
        #读取配置文件
        option_dict = self.get_options()

        eps = 1e-7

        if size:    
            im = np.array(Image.open(image_name).convert("L").resize(size))
        else:
            im = np.array(Image.open(image_name).convert("L"))

        
        lbp = local_binary_pattern(im, option_dict["p"],
            option_dict["r"], option_dict["method"])
        (hist, _) = np.histogram(lbp.ravel(),
            bins=np.arange(0, option_dict["p"] + 3),
            range=(0, option_dict["p"] + 2))
 
        # normalize the histogram
        hist = hist.astype("float")
        hist /= (hist.sum() + eps)
        
        # return the histogram of Local Binary Patterns
        return hist
       

         

if __name__ == '__main__':
    LBP().read_image("2.jpg",(500,500))
    #get_options()