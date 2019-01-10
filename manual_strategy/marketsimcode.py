"""MC2-P1: Market simulator."""

import pandas as pd
import numpy as np
import datetime as dt
import os
from util import get_data, plot_data

def author():
    return 'kkc'

def compute_portvals(orders, start_val = 1000000, commission=9.95, impact=0.005):
    # this is the function the autograder will call to test your code
    # NOTE: orders_file may be a string, or it may be a file object. Your
    # code should work correctly with either input
    # TODO: Your code here

    # get min and max dates
    start_date = orders.index.min()
    end_date = orders.index.max()
    # get list of symbols
    symbols = []
    for s in orders.ix[:,0]:
        if s not in symbols:
            symbols.append(s)

    dates = pd.date_range(start_date, end_date)
    prices = get_data(symbols, dates)
    prices = prices[symbols]

    # add column for cash
    prices['Cash'] = [1] * prices.shape[0]
    # make a copy for trades, and fill in with zeros
    trades = prices.copy()
    trades.ix[:,:] = np.zeros((trades.shape[0], trades.shape[1]))

    # step through orders and fill in trades
    for date, row in orders.iterrows():
        # get symbol, order, shares from orders
        sym = row['Symbol']
        order = row['Order']
        shares1 = row['Shares']
        sign = 0
        if order == 'BUY':
            sign = 1
        else:
            sign = -1

        shares = sign * int(shares1)
        # get price of symbol from prices
        price = float(prices[sym][date])
        # fill in trades and cash
        trades.loc[date,sym] += shares
        trades.loc[date,'Cash'] += shares * price * -1
        # deduct commission and market impact
        trades.loc[date,'Cash'] -= (commission + impact * price * shares1)


    # make holdings dataframe and add start_val to cash
    holdings = trades.copy().cumsum()
    holdings['Cash'] = holdings['Cash'] + start_val
    # make values DataFrame
    values = prices * holdings
    # get portfolio values
    portfolio_values = values.sum(axis=1)

    return portfolio_values

def test_code():
    # this is a helper function you can use to test your code
    # note that during autograding his function will not be called.
    # Define input parameters

    of = "./orders/orders-01.csv"
    sv = 1000000

    # Process orders
    port_val = compute_portvals(orders_file = of, start_val = sv,\
    commission=0.0, impact=0.0)
    if isinstance(port_val, pd.DataFrame):
        port_val = port_val[port_val.columns[0]] # just get the first column
    else:
        "warning, code did not return a DataFrame"

    # Get portfolio stats
    # Here we just fake the data. you should use your code from previous assignments.
    start_date = port_val.index.min()
    end_date = port_val.index.max()
    #cum_ret, avg_daily_ret, std_daily_ret, sharpe_ratio = [0.2,0.01,0.02,1.5]
    #cum_ret_SPY, avg_daily_ret_SPY, std_daily_ret_SPY, sharpe_ratio_SPY = [0.2,0.01,0.02,1.5]

    cum_ret = port_val.ix[-1] / port_val.ix[0] - 1
    daily_ret = port_val / port_val.shift(1) - 1
    avg_daily_ret = daily_ret.mean()
    std_daily_ret = daily_ret.std()
    sharpe_ratio = 252 ** 0.5 * (avg_daily_ret) / std_daily_ret

    # Compare portfolio against $SPX
    print "Date Range: {} to {}".format(start_date, end_date)
    print
    print "Sharpe Ratio of Fund: {}".format(sharpe_ratio)
    #print "Sharpe Ratio of SPY : {}".format(sharpe_ratio_SPY)
    print
    print "Cumulative Return of Fund: {}".format(cum_ret)
    #print "Cumulative Return of SPY : {}".format(cum_ret_SPY)
    print
    print "Standard Deviation of Fund: {}".format(std_daily_ret)
    #print "Standard Deviation of SPY : {}".format(std_daily_ret_SPY)
    print
    print "Average Daily Return of Fund: {}".format(avg_daily_ret)
    #print "Average Daily Return of SPY : {}".format(avg_daily_ret_SPY)
    print
    print "Final Portfolio Value: {}".format(port_val[-1])

if __name__ == "__main__":
    test_code()
