#CHR,MAPINFO,IlmnID
import pandas as pd
from collections import defaultdict
import pickle
import os

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
        n_segment = int((max_loc - min_loc ) / length)
        ranges = get_ranges(length,n_segment,min_loc)
        
        for loc,name in zip(value_frame["MAPINFO"],value_frame["IlmnID"]):
            for index,value in enumerate(ranges):
                if value[0] < loc and value[1] >= loc:
                    chr_dict[index].append(name)

        win[key] = chr_dict    

    with open("win.pkl","wb") as f:
        pickle.dump(win,f)


    return win    




def main(meth_filename,loc_filename, length):
    """
    if os.path.exists("win.pkl"):
        with open("win.pkl","rb") as f:
            win = pickle.load(f)
    else:
        win = generate_win(loc_filename, length)
                
    """
    with open(meth_filename,"r") as f:
        for line in f:
            print(line.split("\t"))
            









                          
            
if __name__ == '__main__':
    #load_loc_dataset("GPL13534_HumanMethylation450_15017482_v.1.1.csv")
    main("matrix_data.tsv","GPL13534_HumanMethylation450_15017482_v.1.1.csv",length = 1000000)
