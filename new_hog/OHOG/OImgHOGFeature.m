function OHOGFeature = OImgHOGFeature( Img )
% 计算输入图像的特征描述子
% ：已经被imread 后的图片
% cell_size: cell的长*宽
% nblock: block的width、height包括的cell的个数 即 1block=2*2cell
% overlap: block重叠的比例
% angle: 180\360
% bin_num: 方向bin的数目

    % default parameter
    cell_size=16;
    nblock=2;
    overlap=0.5;
    angle=180;
    bin_num=9;
    

    % 简化计算，直接转换成灰度图像
    G = rgb2gray(Img);

 
[height, width] = size(G);
 
% 计算x、y方向的梯度
hx = [-1,0,1];
hy = -hx';
grad_x = imfilter(double(G),hx); % 滤波
grad_y = imfilter(double(G),hy);
 
% 计算梯度的模长
grad_mag=sqrt(grad_x.^2+grad_y.^2);
 
% 计算梯度的方向
index= grad_x==0;
grad_x(index)=1e-5;
YX=grad_y./grad_x;
if angle==180
    grad_angle= ((atan(YX)+(pi/2))*180)./pi; 
elseif angle==360
    grad_angle= ((atan2(grad_y,grad_x)+pi).*180)./pi;
end
 
% orient bin
bin_angle=angle/bin_num;
grad_orient=ceil(grad_angle./bin_angle);
 
% 计算block的个数
block_size=cell_size*nblock;
skip_step=block_size*overlap;
x_step_num=floor((width-block_size)/skip_step+1); % 向下取整 
y_step_num=floor((height-block_size)/skip_step+1);
 
% 初始化hog特征描述子
feat_dim=bin_num*nblock^2; %特征的维数 
OHOGFeature=zeros(feat_dim*x_step_num*y_step_num,1);
% 转化成一个行向量 HOGFeature=zeros(feat_dim*x_step_num*y_step_num,1);
for k=1:y_step_num
    for j=1:x_step_num
        % block的左上角坐标
        x_off = (j-1)*skip_step+1;
        y_off = (k-1)*skip_step+1;
 
        % 取得block的梯度大小和方向
        b_mag=grad_mag(y_off:y_off+block_size-1,x_off:x_off+block_size-1);
        b_orient=grad_orient(y_off:y_off+block_size-1,x_off:x_off+block_size-1);
 
        % 当前block的hog直方图
        currFeat = OBinHOGFeature(b_mag, b_orient, cell_size,nblock, bin_num, false);
        OHOGFeature(feat_dim*((k-1)*x_step_num+j-1)+1:feat_dim*((k-1)*x_step_num+j),1) = currFeat;
 
    end
end
end

 
% 归一化 L2-norm
%sump=sum(blockfeat.^2);
%blockfeat = blockfeat./sqrt(sump+eps^2);