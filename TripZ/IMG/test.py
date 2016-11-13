from PIL import Image
import glob, os
import numpy as np

def rotation(degree):
    im = Image.open("doraemon.jpg").rotate(degree)
    im.save("doraemon2.jpg")
    im.show()


def thumbnail(factor):
    for infile in glob.glob("*.jpg"):
        file, ext = os.path.splitext(infile)
        im = Image.open(infile)
        print(im.size)
        size = im.size[0] / factor, im.size[1] / factor
        im.thumbnail(size)
        print(im.size)
        im.save(file + ".thumbnail", "JPEG")
        im.show()

def test_distance():
    a = np.array([1,2,3])
    b = np.array([4,5,6])
    c = b-a

    print(np.sqrt(np.sum(np.square(c))))

def test_size(factor = None):
    dd = float("inf") 
    if 10000 < dd:
        print("yes!")
    


if __name__ == '__main__':
    #rotation(45)  
    #thumbnail(2)  
    test_distance()
    #test_size(2)