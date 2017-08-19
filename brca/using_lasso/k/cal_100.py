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
                for row in reader:
                    if row[0] == "opt":

                        print("k = {}, opt(first 100) = {} ".format(file[-5],np.mean(list(map(float,row[1:101])))))
if __name__ == '__main__':
    main()                    
    