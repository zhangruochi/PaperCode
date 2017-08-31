#!/usr/bin/env python3

#info
#-name   : zhangruochi
#-email  : zrc720@gmail.com


import matplotlib.pyplot as plt
import numpy as np


labels_ultimate = [ "DLBCL", "Pros", "Colon", "Leuk",  "Mye",  "ALL1", "ALL2", "ALL3", "ALL4", "CNS", "Lym", "Adeno", "Gas","Gas1","Gas2", "T1D","Stroke" ]



def process_values(values,labels,labels_ultimate):
    result = []
    for label in labels_ultimate:
        index = labels.index(label)
        result.append(values[index])
    return result    


#---------------- figure 1 -------------------
x = np.arange(17)
labels = ["Adeno",   "ALL1",    "ALL2",   "ALL3",    "ALL4",    "CNS",
          "Colon",   "DLBCL",   "Gas",      "Gas1",    "Gas2",    "Leuk",    
          "Lym",    "Mye",    "Pros",     "Stroke",  "T1D"]

nums =  [  3,   1,   8,   14,  10,  8,   11,  6,   8,   10,  7,   7,   9,   27,  6,   10,  6]

Trank =   [ 1.000,   1.000,   0.751,   0.833,   0.930,   0.758,   0.917,   0.973,   0.971,   0.945,   0.983,   0.988,   1.000,   0.880,   0.923,   1.000,   0.794 ]                                                                          
FPR  =    [ 1.000,   1.000,   0.751,   0.825,   0.930,   0.749,   0.917,   0.973,   0.971,   0.945,   0.983,   0.988,   1.000,   0.880,   0.925,   1.000,   0.794 ]                                                                           
Wrank =   [ 0.625,   0.743,   0.652,   0.809,   0.723,   0.650,   0.774,   0.765,   0.710,   0.917,   0.920,   0.761,   0.763,   0.787,   0.693,   0.471,   0.607 ]                                                                           
RIFS  =   [ 1.000,   1.000,   0.804,   0.877,   0.948,   0.874,   0.933,   0.988,   0.997,   0.976,   1.000,   1.000,   1.000,   0.894,   0.950,   1.000,   0.828 ]                                                                           



fig = plt.figure(figsize = (12,9))
ax1 = fig.add_subplot(611)

ax1.plot(x, process_values(Trank,labels,labels_ultimate),color = "#000000", marker='o',label = "Trank")
ax1.plot(x, process_values(FPR,labels,labels_ultimate), color = "#228B22", marker = '^',label = "FPR")
ax1.plot(x, process_values(Wrank,labels,labels_ultimate), color = "#800080", marker = 's',label = "Wrank")
ax1.plot(x, process_values(RIFS,labels,labels_ultimate), color = "#FF0000", marker = 'D',label = "RIFS")
ax1.set_ylim((0,1.10))
ax1.set_yticks((0.0,0.2,0.4,0.6,0.8,1.0))
ax1.set_xticks(x)
ax1.set_xticklabels(labels_ultimate,fontsize='small')
ax1.set_ylabel("mAcc")
ax1.legend(loc='lower right',ncol = 4,fontsize = 8)

""""
ax2 = ax1.twinx()
ax2.bar(x,nums,color = "#000000")
ax2.set_ylim((0,100))


for x, y in zip(x, nums):
    ax2.text(x + 0.05, y + 0.1, '%d' % y, ha = 'center', va = 'bottom')

"""
#---------------- figure 2 -------------------
x = np.arange(17)
labels = ["Adeno",   "ALL1",    "ALL2",   "ALL3",    "ALL4",    "CNS",
          "Colon",   "DLBCL",   "Gas",      "Gas1",    "Gas2",    "Leuk",    
          "Lym",    "Mye",    "Pros",     "Stroke",  "T1D"]

