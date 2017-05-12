#CHR,MAPINFO,IlmnID
import pandas as pd
from collections import defaultdict
import pickle
import os
import numpy as np
from operator import itemgetter

"""
def test_dataset(loc_filename):
    dataset = defaultdict(list)
    index = 0
    with open(loc_filename,"r") as f:
        for item in f:
            line = item.split(",")
            if index == 0:
                index_IlmnID = line.index("IlmnID")
                index_MAPINFO = line.index("MAPINFO")
                index_CHR = line.index("CHR")
                index += 1
                #print(index_IlmnID,index_CHR,index_MAPINFO)
            else:
                #print(line[index_IlmnID],line[index_CHR],line[index_MAPINFO])
                dataset["names"].append(line[index_IlmnID])
                dataset["chr"].append(line[index_CHR])
                dataset["loc"].append(line[index_MAPINFO])
"""


def load_loc_dataset(loc_filename):
    if os.path.exists("loc.pkl"):
        with open("loc.pkl","rb") as f:
            loc_dataset = pickle.load(f)
    else:
        loc_dataset = pd.read_csv(loc_filename).loc[:,["IlmnID","CHR","MAPINFO"]]
        with open("loc.pkl","wb") as f:
            pickle.dump(loc_dataset,f)
    
    return loc_dataset



def get_ranges(length,n_segment,min_loc):
    ranges = []
    for i in range(n_segment):
        max_loc = min_loc + length
        ranges.append((min_loc,max_loc))
        min_loc = max_loc
    #print(ranges)    
    return ranges


def generate_win(loc_filename, length):
    loc_dataset = load_loc_dataset(loc_filename)
    win = dict()

    for key,value_frame in loc_dataset.groupby("CHR"):
        chr_dict = defaultdict(list)
        max_loc = value_frame["MAPINFO"].max()
        min_loc = value_frame["MAPINFO"].min()
        n_segment = int((max_loc - min_loc ) / length) + 1
        ranges = get_ranges(length,n_segment,min_loc)
        

        #根据位置切割后，有些染色体段中没有基因
        for loc,name in zip(value_frame["MAPINFO"],value_frame["IlmnID"]):
            for index,value in enumerate(ranges):   
                if value[0] <= loc and value[1] > loc:
                    chr_dict[index].append(name)

        win[key] = chr_dict    

    with open("win.pkl","wb") as f:
        pickle.dump(win,f)

    return win       



def processing_win(win):
    #找到染色体的段对应在最终矩阵中的索引
    segment_index = dict()
    for chr_,segment_dict in win.items():
        tmp_dict = dict()
        sorted_segment_dict = sorted(segment_dict.items(), key = itemgetter(0))
        segment_list = [item[0] for item in sorted_segment_dict]
        for i in range(len(segment_list)):
            tmp_dict[segment_list[i]] = i 

        segment_index[chr_] = tmp_dict
    
    return segment_index
        



#找出每个cg 对应在哪个染色体的哪个段
def generate_cg_loc(win):
    cg_dict = dict()
    segment_length_dict = dict() #保存每个染色体的段数
    for chr_,segment_dict in win.items():
        segment_length_dict[chr_] = len(segment_dict)
        for segment,list_ in segment_dict.items():
            for cg_ in list_:
                cg_dict[cg_] = (chr_,segment)
           
    return cg_dict,segment_length_dict   



#产生最终的矩阵形状
def generate_feature_matrix(segment_length_dict,samples = 928):
    chr_matrix = dict()
    for chr_,length in segment_length_dict.items():
        chr_matrix[chr_] = np.zeros((length,samples))
    return  chr_matrix





def processing_chr_denominator_dict(chr_denominator_dict):
    new_chr_denominator_dict = dict()

    for chr_, segment_dict in chr_denominator_dict.items():
        new_chr_denominator_dict[chr_] = np.array([[item[1]] for item in sorted(segment_dict.items(), key = itemgetter(0))])
    #print(new_chr_denominator_dict)

    return new_chr_denominator_dict



def main(meth_filename,loc_filename, length):
    
    if os.path.exists("win.pkl"):
        with open("win.pkl","rb") as f:
            win = pickle.load(f)
    else:
        win = generate_win(loc_filename, length)


     
    segment_index = processing_win(win)
  
    cg_dict,segment_length_dict  = generate_cg_loc(win)  
    chr_matrix = generate_feature_matrix(segment_length_dict)

    

    #记录每条染色体每段cg的数目，最后取平均值用做分母
    chr_denominator_dict = defaultdict(dict)



    with open(meth_filename,"r") as f:

        f.readline()
        count = 0
        for line in f:
            content_list = line.split("\t")
            name = content_list[0]
            feature = list(map(float,content_list[1:]))

            try:
                chr_loc,segment_loc = cg_dict[name] #得到特征的染色体位置和段位置
                chr_matrix[chr_loc][segment_index[chr_loc][segment_loc]] += np.array(feature) 
            except:
                print("can not find {} in the GPL file!".format(name) )

            if  not segment_index[chr_loc][segment_loc] in chr_denominator_dict[chr_loc]:
                chr_denominator_dict[chr_loc][segment_index[chr_loc][segment_loc]] = 1            
            else:
                chr_denominator_dict[chr_loc][segment_index[chr_loc][segment_loc]] += 1

            count += 1
            if count % 10000 == 0:
                print("readlines: " + str(count))

        with open("chr_matrix.pkl","wb") as f:
            pickle.dump(chr_matrix,f)

        with open("chr_denominator_dict.pkl","wb") as f:
            pickle.dump(chr_denominator_dict,f)

    

    #print(chr_matrix) 
    new_chr_denominator_dict = processing_chr_denominator_dict(chr_denominator_dict) 

    if not os.path.exists("output"):
        os.mkdir("output")
    
    for chr_name, data_matrix in chr_matrix.items():
        chr_data_matrix = data_matrix / new_chr_denominator_dict[chr_name]

        
        np.savetxt('output/chromosome_{}.csv'.format(chr_name),chr_data_matrix, delimiter = ',')
    
        print("the data_matrix of {} chromosome is : \n".format(chr_name))
        print(chr_data_matrix.shape)
        print("\n")

        
        




       



                          
            
if __name__ == '__main__':
    #load_loc_dataset("GPL13534_HumanMethylation450_15017482_v.1.1.csv")
    main("matrix_data.tsv","GPL13534_HumanMethylation450_15017482_v.1.1.csv",length = 1000000)

