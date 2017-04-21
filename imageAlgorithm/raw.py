import numpy as np

a = np.eye(6)

for i in a:
    

def get_block(im,n):
    x = int(im.shape[0]/n)
    y = int(im.shape[1]/n)
    block_list = []
    
    start_x = 0
    end_x = x

    for i in range(n):
        start_y = 0
        end_y = y
        for j in range(n):
            block_list.append(im[start_x:end_x,start_y:end_y])
            start_y = end_y
            end_y += y

        start_x = end_x
        end_x += x    

    

       
    return block_list  

block_list = get_block(a,1)
print(len(block_list))
for _ in block_list:
    print(_)
    print("")

