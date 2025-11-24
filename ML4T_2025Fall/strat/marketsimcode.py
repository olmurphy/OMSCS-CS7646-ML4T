from util import get_data
import datetime as dt
import pandas as pd

def compute_portvals(
    orders_df, 
    start_val=100000, 
    commission=9.95, 
    impact=0.005, 
    symbol="JPM"
):
    """
    使用交易数据框计算投资组合价值。
    orders_df: 每日交易的数据框 (e.g., +1000, -2000, 0)
    start_val: 初始资金 (sv)
    commission: 交易佣金
    impact: 市场影响
    symbol: 交易的股票代码
    返回: 投资组合每日价值的 Pandas Series
    """
    
    # 1. 获取价格数据
    dates = orders_df.index
    start_date = dates.min()
    end_date = dates.max()
    
    # 注意：这里的 get_data 必须是可用的。
    # 假设 get_data 已经在 marketsimcode.py 或其导入的 util.py 中可用
    prices_all = get_data([symbol, 'SPY'], pd.date_range(start_date, end_date)) 
    prices = prices_all[[symbol]].copy() # 目标股票的调整后收盘价，确保是 DataFrame
    prices = prices.fillna(method='ffill').fillna(method='bfill')
    
    # 2. 交易矩阵 (记录每日的股数变化)
    trades = orders_df.copy() # 使用输入的交易数据框
    
    # 3. 持仓矩阵 (记录每日结束时的持仓数量)
    holdings = pd.DataFrame(index=trades.index, columns=[symbol, 'Cash'], data=0.0)
    
    # 4. 初始化
    current_cash = start_val
    current_holdings = 0
    
    # 5. 遍历交易
    for date in trades.index:
        current_trade = trades.loc[date, symbol]
        price = prices.loc[date, symbol]
        
        # 交易成本 (佣金 + 市场影响)
        trade_cost = commission + abs(current_trade) * price * impact
        
        # 现金流: 股票价值 +/- 交易成本
        cash_flow = -current_trade * price - trade_cost
        
        # 更新持仓和现金
        current_holdings += current_trade
        current_cash += cash_flow
        
        holdings.loc[date, symbol] = current_holdings
        holdings.loc[date, 'Cash'] = current_cash
        
    # 6. 投资组合价值 (需要考虑非交易日的填充)
    # 确保 holdings 和 prices 的索引匹配，并处理非交易日
    
    # 合并 prices 和 holdings 索引，用于计算最终的投资组合价值
    all_dates = pd.date_range(start_date, end_date)
    holdings = holdings.reindex(all_dates).fillna(method='ffill')
    prices = prices.reindex(all_dates).fillna(method='ffill')

    portvals = prices[symbol] * holdings[symbol] + holdings['Cash']
    
    return portvals

def compute_portfolio_stats(port_val, rfr=0.0, sf=252.0):
    """
    计算投资组合的累计收益、平均每日收益和每日收益标准差。
    这是metrics.py中要求的核心功能。
    port_val: 投资组合价值的 Pandas Series
    rfr: 无风险利率 (默认 0.0)
    sf: 采样频率 (默认 252.0，代表一年中的交易日)
    返回: cr (累计收益), adr (平均每日收益), sddr (每日收益标准差)
    """
    # 每日收益率 (Daily Returns)
    # 使用 .iloc[1:] 排除第一个 NaN
    dr = (port_val / port_val.shift(1) - 1).iloc[1:]

    # 累计收益率 (Cumulative Return)
    cr = (port_val.iloc[-1] / port_val.iloc[0]) - 1

    # 平均每日收益率 (Average Daily Return)
    adr = dr.mean()

    # 每日收益率的标准差 (Standard Deviation of Daily Return)
    sddr = dr.std()

    return cr, adr, sddr

def compute_portfolio_values(df_trades, start_val=100000, commission=0.00, impact=0.00):
    """                                                                                               
    Computes the portfolio values.                                                                                                
    """
    # Determine date range and stock symbols
    dates = df_trades.index
    symbols = df_trades.columns.tolist()

    prices = get_data(symbols, dates)
    prices['Cash'] = 1.0

    # init holdings & values DF
    df_holdings = pd.DataFrame(0.0, index=prices.index, columns=symbols + ['Cash'])
    df_values = pd.DataFrame(0.0, index=prices.index, columns=['Value'])
    
    # initial portfolio cash
    df_holdings.iloc[0, df_holdings.columns.get_loc('Cash')] = start_val
    
    # daily trades
    df_orders = df_trades.copy()
    
    # init daily holdings volume
    df_holdings.iloc[0] = df_holdings.iloc[0].copy()

    # iterate through trading days
    for i in range(len(df_orders)):
        date = df_orders.index[i]
        
        if i > 0:
            df_holdings.iloc[i] = df_holdings.iloc[i-1].copy()

        for symbol in symbols:
            shares = df_orders.loc[date, symbol]
            
            if shares != 0:
                price = prices.loc[date, symbol]
                trade_value = shares * price
                
                cost = commission + abs(trade_value * impact)
                df_holdings.loc[date, symbol] += shares
                df_holdings.loc[date, 'Cash'] -= trade_value + cost
                
        df_values.loc[date, 'Value'] = (df_holdings.iloc[i] * prices.iloc[i]).sum()
    return df_values

def create_benchmark_trades(symbol, sd, ed):
    """
    创建基准策略的交易数据框: 第一天买入 1000 股，持有至结束。
    """
    # 假设 get_data 已经在 marketsimcode.py 或其导入的 util.py 中可用
    dates = pd.date_range(sd, ed)
    prices_all = get_data([symbol], dates)
    prices_df = prices_all[[symbol]].fillna(method='ffill').fillna(method='bfill')
    
    # 初始化交易数据框
    trades = pd.DataFrame(0, index=prices_df.index, columns=[symbol])
    
    # 项目要求: 以 10 万美元现金为初始资金，投资于首个交易日使用的股票代码的 1000 股
    # 第一天买入 1000 股
    if not prices_df.empty:
        first_trade_date = prices_df.index[0]
        trades.loc[first_trade_date, symbol] = 1000
    
    # 注意：我们通常不需要在最后一天平仓，因为 compute_portvals 会处理最后一个交易日的资产价值。
    # 如果项目要求平仓，则取消注释以下代码：
    # if not prices_df.empty and len(prices_df) > 1:
    #     last_trade_date = prices_df.index[-1]
    #     trades.loc[last_trade_date, symbol] = -1000 

    return trades

if __name__ == "__main__":
    start_date = dt.datetime(2008, 1, 1)
    end_date = dt.datetime(2009, 12, 31)
    test_symbol = 'JPM'
    
    # create ex trades DataFrame (buy 1000 shares, hold, then sell 1000 shares)
    dates = pd.date_range(start_date, end_date)
    prices_full = get_data([test_symbol], dates)
    prices_full = prices_full[[test_symbol]]

    df_trades_example = pd.DataFrame(0.0, index=prices_full.index, columns=[test_symbol])
    
    # ex trade: buy 1000 shares on first day
    first_trade_date = df_trades_example.index[0]
    df_trades_example.loc[first_trade_date, test_symbol] = 1000 

    # ex trade: close position on last day
    last_trade_date = df_trades_example.index[-1]
    df_trades_example.loc[last_trade_date, test_symbol] = -1000
    
    # calc portfolio values (using commission 0.00, impact 0.00)
    portvals = compute_portfolio_values(
        df_trades_example, 
        start_val=100000, 
        commission=0.00, 
        impact=0.00
    )

def author():                                                                                             
    return "omurphy8"   

def study_group():
    return "omurphy8"