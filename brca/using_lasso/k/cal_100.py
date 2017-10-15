#!/usr/bin/env python3

# info
# -name   : zhangruochi
# -email  : zrc720@gmail.com


import os
import csv
import numpy as np


def main():
    for file in os.listdir("."):
        if file.endswith(".csv"):
            with open(file) as csvfile:
                reader = csv.reader(csvfile)
                print("\nk = {}".format(file[-5]))
                for row in reader:
                    if len(row) == 0:
                        continue
                    
                    if row[0] == "opt":
                        print("opt(first 500) = {} ".format(np.mean(list(map(float,row[1:501])))))
                    
                    if row[0] == "acc":
                        print("acc(first 500) = {} ".format(np.mean(list(map(float,row[1:501])))))

                    if row[0] == "r_2":
                        print("r_2(first 500) = {} ".format(np.mean(list(map(float,row[1:501])))))
                


if __name__ == '__main__':
    main()                    
    