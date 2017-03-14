import os
import re
import numpy as np




def get_result(file_name):
    pattern = re.compile("0\.[0-9]+|1\.0")
    folder_list = list(map(str,range(1,21)))
    #print(folder_list)
    all_result = []

    with open("20_seed_result.txt","a") as tf:
        for folder in os.listdir("17_dataset"):
            if folder in folder_list:
                for file in os.listdir(os.path.join("17_dataset",folder)):
                    if file == file_name:
                        print(folder+": " + file)
                        with open(os.path.join("17_dataset",folder,file)) as f:
                            line = f.readlines()[-2]
                            #print(line)
                            acc = float(re.findall(pattern,line)[0])
                            print(acc)
                            all_result.append(acc)

        with open(file_name,"w") as f:
            f.write(str(len(all_result))+ " seed\n")
            f.write(str(all_result)+"\n")   
            f.write("mean value: " + str(np.mean(all_result)) + "\n")

        tf.write(file_name + ": " + str(np.mean(all_result)) +  "\n")    

def all_dataset():
    for file_name in os.listdir("17_dataset/1"):
        print(file_name)
        get_result(file_name)



if __name__ == '__main__':
    #get_result("Adenoma_result.txt")
    all_dataset()
