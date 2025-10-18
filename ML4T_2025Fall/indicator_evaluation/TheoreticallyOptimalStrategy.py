import datetime as dt  	
import pandas as pd
import numpy as np
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

def testPolicy(symbol="JPM", sd=dt.datetime(2008, 1, 1), ed=dt.datetime(2009,12,31), sv = 100000):
    """
    Code implementing a TheoreticallyOptimalStrategy. It should implement testPolicy(), which returns a trades Pandas.DataFrame

    Parameters
        symbol    - the stock symbol to act on
        sd        - A DateTime object that represents the start date
        ed        - A DateTime object that represents the end date
        sv        - Start value of the portfolio

    Returns
        A single column data frame, indexed by date, whose values represent trades for each trading day 
       (from the start date to the end date of a given period). Legal values are +1000.0 indicating a BUY 
       of 1000 shares, -1000.0 indicating a SELL of 1000 shares, and 0.0 indicating NOTHING. Values of +2000 
       and -2000 for trades are also legal so long as net holdings are constrained to -1000, 0, and 1000. 
       Note: The format of this data frame differs from the one developed in a prior project.   

    Return Type
        pandas.DataFrame
    """
    # get stock price
    dates = pd.date_range(sd, ed)
    prices_all = get_data([symbol], dates)
    prices = prices_all[[symbol]].dropna() # NaN
    
    # init data fram
    df_trades = pd.DataFrame(0.0, index=prices.index, columns=[symbol])
    current_holdings = 0
    
    # traverse trade days
    for i in range(len(prices.index) - 1):
        t = prices.index[i]  
        t_plus_1 = prices.index[i+1] 
        
        price_t = prices.loc[t, symbol]
        price_t_plus_1 = prices.loc[t_plus_1, symbol]
        
        # TOS decision
        desired_position = 0
        if price_t_plus_1 > price_t:
            desired_position = 1000
        elif price_t_plus_1 < price_t:
            desired_position = -1000
        else:
            desired_position = current_holdings
        
        trade_shares = desired_position - current_holdings
        
        if trade_shares != 0:
            df_trades.loc[t, symbol] = trade_shares
            current_holdings += trade_shares
    
    # last day
    t_final = prices.index[-1]
    final_trade = -current_holdings
    
    if final_trade != 0:
        df_trades.loc[t_final, symbol] = final_trade
        current_holdings += final_trade
    
    return df_trades

if __name__ == "__main__":
    sd = dt.datetime(2008, 1, 1)
    ed = dt.datetime(2009, 12, 31)
    df_trades = testPolicy(symbol="JPM", sd=sd, ed=ed, sv=100000)