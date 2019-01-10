import matplotlib
matplotlib.use('Agg')

''' author: Karel Klein Cardena
    userID: kkc3 
'''
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import matplotlib.patches as mpatches

from util import get_data
from marketsimcode import compute_portvals
from indicators import *

class ManualStrategy(object):
    def __init__(self):
        pass

    def testPolicy(self, symbol, start_date, end_date, start_value):
        # get price data
        dates = pd.date_range(start_date, end_date)
        prices = get_data([symbol], dates).drop(['SPY'], axis=1)
        spy = get_data(['SPY'], dates, addSPY=False)
        lookback = 100
        # get sma ratio and convert to show when price is above/below
        sma = get_sma(prices, lookback)[1]
        sma_cross = pd.DataFrame(0, index=sma.index, columns=sma.columns)
        sma_cross[sma >= 1] = 1
        sma_cross[1:] = sma_cross.diff()
        sma_cross.ix[0] = 0
        # get Bollinger Band % and SPY ratio
        bbp = get_bb(prices, lookback)[3]
        spy_ratio = get_spy_ratio(prices, spy)
        # initialize orders
        orders = prices.copy()
        orders.ix[:,:] = np.NaN
        # rules for trading
        for t in range(prices.shape[0]):
            if sma.ix[t,0]<0.95 and bbp.ix[t,0]<0 and spy_ratio.ix[t,0]>0.1:
                orders.ix[t,0] = 1000
            elif sma.ix[t,0]>1.05 and bbp.ix[t,0]>1 and spy_ratio.ix[t,0]<-0.2:
                orders.ix[t,0] = -1000
           # if sma_cross.ix[t,0] != 0:
           #     orders.ix[t,0] = 0

        # forward fill NaN and remaining NaNs with 0
        orders.ffill(inplace=True)
        orders.fillna(0, inplace=True)
        # get orders by taking difference
        orders[1:] = orders.diff()
        orders.ix[0] = 0
        # convert into proper dataframe
        trades = prices.copy()
        trades.ix[:,:] = 0
        trades['Order'] = 0
        trades['Shares'] = 0
        trades.columns = ['Symbol','Order','Shares']
        # fill out the dataframe using orders df
        for t in range(orders.shape[0]):
            order = orders.ix[t,0]
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
        trades.to_csv('mantrades.csv')
        return trades

    def plot_portfolio(self, symbol, portfolio, benchmark, buys, sells):
        fig = plt.figure()
        ax1 = fig.add_subplot(111)
        portfolio.plot(ax=ax1, color='black', lw=1.2)
        benchmark.plot(ax=ax1, color='blue', lw=1.2)
        ax1.set_ylabel('Normalized Portfolio Value')
        ax1.set_xlabel('Date')
        plt.grid(True)
        red_patch = mpatches.Patch(color='black', label='Manual Strategy')
        blue_patch = mpatches.Patch(color='blue', label='Benchmark')
        plt.legend(handles=[red_patch,blue_patch], loc='upper left')
        plt.title('%s Manual Strategy: In-sample Performance' % symbol)
        for b in buys:
            plt.axvline(x=b, color='green')
        for s in sells:
            plt.axvline(x=s, color='red')
        #plt.show()
        plt.savefig('insample.pdf')

    def plot_outsample(self, symbol, portfolio, benchmark):
        fig = plt.figure()
        ax1 = fig.add_subplot(111)
        portfolio.plot(ax=ax1, color='black', lw=1.2)
        benchmark.plot(ax=ax1, color='blue', lw=1.2)
        ax1.set_ylabel('Normalized Portfolio Value')
        ax1.set_xlabel('Date')
        plt.grid(True)
        red_patch = mpatches.Patch(color='black', label='Manual Strategy')
        blue_patch = mpatches.Patch(color='blue', label='Benchmark')
        plt.legend(handles=[red_patch,blue_patch], loc='lower left')
        plt.title('%s Manual Strategy: Out-of-sample Performance' % symbol)
        #plt.show()
        plt.savefig('outsample.pdf')

    def get_trade_dates(self, trades):
        dates = trades.index.tolist()
        buy_dates, sell_dates = [], []
        for t in range(trades.shape[0]):
            if trades.ix[t,'Order'] == 'BUY':
                if trades.ix[t,'Shares'] > 0:
                    buy_dates.append(dates[t])
            elif trades.ix[t,'Order'] == 'SELL':
                if trades.ix[t,'Shares'] > 0:
                    sell_dates.append(dates[t])
        return buy_dates, sell_dates

    def assess_portfolio(self, portfolio, sv):
        #takes in a normalized portfolio
        port_val = sv * portfolio
        cum_return = port_val.ix[-1] / port_val.ix[0] - 1
        daily_ret = port_val / port_val.shift(1) - 1
        std_daily_ret = daily_ret.std()
        avg_daily_ret = daily_ret.mean()
        return cum_return, std_daily_ret, avg_daily_ret

