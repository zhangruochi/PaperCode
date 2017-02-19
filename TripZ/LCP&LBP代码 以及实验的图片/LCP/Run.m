%   以下是对一幅图片进行整合的系统代码，不包含卡方拟合度检验和T检验等一系列东西
%   读取all-image文件夹中的所有图片
file_path =  'E:\senior\medical health\project\on-test\test\';% 图像文件夹路径  
img_path_list = dir(strcat(file_path,'*.jpg'));%获取该文件夹中所有ppm格式的图像  
img_num = length(img_path_list);%获取图像总数量  
if img_num > 0 %有满足条件的图像  
        for j = 1:img_num %逐一读取图像  
            image_name = img_path_list(j).name;% 图像名  
            imageinput =  imread(strcat(file_path,image_name));  
            fprintf('%d %s\n',j,strcat(file_path,image_name));% 显示正在处理的图像名  
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
%%    以下是进行LCP特征提取的过程，因为所需要的是三维特征的提取，所以是将（8，2） （10，3） （12，4） 都运行一遍，最后保存在对应的三个文件夹中
mapping1=getmapping(10,'3');
[feature_vector] = LCP(double(Newimage),3,10,mapping1,'i');
firstline=[feature_vector]';
%mapping2=getmapping(10,'riu2');
%[feature_vector] = LCP(double(Newimage),3,10,mapping2,'i');
%secondline=[feature_vector];
%mapping2=getmapping(12,'riu2');
%[feature_vector] = LCP(double(Newimage),4,12,mapping2,'i');
%thirdline=[feature_vector];
char1=strcat('E:\senior\medical health\project\on-test\test\',mat2str(j),'.csv');
%char2=strcat('121eyecharacterim',mat2str(j),'.csv');
%char3=strcat('169eyecharacterim',mat2str(j),'.csv');
csvwrite(char1,firstline);
%csvwrite(char2,secondline);
%csvwrite(char3,thirdline);
        end  
end  





