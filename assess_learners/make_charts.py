import numpy as np
import math
import LinRegLearner as lrl
import DTLearner as dtl
import InsaneLearner as il
import BagLearner as bl
import RTLearner as rtl
import sys
import matplotlib.pyplot as plt
import util
import time

def get_rmse(n_leaves):

    inf = 'Istanbul.csv'

    rmse_train, rmse_test = [], []
    percents = np.arange(0.05,0.8,0.05)
    for i in percents:
        with util.get_learner_data_file(inf) as f:
            alldata = np.genfromtxt(f,delimiter=',')
            # Skip the date column and header row if we're working on Istanbul data
            alldata = alldata[1:,1:]
            datasize = alldata.shape[0]
            cutoff = int(datasize * i)
            permutation = np.random.permutation(alldata.shape[0])
            col_permutation = np.random.permutation(alldata.shape[1]-1)
            train_data = alldata[permutation[:cutoff],:]
            trainX = train_data[:,col_permutation]
            trainY = train_data[:,-1]
            test_data = alldata[permutation[cutoff:],:]
            testX = test_data[:,col_permutation]
            testY = test_data[:,-1]

            n = 10
        #times_dt, times_rt = [], []
        #for n in range(1, n_leaves + 1):
            #learner = bl.BagLearner(learner=dtl.DTLearner, kwargs={"leaf_size":n}, bags=20)
            #learner = il.InsaneLearner(verbose=False)

            # rtlearner = rtl.RTLearner(leaf_size=n)
            # t0 = time.time()
            # rtlearner.addEvidence(trainX, trainY) # train it
            # t1 = time.time()
            # times_rt.append(t1-t0)

            learner = rtl.RTLearner(leaf_size=n)
            t2 = time.time()
            learner.addEvidence(trainX, trainY)
            t3 = time.time()
            #times_dt.append(t3-t2)

            # evaluate in sample
            predY = learner.query(trainX) # get the predictions
            rmse_1 = math.sqrt(((trainY - predY) ** 2).sum()/trainY.shape[0])
            rmse_train.append(rmse_1)
            c = np.corrcoef(predY, y=trainY)

            # evaluate out of sample
            predY = learner.query(testX) # get the predictions
            rmse_2 = math.sqrt(((testY - predY) ** 2).sum()/testY.shape[0])
            rmse_test.append(rmse_2)
            c = np.corrcoef(predY, y=testY)

    return rmse_train, rmse_test, percents

def plot_rmse(n_leaves, rmse_train, rmse_test, perc):
    plt.plot(perc, rmse_train, label='Train', color='blue', linewidth=3.0)
    plt.plot(perc, rmse_test, label='Test', color='orange', linewidth=3.0)
    #plt.title('Random Tree Learner: Leaf Size vs RMSE')
    plt.title('Random Tree Learning Curve')
    plt.xlabel('Training Set Size')
    plt.ylabel('RMSE')
    plt.legend(loc='upper right')
    plt.grid(True)
    plt.show()

if __name__=="__main__":
    N = 15
    train_error, test_error, percents = get_rmse(N)
    plot_rmse(N, train_error, test_error, percents)
    #timeDT, timeRT = get_rmse(N)
    #plot_rmse(N, timeDT, timeRT)
