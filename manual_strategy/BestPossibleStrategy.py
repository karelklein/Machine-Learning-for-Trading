import matplotlib
matplotlib.use('Agg')

import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
import matplotlib.patches as mpatches

from util import get_data
from marketsimcode import compute_portvals

class BestPossibleStrategy(object):
    def __init__(self):
        pass

    def testPolicy(self, symbol, start_date, end_date, start_value):
        # get price data
        dates = pd.date_range(start_date, end_date)
        prices = get_data([symbol], dates).drop(['SPY'], axis=1)
        # initialize trades dataframe
        df_trades = prices.copy()
        df_trades.ix[:,:] = 0

        pos = 0
        for t in range(prices.shape[0] - 1):
            if prices.ix[t+1,0] > prices.ix[t,0]:
                if pos == 1000:
                    df_trades.ix[t,0] = 0
                elif pos == 0:
                    df_trades.ix[t,0] = 1000
                    pos += 1000
                elif pos == -1000:
                    df_trades.ix[t,0] = 2000
                    pos += 2000
            elif prices.ix[t+1,0] < prices.ix[t,0]:
                if pos == 1000:
                    df_trades.ix[t,0] = -2000
                    pos -= 2000
                elif pos == 0:
                    df_trades.ix[t,0] = -1000
                    pos -= 1000
                elif pos == -1000:
                    df_trades.ix[t,0] = 0
            elif prices.ix[t+1,0] == prices.ix[t,0]:
                df_trades.ix[t,0] = 0

        # make a proper trades dataframe
        trades = prices.copy()
        trades.ix[:,:] = 0
        trades['Order'] = 0
        trades['Shares'] = 0
        trades.columns = ['Symbol','Order','Shares']
        for t in range(df_trades.shape[0]):
            order = df_trades.ix[t,0]
            trades.ix[t,'Symbol'] = symbol
            if order < 0:
                trades.ix[t,'Order'] = 'SELL'
                trades.ix[t,'Shares'] = abs(order)
            elif order > 0:
                trades.ix[t,'Order'] = 'BUY'
                trades.ix[t,'Shares'] = abs(order)
            else:
                trades.ix[t,'Order'] = 'BUY'
                trades.ix[t,'Shares'] = 0
        return trades

    def assess_portfolio(self, portfolio, sv):
        #takes in a normalized portfolio
        port_val = sv * portfolio
        cum_return = port_val.ix[-1] / port_val.ix[0] - 1
        daily_ret = port_val / port_val.shift(1) - 1
        std_daily_ret = daily_ret.std()
        avg_daily_ret = daily_ret.mean()
        return cum_return, std_daily_ret, avg_daily_ret

    def plot_portfolio(self, symbol, portfolio, benchmark):
        fig = plt.figure()
        ax1 = fig.add_subplot(111)
        portfolio.plot(ax=ax1, color='black', lw=1.2)
        benchmark.plot(ax=ax1, color='blue', lw=1.2)
        ax1.set_ylabel('Normalized Portfolio Value')
        ax1.set_xlabel('Date')
        plt.grid(True)
        red_patch = mpatches.Patch(color='black', label='Best Strategy')
        blue_patch = mpatches.Patch(color='blue', label='Benchmark')
        plt.legend(handles=[red_patch,blue_patch], loc='upper left')
        plt.title('%s Best Possible Strategy' % symbol)
        #plt.show()
        plt.savefig('bestpossible.pdf')

if __name__=="__main__":
    symbol = 'JPM'
    start_value = 100000
    start = '01-01-2008'
    end = '12-31-2009'
    bps = BestPossibleStrategy()
    # create portfolio and benchmark trades dataframes
    trades = bps.testPolicy(symbol, start, end, start_value)
    benchmark_trade = bps.testPolicy(symbol, start, end, start_value)
    benchmark_trade.ix[0,'Order'] = 'BUY'
    benchmark_trade.ix[0,'Shares'] = 1000
    benchmark_trade.ix[1:,'Order'] = 'BUY'
    benchmark_trade.ix[1:,'Shares'] = 0
    # get portfolio values
    portfolio_values = compute_portvals(trades, start_val=start_value, commission=0., impact=0.)
    benchmark_values = compute_portvals(benchmark_trade, start_val=start_value, commission=0., impact=0.)
    normed_port = portfolio_values / portfolio_values.ix[0]
    normed_bench = benchmark_values / benchmark_values.ix[0]
    # plot portfolio values
    bps.plot_portfolio(symbol, normed_port, normed_bench)
    # get portfolio statistics
    port_cum_return, port_std_daily_ret, port_avg_daily_ret = bps.assess_portfolio(normed_port, start_value)
    bench_cum_return, bench_std_daily_ret, bench_avg_daily_ret = bps.assess_portfolio(normed_bench, start_value)
    # print portfolio statistics
    print 'Portfolio Cumulative Return: %f' % port_cum_return
    print 'Benchmark Cumulative Return: %f\n' % bench_cum_return
    print 'Portfolio Stdev of Daily Returns: %f' % port_std_daily_ret
    print 'Benchmark Stdev of Daily Returns: %f\n' % bench_std_daily_ret
    print 'Portfolio Mean of Daily Returns: %f' % port_avg_daily_ret
    print 'Benchmark Mean of Daily Returns: %f' % bench_avg_daily_ret
