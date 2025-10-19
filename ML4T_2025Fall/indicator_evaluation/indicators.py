import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import datetime as dt
from util import get_data

def author():                                                                                             
    """                                                                                               
    :return: The GT username of the student                                                                                               
    :rtype: str                                                                                               
    """                                                                                               
    return "omurphy8"   

def study_group():
    """
    Returns
        A comma separated string of GT_Name of each member of your study group
        # Example: "gburdell3, jdoe77, tbalch7" or "gburdell3" if a single individual working alone
    """
    return "omurphy8"

# Each function must return a single actual result vector (1D NumPy or Pandas array)

def compute_stdev(prices, window=20):
    return prices.rolling(window=window).std()

def compute_sma(prices, window=20):
    return prices.rolling(window=window).mean()

def bollinger_band_value(prices, window=20):
    """
    cal Bollinger Band Value (BBV) or %B.

    BBV[t] = (Price[t] - SMA[t]) / (2 * stdev[t])
    """
    sma = compute_sma(prices, window)
    stdev = compute_stdev(prices, window)
    
    # Avoid division by 0
    stdev_safe = np.where(stdev == 0, 1e-6, stdev)
    
    # BBV
    bbv = (prices - sma) / (2 * stdev_safe)
    return bbv.values

def simple_moving_average_ratio(prices, window=20):
    """
    calc the ratio of price to sma

    SMAR[t] = Price[t] / SMA[t]
    """
    sma = compute_sma(prices, window)
    
    # Avoid division by zero
    sma_safe = np.where(sma == 0, 1e-6, sma)
    
    smar = prices / sma_safe
    return smar.values

def momentum(prices, window=10):
    """
    Calculate Momentum.

    Momentum[t] = (Price[t] / Price[t - window]) - 1
    """
    mom = (prices / prices.shift(window)) - 1
    return mom.values

def commodity_channel_index(prices, window=14):
    """
    Calculate Commodity Channel Index (CCI).

    CCI = (Typical Price - SMA(Typical Price)) / (0.015 * Mean Deviation)

    Note: Typical Price (TP) = (High + Low + Close) / 3
    Here we use daily closing price as an approximation for TP, as we only retrieve closing price data.
    """
    typical_price = prices
    sma_tp = typical_price.rolling(window=window).mean()
    
    # calc mean deviation (MD)
    # MD is the SMA of the absolute difference between TP and SMA(TP)
    md = abs(typical_price - sma_tp).rolling(window=window).mean()
    
    # Avoid division by 0
    md_safe = np.where(md == 0, 1e-6, md)
    
    # calc CCI
    cci = (typical_price - sma_tp) / (0.015 * md_safe)
    return cci.values

def percentage_price_oscillator(prices, short_window=12, long_window=26):
    """
    Calculate Percentage Price Oscillator (PPO).

    PPO = ((EMA_short - EMA_long) / EMA_long) * 100
    """
    # calc Short-period Exponential Moving Average (EMA)
    ema_short = prices.ewm(span=short_window, adjust=False).mean()
    
    # calc Long-period Exponential Moving Average (EMA)
    ema_long = prices.ewm(span=long_window, adjust=False).mean()
    
    # aoid division by 0
    ema_long_safe = np.where(ema_long == 0, 1e-6, ema_long)

    # calc PPO
    ppo = ((ema_short - ema_long) / ema_long_safe) * 100
    
    return ppo.values

def save_plot(filename):
    """Save the current figure using the provided filename."""
    plt.savefig("images/" + filename + ".png", format="png")
    plt.close()

def plot_indicator(df_data, prices, indicator_values, indicator_name, ylabel, window):
    """
    Generate and save a chart for a single indicator.
    """
    plt.figure(figsize=(10, 6))
    
    # Normalize prices (for comparison with the indicator)
    normed_prices = prices / prices.iloc[0]
    
    # Indicator DataFrame (for plotting)
    df_indicator = pd.DataFrame(index=df_data.index)
    df_indicator[indicator_name] = indicator_values
    df_indicator['Price (Normalized)'] = normed_prices.values
    
    # Create subplots
    ax1 = plt.subplot(211)
    ax1.plot(normed_prices, label="JPM Price (Normalized)", color='blue')
    ax1.set_title(f"JPM Price and {indicator_name} ({window} Window)", fontsize=14)
    ax1.set_ylabel("Price (Normalized)", fontsize=10)
    ax1.legend(loc='upper left')
    ax1.grid(True)
    
    ax2 = plt.subplot(212, sharex=ax1)
    ax2.plot(df_indicator[indicator_name], label=indicator_name, color='orange')
    ax2.set_ylabel(ylabel, fontsize=10)
    ax2.set_xlabel("Date", fontsize=10)
    ax2.legend(loc='upper left')
    ax2.grid(True)

    # For BBV and CCI, add extra horizontal lines for visualizing trading signals
    if indicator_name == 'Bollinger Band Value (BBV)':
        ax2.axhline(y=1.0, color='r', linestyle='--', label='Upper Band (+2 SD)')
        ax2.axhline(y=-1.0, color='g', linestyle='--', label='Lower Band (-2 SD)')
        ax2.legend(loc='upper left')
    elif indicator_name == 'Commodity Channel Index (CCI)':
        ax2.axhline(y=100, color='r', linestyle='--', label='Overbought (+100)')
        ax2.axhline(y=-100, color='g', linestyle='--', label='Oversold (-100)')
        ax2.legend(loc='upper left')

    plt.tight_layout()
    save_plot(f"{indicator_name.replace(' ', '_')}_Plot")


def run_all_indicators(symbol="JPM", sd=dt.datetime(2008, 1, 1), ed=dt.datetime(2009, 12, 31)):
    """
    Run all indicators, calculate values, and generate charts.
    """
    dates = pd.date_range(sd, ed)
    prices_all = get_data([symbol], dates)
    prices = prices_all[[symbol]].dropna()
    
    # ensure price data is Pandas Series
    prices = prices[symbol] 
    
    # def indicators & their parameters for better code organization
    indicators = [
        ('Bollinger Band Value (BBV)', bollinger_band_value, 20, 'BBV Value'),
        ('Simple Moving Average Ratio (SMAR)', simple_moving_average_ratio, 20, 'Price/SMA Ratio'),
        ('Momentum (MOM)', momentum, 10, 'Momentum'),
        ('Commodity Channel Index (CCI)', commodity_channel_index, 14, 'CCI Value'),
        ('Percentage Price Oscillator (PPO)', percentage_price_oscillator, (12, 26), 'PPO Value')
    ]

    # dic store indicator result vectors
    df_indicator_results = pd.DataFrame(index=prices.index)
    
    for name, func, window, ylabel in indicators:
        
        # compatibility handling: PPO window is tuple, others ints
        if isinstance(window, tuple):
            result_vector = func(prices, window[0], window[1])
        else:
            result_vector = func(prices, window)
            
        # convert result -> Series, ensure idx correct
        result_series = pd.Series(result_vector, index=prices.index)
        df_indicator_results[name] = result_series
        
        plot_indicator(prices, prices, result_series, name, ylabel, window)
        
    return df_indicator_results

if __name__ == "__main__":
    run_all_indicators()