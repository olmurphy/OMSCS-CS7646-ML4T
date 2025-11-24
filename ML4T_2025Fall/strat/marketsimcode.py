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
    Computes the portfolio value using the daily trades DataFrame.
    orders_df: DataFrame of daily trades (e.g., +1000, -2000, 0)
    start_val: Initial cash (sv)
    commission: Transaction commission
    impact: Market impact
    symbol: The stock ticker being traded
    Returns: A Pandas Series of the portfolio's daily value
    """
    
    # 1. Get price data
    dates = orders_df.index
    start_date = dates.min()
    end_date = dates.max()
    
    # Note: get_data must be available here.
    # Assumes get_data is available in marketsimcode.py or the imported util.py
    prices_all = get_data([symbol, 'SPY'], pd.date_range(start_date, end_date)) 
    prices = prices_all[[symbol]].copy() # Adjusted closing price of the target stock, ensure it's a DataFrame
    prices = prices.fillna(method='ffill').fillna(method='bfill')
    
    # 2. Trades matrix (records daily change in share count)
    trades = orders_df.copy() # Use the input trades DataFrame
    
    # 3. Holdings matrix (records share count at the end of each day)
    holdings = pd.DataFrame(index=trades.index, columns=[symbol, 'Cash'], data=0.0)
    
    # 4. Initialization
    current_cash = start_val
    current_holdings = 0
    
    # 5. Iterate through trades
    for date in trades.index:
        current_trade = trades.loc[date, symbol]
        price = prices.loc[date, symbol]
        
        # Transaction cost (commission + market impact)
        trade_cost = commission + abs(current_trade) * price * impact
        
        # Cash flow: stock value +/- transaction cost
        cash_flow = -current_trade * price - trade_cost
        
        # Update holdings and cash
        current_holdings += current_trade
        current_cash += cash_flow
        
        holdings.loc[date, symbol] = current_holdings
        holdings.loc[date, 'Cash'] = current_cash
        
    # 6. Portfolio Value (needs to handle filling non-trading days)
    # Ensure indices of holdings and prices match and handle non-trading days
    
    # Combine prices and holdings indices to calculate the final portfolio value
    all_dates = pd.date_range(start_date, end_date)
    holdings = holdings.reindex(all_dates).fillna(method='ffill')
    prices = prices.reindex(all_dates).fillna(method='ffill')

    portvals = prices[symbol] * holdings[symbol] + holdings['Cash']
    
    return portvals

def compute_portfolio_stats(port_val, rfr=0.0, sf=252.0):
    """
    Computes the portfolio's cumulative return, average daily return, and standard deviation of daily return.
    This is the core function required by metrics.py.
    port_val: Pandas Series of portfolio values
    rfr: Risk-free rate (default 0.0)
    sf: Sampling frequency (default 252.0, representing trading days in a year)
    Returns: cr (cumulative return), adr (average daily return), sddr (standard deviation of daily return)
    """
    # Daily Returns (dr)
    # Use .iloc[1:] to exclude the first NaN
    dr = (port_val / port_val.shift(1) - 1).iloc[1:]

    # Cumulative Return (cr)
    cr = (port_val.iloc[-1] / port_val.iloc[0]) - 1

    # Average Daily Return (adr)
    adr = dr.mean()

    # Standard Deviation of Daily Return (sddr)
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
    Creates the benchmark strategy's trades DataFrame: buys 1000 shares on the first day and holds until the end.
    """
    # Assumes get_data is available in marketsimcode.py or the imported util.py
    dates = pd.date_range(sd, ed)
    prices_all = get_data([symbol], dates)
    prices_df = prices_all[[symbol]].fillna(method='ffill').fillna(method='bfill')
    
    # Initialize trades DataFrame
    trades = pd.DataFrame(0, index=prices_df.index, columns=[symbol])
    
    # Project Requirement: Start with $100,000 in cash and invest in 1000 shares of the stock ticker used on the first trading day.
    # Buy 1000 shares on the first day
    if not prices_df.empty:
        first_trade_date = prices_df.index[0]
        trades.loc[first_trade_date, symbol] = 1000
    
    # Note: We usually don't need to close the position on the last day, as compute_portvals handles the asset value on the last trading day.
    # If the project requires closing the position, uncomment the following code:
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