import os

def main():
    main_folder = os.getcwd()
    for folder in os.listdir():
        if folder != ".DS_Store" and not folder.endswith(".py"):
            move_images(os.path.join(main_folder,folder))


def move_images(folder_path):
    os.chdir(folder_path)
    main_folder = os.getcwd()

    if not os.path.exists("result"):
        os.mkdir("result")

    foldername = os.listdir()
    foldername.remove(".DS_Store") 
 
    
    for folder in foldername:
        if folder.endswith("Img"):
            big_folder_name = folder
            big_folder_list = os.listdir(folder)
            foldername.remove(folder)

    small_folder_list = ["".join(filename.split("_s")).replace("(","") for filename in os.listdir(foldername[0])]
    for filename in big_folder_list:
        """
        #批量去除文件名中的(
        if "(" in filename:
            new_name = filename.replace("(","")
            os.system("mv {} {}".format(os.path.join(os.getcwd(),big_folder_name,filename.replace("(","\(")),os.path.join(os.getcwd(),big_folder_name,new_name)))  # ( 字符需要转义 eg: os.system("mv I\(mag imag")
        """    
         
        if filename in small_folder_list:  #/Users/ZRC/Desktop/work/Gastric_polyp
            print("moving: ",filename)
            os.system("cp {} result/".format(os.path.join(os.getcwd(),big_folder_name,filename)))    
        


    #测试  看转移后的文件夹中的 image 的数量和 sub 文件夹中image 的数量是否相同
    if len(os.listdir("result")) == len(small_folder_list):
        print("\n\n moving {} successful! \n\n".format(big_folder_name))     

if __name__ == '__main__':
    main()        