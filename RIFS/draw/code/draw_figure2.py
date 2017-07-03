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

fig, axes = plt.subplots(nrows=2, ncols=2, figsize=(10,6))
ax0, ax1, ax2, ax3 = axes.flatten()



#---------figure 0------------------
group_labels=['ALL2','ALL3']
bar_width = 0.35 
index = np.arange(2)

IFS_I = (0.795,0.863)
IFS_0 = (0.770,0.850)

ax0.bar(index, IFS_I, bar_width, color='#808080',label='IFS(i)')
ax0.bar(index+bar_width, IFS_0, bar_width,color='#000000',label='IFS(0)')


ax0.set_xticks(index + bar_width / 2 )
ax0.set_xticklabels(("ALL2","ALL3")) 
ax0.set_xlabel("(a)",fontdict = font)
ax0.legend()
ax0.set_ylim(0.720,0.880)


#-----------figure 1 ---------------
T1D =[0.656 ,0.667 ,0.654 ,0.708 ,0.742 ,0.786 ]
x_2 = [757,758,759,760,761,762] 

ax1.plot(x_2,T1D,color = "#000000", marker='D',label = "T1D")
ax1.set_xlabel("(b)",fontdict = font)
ax1.legend(loc='upper center')
#ax3.set_title("T1D")
ax1.set_ylim(0.500,0.850)



# --------------- figure 2 ----------------
Colon = [0.757 ,0.836 ,0.855 ,0.840 ,0.869 ,0.869]
x = [37,38,39,40,41,42] 

ax2.plot(x,Colon,color = "#000000", marker='D',label = "Colon")
ax2.set_xlabel("(c)",fontdict = font)
ax2.legend(loc='upper center')
#ax2.set_title("Colon")
ax2.set_ylim(0.700,0.900)



# --------------- figure 3 ----------------
ALL1 = [1.000 ,1.000 ,1.000 ,1.000 ,1.000 ]
ALL2 = [0.795 ,0.795 ,0.797 ,0.797 ,0.797]
ALL3 = [0.883 ,0.883 ,0.883 ,0.883 ,0.883]
ALL4 = [0.939 ,0.939 ,0.939 ,0.948 ,0.939]

x = [0.15,0.25,0.35,0.45,0.55]
ax3.plot(x,ALL1,color = "#000000", marker='o',label = "ALL1")
ax3.plot(x, ALL2, color = "#696969", marker = '^',label = "ALL2")
ax3.plot(x, ALL3, color = "#808080", marker = 's',label = "ALL3")
ax3.plot(x, ALL4, color = "#A9A9A9", marker = 'D',label = "ALL4")

ax3.set_xticks(x)
ax3.set_xticklabels(("15%","25%","35%","45%","55%"))
ax3.set_xlabel("(d)",fontdict = font) 
ax3.legend(loc='upper center',ncol = 4,fontsize = 6)
ax3.set_ylim(0.750,1.100)


plt.tight_layout()
plt.savefig('Figure2.svg',format='svg')
plt.savefig('Figure2.png',dpi = 600)
plt.show()


