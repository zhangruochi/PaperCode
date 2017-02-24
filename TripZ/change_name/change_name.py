import os 

folder_name = "."
index = 0
for file_name in os.listdir(folder_name): 
    if file_name.endswith(".jpg"):
        new_name = str(index) +'.jpg' 
        os.rename(os.path.join(folder_name,file_name),os.path.join(folder_name,new_name)) 
        print(file_name,'ok') 
        index += 1
    