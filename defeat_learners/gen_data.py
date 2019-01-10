import numpy as np
import math

# this function should return a dataset (X and Y) that will work
# better for linear regression than decision trees
def best4LinReg(seed=1489683273):
    np.random.seed(seed)

    X = np.random.random((100,3))
    Y = X[:,0] + X[:,1] + X[:,2]
    return X, Y

def best4DT(seed=1489683273):
    np.random.seed(seed)

    X = np.random.random((100,2))
    y = []
    for i in range(X.shape[0]):
        a, b = X[i,0], X[i,1]
        if a > 0.5:
            if b > 0.5: y.append(-200)
            else: y.append(100)
        else:
            if b > 0.5: y.append(50)
            else: y.append(-300)

    Y = np.array(y)
    return X, Y

def author():
    return 'kkc3'

if __name__=="__main__":
    print "they call me Tim."
