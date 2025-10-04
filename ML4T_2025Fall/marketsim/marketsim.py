""""""  		  	   		 	 	 		  		  		    	 		 		   		 		  
"""MC2-P1: Market simulator.  		  	   		 	 	 		  		  		    	 		 		   		 		  
  		  	   		 	 	 		  		  		    	 		 		   		 		  
Copyright 2018, Georgia Institute of Technology (Georgia Tech)  		  	   		 	 	 		  		  		    	 		 		   		 		  
Atlanta, Georgia 30332  		  	   		 	 	 		  		  		    	 		 		   		 		  
All Rights Reserved  		  	   		 	 	 		  		  		    	 		 		   		 		  
  		  	   		 	 	 		  		  		    	 		 		   		 		  
Template code for CS 4646/7646  		  	   		 	 	 		  		  		    	 		 		   		 		  
  		  	   		 	 	 		  		  		    	 		 		   		 		  
Georgia Tech asserts copyright ownership of this template and all derivative  		  	   		 	 	 		  		  		    	 		 		   		 		  
works, including solutions to the projects assigned in this course. Students  		  	   		 	 	 		  		  		    	 		 		   		 		  
and other users of this template code are advised not to share it with others  		  	   		 	 	 		  		  		    	 		 		   		 		  
or to make it available on publicly viewable websites including repositories  		  	   		 	 	 		  		  		    	 		 		   		 		  
such as github and gitlab.  This copyright statement should not be removed  		  	   		 	 	 		  		  		    	 		 		   		 		  
or edited.  		  	   		 	 	 		  		  		    	 		 		   		 		  
  		  	   		 	 	 		  		  		    	 		 		   		 		  
We do grant permission to share solutions privately with non-students such  		  	   		 	 	 		  		  		    	 		 		   		 		  
as potential employers. However, sharing with other current or future  		  	   		 	 	 		  		  		    	 		 		   		 		  
students of CS 7646 is prohibited and subject to being investigated as a  		  	   		 	 	 		  		  		    	 		 		   		 		  
GT honor code violation.  		  	   		 	 	 		  		  		    	 		 		   		 		  
  		  	   		 	 	 		  		  		    	 		 		   		 		  
-----do not edit anything above this line---  		  	   		 	 	 		  		  		    	 		 		   		 		  
  		  	   		 	 	 		  		  		    	 		 		   		 		  
Student Name: Tucker Balch (replace with your name)  		  	   		 	 	 		  		  		    	 		 		   		 		  
GT User ID: omurphy8 (replace with your User ID)
GT ID: 904015662
"""  		  	   		 	 	 		  		  		    	 		 		   		 		  
  		  	   		 	 	 		  		  		    	 		 		   		 		  
import datetime as dt  		  	   		 	 	 		  		  		    	 		 		   		 		  
import os  		  	   		 	 	 		  		  		    	 		 		   		 		  
  		  	   		 	 	 		  		  		    	 		 		   		 		  
import numpy as np  		  	   		 	 	 		  		  		    	 		 		   		 		  
  		  	   		 	 	 		  		  		    	 		 		   		 		  
import pandas as pd  		  	   		 	 	 		  		  		    	 		 		   		 		  
from util import get_data, plot_data

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

def get_stats(port_val, daily_risk_free_rate=0.0):
    """
    This function computes and returnsthe portfolio statistics like cumulative return, average daily return,
    stdev of daily return and Sharpe ratio of the given prices in the portfolio

    :param allocs: list of allocations for each stock
    :param prices: Pandas Dataframe holding data of stock prices
    """

    # daily returns minus the first return
    daily_rets = (port_val / port_val.shift(1)) - 1
    daily_rets = daily_rets[1:]

    cum_ret = (port_val[-1] / port_val[0]) - 1
    avg_daily_ret = daily_rets.mean()
    std_daily_ret = daily_rets.std()

    # computing annualized Sharpe ratio, assuming 252 trading days
    # with a risk-free rate of 0%
    sr = np.sqrt(252) * ((avg_daily_ret - daily_risk_free_rate) / std_daily_ret)

    return cum_ret, avg_daily_ret, std_daily_ret, sr
  		  	   		 	 	 		  		  		    	 		 		   		 		  
  		  	   		 	 	 		  		  		    	 		 		   		 		  
