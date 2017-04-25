import os
from skimage.feature import greycomatrix
from skimage.feature import greycoprops
from PIL import Image

try:
    import ConfigParser
except ImportError:
    import configparser as ConfigParser 

from sklearn.preprocessing import MinMaxScaler
import numpy as np



class GLCM(object):

    def __str__(self):
        return "\nUsing the algorithm GLCM.....\n"


    def get_options(self):
        cf = ConfigParser.ConfigParser()
        cf.read("config.cof")
        
        option_dict = dict()

        for key,value in cf.items("GLCM"):
            option_dict[key] = eval(value)

        #print(option_dict)    
        return option_dict
    

    def get_block(self,im,n):
        x = int(im.shape[0]/n)
        y = int(im.shape[1]/n)
        block_list = []
        
        start_x = 0
        end_x = x

        for i in range(n):
            start_y = 0
            end_y = y
            for j in range(n):
                block_list.append(im[start_x:end_x,start_y:end_y])
                start_y = end_y
                end_y += y

            start_x = end_x
            end_x += x   
           
        return block_list        
                
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
        block_list = self.get_block(im,options["block_num"]) 
        feature_list = []
        for block in block_list:
            feature_matrix = greycomatrix(block,options["distances"],options["angles"],options["levels"],options["symmetric"],options["normed"])
            feature_2D = greycoprops(feature_matrix,options["prop"])
            if feature_2D.shape[0] >= 2 and feature_2D.shape[1] >= 2:
                feature_2D = feature_2D.reshape((1,feature_2D.shape[0]*feature_2D.shape[1]))   
            feature_list.append(feature_2D[0])

        feature_list_matrix = np.array(feature_list)
        if options["normalize"]:
            feature_list_matrix = self.normalize(feature_list_matrix)

        return feature_list_matrix.reshape((1,feature_list_matrix.shape[0]*feature_list_matrix.shape[1]))[0]      


if __name__ == '__main__':
    feature = GLCM().read_image("../Img_sub/Gastric_polyp_sub/Erosionscromatosc_1_s.jpg")
    print(feature)
    #get_options()
