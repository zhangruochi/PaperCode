%   �����Ƕ�һ��ͼƬ�������ϵ�ϵͳ���룬������������϶ȼ����T�����һϵ�ж���
%   ��ȡall-image�ļ����е�����ͼƬ
file_path =  'E:\senior\medical health\project\pre-test\matlab code\feature detection\IMG_sub\Gastric ulcer_Sub\'    % ͼ���ļ���·��  
img_path_list = dir(strcat(file_path,'*.jpg'));%��ȡ���ļ���������jpg��ʽ��ͼ��  
img_num = length(img_path_list);%��ȡͼ��������  
max = 0
Len = zeros(1,img_num)
%feature =zeros(img_num,6480); %Gastric poly_Sub
%feature = zeros(img_num,3168)
%feature = zeros(img_num,42336)
feature = zeros(img_num,6912)
if img_num > 0 %������������ͼ��  
        for j = 1:img_num %��һ��ȡͼ��  
            image_name = img_path_list(j).name;% ͼ����  
            imageinput = imread(strcat(file_path,image_name));  
%      ͼ�������:
%%    �����ǽ������ƶԱȶ�����Ӧֱ��ͼ���⻯ CLAHE
%     ��ͼƬ��RGBɫ�ȿռ�ת��ΪLABɫ�ȿռ�
cform2lab = makecform('srgb2lab');
LAB = applycform(imageinput, cform2lab);
%     ��׼����������ֵ�趨��[0,1]֮��
StreetL = LAB(:,:,1)/100;
%     ��ʽִ�����ƶԱȶ�����Ӧֱ��ͼ���⻯��CLAHE)�ĳ���
LAB(:,:,1) = adapthisteq(StreetL,'NumTiles',...
                         [8 8],'ClipLimit',0.005)*100;
%     ��LABɫ�ȿռ�����ת��ΪRGBɫ�ȿռ�
cform2srgb = makecform('lab2srgb');
Newimage = applycform(LAB, cform2srgb);
%%    �����ǽ���HOG������ȡ�Ĺ���

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