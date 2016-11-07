import os
from PIL import Image
import numpy as np
from scipy.ndimage import filters
from math import ceil
from math import pi


#主函数
def main():
    image_folder = "Gastric_polyp_Sub"
    result_list = []

    for filename in os.listdir(image_folder):
        if filename.endswith(".jpg"):
            im = np.array(Image.open(os.path.join(image_folder,filename)).convert("L"))
            magnitude,direction = get_magnitude(im)
            all_start_point,chunk_size = get_all_start_point(magnitude)
            exit()
            for start_point in all_start_point:
                raw_feature_list = get_chunk_feature(start_point,chunk_size,magnitude,direction)
                feature_list = transform_feature(raw_feature_list)
                result_list.append(feature_list)

    feature_matrix = np.array(result_list)            


            

#根据像素矩阵得到梯度矩阵以及相应的值的矩阵
def get_magnitude(im,sigma = 5):
    #sigma 标准差
    imx = np.zeros(im.shape)
    filters.gaussian_filter(im, (sigma,sigma), (0,1), imx)
    imy = np.zeros(im.shape)
    filters.gaussian_filter(im, (sigma,sigma), (1,0), imy)
    magnitude = np.sqrt(imx**2+imy**2)
    direction = np.arctan(imy/imx)
    
    return magnitude,direction


def get_all_start_point(magnitude,scale_factor = 10):
    center_point = ( ceil(magnitude.shape[0] / 2.0),ceil(magnitude.shape[1] / 2.0) )
    print("the center point:",center_point)
    width,length = chunk_size =  magnitude.shape[0] // scale_factor, magnitude.shape[1] // scale_factor
    print("chunk_size:",chunk_size)
    
    all_start_point = []
    for circle in range(1,scale_factor+1):
        if circle == 1 :
            start_point = ( center_point[0] - int(width / 2.0), center_point[1] - int(length / 2.0))
            print(start_point)
            all_start_point.append(start_point)
        else:
            #左上
            start_point_left_up = (center_point[0] - ( width * circle - ceil(width / 2.0)),center_point[1] - ( length * circle - ceil(length / 2.0)))
            for i in range(circle):
                all_start_point.append((start_point_left_up[0] + i * width,start_point_left_up[1]))
            #左下
            start_point_left_down = (center_point[0] - ( width * circle - ceil(width / 2.0)),center_point[1] + ( length * circle - ceil(length / 2.0)))
            for i in range(circle):
                all_start_point.append( (start_point_left_down[0],start_point_left_down[1] - circle * length ))
            #右上
            start_point_right_up = (center_point[0] + ( width * circle - ceil(width / 2.0)),center_point[1] - ( length * circle - ceil(length / 2.0))) 
            for i in range(circle):
                all_start_point.append(( start_point_right_up[0],start_point_right_up[1] + circle * length))
            #右下
            start_point_right_down =  (center_point[0] + ( width * circle - ceil(width / 2.0)),center_point[1] + ( length * circle - ceil(length / 2.0)))   
            for i in range(circle):
                all_start_point.append((start_point_right_down[0] - i * width, start_point_right_down[1]))

    return all_start_point,chunk_size
                



        


#根据每个块的起始点得到这个块中所有的像素  生成列别返回
def get_chunk_feature(start_point,chunk_size,magnitude,direction):
    raw_feature_list = []
    for x in range(start_point[0],start_point[0]+chunk_size[0]):
        for y in range(start_point[1],start_point[1] + chunk_size[1]):
            raw_feature_list.append((direction[x][y],magnitude[x][y]))
    
    return  raw_feature_list           


#统计每个梯度范围各有多少个  得到每个梯度中所有值的和  生成特征向量并返回
def transform_feature(raw_feature_list,k=9):
    from collections import defaultdict
    feature_dict = defaultdict(list) 
    result_list = []

    every_component =  pi / k 
    
    #magnitude = feature[1]
    for feature in raw_feature_list:
        index = 0
        start = 0
        end = every_component
        while True:
            if(feature[1] >= start and feature[1] < end):
                feature_dict[index].append(feature[0])
                break

            start = end
            end += every_component
            index += 1

    for k,values in feature_dict.items():
        result_list.append(sum(values))

    return result_list


                
                













    






            
if __name__ == '__main__':
    main()

