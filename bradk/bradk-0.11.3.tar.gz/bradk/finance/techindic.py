
# coding: utf-8

# In[1]:


import numpy as np
import matplotlib.pyplot as plt
import matplotlib.dates as mdates


# In[2]:


def get_RSI(xx, AVGPERIODS): # Relative Strength Index (RSI)
    # ref) http://stockcharts.com/school/doku.php?id=chart_school:technical_indicators:relative_strength_index_rsi
    assert(len(xx.shape) == 1) # assert that xx be rank 0
    Change = np.full(xx.shape, 0) # initialize
    Change[1:] = np.diff(xx, n=1)
    Gain = np.full(xx.shape, 0) # initialize
    Gain[Change > 0] = Change[Change > 0]
    Loss = np.full(xx.shape, 0) # initialize
    Loss[Change < 0] = np.absolute(Change[Change < 0])
    AvgGain = np.full(xx.shape, np.nan) # initialize
    AvgLoss = np.full(xx.shape, np.nan) # initialize
    RS = np.full(xx.shape, np.nan) # ref) https://stackoverflow.com/questions/1704823/initializing-numpy-matrix-to-something-other-than-zero-or-one
    RSI = np.full(xx.shape, np.nan)
    #----------------------------------------------------------------
    AvgGain[AVGPERIODS-1] = np.mean(Gain[:AVGPERIODS])
    AvgLoss[AVGPERIODS-1] = np.mean(Loss[:AVGPERIODS])
    RS[AVGPERIODS-1] = AvgGain[AVGPERIODS-1] / AvgLoss[AVGPERIODS-1]
    RSI[AVGPERIODS-1] = 100 - 100 / (1 + RS[AVGPERIODS-1])
    for n in range(AVGPERIODS, len(xx)):
        AvgGain[n] = (AvgGain[n-1]*(AVGPERIODS - 1) + Gain[n]) / AVGPERIODS
        AvgLoss[n] = (AvgLoss[n-1]*(AVGPERIODS - 1) + Loss[n]) / AVGPERIODS
        RS[n] = AvgGain[n] / AvgLoss[n]
        RSI[n] = 100 - 100 / (1 + RS[n])    
    return RSI
def get_EMA(xx, AVGPERIODS): # Moving Averages - Simple and Exponential
    # ref) http://stockcharts.com/school/doku.php?id=chart_school:technical_indicators:moving_averages
    assert(len(xx.shape) == 1) # assert that xx be rank 0
    Multiplier = 2 / (AVGPERIODS + 1)
    EMA = np.full(xx.shape, np.nan)
    if AVGPERIODS < len(xx):
        EMA[AVGPERIODS-1] = np.mean(xx[:AVGPERIODS])
    for n in range(AVGPERIODS, len(xx)):
        EMA[n] = (xx[n] - EMA[n-1])*Multiplier + EMA[n-1]
    return EMA
def get_MACD(xx, AVGPERIODS1, AVGPERIODS2, AVGPERIODS3): # MACD (Moving Average Convergence/Divergence Oscillator)
    # ref) http://stockcharts.com/school/doku.php?st=macd&id=chart_school:technical_indicators:moving_average_convergence_divergence_macd
    assert(len(xx.shape) == 1) # assert that xx be rank 0
    MACD = get_EMA(xx, AVGPERIODS1) - get_EMA(xx, AVGPERIODS2)
    SIGNAL = np.full(xx.shape, np.nan); # initialize
    SIGNAL[~np.isnan(MACD)] = get_EMA(MACD[~np.isnan(MACD)], AVGPERIODS3);
    MACD_HIST = MACD - SIGNAL
    return MACD, SIGNAL, MACD_HIST
