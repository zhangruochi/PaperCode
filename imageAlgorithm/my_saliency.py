#encoding: utf-8
import os
from PIL import Image
import ConfigParser 
import numpy as np
import cv2
import pySaliencyMap


class SALIENCY(object):

    """
    def get_options(self):
        cf = ConfigParser.ConfigParser()
        cf.read('config.cof')
        
        option_dict = dict()

        for key,value in cf.items("SALIENCY"):
            option_dict[key] = eval(value)

        #print(option_dict)    
        return option_dict
    """


    def read_image(self,image_name,size):
        #读取配置文件
        #options = self.get_options()

        if size:    
            im = np.array(Image.open(image_name).resize(size))
        else:
            im = np.array(Image.open(image_name))


        sm = pySaliencyMap.pySaliencyMap(im.shape[1], im.shape[0])
        
        #binarized_map = sm.SMGetBinarizedSM(im)  
        #salient_region = sm.SMGetSalientRegion(im)
        saliency_map = sm.SMGetSM(im)
        feature = np.resize(saliency_map,(size[0]*size[1]))

        #print(saliency_map.shape)
        #print(feature.shape)
        return feature       

         

if __name__ == '__main__':
    SALIENCY().read_image("2.jpg",(500,500))
    #get_options()
