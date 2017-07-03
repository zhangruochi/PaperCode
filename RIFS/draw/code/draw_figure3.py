#!/usr/bin/env python3

#info
#-name   : zhangruochi
#-email  : zrc720@gmail.com


import matplotlib.pyplot as plt
import numpy as np

plt.figure(1,figsize = (8,6))


font = {#'family' : 'serif',  
        'color'  : '#000000',  
        'weight' : 'normal',  
        'size'   : 14,  
        }  

#-----------figure 1 ---------------
ALL1 = [ 1.000,   1.000,   1.000,   1.000,   1.000] 
ALL2 = [ 0.795,   0.795,   0.795,   0.799,   0.799]
ALL3 = [ 0.856,   0.856,   0.856,   0.883,   0.883] 
ALL4 = [ 0.906,   0.930,   0.939,   0.939,   0.939] 
x = [1,2,3,4,5]

plt.subplot(321)
plt.plot(x,ALL1,color = "#000000", marker='o',label = "ALL1")
plt.plot(x, ALL2, color = "#696969", marker = '^',label = "ALL2")
plt.plot(x, ALL3, color = "#808080", marker = 's',label = "ALL3")
plt.plot(x, ALL4, color = "#A9A9A9", marker = 'D',label = "ALL4")



plt.legend(loc='upper center',ncol = 4,fontsize = 6)
plt.title("PstartingPercentage=10%")
plt.ylim(0.750,1.100)

#-----------figure 2 ---------------
ALL1=[    1.000,   1.000,   1.000,   1.000,   1.000 ] 
ALL2=[    0.795,   0.795,   0.795,   0.799,   0.799 ] 
ALL3=[    0.856,   0.863,   0.863,   0.883,   0.883 ] 
ALL4=[    0.906,   0.930,   0.939,   0.939,   0.939 ]

x = [1,2,3,4,5]

plt.subplot(322)
plt.plot(x,ALL1,color = "#000000", marker='o',label = "ALL1")
plt.plot(x, ALL2, color = "#696969", marker = '^',label = "ALL2")
plt.plot(x, ALL3, color = "#808080", marker = 's',label = "ALL3")
plt.plot(x, ALL4, color = "#A9A9A9", marker = 'D',label = "ALL4")



plt.legend(loc='upper center',ncol = 4,fontsize = 6)
plt.title("PstartingPercentage=20%")
plt.ylim(0.750,1.100)


#-----------figure 3 ---------------
ALL1 = [    1.000,   1.000,   1.000,   1.000,   1.000 ] 
ALL2 = [    0.795,   0.795,   0.796,   0.816,   0.799 ] 
ALL3 = [    0.856,   0.863,   0.863,   0.883,   0.883 ] 
ALL4 = [    0.906,   0.930,   0.939,   0.939,   0.939 ]

x = [1,2,3,4,5]

plt.subplot(323)
plt.plot(x,ALL1,color = "#000000", marker='o',label = "ALL1")
plt.plot(x, ALL2, color = "#696969", marker = '^',label = "ALL2")
plt.plot(x, ALL3, color = "#808080", marker = 's',label = "ALL3")
plt.plot(x, ALL4, color = "#A9A9A9", marker = 'D',label = "ALL4")



plt.legend(loc='upper center',ncol = 4,fontsize = 6)
plt.title("PstartingPercentage=30%")
plt.ylim(0.750,1.100)


#-----------figure 4 ---------------
ALL1  = [  1,   1,   1,   1,   1 ]
ALL2  = [ 0.795,   0.795,   0.809,   0.806,   0.806 ]
ALL3  = [ 0.856,   0.863,   0.863,   0.883,   0.883 ]
ALL4  = [ 0.91,    0.93,    0.939,   0.949,   0.949 ]

x = [1,2,3,4,5]

plt.subplot(324)
plt.plot(x,ALL1,color = "#000000", marker='o',label = "ALL1")
plt.plot(x, ALL2, color = "#696969", marker = '^',label = "ALL2")
plt.plot(x, ALL3, color = "#808080", marker = 's',label = "ALL3")
plt.plot(x, ALL4, color = "#A9A9A9", marker = 'D',label = "ALL4")

 
plt.legend(loc='upper center',ncol = 4,fontsize = 6)
plt.title("PstartingPercentage=40%")
plt.ylim(0.750,1.100)


#-----------figure 5 ---------------
ALL1  = [   1,   1,   1,   1,   1 ]
ALL2  = [ 0.795,   0.795,   0.809,   0.806,   0.806 ]
ALL3  = [ 0.856,   0.863,   0.863,   0.883,   0.883 ]
ALL4  = [ 0.91,    0.93,    0.939,   0.949,   0.949 ]

x = [1,2,3,4,5]

plt.subplot(313)
plt.plot(x,ALL1,color = "#000000", marker='o',label = "ALL1")
plt.plot(x, ALL2, color = "#696969", marker = '^',label = "ALL2")
plt.plot(x, ALL3, color = "#808080", marker = 's',label = "ALL3")
plt.plot(x, ALL4, color = "#A9A9A9", marker = 'D',label = "ALL4")


plt.legend(loc='upper center',ncol = 4,fontsize = 6)
plt.title("PstartingPercentage=50%")
plt.ylim(0.750,1.100)


plt.tight_layout()
plt.savefig('Figure3.svg',format='svg')
plt.savefig('Figure3.png',dpi = 600)
plt.show()