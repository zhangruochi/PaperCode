%   �����Ƕ�һ��ͼƬ�������ϵ�ϵͳ���룬������������϶ȼ����T�����һϵ�ж���
%   ��ȡall-image�ļ����е�����ͼƬ
file_path =  'E:\senior\medical health\project\on-test\test\';% ͼ���ļ���·��  
img_path_list = dir(strcat(file_path,'*.jpg'));%��ȡ���ļ���������ppm��ʽ��ͼ��  
img_num = length(img_path_list);%��ȡͼ��������  
if img_num > 0 %������������ͼ��  
        for j = 1:img_num %��һ��ȡͼ��  
            image_name = img_path_list(j).name;% ͼ����  
            imageinput =  imread(strcat(file_path,image_name));  
            fprintf('%d %s\n',j,strcat(file_path,image_name));% ��ʾ���ڴ����ͼ����  
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
%%    �����ǽ���LCP������ȡ�Ĺ��̣���Ϊ����Ҫ������ά��������ȡ�������ǽ���8��2�� ��10��3�� ��12��4�� ������һ�飬��󱣴��ڶ�Ӧ�������ļ�����
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





