import matplotlib
matplotlib.use('Agg')

''' 
author: Karel Klein Cardena
userID: kkc3 
'''
import pandas as pd
import matplotlib.pyplot as plt
import matplotlib.patches as mpatches
import numpy as np
from util import get_data

def get_sma(prices, lookback):
    # calculate simple moving average
    sma = prices.rolling(window=lookback, min_periods=lookback).mean()
    sma_ratio = prices / sma
    return sma, sma_ratio

def get_bb(prices, lookback):
    # calculate Bollinger Bands
    sma, _ = get_sma(prices, lookback)
    rolling_std = prices.rolling(window=lookback, min_periods=lookback).std()
    top_bb = sma + (2 * rolling_std)
    bot_bb = sma - (2 * rolling_std)
    bbp = (prices - bot_bb) / (top_bb - bot_bb)
    return top_bb, bot_bb, sma, bbp

def get_spy_ratio(prices, spy_prices):
    # calculate ratio of spy to stock
    prices.columns = ['SPY']
    normed = prices / prices.ix[0]
    normed_spy = spy_prices / spy_prices.ix[0]
    ratio = normed_spy/normed
    indicator = ratio / ratio.ix[0] - 1
    indicator.columns = ['Ratio']
    return indicator

################## Now plot the indicators ##################

def plot_sma(prices, lookback):
    sma, ratio = get_sma(prices, lookback)
    fig = plt.figure()
    ax1 = fig.add_subplot(111)
    ax2 = ax1.twinx()
    prices.plot(ax=ax1, color='blue', legend=False, lw=1.2)
    sma.plot(ax=ax1, color='orange', legend=False, lw=2.4)
    ratio.plot(ax=ax2, color='purple', legend=False)
    ax1.set_ylabel('Price')
    ax1.set_xlabel('Date')
    ax2.set_ylabel('Price/SMA')
    plt.grid(True)
    red_patch = mpatches.Patch(color='blue', label='Price')
    blue_patch = mpatches.Patch(color='orange', label='SMA')
    purp_patch = mpatches.Patch(color='purple', label='Price/SMA')
    plt.legend(handles=[red_patch,blue_patch,purp_patch], loc='lower left')
    plt.title('JPM %i-day Simple Moving Average' % lookback)
    #plt.show()
    plt.savefig('sma.pdf')

def plot_bb(prices, lookback):
    top_band, bot_band, sma, bbp = get_bb(prices, lookback)
    fig = plt.figure()
    ax = fig.add_subplot(111)
    ax2 = ax.twinx()
    prices.plot(ax=ax, color='green', lw=1.2)
    top_band.plot(ax=ax, color='orange', lw=2)
    bot_band.plot(ax=ax, color='blue', lw=2)
    sma.plot(ax=ax, legend=False, color='purple', lw=2.4)
    bbp.plot(ax=ax2, legend=False, color='brown', lw=.7)
    ax.set_xlabel('Date')
    ax.set_ylabel('Price')
    plt.grid(True)
    red_patch = mpatches.Patch(color='green', label='Price')
    or_patch = mpatches.Patch(color='orange', label='Top BB')
    blue_patch = mpatches.Patch(color='blue', label='Bottom BB')
    lblue_patch = mpatches.Patch(color='brown', label='BB %')
    purp_patch = mpatches.Patch(color='purple', label='SMA')
    plt.legend(handles=[red_patch,or_patch, blue_patch, purp_patch, lblue_patch], loc='lower left')
    plt.title('JPM Bollinger Bands with %i-day lookback' % lookback)
    #plt.show()
    plt.savefig('bollinger_bands.pdf')

def plot_spy_ratio(prices, spy_prices):
    ratio = get_spy_ratio(prices, spy_prices)
    fig = plt.figure()
    ax1 = fig.add_subplot(111)
    ax2 = ax1.twinx()
    normed = prices / prices.ix[0]
    normed_spy = spy_prices / spy_prices.ix[0]
    normed.plot(ax=ax1, color='orange', lw=1.2 ,legend=False)
    normed_spy.plot(ax=ax1, color='green', lw=1.2, legend=False)
    ratio.plot(ax=ax2, color='blue', lw=1.2)
    ax1.set_ylabel('Normalized Price')
    ax2.set_ylabel('Ratio of SPY to JPM')
    ax1.set_xlabel('Date')
    plt.grid(True)
    or_patch = mpatches.Patch(color='orange', label='JPM')
    green_patch = mpatches.Patch(color='green', label='SPY')
    blue_patch = mpatches.Patch(color='blue', label='Ratio of SPY to JPM')
    plt.legend(handles=[or_patch, green_patch, blue_patch], loc='lower left')
    plt.title('SPY-to-JPM Normalized Ratio Indicator')
    #plt.show()
    plt.savefig('spy_jpm_ratio.pdf')

if __name__ == "__main__":
    start = '01-01-2008'
    end = '12-31-2009'
    dates = pd.date_range(start, end)
    prices = get_data(['JPM'], dates).drop(['SPY'], axis=1)
    spy = get_data(['SPY'], dates, addSPY=False)
    sma = get_sma(prices, 50)[1]
    print (sma.join(sma, lsuffix='_sma', rsuffix='_sma')).join(sma).as_matrix()
    #sma_plot = plot_sma(prices, 50)
    #bb_plot = plot_bb(prices, 50)
    #ratio_plot = plot_spy_ratio(prices, spy)