def compute_portvals(  		  	   		 	 	 		  		  		    	 		 		   		 		  
    orders_file="./orders/orders.csv",  		  	   		 	 	 		  		  		    	 		 		   		 		  
    start_val=1000000,  		  	   		 	 	 		  		  		    	 		 		   		 		  
    commission=9.95,  		  	   		 	 	 		  		  		    	 		 		   		 		  
    impact=0.005,  		  	   		 	 	 		  		  		    	 		 		   		 		  
):  		  	   		 	 	 		  		  		    	 		 		   		 		  
    """  		  	   		 	 	 		  		  		    	 		 		   		 		  
    Computes the portfolio values.  		  	   		 	 	 		  		  		    	 		 		   		 		  
  		  	   		 	 	 		  		  		    	 		 		   		 		  
    :param orders_file: Path of the order file or the file object  		  	   		 	 	 		  		  		    	 		 		   		 		  
    :type orders_file: str or file object  		  	   		 	 	 		  		  		    	 		 		   		 		  
    :param start_val: The starting value of the portfolio  		  	   		 	 	 		  		  		    	 		 		   		 		  
    :type start_val: int  		  	   		 	 	 		  		  		    	 		 		   		 		  
    :param commission: The fixed amount in dollars charged for each transaction (both entry and exit)  		  	   		 	 	 		  		  		    	 		 		   		 		  
    :type commission: float  		  	   		 	 	 		  		  		    	 		 		   		 		  
    :param impact: The amount the price moves against the trader compared to the historical data at each transaction  		  	   		 	 	 		  		  		    	 		 		   		 		  
    :type impact: float  		  	   		 	 	 		  		  		    	 		 		   		 		  
    :return: the result (portvals) as a single-column dataframe, containing the value of the portfolio for each trading day in the first column from start_date to end_date, inclusive.  		  	   		 	 	 		  		  		    	 		 		   		 		  
    :rtype: pandas.DataFrame  		  	   		 	 	 		  		  		    	 		 		   		 		  
    """  		  	   		 	 	 		  		  		    	 		 		   		 		  
    # this is the function the autograder will call to test your code  		  	   		 	 	 		  		  		    	 		 		   		 		  
    # NOTE: orders_file may be a string, or it may be a file object. Your  		  	   		 	 	 		  		  		    	 		 		   		 		  
    # code should work correctly with either input  		  	   		 	 	 		  		  		    	 		 		   		 		  
    # TODO: Your code here  		  	   		 	 	 		  		  		    	 		 		   		 		  
  		  	   		 	 	 		  		  		    	 		 		   		 		  
    # In the template, instead of computing the value of the portfolio, we just  		  	   		 	 	 		  		  		    	 		 		   		 		  
    # read in the value of IBM over 6 months  	

    # read & process orders
    orders_df = pd.read_csv(orders_file, index_col="Date", parse_dates=True, na_values=["nan"])
    orders_df.sort_index(inplace=True)

    # get date range & symb
    start_date = orders_df.index.min()
    end_date = orders_df.index.max()
    all_dates = pd.date_range(start_date, end_date)
    symbols = orders_df["Symbol"].unique().tolist()
    
    if 'SPY' not in symbols:
        symbols.append('SPY')

    # get prices for all symb & date range
    prices = get_data(symbols, pd.date_range(start_date, end_date))
    prices = prices.drop("SPY", axis=1) # removing spy
    prices["cash"] = 1.0  # add a cash column for cash

    dates = prices.index

    trades = pd.DataFrame(0, index=dates, columns=prices.columns)
    for date, row in orders_df.iterrows():
        symbol = row['Symbol']
        order = row['Order']
        shares = row['Shares']

        price_at_trade = prices.loc[date, symbol]
        trade_cost = shares * price_at_trade
        if order == "BUY":
            trades.loc[date, symbol] += shares
            trades.loc[date, 'cash'] -= trade_cost + (impact * trade_cost) + commission
        elif order == "SELL":
            trades.loc[date, symbol] -= shares
            trades.loc[date, 'cash'] += trade_cost - (impact * trade_cost) - commission
    # init holdings for symb
    holdings = trades.copy()
    holdings.loc[holdings.index[0], 'cash'] += start_val
    holdings = holdings.cumsum()

    # cacl daily port val
    portvals = (holdings * prices).sum(axis=1)
    return portvals

