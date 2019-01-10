Manual Strategy
===============

-------------- parameters used --------------
- lookback = 50
- symbol = JPM
- in-sample period = 01-01-2008 to 12-31-2009
- out-sample period = 01-01-2010 to 12-31-2011

----------------- code ----------------------
- indicators.py
    - run: python indicators.py
    - output:
        - charts for the following indicators:
            - Simple Moving average as 'sma.pdf'
            - Bollinger Bands as 'bollinger_bands.pdf'
            - SPY/JPM Normalized Price ratio as 'spy_jpm_ratio.pdf'

- BestPossibleStrategy.py
    - run: python BestPossibleStrategy.py
    - output:
        - chart for best possible portfolio strategy as 'bestposible.pdf'


- ManualStrategy.py
    - run: python ManualStrategy.py
    - output:
        - charts for in and out-of-sample data as 'insample.pdf' and outsample.pdf'
        - statistics for portfolio and benchmark
            - cumulative return
            - standard deviation of daily returns
            - mean of daily returns

- marketsimcode.py
    - run: imported into above files
