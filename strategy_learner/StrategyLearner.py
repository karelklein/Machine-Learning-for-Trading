''' 
author: Karel Klein Cardena
userID: kkc3 
'''
import datetime as dt
import pandas as pd
import numpy as np
import util as ut
import random
import RTLearner as rt
import BagLearner as bl
from indicators import *

class StrategyLearner(object):

    # constructor
    def __init__(self, verbose=False, impact=0.0, flag=0):
        self.verbose = verbose
        self.impact = impact
        self.ybuy = 0.001 + self.impact
        self.ysell = -0.001 - self.impact
        self.lookback = 50
        self.N = 30
        self.leaf_size = 10
        self.bags = 15

        if flag==1: # exp 1
            self.ybuy = 0.001 + self.impact
            self.ysell = -0.001 - self.impact
            self.lookback = 50
            self.N = 30
            self.leaf_size = 10
            self.bags = 15

        if flag==2: # exp 2
            self.ybuy = 0.002 + self.impact
            self.ysell = -0.002 - self.impact
            self.lookback = 50
            self.N = 10
            self.leaf_size = 20
            self.bags = 15

        self.baggy = bl.BagLearner(learner=rt.RTLearner, \
            kwargs={'leaf_size':self.leaf_size}, bags=self.bags)

    # this method should create a RTLearner, and train it for trading
    def addEvidence(self, symbol = "AAPL", \
        sd=dt.datetime(2008,1,1), \
        ed=dt.datetime(2009,12,31), \
        sv = 100000):

        # get price data
        syms = [symbol]
        dates = pd.date_range(sd, ed)
        prices = ut.get_data(syms, dates).drop(['SPY'], axis=1)
        spy = ut.get_data(['SPY'], dates, addSPY=False)

        # get indicator data
        sma = get_sma(prices, self.lookback)[1]
        bbp = get_bb(prices, self.lookback)[3]
        spy_ratio = get_spy_ratio(prices, spy)

        sma.fillna(method='bfill', inplace=True)
        bbp.fillna(method='bfill', inplace=True)
        spy_ratio.fillna(method='bfill', inplace=True)

        # concatenate indicators into one df
        dataX = (sma.join(bbp, lsuffix='_sma', rsuffix='_bbp')).join(spy_ratio).as_matrix()

        # calculate returns and make Y data
        returns = [0] * len(prices)
        for t in range(len(prices) - self.N):
            if t < self.N:
                returns[t] = 0
            else:
                returns[t] = (prices.ix[t + self.N].values / prices.ix[t].values - 1)[0]

        Y = [0] * len(returns)
        for i in range(len(returns)):
            if i < self.lookback:
                Y[t] = 0
            elif returns[i] > self.ybuy:
                Y[i] = 1
            elif returns[i] < self.ysell:
                Y[i] = -1
            else:
                Y[i] = 0
        Y = np.array(Y)

        # instantiatiate bag learner and train it
        self.baggy.addEvidence(dataX, Y)

    # this method should use the existing policy and test it against new data
    def testPolicy(self, symbol = "AAPL", \
        sd=dt.datetime(2009,1,1), \
        ed=dt.datetime(2010,12,31), \
        sv = 100000):

        # get price data
        syms = [symbol]
        dates = pd.date_range(sd, ed)
        prices = ut.get_data(syms, dates).drop(['SPY'], axis=1)
        spy = ut.get_data(['SPY'], dates, addSPY=False)

        # get indicator data
        sma = get_sma(prices, self.lookback)[1]
        bbp = get_bb(prices, self.lookback)[3]
        spy_ratio = get_spy_ratio(prices, spy)

        # concatenate indicators into one df
        xtest = (sma.join(bbp, lsuffix='_sma', rsuffix='_bbp')).join(spy_ratio).as_matrix()

        # query the bag learner for test data
        decisions = self.baggy.query(xtest)

        # convert beliefs into trades df
        trades = prices.copy()
        trades.ix[:,:] = 0
        trades.columns = [symbol]

        position = 0
        # fill out the trades df using decisions
        for t in range(1, trades.shape[0]):
            stance = decisions[t]
            position += trades.ix[t-1, symbol]

            if stance > 0:
                if position == 1000:
                    trades.ix[t,:] = 0
                elif position == -1000:
                    trades.ix[t,:] = 2000
                else:
                    trades.ix[t,:] = 1000
            elif stance < 0:
                if position == 1000:
                    trades.ix[t,:] = -2000
                elif position == 0:
                    trades.ix[t,:] = -1000
                else:
                    trades.ix[t,:] = 0
            else:
                trades.ix[t,:] = 0
        return trades

    def author(self):
        return 'kkc3'

if __name__=="__main__":
    print "One does not simply think up a strategy"