def get_OBV(price, volume): # On Balance Volume (OBV)
    # ref) https://stockcharts.com/school/doku.php?id=chart_school:technical_indicators:on_balance_volume_obv
    assert(len(price.shape) == 1) # make sure that the rank is 0
    assert(len(volume.shape) == 1) # make sure that the rank is 0
    assert(len(price.shape) == len(volume.shape)) # make sure that the ranks are the same
    up_down = np.diff(price, n=1) # detect the up and down of the price
    up_down[up_down > 0] = +1 # plus sign
    up_down[up_down < 0] = -1 # minus sign
    sign_volume = up_down * volume[1:] # exclude the first element of volume
    OBV = np.full(price.shape, np.nan) # initialize
    OBV[1:] = np.cumsum(sign_volume)
    return OBV
def get_MovingMomentumStrategy(prices, EMA_short_period = 15, EMA_long_period = 200, RSI_period = 14
                               , MACD_period1 = 12, MACD_period2 = 26, MACD_period3 = 9):
    EMA_short = get_EMA(prices, EMA_short_period) # 15
    EMA_long = get_EMA(prices, EMA_long_period) # 200
    RSI = get_RSI(prices, RSI_period) # 14
    MACD, SIGNAL, MACD_HIST = get_MACD(prices, MACD_period1, MACD_period2, MACD_period3) # 12, 26, 9
    return EMA_short, EMA_long, RSI, MACD_HIST
def plot_MovingMomentumStrategy(dates, prices, EMA_short, EMA_long, RSI, MACD_HIST):
    # ref) https://matplotlib.org/examples/pylab_examples/subplots_demo.html
    # ref) https://matplotlib.org/faq/usage_faq.html
    f, (ax1, ax2, ax3) = plt.subplots(3, sharex=True, sharey=True, figsize=(16, 15))
    ax1.plot_date(dates, prices, 'k.-') # prices vs. dates
    ax1.plot_date(dates, EMA_short, 'r-') # prices vs. short MV
    ax1.plot_date(dates, EMA_long, 'b-') # prices vs. long MV
    ax1.set_ylabel('Price')
    ax1.xaxis.grid(which='major')
    ax1.xaxis.grid(which='minor')
    ax1.yaxis.grid()
    ax2.plot_date(dates, prices, 'k.-') # prices vs. dates
    ax2.set_ylabel('Price')
    ax22 = ax2.twinx()
    ax22.plot_date(dates, RSI, 'r-') # RSI vs. dates
    ax22.plot_date(dates, 70 + np.zeros(dates.shape), 'b-.') # auxiliary line
    ax22.plot_date(dates, 50 + np.zeros(dates.shape), 'b-.') # auxiliary line
    ax22.plot_date(dates, 30 + np.zeros(dates.shape), 'b-.') # auxiliary line
    ax22.set_ylabel('RSI [%]')
    ax2.xaxis.grid(which='major')
    ax2.xaxis.grid(which='minor')
    ax2.yaxis.grid()
    ax3.plot_date(dates, prices, 'k.-') # prices vs. dates
    ax3.set_ylabel('Price')
    ax32 = ax3.twinx()
#    ax32.bar(dates, MACD_HIST, 1.0, color='c') # MACD_HIST vs. dates       # TOO SLOW
    ax32.plot_date(dates, MACD_HIST, 'b-') # MACD_HIST vs. dates
    ax32.plot_date(dates, 0 + np.zeros(dates.shape), 'b-') # auxiliary line
    ax32.set_ylabel('MACD_HIST')
    ax3.xaxis.grid(which='major')
    ax3.xaxis.grid(which='minor')
    ax3.yaxis.grid()
    ax3.xaxis.set_major_locator(mdates.YearLocator())
#    ax3.xaxis.set_major_formatter(mdates.DateFormatter('%Y '))
    ax3.xaxis.set_minor_locator(mdates.MonthLocator())
#    ax3.xaxis.set_minor_formatter(mdates.DateFormatter('%m'))
    f.autofmt_xdate()
    f.subplots_adjust(hspace=0)
    #plt.setp([a.get_xticklabels() for a in f.axes[:-1]], visible=False)
#    plt.xlim(min_date, max_date)
    plt.show()

