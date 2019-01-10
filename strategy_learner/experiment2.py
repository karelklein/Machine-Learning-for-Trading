import matplotlib
matplotlib.use('Agg')

''' 
author: Karel Klein Cardena
userID: kkc3 
'''
import numpy as np
import pandas as pd
import datetime as dt
import matplotlib.pyplot as plt
import StrategyLearner as sle
from marketsimcode import compute_portvals

def assess_portfolio(portfolio, sv):
        #takes in a normalized portfolio
        port_val = sv * portfolio
        cum_return = port_val.ix[-1] / port_val.ix[0] - 1
        daily_ret = port_val / port_val.shift(1) - 1
        std_daily_ret = daily_ret.std()
        avg_daily_ret = daily_ret.mean()
        return cum_return, std_daily_ret, avg_daily_ret

def plot_results(x, y, title, ylabel, filename):
        plt.plot(x, y)
        plt.title(title)
        plt.xlabel('Impact')
        plt.ylabel(ylabel)
        plt.grid(True)
        plt.savefig(filename + '.pdf')

# how would changing the value of impact affect 
# in sample trading behavior and results (provide at least two metrics)

if __name__=='__main__':
	# in-sample period
	symbol = 'JPM'
	start = '01-01-2008'
	end = '12-31-2009'
	start_value = 100000
	impacts = np.arange(0,10.)/100 + 0.005

	# arrays for gathering results
	num_trades_array = []
	cum_returns = []
	std_daily_rets = []
	avg_daily_rets = []

	for impact in impacts:
	    # Strategy Learner
		sd=dt.datetime(2008,1,1)
		ed=dt.datetime(2009,12,31)
		sl = sle.StrategyLearner(impact=impact, flag=2)
		sl.addEvidence(symbol=symbol, sd=sd, ed=ed, sv=start_value)
		trades_sl = sl.testPolicy(symbol=symbol, sd=sd, ed=ed, sv=start_value)

		# count the number of trades that occured
		num_trades = 0
		for i in range(trades_sl.shape[0]):
			if trades_sl.ix[i,symbol] != 0:
				num_trades += 1
		num_trades_array.append(num_trades)

		# get strategy learner portfolio values
		port_values_sl = compute_portvals(trades_sl, start_val=start_value)
		normed_port_sl = port_values_sl / port_values_sl.ix[0]
		sl_cum_return, sl_std_daily_ret, sl_avg_daily_ret = assess_portfolio(normed_port_sl, start_value)

		cum_returns.append(sl_cum_return)
		std_daily_rets.append(sl_std_daily_ret)
		avg_daily_rets.append(sl_avg_daily_ret)

	# plot results
	#plot_results(impacts, num_trades_array, 'Impact vs Number of Trades', 'Number of Trades Executed' ,'exp2aa')
	plot_results(impacts, cum_returns, 'Impact vs Cumulative Return', 'Cumulative Return', 'exp2bb')
