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

# 每个函数必须返回单个实际结果向量 (一维 NumPy 或 Pandas 数组)

def compute_stdev(prices, window=20):
    """ 
    计算标准差 (stdev)
    """
    return prices.rolling(window=window).std()

def compute_sma(prices, window=20):
    """ 计算简单移动平均线 (SMA) """
    return prices.rolling(window=window).mean()

def bollinger_band_value(prices, window=20):
    """
    计算布林带值 (BBV) 或 %B。

    BBV[t] = (价格[t] - SMA[t]) / (2 * stdev[t])
    """
    sma = compute_sma(prices, window)
    stdev = compute_stdev(prices, window)
    
    # 避免除以 0
    stdev_safe = np.where(stdev == 0, 1e-6, stdev)
    
    # 布林带值
    bbv = (prices - sma) / (2 * stdev_safe)
    
    return bbv.values

def simple_moving_average_ratio(prices, window=20):
    """
    计算价格与简单移动平均线 (SMA) 的比率。

    SMAR[t] = 价格[t] / SMA[t]
    """
    sma = compute_sma(prices, window)
    
    # 避免除以 0
    sma_safe = np.where(sma == 0, 1e-6, sma)
    
    smar = prices / sma_safe
    
    return smar.values

def momentum(prices, window=10):
    """
    计算动量 (Momentum)。

    Momentum[t] = (价格[t] / 价格[t - window]) - 1
    """
    mom = (prices / prices.shift(window)) - 1
    
    return mom.values

def commodity_channel_index(prices, window=14):
    """
    计算商品通道指数 (CCI)。

    CCI = (典型价格 - SMA(典型价格)) / (0.015 * 均值偏差)

    注意: 典型价格 (TP) = (最高价 + 最低价 + 收盘价) / 3
    这里我们使用每日收盘价作为 TP 的近似，因为我们只获取收盘价数据。
    """
    # 实际应用中需要 OHLC 数据。此处使用收盘价作为典型价格的近似。
    typical_price = prices
    
    # 1. 计算 SMA(TP)
    sma_tp = typical_price.rolling(window=window).mean()
    
    # 2. 计算均值偏差 (Mean Deviation)
    # 均值偏差是 TP 与 SMA(TP) 差值的 SMA 绝对值
    md = abs(typical_price - sma_tp).rolling(window=window).mean()
    
    # 避免除以 0
    md_safe = np.where(md == 0, 1e-6, md)
    
    # 3. 计算 CCI
    cci = (typical_price - sma_tp) / (0.015 * md_safe)
    
    return cci.values

def percentage_price_oscillator(prices, short_window=12, long_window=26):
    """
    计算百分比价格振荡器 (PPO)。

    PPO = ((EMA_short - EMA_long) / EMA_long) * 100
    """
    # 计算短周期指数移动平均线 (EMA)
    ema_short = prices.ewm(span=short_window, adjust=False).mean()
    
    # 计算长周期指数移动平均线 (EMA)
    ema_long = prices.ewm(span=long_window, adjust=False).mean()
    
    # 避免除以 0
    ema_long_safe = np.where(ema_long == 0, 1e-6, ema_long)

    # 计算 PPO
    ppo = ((ema_short - ema_long) / ema_long_safe) * 100
    
    return ppo.values

def save_plot(filename):
    """Save the current figure using the provided filename."""
    plt.savefig("images/" + filename + ".png", format="png")
    plt.close()

def plot_indicator(df_data, prices, indicator_values, indicator_name, ylabel, window):
    """
    生成并保存单个指标的图表。
    """
    plt.figure(figsize=(10, 6))
    
    # 归一化价格 (用于对比指标)
    normed_prices = prices / prices.iloc[0]
    
    # 指标数据框 (用于绘图)
    df_indicator = pd.DataFrame(index=df_data.index)
    df_indicator[indicator_name] = indicator_values
    df_indicator['Price (Normalized)'] = normed_prices.values
    
    # 创建子图
    ax1 = plt.subplot(211)
    ax1.plot(normed_prices, label="JPM 价格 (归一化)", color='blue')
    ax1.set_title(f"JPM 价格与 {indicator_name} ({window} 窗口)", fontsize=14)
    ax1.set_ylabel("价格 (归一化)", fontsize=10)
    ax1.legend(loc='upper left')
    ax1.grid(True)
    
    ax2 = plt.subplot(212, sharex=ax1)
    ax2.plot(df_indicator[indicator_name], label=indicator_name, color='orange')
    ax2.set_ylabel(ylabel, fontsize=10)
    ax2.set_xlabel("日期", fontsize=10)
    ax2.legend(loc='upper left')
    ax2.grid(True)

    # 对于 BBV 和 CCI，添加额外的水平线以便可视化交易信号
    if indicator_name == 'Bollinger Band Value (BBV)':
        ax2.axhline(y=1.0, color='r', linestyle='--', label='上轨 (+2 SD)')
        ax2.axhline(y=-1.0, color='g', linestyle='--', label='下轨 (-2 SD)')
        ax2.legend(loc='upper left')
    elif indicator_name == 'Commodity Channel Index (CCI)':
        ax2.axhline(y=100, color='r', linestyle='--', label='超买 (+100)')
        ax2.axhline(y=-100, color='g', linestyle='--', label='超卖 (-100)')
        ax2.legend(loc='upper left')

    plt.tight_layout()
    save_plot(f"{indicator_name.replace(' ', '_')}_Plot")


def run_all_indicators(symbol="JPM", sd=dt.datetime(2008, 1, 1), ed=dt.datetime(2009, 12, 31)):
    """
    运行所有指标，计算值并生成图表。
    """
    print("--- 正在计算并绘图技术指标... ---")
    
    dates = pd.date_range(sd, ed)
    prices_all = get_data([symbol], dates)
    prices = prices_all[[symbol]].dropna()
    
    # 确保价格数据是 Pandas Series
    prices = prices[symbol] 
    
    # 定义指标及其参数
    indicators = [
        ('Bollinger Band Value (BBV)', bollinger_band_value, 20, 'BBV 值'),
        ('Simple Moving Average Ratio (SMAR)', simple_moving_average_ratio, 20, '价格/SMA 比率'),
        ('Momentum (MOM)', momentum, 10, '动量'),
        ('Commodity Channel Index (CCI)', commodity_channel_index, 14, 'CCI 值'),
        ('Percentage Price Oscillator (PPO)', percentage_price_oscillator, (12, 26), 'PPO 值')
    ]

    # 存储指标结果向量的字典
    df_indicator_results = pd.DataFrame(index=prices.index)
    
    for name, func, window, ylabel in indicators:
        
        # 兼容性处理：PPO 窗口是元组，其他是整数
        if isinstance(window, tuple):
            result_vector = func(prices, window[0], window[1])
        else:
            result_vector = func(prices, window)
            
        # 将结果转换为 Series (确保索引正确)
        result_series = pd.Series(result_vector, index=prices.index)
        df_indicator_results[name] = result_series
        
        # 绘图
        plot_indicator(prices, prices, result_series, name, ylabel, window)
        print(f"✅ {name} 图表已生成并保存。")
        
    return df_indicator_results

if __name__ == "__main__":
    # 示例运行所有指标
    run_all_indicators()