def test_code():  		  	   		 	 	 		  		  		    	 		 		   		 		  
    """  		  	   		 	 	 		  		  		    	 		 		   		 		  
    Helper function to test code  		  	   		 	 	 		  		  		    	 		 		   		 		  
    """  		  	   		 	 	 		  		  		    	 		 		   		 		  
    # this is a helper function you can use to test your code  		  	   		 	 	 		  		  		    	 		 		   		 		  
    # note that during autograding his function will not be called.  		  	   		 	 	 		  		  		    	 		 		   		 		  
    # Define input parameters  		  	   		 	 	 		  		  		    	 		 		   		 		  
  		  	   		 	 	 		  		  		    	 		 		   		 		  
    of = "./orders/orders-10.csv"  		  	   		 	 	 		  		  		    	 		 		   		 		  
    # of = "./orders/orders-02.csv"  		  	   		 	 	 		  		  		    	 		 		   		 		  
    sv = 1000000  		  	   		 	 	 		  		  		    	 		 		   		 		  
  		  	   		 	 	 		  		  		    	 		 		   		 		  
    # Process orders  		  	   		 	 	 		  		  		    	 		 		   		 		  
    portvals = compute_portvals(orders_file=of, start_val=sv)
    if isinstance(portvals, pd.DataFrame):  		  	   		 	 	 		  		  		    	 		 		   		 		  
        portvals = portvals[portvals.columns[0]]  # just get the first column  		  	   		 	 	 		  		  		    	 		 		   		 		  
    else:  		  	   		 	 	 		  		  		    	 		 		   		 		  
        "warning, code did not return a DataFrame"  		  	   		 	 	 		  		  		    	 		 		   		 		  
  		  	   		 	 	 		  		  		    	 		 		   		 		  
    # Get portfolio stats  		  	   		 	 	 		  		  		    	 		 		   		 		  
    # Here we just fake the data. you should use your code from previous assignments.  		  	   		 	 	 		  	

    cum_ret, avg_daily_ret, std_daily_ret, sharpe_ratio = get_stats(portvals)
    start_date = portvals.index.min()
    end_date = portvals.index.max()	    	 		 		   		

    spy_prices = get_data(['SPY'], pd.date_range(start_date, end_date))
    spy_prices = spy_prices['SPY'] 		  
    cum_ret_SPY, avg_daily_ret_SPY, std_daily_ret_SPY, sharpe_ratio_SPY = get_stats(spy_prices)		  	   		 	 	 		  		  		    	 		 		   		 		  
  		  	   		 	 	 		  		  		    	 		 		   		 		  
    # Compare portfolio against $SPX  		  	   		 	 	 		  		  		    	 		 		   		 		  
    print(f"Date Range: {start_date} to {end_date}")  		  	   		 	 	 		  		  		    	 		 		   		 		  
    print()  		  	   		 	 	 		  		  		    	 		 		   		 		  
    print(f"Sharpe Ratio of Fund: {sharpe_ratio}")  		  	   		 	 	 		  		  		    	 		 		   		 		  
    print(f"Sharpe Ratio of SPY : {sharpe_ratio_SPY}")  		  	   		 	 	 		  		  		    	 		 		   		 		  
    print()  		  	   		 	 	 		  		  		    	 		 		   		 		  
    print(f"Cumulative Return of Fund: {cum_ret}")  		  	   		 	 	 		  		  		    	 		 		   		 		  
    print(f"Cumulative Return of SPY : {cum_ret_SPY}")  		  	   		 	 	 		  		  		    	 		 		   		 		  
    print()  		  	   		 	 	 		  		  		    	 		 		   		 		  
    print(f"Standard Deviation of Fund: {std_daily_ret}")  		  	   		 	 	 		  		  		    	 		 		   		 		  
    print(f"Standard Deviation of SPY : {std_daily_ret_SPY}")  		  	   		 	 	 		  		  		    	 		 		   		 		  
    print()  		  	   		 	 	 		  		  		    	 		 		   		 		  
    print(f"Average Daily Return of Fund: {avg_daily_ret}")  		  	   		 	 	 		  		  		    	 		 		   		 		  
    print(f"Average Daily Return of SPY : {avg_daily_ret_SPY}")  		  	   		 	 	 		  		  		    	 		 		   		 		  
    print()  		  	   		 	 	 		  		  		    	 		 		   		 		  
    print(f"Final Portfolio Value: {portvals[-1]}")  		  	   		 	 	 		  		  		    	 		 		   		 		  
  		  	   		 	 	 		  		  		    	 		 		   		 		  
  		  	   		 	 	 		  		  		    	 		 		   		 		  
if __name__ == "__main__":  		  	   		 	 	 		  		  		    	 		 		   		 		  
    test_code()	  	   		 	 	 		  		  		    	 		 		   		 		  

# MarketsimTestCase(  		  	   		 	 	 		  		  		    	 		 		   		 		  
#         description="Orders 10, impact and commission",  		  	   		 	 	 		  		  		    	 		 		   		 		  
#         group="both",  		  	   		 	 	 		  		  		    	 		 		   		 		  
#         inputs=dict(  		  	   		 	 	 		  		  		    	 		 		   		 		  
#             orders_file="orders-10.csv",  		  	   		 	 	 		  		  		    	 		 		   		 		  
#             start_val=1000000,  		  	   		 	 	 		  		  		    	 		 		   		 		  
#             commission=9.95,  		  	   		 	 	 		  		  		    	 		 		   		 		  
#             impact=0.005,  		  	   		 	 	 		  		  		    	 		 		   		 		  
#         ),  		  	   		 	 	 		  		  		    	 		 		   		 		  
#         outputs=dict(  		  	   		 	 	 		  		  		    	 		 		   		 		  
#             num_days=141,  		  	   		 	 	 		  		  		    	 		 		   		 		  
#             last_day_portval=1026658.3265,  		  	   		 	 	 		  		  		    	 		 		   		 		  
#             sharpe_ratio=0.627643575702,  		  	   		 	 	 		  		  		    	 		 		   		 		  
#             avg_daily_ret=0.000222013722594,  		  	   		 	 	 		  		  		    	 		 		   		 		  
#         ),  		  	   		 	 	 		  		  		    	 		 		   		 		  
#     ), 