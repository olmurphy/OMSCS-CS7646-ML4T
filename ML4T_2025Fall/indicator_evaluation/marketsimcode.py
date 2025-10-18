from util import get_data
import datetime as dt
import pandas as pd

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

def compute_portfolio_values(df_trades, start_val=100000, commission=0.00, impact=0.00):
    """  		  	   		 	 	 		  		  		    	 		 		   		 		  
    Computes the portfolio values.  		  	   		 	 	 		  		  		    	 		 		   		 		  
  		  	   		 	 	 		  		  		    	 		 		   		 		  
    :param start_val: The starting value of the portfolio  		  	   		 	 	 		  		  		    	 		 		   		 		  
    :type start_val: int  		  	   		 	 	 		  		  		    	 		 		   		 		  
    :param commission: The fixed amount in dollars charged for each transaction (both entry and exit)  		  	   		 	 	 		  		  		    	 		 		   		 		  
    :type commission: float  		  	   		 	 	 		  		  		    	 		 		   		 		  
    :param impact: The amount the price moves against the trader compared to the historical data at each transaction  		  	   		 	 	 		  		  		    	 		 		   		 		  
    :type impact: float  		  	   		 	 	 		  		  		    	 		 		   		 		  
    :return: the result (portvals) as a single-column dataframe, containing the value of the portfolio for each trading day in the first column from start_date to end_date, inclusive.  		  	   		 	 	 		  		  		    	 		 		   		 		  
    :rtype: pandas.DataFrame  		  	   		 	 	 		  		  		    	 		 		   		 		  
    """
    # 确定日期范围和股票代码
    dates = df_trades.index
    symbols = df_trades.columns.tolist()

    prices = get_data(symbols, dates)
    prices['Cash'] = 1.0

    # 初始化持股 (Holdings) 和价值 (Values) 数据框
    df_holdings = pd.DataFrame(0.0, index=prices.index, columns=symbols + ['Cash'])
    df_values = pd.DataFrame(0.0, index=prices.index, columns=['Value'])
    
    # 投资组合初始现金
    df_holdings.iloc[0, df_holdings.columns.get_loc('Cash')] = start_val
    
    # 每日交易
    df_orders = df_trades.copy()
    
    # 初始化每日持股量
    df_holdings.iloc[0] = df_holdings.iloc[0].copy()

    # 遍历每个交易日
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
    print(df_values)
    return df_values

if __name__ == "__main__":
    # 这是一个示例，展示如何使用 marketsimcode.py
    print("Marketsim Code 示例运行中...")
    
    # 1. 定义日期和股票代码
    start_date = dt.datetime(2008, 1, 1)
    end_date = dt.datetime(2009, 12, 31)
    test_symbol = 'JPM'
    
    # 2. 创建一个示例交易数据框 (买入 1000 股，持有，然后卖出 1000 股)
    dates = pd.date_range(start_date, end_date)
    prices_full = get_data([test_symbol], dates)
    prices_full = prices_full[[test_symbol]]

    df_trades_example = pd.DataFrame(0.0, index=prices_full.index, columns=[test_symbol])
    
    # 示例交易：第一天买入 1000 股
    first_trade_date = df_trades_example.index[0]
    df_trades_example.loc[first_trade_date, test_symbol] = 1000 

    # 示例交易：最后一天平仓
    last_trade_date = df_trades_example.index[-1]
    df_trades_example.loc[last_trade_date, test_symbol] = -1000
    
    # 3. 计算投资组合价值 (使用项目 6 的成本：佣金 0.00，影响 0.00)
    portvals = compute_portfolio_values(
        df_trades_example, 
        start_val=100000, 
        commission=0.00, 
        impact=0.00
    )
    
    print("\n示例投资组合价值 (前 5 天):")
    print(portvals.head())