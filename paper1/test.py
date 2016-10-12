import numpy as np


a = np.array([ 2,7,1,-3,0,10,15,-2,36,-1, -4,  1,  3, 39,  8,  5,  1,0])
b = np.array([  6,   1,   1,   7,   9,   7,  36,   4, 626,   0,   0,  74,   4,  13,  24,   4,   4,  -1])

c = abs(np.mean(a) - np.mean(b)) / pow( pow(np.std(a),2) / len(a) + pow(np.std(b),2) / len(b), 0.5 )
print(c)

from scipy.stats import ttest_rel
from scipy.stats import ttest_ind
from scipy.stats import ttest_ind_from_stats

print(ttest_rel(a,b))
print(ttest_ind(a,b))
print(ttest_ind_from_stats(np.mean(a),np.std(a),len(a),np.mean(b),np.std(b),len(b)))



from sklearn.cross_validation import KFold

a = list(KFold(9,n_folds=3,shuffle=True))
print(a)