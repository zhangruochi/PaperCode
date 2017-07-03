#!/usr/bin/env python3

#info
#-name   : zhangruochi
#-email  : zrc720@gmail.com

import matplotlib.pyplot as plt
import numpy as np


font = {#'family' : 'serif',  
        'color'  : '#000000',  
        'weight' : 'normal',  
        'size'   : 14,  
        }  

labels = ["Adeno",   "ALL1",    "ALL2",   "ALL3",    "ALL4",    "CNS",
          "Colon",   "DLBCL",   "Gas",      "Gas1",    "Gas2",    "Leuk",    
          "Lymp",    "Myel",    "Pros",     "Stroke",  "T1D" ]

f_score = [ 1,          1,          0.82556234,  0.51666667,  0.93809524,  0.825, 0.94126984,  0.99090909,  0.94538749,  0.91590077,  0.93142857,  1,         1, 0.93517304,  0.95392385,  1,          0.81625269]

x = np.arange(17)
plt.figure(1,figsize = (12,4))
plt.bar(x,f_score,color='#696969')
plt.xticks(x,labels)
plt.ylabel("F-score",fontdict = font)
plt.ylim((0.000,1.100))

for x, y in zip(x, f_score):
    plt.text(x + 0.05, y, '%0.3f' % y, ha = 'center', va = 'bottom')
    
plt.savefig('Figure6.svg',format='svg')
plt.savefig('Figure6.png',dpi = 600)
plt.show()