Trank =  [ 1,  1, 0.82711569,  0.5547619,  0.89880952,  0.65416667,  0.93214286,  0.97979798,  0.94182504,  0.96461538,  0.94571429,  0.98571429,  1,  0.92555119,  0.91714744,  1,  0.83835047]  
FPR  =   [ 1,  1, 0.82711569,  0.51690476,  0.89880952, 0.656,  0.93214286,  0.97979798,  0.94182504,  0.96461538,  0.94571429,  0.98571429, 1,  0.92555119,  0.91812626,  1,  0.83835047]
Wrank =  [ 0.49333333,  0.29666667,  0.78888889,  0.14480952,  0.5152381,   0.39214286, 0.84611111,  0.85995671,  0.91011685,  0.92310023,  0.60560714,  0.59480952, 0.76190476,  0.88034721,  0.72099456,  0.43366667,  0.72163866]
RIFS  =  [ 1,  1,  0.82556234,  0.51666667,  0.93809524,  0.825, 0.94126984,  0.99090909,  0.94538749,  0.91590077,  0.93142857,  1,  1,  0.93517304,  0.95392385,  1,  0.81625269]


ax2 = fig.add_subplot(612)

ax2.plot(x, process_values(Trank,labels,labels_ultimate),color = "#000000", marker='o',label = "Trank")
ax2.plot(x, process_values(FPR,labels,labels_ultimate), color = "#228B22", marker = '^',label = "FPR")
ax2.plot(x, process_values(Wrank,labels,labels_ultimate), color = "#800080", marker = 's',label = "Wrank")
ax2.plot(x, process_values(RIFS,labels,labels_ultimate), color = "#FF0000", marker = 'D',label = "RIFS")
ax2.set_ylim((0,1.10))
ax2.set_yticks((0.0,0.2,0.4,0.6,0.8,1.0))
ax2.set_xticks(x)
ax2.set_xticklabels(labels_ultimate,fontsize='small')
ax2.set_ylabel("F-score")
ax2.legend(loc='lower right',ncol = 4,fontsize = 8)



#----------------table 1 --------------------
nums =  [  3,   1,   8,   14,  10,  8,   11,  6,   8,   10,  7,   7,   9,   27,  6,   10,  6]
ax3 = fig.add_subplot(613)
ax3.axis('off')

cellText = [process_values(nums,labels,labels_ultimate)]
rowLabels = ["RIFS"]
ax3.table(cellText = cellText, rowLabels = rowLabels, colLabels = labels_ultimate,loc='center')







#---------------- figure 3 -------------------

x = np.arange(17)

Lasso =  [ 0.993,   1.000,   0.716,   0.809,   0.920,   0.768,   0.900,   0.975,   0.971,   0.958,   0.992,   1.000,   1.000,   0.918,   0.930,   0.900,   0.625]   
RF =  [ 0.993,   1.000,   0.672,   0.810,   0.873,   0.728,   0.892,   0.975,   0.936,   0.961,   0.988,   0.985,   0.966,   0.82,  0.922,  0.791,   0.714 ]   
Ridge = [ 0.961,   1.000,   0.652,   0.809,   0.785,   0.650,   0.869,   0.950,   0.893,   0.959,   0.983,   0.932,   0.892,   0.793,   0.838,   0.650,   0.633]   
RIFS  = [ 1.000,   1.000,   0.804,   0.877,   0.948,   0.874,   0.933,   0.988,   0.997,   0.976,   1.000,   1.000,   1.000,   0.894,   0.950,   1.000,   0.828]

                                                                                                                                        
ax4 = fig.add_subplot(614)

ax4.plot(x, process_values(Lasso,labels,labels_ultimate),color = "#000000", marker='o',label = "Lasso")
ax4.plot(x, process_values(RF,labels,labels_ultimate), color = "#228B22", marker = '^',label = "RF")
ax4.plot(x, process_values(Ridge,labels,labels_ultimate), color = "#800080", marker = 's',label = "Ridge")
ax4.plot(x, process_values(RIFS,labels,labels_ultimate), color = "#FF0000", marker = 'D',label = "RIFS")
ax4.set_ylim((0,1.10))
ax4.set_yticks((0.0,0.2,0.4,0.6,0.8,1.0))
ax4.set_xticks(x)
ax4.set_xticklabels(labels_ultimate,fontsize='small')
ax4.set_ylabel("mAcc")
ax4.legend(loc='lower right',ncol = 4,fontsize = 8)


