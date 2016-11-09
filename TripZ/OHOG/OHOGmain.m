%   以下是对一幅图片进行整合的系统代码，不包含卡方拟合度检验和T检验等一系列东西
%   读取all-image文件夹中的所有图片
file_path =  'E:\senior\medical health\project\pre-test\matlab code\feature detection\IMG_sub\Gastric ulcer_Sub\'    % 图像文件夹路径  
img_path_list = dir(strcat(file_path,'*.jpg'));%获取该文件夹中所有jpg格式的图像  
img_num = length(img_path_list);%获取图像总数量  
max = 0
Len = zeros(1,img_num)
%feature =zeros(img_num,6480); %Gastric poly_Sub
%feature = zeros(img_num,3168)
%feature = zeros(img_num,42336)
feature = zeros(img_num,6912)
if img_num > 0 %有满足条件的图像  
        for j = 1:img_num %逐一读取图像  
            image_name = img_path_list(j).name;% 图像名  
            imageinput = imread(strcat(file_path,image_name));  
%      图像处理过程:
%%    首先是进行限制对比度自适应直方图均衡化 CLAHE
%     将图片由RGB色度空间转化为LAB色度空间
cform2lab = makecform('srgb2lab');
LAB = applycform(imageinput, cform2lab);
%     标准化：将所有值设定在[0,1]之间
StreetL = LAB(:,:,1)/100;
%     正式执行限制对比度自适应直方图均衡化（CLAHE)的程序
LAB(:,:,1) = adapthisteq(StreetL,'NumTiles',...
                         [8 8],'ClipLimit',0.005)*100;
%     将LAB色度空间重新转化为RGB色度空间
cform2srgb = makecform('lab2srgb');
Newimage = applycform(LAB, cform2srgb);
%%    以下是进行HOG特征提取的过程

current_feature = OImgHOGFeature(Newimage);
len = length(current_feature)
Len(1,j) = len

if max < len 
   max = len
end 
feature(j,1:len) = current_feature;
        end 
        
%char=strcat('E:\senior\medical health\project\pre-test\matlab code\feature detection\IMG_sub\Gastric polyp_Sub\','Gastric poly_Sub.csv');
%char=strcat('E:\senior\medical health\project\pre-test\matlab code\feature detection\IMG_sub\Gastritis_Sub\','Gastritis_Sub.csv');
%char=strcat('E:\senior\medical health\project\pre-test\matlab code\feature detection\IMG_sub\Normal_Sub\','Normal_Sub.csv');
char=strcat('E:\senior\medical health\project\pre-test\matlab code\feature detection\IMG_sub\Gastric ulcer_Sub\','Gastric ulcer_Sub.csv');

csvwrite(char,feature);
end 