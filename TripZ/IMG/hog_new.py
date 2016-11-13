'''
python3

Required packages
- pandas
- numpy
- sklearn
- scipy
- PIL


Info
- name   : "zhangruochi"
- email  : "zrc720@gmail.com"
- date   : "2016.11.09"
- Version : 2.0.0

Description
    New HOG
'''


import os
from PIL import Image
import numpy as np
from scipy.ndimage import filters
from math import ceil
from math import pi
from collections import defaultdict
from operator import itemgetter
import pickle


from sklearn.svm import SVC
from sklearn.naive_bayes import GaussianNB
from sklearn.neighbors import KNeighborsClassifier
from sklearn.tree import DecisionTreeClassifier
from sklearn.linear_model import LogisticRegression
from sklearn.cross_validation import cross_val_score


#根据像素矩阵得到梯度矩阵以及相应的值的矩阵
def get_magnitude(im,sigma = 5):
    #sigma 标准差
    imx = np.zeros(im.shape)
    filters.gaussian_filter(im, (sigma,sigma), (0,1), imx)
    imy = np.zeros(im.shape)
    filters.gaussian_filter(im, (sigma,sigma), (1,0), imy)
    magnitude = np.sqrt(imx**2+imy**2)
    direction = np.arctan(imy/imx)
    
    direction = np.nan_to_num(direction)
    
    return magnitude,direction


#得到图片中所有块的起始点
def get_all_start_point(magnitude,scale_factor = 5):   # scale_factor 表示取多少圈
    center_point = ( ceil(magnitude.shape[0] / 2.0),ceil(magnitude.shape[1] / 2.0) )
    width,length = chunk_size =  magnitude.shape[0] // (scale_factor * 2 -1), magnitude.shape[1] // (scale_factor * 2 -1 )
    '''
    print("image size:",magnitude.shape)
    print("the center point:",center_point)
    print("chunk_size:",chunk_size)
    '''
    all_start_point = []
    temp_start_point = []
    increment = 1
    for circle in range(0,scale_factor):

        if circle == 0 :
            start_point = ( center_point[0] - (ceil(width/2.0) - 1), center_point[1] - (ceil(length / 2.0) - 1))
            all_start_point.append([start_point])
        else:
            temp_start_point = []
            #左上
            start_point_left_up = (center_point[0] - width * circle - (ceil(width/2.0) - 1),center_point[1] - length * circle - (ceil(length / 2.0) - 1))
            for i in range(circle + increment):
                temp_start_point.append((start_point_left_up[0] + i * width,start_point_left_up[1]))
                #print(circle + 1)
                #print(temp_start_point)

            #右上
            start_point_right_up = (center_point[0] + width * (circle-1) +  int(width / 2.0) + 1, center_point[1] -  length * circle - (ceil(length / 2.0) - 1))
            for i in range(circle + increment):
                temp_start_point.append(( start_point_right_up[0],start_point_right_up[1] + i * length)) 
                #print(circle + 1)
                #print(temp_start_point)   

            #左下
            start_point_left_down = (center_point[0] - width * circle - (ceil(width/2.0) - 1),center_point[1] - length *(circle - 1) - (ceil(length / 2.0) - 1))
            for i in range(circle + increment):
                temp_start_point.append((start_point_left_down[0],start_point_left_down[1] + i * length ))
                #print(circle + 1)
                #print(temp_start_point) 
            
            #右下
            start_point_right_down =  (center_point[0] - width * (circle - 1) - (ceil(width/2.0) - 1), center_point[1] + length * (circle-1) + int(length / 2.0) + 1) 

            for i in range(circle + increment):
                temp_start_point.append((start_point_right_down[0] + i * width, start_point_right_down[1]))
                #print(circle + 1)
                #print(temp_start_point)

            all_start_point.append(temp_start_point)     

            increment += 1    
    
    #print(all_start_point)        
    return all_start_point,chunk_size
                

#根据每个块的起始点得到这个块中所有的像素和对应的值  生成列表返回
def get_chunk_feature(all_start_point,chunk_size,magnitude,direction):
    raw_feature_list = []  #包含所有的转
    for circle in all_start_point:
        temp_circle_list = [] #包含每一转所有的块
        for start_point in circle:
            temp_point_list = []  #包含每一块所有的点
            for x in range(start_point[0],start_point[0]+chunk_size[0]):
                for y in range(start_point[1],start_point[1] + chunk_size[1]):
                    temp_point_list.append((direction[x-1][y-1],magnitude[x-1][y-1]))    #下标从0开始
            temp_circle_list.append(temp_point_list)        
        raw_feature_list.append(temp_circle_list)      

    
    '''
    #测试保留多少个点
    count = 0
    for circle in raw_feature_list:
        for chunk in circle:
            for point in chunk:
                count += 1
    print(count)            
    exit()
    '''
    
    return  raw_feature_list           


#统计每个梯度范围各有多少个  得到每个梯度中所有值的和  生成特征向量并返回
def transform_feature(raw_feature_list,k=9):
    result_list = []
    every_component =  pi / k 

    for circle in raw_feature_list:
        temp_circle_list = []  #每一个圈所有的块特征
        
        for chunk in circle: 
            feature_dict = defaultdict(list) 
            for point in chunk:   #每块中所有的像素点
                start = -pi / 2
                end = -pi / 2 + every_component
                index = 0
                while True:
                    if(point[0] >= start and point[0] < end):
                        feature_dict[index].append(point[0])
                        break
                    start = end
                    end += every_component
                    index += 1
            temp_circle_list.append(feature_dict)
        result_list.append(temp_circle_list)    

    '''
    for circle in result_list:
        index = 0
        for feature in circle:
            index += 1
            print(feature.keys())
        print(index)    
    exit()    
    '''
    result_dict = defaultdict(list)
    for index,circle in enumerate(result_list):
        temp_point_list = []
        for chunk in circle:
            feature = []
            for i in range(k):
                feature.append(sum(chunk[i]))
            #print(len(feature)) 
            temp_point_list.append(feature)
        result_dict[index] = temp_point_list    
    
    return result_dict  #{0: [[0, 0, 0, 0, 0, 0, 0.8663430286598629, 20.413658681311983, 15.831469133521393]], 1:.....
 

