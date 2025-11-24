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
        # Optimized indicator parameters (for manual strategy)
        self.cci_window = 14
        self.ppo_short = 12
        self.ppo_long = 26
        self.mom_window = 10

    def add_evidence(self, symbol='IBM', sd=dt.datetime(2008, 1, 1, 0, 0), ed=dt.datetime(2009, 1, 1, 0, 0), sv=100000):
        # The manual strategy does not require training, but this function is kept for API compatibility.
        pass

    def get_indicators(self, symbol, sd, ed):
        """Get indicator data and handle NaNs"""
        dates = pd.date_range(sd, ed)
        prices_all = get_data([symbol], dates)
        prices = prices_all[[symbol]]  # Only keep the target stock
        prices = prices.fillna(method='ffill').fillna(method='bfill')

        # Commodity Channel Index
        cci = commodity_channel_index(prices[symbol], window=self.cci_window)
        # 2. Percentage Price Oscillator
        ppo = percentage_price_oscillator(prices[symbol], short_window=self.ppo_short, long_window=self.ppo_long)
        # 3. Momentum
        mom = momentum(prices[symbol], window=self.mom_window)

        indicators = pd.DataFrame(index=prices.index)
        indicators['CCI'] = cci
        indicators['PPO'] = ppo
        indicators['MOM'] = mom

        # Drop rows where all indicators are NaN, or only keep rows after the first indicator value is calculated
        return indicators.dropna()
    
    def testPolicy(self, symbol='IBM', sd=dt.datetime(2009, 1, 1, 0, 0), ed=dt.datetime(2010, 1, 1, 0, 0), sv=100000):
        indicators = self.get_indicators(symbol, sd, ed)
        trades = pd.DataFrame(data=0, index=indicators.index, columns=[symbol])

        # Trading thresholds (manually adjusted to optimize in-sample performance)
        CCI_LONG_TH = -100.0  # CCI below this value: oversold/long signal
        CCI_SHORT_TH = 100.0  # CCI above this value: overbought/short signal
        PPO_LONG_TH = 0.0     # PPO above this value: short-term trend bullish
        PPO_SHORT_TH = 0.0    # PPO below this value: short-term trend bearish
        MOM_LONG_TH = 0.00    # Momentum above this value: bullish
        MOM_SHORT_TH = 0.00   # Momentum below this value: bearish

        holdings = 0

        for i in range(len(indicators)):
            current_date = indicators.index[i]
            current_cci = indicators['CCI'].iloc[i]
            current_ppo = indicators['PPO'].iloc[i]
            current_mom = indicators['MOM'].iloc[i]

            # 1. Long/Buy signal
            long_signals = 0
            if current_cci < CCI_LONG_TH:
                long_signals += 1
            if current_ppo > PPO_LONG_TH:
                long_signals += 1
            if current_mom > MOM_LONG_TH:
                long_signals += 1

            # 2. Short/Sell signal
            short_signals = 0
            if current_cci > CCI_SHORT_TH:
                short_signals += 1
            if current_ppo < PPO_SHORT_TH:
                short_signals += 1
            if current_mom < MOM_SHORT_TH:
                short_signals += 1
            
            # --- Make trading decision ---
            trade_amount = 0
            
            if holdings == 0:
                # No position, wait for signal
                if long_signals >= 2:
                    trade_amount = 1000  # Buy 1000 shares -> Long
                elif short_signals >= 2:
                    trade_amount = -1000 # Sell 1000 shares -> Short
            
            elif holdings == 1000:
                # Long position, wait for sell signal or close position
                if short_signals >= 2:
                    trade_amount = -2000 # Reverse from long to short (Sell 2000 shares)
                elif short_signals >= 1: # Slightly looser close signal
                    # If at least one short signal, close position
                    trade_amount = -1000 # Sell 1000 shares -> Close position
                
            elif holdings == -1000:
                # Short position, wait for buy signal or close position
                if long_signals >= 2:
                    trade_amount = 2000 # Reverse from short to long (Buy 2000 shares)
                elif long_signals >= 1: # Slightly looser close signal
                    # If at least one long signal, close position
                    trade_amount = 1000 # Buy 1000 shares -> Close position

            # Record trade and update holdings
            trades.loc[current_date, symbol] = trade_amount
            holdings += trade_amount // 1000 # Update holdings (-1, 0, 1)

        return trades
    def author():                                                                                             
        return "omurphy8"
    
    def study_group():
        return "omurphy8"