if __name__=="__main__":
    symbol = 'JPM'
    start = '01-01-2008'
    end = '12-31-2009'
    start_value = 100000

    ###### in-sample analysis ######
    ms = ManualStrategy()
    trades = ms.testPolicy(symbol, start, end, start_value)
    buys, sells = ms.get_trade_dates(trades)
    # get benchmark values
    benchmark_trade = ms.testPolicy(symbol, start, end, start_value)
    benchmark_trade.ix[0,'Order'] = 'BUY'
    benchmark_trade.ix[0,'Shares'] = 1000
    benchmark_trade.ix[1:,'Order'] = 'BUY'
    benchmark_trade.ix[1:,'Shares'] = 0
    # get portfolio values
    portfolio_values = compute_portvals(trades, start_val=start_value)
    benchmark_values = compute_portvals(benchmark_trade, start_val=start_value)
    normed_port = portfolio_values / portfolio_values.ix[0]
    normed_bench = benchmark_values / benchmark_values.ix[0]
    # plot portfolio values
    ms.plot_portfolio(symbol, normed_port, normed_bench, buys, sells)
    # get portfolio statistics
    port_cum_return, port_std_daily_ret, port_avg_daily_ret = ms.assess_portfolio(normed_port, start_value)
    bench_cum_return, bench_std_daily_ret, bench_avg_daily_ret = ms.assess_portfolio(normed_bench, start_value)
    # print portfolio statistics
    print '\n---------- In-sample Statistics ----------'
    print 'Portfolio Cumulative Return: %f' % port_cum_return
    print 'Benchmark Cumulative Return: %f\n' % bench_cum_return
    print 'Portfolio Stdev of Daily Returns: %f' % port_std_daily_ret
    print 'Benchmark Stdev of Daily Returns: %f\n' % bench_std_daily_ret
    print 'Portfolio Mean of Daily Returns: %f' % port_avg_daily_ret
    print 'Benchmark Mean of Daily Returns: %f\n' % bench_avg_daily_ret

    ###### comparative analysis - test with out of sample data ######
    start_o = '01-01-2010'
    end_o = '12-31-2011'
    trades_o = ms.testPolicy(symbol, start_o, end_o, start_value)
    benchmark_o = ms.testPolicy(symbol, start_o, end_o, start_value)
    benchmark_o.ix[0,'Order'] = 'BUY'
    benchmark_o.ix[0,'Shares'] = 1000
    benchmark_o.ix[1:,'Order'] = 'BUY'
    benchmark_o.ix[1:,'Shares'] = 0
    # get portfolio values
    portfolio_values_o = compute_portvals(trades_o, start_val=start_value)
    benchmark_values_o = compute_portvals(benchmark_o, start_val=start_value)
    normed_port_o = portfolio_values_o / portfolio_values_o.ix[0]
    normed_bench_o = benchmark_values_o / benchmark_values_o.ix[0]
    # plot portfolio values
    ms.plot_outsample(symbol, normed_port_o, normed_bench_o)
    # get portfolio statistics
    port_cum_return, port_std_daily_ret, port_avg_daily_ret = ms.assess_portfolio(normed_port_o, start_value)
    bench_cum_return, bench_std_daily_ret, bench_avg_daily_ret = ms.assess_portfolio(normed_bench_o, start_value)
    # print portfolio statistics
    print '--------- Out-of-sample Statistics -----------'
    print 'Portfolio Cumulative Return: %f' % port_cum_return
    print 'Benchmark Cumulative Return: %f\n' % bench_cum_return
    print 'Portfolio Stdev of Daily Returns: %f' % port_std_daily_ret
    print 'Benchmark Stdev of Daily Returns: %f\n' % bench_std_daily_ret
    print 'Portfolio Mean of Daily Returns: %f' % port_avg_daily_ret
    print 'Benchmark Mean of Daily Returns: %f\n' % bench_avg_daily_ret
