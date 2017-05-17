from get_win_chr import get_chr_file
from wilcox_test import w_test_main
from t_test import t_test_main
from ridge import ridge_main
from fpr_test import fpr_main
from lasso import lasso_main
from random_forest import rf_main
import os
import csv


def main():
    
    win_list = [100000,500000,5000000,10000000]
    data_matrix_file = "matrix_data.tsv"
    GPL_file = "GPL13534_HumanMethylation450_15017482_v.1.1.csv"
    json_file = "clinical.project-TCGA-BRCA.2017-04-20T02_01_20.302397.json"
    
    for win in win_list: 
        get_chr_file(data_matrix_file,GPL_file,json_file,win)

    
    labels_file = "labels.csv"

    algorithms = [t_test_main,w_test_main,fpr_main,lasso_main,rf_main,ridge_main]
    algorithm_names = ["t_test","w_test","fpr","lasso","rf","ridge"]

    index = 0

    for algorithm in algorithms: 
        for dir_ in os.listdir("."):
            #对应不同的窗口
            if os.path.isdir(dir_) and dir_.startswith("out"):
                #每个算法的每个窗口一个文件
                with open('{}_{}.csv'.format(algorithm_names[index],dir_),"w") as csvfile:
                    writer = csv.writer(csvfile)
                    writer.writerow(["","SVM","KNN","DT","NB","LG","MACC"])
                    for chr_file in os.listdir(dir_):
                        if chr_file.startswith("chr"):
                            acc_list = algorithm(os.path.join(dir_,chr_file),labels_file)
                            print(acc_list)
                            writer.writerow([chr_file.split(".")[0]] + acc_list)

        index += 1                    


            


if __name__ == '__main__':
    main()    

        

    




    

