'''
python3

Required packages
- pandas
- scipy
- numpy
- sklearn
- scipy
- PIL


Info
- name   : "zhangruochi"
- email  : "zrc720@gmail.com"
- date   : "2017.02.18"
- Version : 3.0.0

Description
    Trip-Z 算法的实现
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
from sklearn.ensemble import RandomForestClassifier
from sklearn.linear_model import LogisticRegression
from sklearn.model_selection import cross_val_score
from sklearn.model_selection import StratifiedKFold

from sklearn.metrics import precision_recall_fscore_support


#根据像素矩阵得到梯度矩阵以及相应的值的矩阵
def get_magnitude(im,sigma = 5):
    #sigma 标准差
    imx = np.zeros(im.shape)
    filters.gaussian_filter(im, (sigma,sigma), (0,1), imx)
    imy = np.zeros(im.shape)
    filters.gaussian_filter(im, (sigma,sigma), (1,0), imy)
    magnitude = np.sqrt(imx**2+imy**2)   #梯度幅值
    direction = np.arctan(imy/imx)       #梯度方向
    
    direction = np.nan_to_num(direction)
    
    return magnitude,direction


#得到图片中所有块的起始点
def get_all_start_point(magnitude,scale_factor = 5):   # scale_factor 表示取多少圈
    center_point = ( ceil(magnitude.shape[0] / 2.0),ceil(magnitude.shape[1] / 2.0) )
    width,length = chunk_size =  magnitude.shape[0] // (scale_factor * 2 -1), magnitude.shape[1] // (scale_factor * 2 -1)
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
                #print(circle + 1)p
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
            #print(len(temp_point_list));exit()   每块180个像素点   
            temp_circle_list.append(temp_point_list)        
        raw_feature_list.append(temp_circle_list) 

    #print(len(raw_feature_list));exit()      共有5个圈    
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
                start = -pi / 2; end = -pi / 2 + every_component
                index = 0
                while True:
                    if(point[0] >= start and point[0] < end):   #判断每个点的梯度
                        feature_dict[index].append(point[0])
                        break
                    start = end
                    end += every_component
                    index += 1    
            temp_circle_list.append(feature_dict)    #每个块是一个特征  temp_circle_list放入每一圈里面所有的块
        result_list.append(temp_circle_list)  

    #print(len(result_list))  #5圈      
    
    result_dict = defaultdict(list)
    result = []
    for index,circle in enumerate(result_list):
        tmp_feature = []
        for chunk in circle:
            feature_list = []
            for i in range(k):
                feature_list.append(sum(chunk[i]))    
            #print(tmp_feature)  #每个chunk9个值, [-42.776486557553589, -33.977213583081131, -12.29493586581221, -5.5682229960047227, 0.15148943481737917, 3.4264964356761385, 7.9017645609536578, 13.918112670444323, 44.62213014473717]
            tmp_feature.append(feature_list)   
        #print(tmp_feature)   #4k个cell在此bin的平均值
        if index == 0:
            feature = list(np.array(tmp_feature).mean(0))
        else:
            feature = list(np.array(tmp_feature).mean(0)) + list(np.array(tmp_feature).std(0))

        result += feature    
    return result
 

    
def get_feature(foldername,scale = 5,bins = 9,degree = None):
    
    image_folder = foldername
    all_feature = []
    for filename in sorted(os.listdir(image_folder)):
        if filename.endswith(".ras"):
            print(filename)
            im = Image.open(os.path.join(image_folder,filename))
            
            if degree:
                im = im.rotate(degree)

            im = np.array(im.convert("L"))    
            magnitude,direction = get_magnitude(im)

            all_start_point,chunk_size = get_all_start_point(magnitude,scale_factor = scale)  #[[(20, 35)], [(16, 27), (20, 27), (24, 27), (24, 35), (16, 35), (16, 43), (20, 43), (24, 43)], [(12, 19), (16, 19),......
            raw_feature_list = get_chunk_feature(all_start_point,chunk_size,magnitude,direction)
            tmp_feature = transform_feature(raw_feature_list, k= bins)
            all_feature.append(tmp_feature)    
    
    feature = np.array(all_feature)

    with open("{}_two.pkl".format(foldername.split('.')[0]),"wb") as f:
        pickle.dump(feature,f)
    
    return feature    


#选择分类器 D-tree,SVM,NBayes,KNN
def select_estimator(case):

    if case == 0:
        estimator = SVC()
    elif case == 1:
        estimator = RandomForestClassifier(random_state = 7)
    elif case == 2:
        estimator = DecisionTreeClassifier(random_state = 7)
    elif case == 3:
        estimator = GaussianNB()
    elif case == 4:
        estimator = LogisticRegression()    

    return estimator


#主函数
def main():
#------- 参数设定 -----------------------------------------------------------
    n_foldername = "p"
    p_foldername = "n"
    n = 5    #采用 n 折交叉验证
    n_feature = get_feature(n_foldername,scale = 5, bins = 9)
    p_feature = get_feature(p_foldername)    #什么都不设定默认为 scale = 5, bins = 9
#---------------------------------------------------------------------------   
     
    dataset = np.vstack((n_feature,p_feature))   

    print("\ndataset shape:",dataset.shape)  
    #生成类标
    labels = []
    for i in range(n_feature.shape[0]):
        labels.append(0)
    for i in range(p_feature.shape[0]):
        labels.append(1)

    estimator_list = [0,1,2,3,4]
    skf = StratifiedKFold(n_splits= n,random_state = 7)

    score_func_list = ["accuracy","recall","roc_auc"]
    for score_func in score_func_list:
        print(score_func+": ")
        for i in estimator_list:
            score = cross_val_score(select_estimator(i),dataset,labels,scoring = score_func ,cv=skf).mean()
            print(score)  
        print("\n")


            
if __name__ == '__main__':
    main()



"""
数据结构示例：  

chunk:  (key表示梯度， list 表示每个块中不同的像素点在此梯度上的值)

{4: [0.065262925322836826, 0.094830969843102048, 0.095183841617915571, 0.075017737768345513, 0.039899239240549951, 0.14558665525898329, -0.0066433849618339827, 0.056843684859567312, 0.14327026539755225, -0.060960875638167877, -0.039851385144381996, -0.025673849735192062, -0.01461249455330617, 0.011674543697264287, -0.17402711187913222, -0.12291674928627035, 0.12931646045056874, -0.11962520170636932, -0.14108583573465269], 
 5: [0.39363656720883489, 0.34688020795915414, 0.29105546562259799, 0.22388620508601625, 0.43720362487102366, 0.29866595493523301, 0.31425028983773712, 0.42054883827808925, 0.48572742573402189, 0.2146418561434299], 
 6: [0.79358540744973993, 0.675896892835123, 0.56108319488351621, 0.79911730658986202, 0.79587179129728536, 0.58762216347619012, 0.64056297865370315, 0.83601619384271819, 0.62709470528101385, 0.80531268966798675, 0.7796012369765194], 
 8: [1.2531506491175948, 1.5487845000895057, 1.2525894162099998, 1.549156816696323, 1.5041888954900786, 1.4536696379399019, 1.4585863887397685, 1.3422906763985738, 1.401830404251315, 1.3121231283830812, 1.2882573573327101, 1.2714402662505844, 1.4422517115898619, 1.5173596873632014, 1.4857332988368595, 1.3317224126268865, 1.3708330118202721, 1.5007715789003235, 1.407981412907422, 1.4610643523928688, 1.5029982295599646, 1.4525482517928372, 1.519624153924658, 1.4965243225776632, 1.4798548487973167, 1.5626495456353851, 1.4820408911882552, 1.4956154491546241, 1.5157516286490713, 1.4587561602298937, 1.5019810598903587], 
 0: [-1.4936327557416, -1.2501474058279256, -1.3273870545993152, -1.3022600257208623, -1.3604870883355358, -1.3336007865345143, -1.3758196732138914, -1.3436684114590993, -1.3733551757164106, -1.3220158756778577, -1.3458095583232761, -1.2568506887253332, -1.2964997978409782, -1.5447732554462692, -1.3882710992732865, -1.4961421195111955, -1.232113363273617, -1.45510909900826, -1.4568752351291385, -1.242561192449573, -1.2552211581140393, -1.5119634113512785, -1.4201758177878288, -1.2333413971310099, -1.3533449270424773, -1.5670770013191768, -1.5447579925428254, -1.3833868124939357, -1.4495107547710158, -1.5160392025899467, -1.3442884206021033], 
 1: [-1.1498110047061987, -1.1752511454688475, -1.1797648671208878, -1.2010843096674522, -1.1817940738252388, -1.1999480585955364, -1.1488637421565155, -1.165788784654979, -1.0563737057457079, -1.0767105561375399, -1.208400809821321, -1.1427876298684951, -1.0640575110559687, -1.187959785047479, -0.87855728299637692, -1.0181538510808608, -0.99645549418093549, -1.1471951362331498, -1.0573442855816311, -0.95671515710849697, -0.92426857787070127, -1.0818249500100583, -1.0093352421529227, -1.0391179155182231, -1.2104319590507659, -1.0806621784121089, -1.0299259128025051, -1.1543772337955422, -1.1750833352129177, -1.0575496436047567, -1.0216194435970103], 
 7: [1.0249884102049032, 1.1113076843987304, 1.2030715610453655, 0.97841733861503444, 0.96680715073425727, 1.1347375529700823, 0.90433313346571487, 1.0357018968825313, 1.1759871697847732, 0.88228973159986224, 1.1174660017331179, 1.1813195223497632, 1.2016855166601839], 
 2: [-0.81606025744403121, -0.8547795043659131, -0.73713047509570806, -0.8100734395324094, -0.66330669438021028, -0.63514831212382561, -0.66053434161564961, -0.53005183882749185, -0.85372758182143293, -0.71467490267066824, -0.67405932037898275, -0.86296516174883198, -0.53222370915743555, -0.80437932062111839, -0.6224775880707778, -0.71357662615272577, -0.80976679180499789], 
 3: [-0.21055513347146651, -0.2003029992594953, -0.34989945273406486, -0.28342532774519291, -0.19894545086330293, -0.17967292188157194, -0.24327801278491501, -0.37094924076297409, -0.49416022154067274, -0.23866457917044806, -0.34340243619453076, -0.29514814191322991, -0.43960563074799874, -0.34924065805642474, -0.40177386835906959, -0.45528851089174327, -0.51391040962762125]})
""" 

"""
chunk_feature  对上面chunk 的 value 求 sum， 形成每个cell 的特征值
[-42.776486557553589, -33.977213583081131, -12.29493586581221, -5.5682229960047227, 0.15148943481737917, 3.4264964356761385, 7.9017645609536578, 13.918112670444323, 44.62213014473717]
"""

