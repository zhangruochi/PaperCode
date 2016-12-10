import pickle
import numpy as np

with open("dataset.pkl","rb") as f:
    dataset = pickle.load(f)

with open("labels.pkl","rb") as f:
    labels = pickle.load(f)


dataset = np.hstack((dataset.real,dataset.imag))
print(dataset.shape)
print(labels)