#---------------- figure 4 -------------------

x = np.arange(17)

Lasso =  [ 0.989,      1,          0.80563131,  0.24858333,  0.89047619 , 0.60666667,  0.92777778,  0.98321678,  0.9564986,   0.99230769,  0.96571429,  1,         1.,  0.94746259,  0.92661869,  0.89333333,  0.60681201]
RF =  [ 0.98966667,  1.,          0.79032688,  0.27927056,  0.76777092,  0.54258333,  0.92103175,  0.98278494,  0.95800827,  0.98707925,  0.9277619,   0.97590476, 0.95497619, 0.89494537,  0.91462232,  0.7915, 0.76672453]
Ridge = [ 0.96883333,  1,        0.78888889,  0.18794841,  0.61404762,  0.37540476,  0.89246032,  0.96363636,  0.95793651,  0.98181818,  0.86221429,  0.87333333, 0.89,       0.8842881,   0.8384591,   0.69,        0.72163866]
RIFS  = [ 1,  1,  0.82556234,  0.51666667,  0.93809524,  0.825, 0.94126984,  0.99090909,  0.94538749,  0.91590077,  0.93142857,  1,  1,  0.93517304,  0.95392385,  1,  0.81625269]


Lasso_ = [  56,  5,   9,   2,   15,  223, 11,  9,   12,  6,   14,  11,  9,   27,  8,   16,  4] 
RF_  = [ 16,  37,  87,  84,  59,  53,   46,  40,  37,  58,  38,  43,  33,  115,  75,  30,  79]
Ridge_  = [  3729,    6399,    6073,    6188,    6227,    3681,    1000,    3586,    11971,   11699,   11454,   1454,    2146,    6268,    6567,    26773,   28067]
RIFS_ = [ 3,   1,   8,   14,  10,  8,   11,  6,   8,   10,  7,   7,   9,   27,  6,   10,  6] 
                                                                                                                                                    

ax5 = fig.add_subplot(615)

ax5.plot(x, process_values(Lasso,labels,labels_ultimate),color = "#000000", marker='o',label = "Lasso")
ax5.plot(x, process_values(RF,labels,labels_ultimate), color = "#228B22", marker = '^',label = "RF")
ax5.plot(x, process_values(Ridge,labels,labels_ultimate), color = "#800080", marker = 's',label = "Ridge")
ax5.plot(x, process_values(RIFS,labels,labels_ultimate), color = "#FF0000", marker = 'D',label = "RIFS")
ax5.set_ylim((0,1.10))
ax5.set_yticks((0.0,0.2,0.4,0.6,0.8,1.0))
ax5.set_xticks(x)
ax5.set_xticklabels(labels_ultimate,fontsize='small')
ax5.set_ylabel("F-score")
ax5.legend(loc='lower right',ncol = 4,fontsize = 8)



#----------------table 2 --------------------
Lasso_ = [  56,  5,   9,   2,   15,  223, 11,  9,   12,  6,   14,  11,  9,   27,  8,   16,  4] 
RF_  = [ 16,  37,  87,  84,  59,  53,   46,  40,  37,  58,  38,  43,  33,  115,  75,  30,  79]
Ridge_  = [  3729,    6399,    6073,    6188,    6227,    3681,    1000,    3586,    11971,   11699,   11454,   1454,    2146,    6268,    6567,    26773,   28067]
RIFS_ = [ 3,   1,   8,   14,  10,  8,   11,  6,   8,   10,  7,   7,   9,   27,  6,   10,  6] 

ax6 = fig.add_subplot(616)
ax6.axis('off')

cellText = [process_values(item,labels,labels_ultimate) for item in  [Lasso_, RF_, Ridge_, RIFS_]]
rowLabels = ["Lasso","RF","Ridge","RIFS"]
ax6.table(cellText = cellText, rowLabels = rowLabels, colLabels = labels_ultimate,loc='center')

plt.tight_layout()
plt.savefig('Figure5.svg',format='svg')
plt.savefig('Figure5.png',dpi = 600)
plt.show()

