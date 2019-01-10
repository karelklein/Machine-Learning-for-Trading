"""MC1-P2: Optimize a portfolio."""

import pandas as pd
import matplotlib.pyplot as plt
import numpy as np
import datetime as dt
from util import get_data, plot_data
from scipy.optimize import minimize

# This is the function that will be tested by the autograder
# The student must update this code to properly implement the functionality
def optimize_portfolio(sd=dt.datetime(2008,1,1), ed=dt.datetime(2009,1,1), \
    syms=['GOOG','AAPL','GLD','XOM'], gen_plot=False):

    # Read in adjusted closing prices for given symbols, date range
    dates = pd.date_range(sd, ed)
    prices_all = get_data(syms, dates)  # automatically adds SPY
    prices = prices_all[syms]  # only portfolio symbols
    prices_SPY = prices_all['SPY']  # only SPY, for comparison later

    # find the allocations for the optimal portfolio
    def compute_stats(prices, allocs, sv):
        normed = prices / prices.ix[0]
        alloced =  allocs * normed
        port_val = sv * alloced.sum(axis=1)
        # compute statistics
        cr = port_val.ix[-1] / port_val.ix[0] - 1
        daily_ret = port_val / port_val.shift(1) - 1
        adr = daily_ret.mean()
        sddr = daily_ret.std()
        sf = 252
        sr = sf ** 0.5 * (adr - 0) / sddr
        ev = port_val.ix[-1]

        return cr, adr, sddr, sr, ev

    def minimize_func_vol(allocs, prices):
        sv = 1
        return compute_stats(prices, allocs, sv)[2]

    noa = len(syms)
    cons = ({'type': 'eq', 'fun': lambda x: np.sum(x) - 1})
    bnds = tuple((0, 1) for x in range(noa))
    alloc_guess = [1. / noa] * noa

    optv = minimize(minimize_func_vol, alloc_guess, args=(prices), method='SLSQP', bounds=bnds, constraints=cons)

    allocs = optv['x']
    cr, adr, sddr, sr, ev = compute_stats(prices, allocs, 1)


    # Get daily portfolio value
    port_val = prices_SPY # add code here to compute daily portfolio values

    # Compare daily portfolio value with SPY using a normalized plot
    if gen_plot:
        # add code to plot here
        normed_SPY = prices_SPY / prices_SPY.ix[0]
        normed = prices / prices.ix[0]
        alloced =  allocs * normed

        df_temp = pd.concat([alloced.sum(axis=1), normed_SPY], keys=['Portfolio', 'SPY'], axis=1)
        plot_data(df_temp, title="Daily Portfolio Value and SPY", xlabel="Date", \
            ylabel="Normalized price")        
        pass

    return allocs, cr, adr, sddr, sr

def test_code():
    # This function WILL NOT be called by the auto grader
    # Do not assume that any variables defined here are available to your function/code
    # It is only here to help you set up and test your code

    # Define input parameters
    # Note that ALL of these values will be set to different values by
    # the autograder!

    start_date = dt.datetime(2008,6,1)
    end_date = dt.datetime(2009,6,1)
    symbols = ['IBM', 'X', 'GLD']

    # Assess the portfolio
    allocations, cr, adr, sddr, sr = optimize_portfolio(sd = start_date, ed = end_date,\
        syms = symbols, \
        gen_plot = True)

    # Print statistics
    print "Start Date:", start_date
    print "End Date:", end_date
    print "Symbols:", symbols
    print "Allocations:", allocations
    print "Sharpe Ratio:", sr
    print "Volatility (stdev of daily returns):", sddr
    print "Average Daily Return:", adr
    print "Cumulative Return:", cr

if __name__ == "__main__":
    # This code WILL NOT be called by the auto grader
    # Do not assume that it will be called
    test_code()
