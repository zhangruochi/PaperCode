import numpy as np
a = np.zeros(16)
print(type(a))

b = np.zeros((16))
print(type(b))


print(np.vstack((a,b)))