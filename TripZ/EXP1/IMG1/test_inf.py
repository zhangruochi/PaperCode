import numpy as np
import pickle


def test1():
    a = np.array([[1,2,3],[4,5,6]])
    b = np.array([[1,2,3],[2,0,0]])

    c = np.divide(a,b)
    print(c)

    c[np.isnan(c) | np.isinf(c)] = 0
    print(np.isnan(c) & np.isinf(c))
    print(c)

def test2():  
    with open("Gastric_polyp_P_two.pkl","rb") as f:
        dataset = pickle.load(f)
        print(dataset)

        

if __name__ == '__main__':
    test2()     