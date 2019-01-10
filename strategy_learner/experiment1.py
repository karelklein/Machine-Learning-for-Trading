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
import matplotlib.patches as mpatches
import StrategyLearner as sl
import ManualStrategy as ms
from marketsimcode import compute_portvals

def assess_portfolio(portfolio, sv):
        #takes in a normalized portfolio
        port_val = sv * portfolio
        cum_return = port_val.ix[-1] / port_val.ix[0] - 1
        daily_ret = port_val / port_val.shift(1) - 1
        std_daily_ret = daily_ret.std()
        avg_daily_ret = daily_ret.mean()
        return cum_return, std_daily_ret, avg_daily_ret

def plot_portfolio(symbol, manual, learner, benchmark):
        fig = plt.figure()
        ax1 = fig.add_subplot(111)
        manual.plot(ax=ax1, color='black', lw=1.2)
        learner.plot(ax=ax1, color='red', lw=1.2)
        benchmark.plot(ax=ax1, color='blue', lw=1.2)
        ax1.set_ylabel('Normalized Portfolio Value')
        ax1.set_xlabel('Date')
        plt.grid(True)
        black_patch = mpatches.Patch(color='black', label='Manual Strategy')
        red_patch = mpatches.Patch(color='red', label='Strategy Learner')
        blue_patch = mpatches.Patch(color='blue', label='Benchmark')
        plt.legend(handles=[black_patch,red_patch, blue_patch], loc='upper left')
        plt.title('%s ManualStrategy vs StrategyLearner: In-sample' % symbol)
        plt.savefig('exp1a.pdf')

if __name__=='__main__':

	# in-sample period
	symbol = 'JPM'
	start = '01-01-2008'
	end = '12-31-2009'
	start_value = 100000
	impact = 0.005

    # Manual Strategy
	ms = ms.ManualStrategy()
	trades = ms.testPolicy(symbol, start, end, start_value)

    # Strategy Learner
	sd=dt.datetime(2008,1,1)
	ed=dt.datetime(2009,12,31)
	sl = sl.StrategyLearner(impact=impact, flag=1)
	sl.addEvidence(symbol=symbol, sd=sd, ed=ed, sv=start_value)
	trades_sl = sl.testPolicy(symbol=symbol, sd=sd, ed=ed, sv=start_value)

    # Benchmark
	benchmark_trade = ms.testPolicy(symbol, start, end, start_value)
	benchmark_trade.ix[0,'Order'] = 'BUY'
	benchmark_trade.ix[0,'Shares'] = 1000
	benchmark_trade.ix[1:,'Order'] = 'BUY'
	benchmark_trade.ix[1:,'Shares'] = 0

    # get manual strategy and benchmark values
	portfolio_values = compute_portvals(trades, start_val=start_value)
	benchmark_values = compute_portvals(benchmark_trade, start_val=start_value)
	normed_port = portfolio_values / portfolio_values.ix[0]
	normed_bench = benchmark_values / benchmark_values.ix[0]

    # get strategy learner portfolio values
	port_values_sl = compute_portvals(trades_sl, start_val=start_value)
	normed_port_sl = port_values_sl / port_values_sl.ix[0]

    # plot the 3 portfolios
	plot_portfolio(symbol, normed_port, normed_port_sl, normed_bench)

    # get portfolio statistics
	port_cum_return, port_std_daily_ret, port_avg_daily_ret = ms.assess_portfolio(normed_port, start_value)
	bench_cum_return, bench_std_daily_ret, bench_avg_daily_ret = ms.assess_portfolio(normed_bench, start_value)
	sl_cum_return, sl_std_daily_ret, sl_avg_daily_ret = assess_portfolio(normed_port_sl, start_value)

    # print portfolio statistics
	print '\n---------- In-sample Statistics ----------'
	print 'ManualStrategy Cumulative Return: %f' % port_cum_return
	print 'StrategyLearner Cumulative Return: %f' % sl_cum_return
	print 'Benchmark Cumulative Return: %f\n' % bench_cum_return

	print 'ManualStrategy Stdev of Daily Returns: %f' % port_std_daily_ret
	print 'StrategyLearner Stdev of Daily Returns: %f' % sl_std_daily_ret
	print 'Benchmark Stdev of Daily Returns: %f\n' % bench_std_daily_ret

	print 'ManualStrategy Mean of Daily Returns: %f' % port_avg_daily_ret
	print 'StrategyLearner Mean of Daily Returns: %f' % sl_avg_daily_ret
	print 'Benchmark Mean of Daily Returns: %f\n' % bench_avg_daily_ret