#排序辅助函数  #[-29.028116197759918, 0, 0, 0, 0, 0, 0, 0, 17.823901735969809]
def sort_list(list_,chunk_size):
    return_list = []
    temp_dict = dict()
    for feature_list in list_:
        value = sum(feature_list) / (chunk_size[0] * chunk_size[1])
        temp_dict[value] = feature_list

    return_list = sorted(temp_dict.values(),key = itemgetter(0))  # 根据每个 list 对应的 value 值排序
    return return_list    



#得到排序后的特征
def sort_feature(feature_dict,chunk_size):
    feature = []
    chunk_feature = []
    for key,list_ in feature_dict.items():
        if key == 1:
            chunk_feature += list_
        else:
            chunk_feature += sort_list(list_,chunk_size)

    for list_ in chunk_feature:
        feature += list_

    #print(len(feature))        
    #exit()       
    return feature        

    
def get_feature(foldername,degree = None, factor = None):
    image_folder = foldername
    all_feature = []
    for filename in sorted(os.listdir(image_folder)):
        if filename.endswith(".jpg"):
            print(filename)
            im = Image.open(os.path.join(image_folder,filename))
            
            if degree:
                im = im.rotate(degree)
            if factor:
                size = im.size[0] / factor, im.size[1] / factor
                im.thumbnail(size)    

            im = np.array(im.convert("L"))    

            magnitude,direction = get_magnitude(im)

            all_start_point,chunk_size = get_all_start_point(magnitude)  #[[(20, 35)], [(16, 27), (20, 27), (24, 27), (24, 35), (16, 35), (16, 43), (20, 43), (24, 43)], [(12, 19), (16, 19),......
            raw_feature_list = get_chunk_feature(all_start_point,chunk_size,magnitude,direction)
            feature_dict = transform_feature(raw_feature_list)

            feature = sort_feature(feature_dict,chunk_size)  #得到排序后的最终特征向量
        all_feature.append(feature)    
    feature = np.array(all_feature)

    with open("{}_two.pkl".format(foldername.split('.')[0]),"wb") as f:
        pickle.dump(feature,f)
    
    return feature    


#选择分类器 D-tree,SVM,NBayes,KNN
def select_estimator(case):

    if case == 0:
        estimator = SVC()
    elif case == 1:
        estimator = KNeighborsClassifier()
    elif case == 2:
        estimator = DecisionTreeClassifier()
    elif case == 3:
        estimator = GaussianNB()
    elif case == 4:
        estimator = LogisticRegression()    

    return estimator



def get_acc(features_a,features_b):
    feature_a_dict = dict()
    feature_b_dict = dict()

    index = 0
    for feature in features_a:
        feature_a_dict[index] = feature
        index += 1
        
    index = 0    
    for feature in features_b:
        feature_b_dict[index] = feature
        index += 1    
 
    count = 0  

    for key_a,value_a in feature_a_dict.items():
        min_distance = float("inf")  
        position = -1
        for key_b,value_b in feature_b_dict.items():
            current_distance = np.sqrt(np.sum(np.square(value_a - value_b)))
            print(current_distance)
            if current_distance < min_distance:
                min_distance = current_distance
                position = key_b

        exit()    
        if key_a == position:
            count += 1    

    return count / features_a.shape[0]            



def test_distance():
    with open("Normal_Sub_two.pkl","rb") as f:
        features_a  = pickle.load(f)

    with open("Normal_Sub.pkl","rb") as f:
        features_b  = pickle.load(f)  

      
    acc = get_acc(features_a,features_b)
    print(acc)    


#主函数
def main():
    
    n_foldername = "Gastritis_Sub"
    p_foldername = "Normal_Sub"

    n_feature = get_feature(n_foldername)
    p_feature = get_feature(p_foldername)
    """
    with open("Gastric_polyp_Sub.pkl","rb") as f:
        n_feature  = pickle.load(f)

    with open("Normal_Sub.pkl","rb") as f:
        p_feature  = pickle.load(f)    
    """
    dataset = np.vstack((n_feature,p_feature))
    print("dataset shape:",dataset.shape)
    #生成类标
    labels = []
    for i in range(n_feature.shape[0]):
        labels.append(0)
    for i in range(p_feature.shape[0]):
        labels.append(1)

    estimator_list = [0,1,2,3,4]

    for i in estimator_list:
        score = cross_val_score(select_estimator(i),dataset,labels,scoring = "accuracy").mean()
        print(score)   

    
        '''
        dataset shape: (402, 729)
        0.606969191913
        0.950303481202
        0.928044406206
        0.95030375829
        0.858242205846
        '''

        '''
        dataset shape: (344, 729)
        0.709316394434
        0.91822948175
        0.897963299052
        0.923976608187
        0.877697116354
        '''

        """
        dataset shape: (318, 729)
        0.767311551671
        0.955913825002
        0.974900986081
        0.962292420642
        0.886875022742
        """


#使用 rifs 算法 (我的特征选择算法)
def main_rifs():
    from rifs import single
    single("Gastritis_Sub.folder")



            
if __name__ == '__main__':
    test_distance()
    #get_feature("Normal_Sub",factor = 0.5)
