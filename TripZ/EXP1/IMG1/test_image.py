from PIL import Image
import numpy as np
from matplotlib import pyplot as plt
from scipy.ndimage import filters


def get_magnitude(im,sigma = 5):
    #sigma 标准差
    imx = np.zeros(im.shape)
    filters.gaussian_filter(im, (sigma,sigma), (0,1), imx)
    imy = np.zeros(im.shape)
    filters.gaussian_filter(im, (sigma,sigma), (1,0), imy)
    
    magnitude = np.sqrt(imx**2+imy**2)   #梯度幅值
    direction = np.arctan(np.divide(imy,imx))       #梯度方向
    direction[np.isnan(direction) | np.isinf(direction)] = 0
    print(direction)
    return magnitude,direction


im = Image.open("MultilobulatedAdenoma_21.jpg")
get_magnitude(np.array(im.convert("L")))
