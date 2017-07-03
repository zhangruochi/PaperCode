#!/usr/bin/env python3

#info
#-name   : zhangruochi
#-email  : zrc720@gmail.com


import matplotlib.pyplot as plt
import numpy as np




#---------------- figure 1 -------------------
x = np.arange(17)
labels = ["Adeno",   "ALL1",    "ALL2",   "ALL3",    "ALL4",    "CNS",
          "Colon",   "DLBCL",   "Gas",      "Gas1",    "Gas2",    "Leuk",    
          "Lymp",    "Myel",    "Pros",     "Stroke",  "T1D"]

nums =  [  3,   1,   8,   14,  10,  8,   11,  6,   8,   10,  7,   7,   9,   27,  6,   10,  6]

TRank =   [ 1.000,   1.000,   0.751,   0.833,   0.930,   0.758,   0.917,   0.973,   0.971,   0.945,   0.983,   0.988,   1.000,   0.880,   0.923,   1.000,   0.794 ]                                                                          
FPR  =    [ 1.000,   1.000,   0.751,   0.825,   0.930,   0.749,   0.917,   0.973,   0.971,   0.945,   0.983,   0.988,   1.000,   0.880,   0.925,   1.000,   0.794 ]                                                                           
WRank =   [ 0.625,   0.743,   0.652,   0.809,   0.723,   0.650,   0.774,   0.765,   0.710,   0.917,   0.920,   0.761,   0.763,   0.787,   0.693,   0.471,   0.607 ]                                                                           
RIFS  =   [ 1.000,   1.000,   0.804,   0.877,   0.948,   0.874,   0.933,   0.988,   0.997,   0.976,   1.000,   1.000,   1.000,   0.894,   0.950,   1.000,   0.828 ]                                                                           


fig = plt.figure(figsize = (12,6))
ax1 = fig.add_subplot(411)

ax1.plot(x, TRank,color = "#800080", marker='o',label = "TRank")
ax1.plot(x, FPR, color = "#228B22", marker = '^',label = "FPR")
ax1.plot(x, WRank, color = "#FF0000", marker = 's',label = "WRank")
ax1.plot(x, RIFS, color = "#000000", marker = 'D',label = "RIFS")
ax1.set_ylim((0,1.10))

ax1.set_xticks(x)
ax1.set_xticklabels(labels,fontsize='small')
ax1.set_ylabel("mAcc")
ax1.legend(loc='lower center',ncol = 4,fontsize = 10)

""""
ax2 = ax1.twinx()
ax2.bar(x,nums,color = "#000000")
ax2.set_ylim((0,100))


for x, y in zip(x, nums):
    ax2.text(x + 0.05, y + 0.1, '%d' % y, ha = 'center', va = 'bottom')
"""



#----------------table 1 --------------------

ax2 = fig.add_subplot(412)
ax2.axis('off')

cellText = [nums]
rowLabels = ["RIFS"]
ax2.table(cellText = cellText, rowLabels = rowLabels, colLabels = labels,loc='center')


#---------------- figure 2 -------------------

x = np.arange(17)

Lasso =  [ 0.993,   1.000,   0.716,   0.809,   0.920,   0.768,   0.900,   0.975,   0.971,   0.958,   0.992,   1.000,   1.000,   0.918,   0.930,   0.900,   0.625]   
RF =  [ 0.993,   1.000,   0.672,   0.810,   0.873,   0.728,   0.892,   0.975,   0.936,   0.961,   0.988,   0.985,   0.966,   0.82,  0.922,  0.791,   0.714 ]   
Ridge = [ 0.961,   1.000,   0.652,   0.809,   0.785,   0.650,   0.869,   0.950,   0.893,   0.959,   0.983,   0.932,   0.892,   0.793,   0.838,   0.650,   0.633]   
RIFS  = [ 1.000,   1.000,   0.804,   0.877,   0.948,   0.874,   0.933,   0.988,   0.997,   0.976,   1.000,   1.000,   1.000,   0.894,   0.950,   1.000,   0.828]


Lasso_ = [  56,  5,   9,   2,   15,  223, 11,  9,   12,  6,   14,  11,  9,   27,  8,   16,  4] 
RF_  = [ 16,  37,  87,  84,  59,  53,   46,  40,  37,  58,  38,  43,  33,  115,  75,  30,  79]
Ridge_  = [  3729,    6399,    6073,    6188,    6227,    3681,    1000,    3586,    11971,   11699,   11454,   1454,    2146,    6268,    6567,    26773,   28067]
RIFS_ = [ 3,   1,   8,   14,  10,  8,   11,  6,   8,   10,  7,   7,   9,   27,  6,   10,  6] 
                                                                                                                                                    

ax3 = fig.add_subplot(413)

ax3.plot(x, Lasso,color = "#800080", marker='o',label = "Lasso")
ax3.plot(x, RF, color = "#228B22", marker = '^',label = "RF")
ax3.plot(x, Ridge, color = "#FF0000", marker = 's',label = "Ridge")
ax3.plot(x, RIFS, color = "#000000", marker = 'D',label = "RIFS")
ax3.set_ylim((0,1.10))

ax3.set_xticks(x)
ax3.set_xticklabels(labels,fontsize='small')
ax3.set_ylabel("mAcc")
ax3.legend(loc='lower center',ncol = 4,fontsize = 10)


#----------------table 4 --------------------
ax4 = fig.add_subplot(414)
ax4.axis('off')

cellText = [Lasso_, RF_, Ridge_, RIFS_]
rowLabels = ["Lasso","RF","Ridge","RIFS"]
ax4.table(cellText = cellText, rowLabels = rowLabels, colLabels = labels,loc='center')

plt.tight_layout()
plt.savefig('Figure5.svg',format='svg')
plt.savefig('Figure5.png',dpi = 600)
plt.show()

