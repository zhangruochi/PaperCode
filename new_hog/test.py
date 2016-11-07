import numpy as np
from sklearn.decomposition import PCA

pca = PCA(n_components = 1)
X = np.array([[-1, -1], [-2, -1], [-3, -2], [1, 1], [2, 1], [3, 2]])
print(X.shape)
new_X =  pca.fit_transform(X)
print(new_X)