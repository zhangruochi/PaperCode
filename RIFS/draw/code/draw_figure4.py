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

mAcc = [1.000,   1.000,   0.804,   0.877,   0.948,   0.874,   0.933,   0.988,   0.997,   0.976,   1.000,   1.000,   1.000,   0.894,   0.950,   1.000,   0.828] 
x = np.arange(17)
plt.figure(1,figsize = (12,4))
plt.bar(x,mAcc,color='#696969')
plt.xticks(x,labels)
plt.ylabel("mAcc",fontdict = font)
plt.ylim((0.000,1.100))

for x, y in zip(x, mAcc):
    plt.text(x + 0.05, y, '%0.3f' % y, ha = 'center', va = 'bottom')

plt.savefig('Figure4.svg',format='svg')
plt.savefig('Figure4.png',dpi = 600)
plt.show()