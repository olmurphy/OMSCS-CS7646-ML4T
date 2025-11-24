import numpy as np

def author():                                                                                             
    return "omurphy8"   

def study_group():
    return "omurphy8"

def compute_stdev(prices, window=20):
    return prices.rolling(window=window).std()

def compute_sma(prices, window=20):
    return prices.rolling(window=window).mean()

# 商品通道指数 (CCI)
def commodity_channel_index(prices, window=14):
    typical_price = prices
    sma_tp = typical_price.rolling(window=window).mean()
    
    # calc mean deviation (MD)
    # MD is the SMA of the absolute difference between TP and SMA(TP)
    md = abs(typical_price - sma_tp).rolling(window=window).mean()
    
    # 避免除以 0，使用一个小的安全值
    md_safe = np.where(md == 0, 1e-6, md)
    
    # calc CCI
    cci = (typical_price - sma_tp) / (0.015 * md_safe)

    # 返回 Series，方便后续合并
    return cci.values

# 价格百分比振荡器 (PPO)
def percentage_price_oscillator(prices, short_window=12, long_window=26):
    # calc Short-period Exponential Moving Average (EMA)
    ema_short = prices.ewm(span=short_window, adjust=False).mean()
    
    # calc Long-period Exponential Moving Average (EMA)
    ema_long = prices.ewm(span=long_window, adjust=False).mean()
    
    # aoid division by 0
    ema_long_safe = np.where(ema_long == 0, 1e-6, ema_long)

    # calc PPO
    ppo = ((ema_short - ema_long) / ema_long_safe) * 100
    
    return ppo.values

# 动量
def momentum(prices, window=10):
    mom = (prices / prices.shift(window)) - 1
    return mom.values
