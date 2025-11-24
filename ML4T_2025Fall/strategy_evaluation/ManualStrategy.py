""""""  		  	   		 	 	 		  		  		    	 		 		   		 		  
"""  		  	   		 	 	 		  		  		    	 		 		   		 		  
Template for implementing StrategyLearner  (c) 2016 Tucker Balch  		  	   		 	 	 		  		  		    	 		 		   		 		  
  		  	   		 	 	 		  		  		    	 		 		   		 		  
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
  		  	   		 	 	 		  		  		    	 		 		   		 		  
Student Name: Owen Li Murphy 		  	   		 	 	 		  		  		    	 		 		   		 		  
GT User ID: omurphy8
GT ID: 904015662 		 	 	 		  		  		    	 		 		   		 		  
"""

from util import get_data
import datetime as dt
import pandas as pd

from indicators import commodity_channel_index, percentage_price_oscillator, momentum

class ManualStrategy(object):
    # 
    """
    A manual learner that can learn (essenitally human coded rules) a trading policy using the same indicators used in StrategyLearner=."""

    def __init__(self, verbose=False, impact=0.005, commission=9.95):
        self.verbose = verbose
        self.impact = impact
        self.commission = commission
        # 优化后的指标参数（用于手动策略）
        self.cci_window = 14
        self.ppo_short = 12
        self.ppo_long = 26
        self.mom_window = 10

    def add_evidence(self, symbol='IBM', sd=dt.datetime(2008, 1, 1, 0, 0), ed=dt.datetime(2009, 1, 1, 0, 0), sv=100000):
        # 手动策略无需训练，但为了API兼容性保留此函数。
        pass

    def get_indicators(self, symbol, sd, ed):
        """获取指标数据, 并处理NaNs"""
        dates = pd.date_range(sd, ed)
        prices_all = get_data([symbol], dates)
        prices = prices_all[[symbol]]  # 只保留目标股票
        prices = prices.fillna(method='ffill').fillna(method='bfill')

        # 商品通道指数
        cci = commodity_channel_index(prices[symbol], window=self.cci_window)
        # 2. 价格百分比振荡器
        ppo = percentage_price_oscillator(prices[symbol], short_window=self.ppo_short, long_window=self.ppo_long)
        # 3. 动量
        mom = momentum(prices[symbol], window=self.mom_window)

        indicators = pd.DataFrame(index=prices.index)
        indicators['CCI'] = cci
        indicators['PPO'] = ppo
        indicators['MOM'] = mom

        # 删除所有指标都为 NaN 的行，或只保留从第一个指标计算出值后的行
        return indicators.dropna()
    
    def testPolicy(self, symbol='IBM', sd=dt.datetime(2009, 1, 1, 0, 0), ed=dt.datetime(2010, 1, 1, 0, 0), sv=100000):
        """
        Tests your learner using data outside of the training data

        Parameters
            symbol (str) - The stock symbol that you trained on on
            sd (datetime) - A datetime object that represents the start date, defaults to 1/1/2008
            ed (datetime) - A datetime object that represents the end date, defaults to 1/1/2009
            sv (int) - The starting value of the portfolio
        Returns
            A single column data frame, indexed by date, representing trades for each day. Legal values are +1000.0 indicating
            a BUY of 1000 shares, -1000.0 indicating a SELL of 1000 shares, and 0.0 indicating NOTHING.
            Values of +2000 and -2000 for trades are also legal when switching from long to short or short to
            long so long as net holdings are constrained to -1000, 0, and 1000.

        Return type
            pandas.DataFrame
        """
        indicators = self.get_indicators(symbol, sd, ed)
        trades = pd.DataFrame(data=0, index=indicators.index, columns=[symbol])

        # 交易阈值 (手动调整以优化样本内性能)
        CCI_LONG_TH = -100.0  # CCI 低于此值：超卖/长期信号
        CCI_SHORT_TH = 100.0  # CCI 高于此值：超买/短期信号
        PPO_LONG_TH = 0.0     # PPO 高于此值：短期趋势看涨
        PPO_SHORT_TH = 0.0    # PPO 低于此值：短期趋势看跌
        MOM_LONG_TH = 0.00    # 动量高于此值：看涨
        MOM_SHORT_TH = 0.00   # 动量低于此值：看跌

        holdings = 0

        for i in range(len(indicators)):
            current_date = indicators.index[i]
            current_cci = indicators['CCI'].iloc[i]
            current_ppo = indicators['PPO'].iloc[i]
            current_mom = indicators['MOM'].iloc[i]

            # 1. 长期/买入信号
            long_signals = 0
            if current_cci < CCI_LONG_TH:
                long_signals += 1
            if current_ppo > PPO_LONG_TH:
                long_signals += 1
            if current_mom > MOM_LONG_TH:
                long_signals += 1

            # 2. 短期/卖出信号
            short_signals = 0
            if current_cci > CCI_SHORT_TH:
                short_signals += 1
            if current_ppo < PPO_SHORT_TH:
                short_signals += 1
            if current_mom < MOM_SHORT_TH:
                short_signals += 1
            
            # --- 制定交易决策 ---
            trade_amount = 0
            
            if holdings == 0:
                # 空仓，等待信号
                if long_signals >= 2:
                    trade_amount = 1000  # 买入 1000 股 -> 长期
                elif short_signals >= 2:
                    trade_amount = -1000 # 卖出 1000 股 -> 短期
            
            elif holdings == 1000:
                # 多头，等待卖出信号或平仓
                if short_signals >= 2:
                    trade_amount = -2000 # 从多头转空头 (卖出 2000 股)
                elif short_signals >= 1: # 稍微宽松的平仓信号
                    # 如果至少有一个短期信号，平仓
                    trade_amount = -1000 # 卖出 1000 股 -> 平仓
                
            elif holdings == -1000:
                # 空头，等待买入信号或平仓
                if long_signals >= 2:
                    trade_amount = 2000 # 从空头转多头 (买入 2000 股)
                elif long_signals >= 1: # 稍微宽松的平仓信号
                    # 如果至少有一个长期信号，平仓
                    trade_amount = 1000 # 买入 1000 股 -> 平仓

            # 记录交易并更新持仓
            trades.loc[current_date, symbol] = trade_amount
            holdings += trade_amount // 1000 # 更新持仓 (-1, 0, 1)

        return trades
    def author():  		  	   		 	 	 		  		  		    	 		 		   		 		  
        return "omurphy8"
    
    def study_group():
        return "omurphy8"
