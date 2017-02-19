%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%
%  Compute the LCP Feature, both the pattern occurrence
%   and linear configuration coefficients are calculated
%             
%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%

function [feature_vector] = LCP_Feature(result,Neighbor_Tensor,d_C,patterncode)
% Version 1.0
% Author: Yimo Guo

M = (result==patterncode);

nSize = size(Neighbor_Tensor,3);
patternOccu = sum(M(:));

for index1 = 1:size(Neighbor_Tensor,3)
    PlaneTemp=Neighbor_Tensor(:,:,index1);
    resultTemp(:,index1)=PlaneTemp(M);
end

DC_Plane = d_C(M);

if(patternOccu >= nSize)
    A = inv(resultTemp'*resultTemp)*resultTemp'*double(DC_Plane);
    featureCoe = abs(fft(A));
else %Small sample size occurs, set all linear configuration coefficient to zero
    featureCoe = zeros(nSize,1)
end

feature_vector = [featureCoe;patternOccu]; %Output feature is in column format

