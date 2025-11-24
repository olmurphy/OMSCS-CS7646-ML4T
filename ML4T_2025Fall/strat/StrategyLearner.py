"""                                                                                                
Template for implementing StrategyLearner (c) 2016 Tucker Balch                                                                                              
                                                                                              
Copyright 2018, Georgia Institute of Technology (Georgia Tech)                                                                                                
Atlanta, Georgia 30332                                                                                                
All Rights Reserved                                                                                               
                                                                                              
Template code for CS 4646/7646                                                                                                
                                                                                              
Georgia Tech asserts copyright ownership of this template and all derivative                                                                                              
works, including solutions to the projects assigned in this course. Students                                                                                              
and other users of this template code are advised not to share it with others                                                                                             
or to make it available on publicly viewable websites including repositories                                                                                              
such as github and gitlab. This copyright statement should not be removed                                                                                                
or edited.                                                                                                
                                                                                              
We do grant permission to share solutions privately with non-students such                                                                                                
as potential employers. However, sharing with other current or future                                                                                             
students of CS 7646 is prohibited and subject to being investigated as a                                                                                              
GT honor code violation.                                                                                              
                                                                                              
-----do not edit anything above this line---                                                                                              
                                                                                              
Student Name: Tucker Balch (replace with your name)                                                                                               
GT User ID: tb34 (replace with your User ID)                                                                                              
GT ID: 900897987 (replace with your GT ID)                                                                                                
"""                                                                                               
                                                                                              
import datetime as dt                                                                                             
import random                                                                                             
                                                                                              
import pandas as pd                                                                                               
import util as ut
import numpy as np                                                                                                

from BagLearner import BagLearner
from RTLearner import RTLearner
from indicators import commodity_channel_index, percentage_price_oscillator, momentum

class StrategyLearner(object):                                                                                                
    def __init__(self, verbose=False, impact=0.0, commission=0.0):                                                                                                
        """                                                                                               
        Constructor method                                                                                                
        """                                                                                               
        self.verbose = verbose                                                                                                
        self.impact = impact                                                                                              
        self.commission = commission

        self.verbose = verbose
        self.impact = impact
        self.commission = commission
        
        # Hyperparameters
        self.prediction_window = 20 # Predict price change in the next N days
        self.threshold = 0.0015 # Percentage threshold for strong buy/strong sell (0.5%)
        
        # Indicator parameters (can be optimized)
        self.cci_window = 14
        self.ppo_short = 12
        self.ppo_long = 26
        self.mom_window = 10
        
        # Classifier parameters
        self.leaf_size = 10 # Must be >= 5
        self.bags = 20     # Number of bags for BagLearner
        self.learner = BagLearner(learner=RTLearner, kwargs={"leaf_size": self.leaf_size}, bags=self.bags, boost=False, verbose=False)
        
        # Variables for feature standardization
        self.means = None
        self.stdevs = None

    # this method should create a QLearner, and train it for trading                                                                                              
    def add_evidence(                                                                                             
        self,                                                                                             
        symbol="IBM",                                                                                             
        sd=dt.datetime(2008, 1, 1),                                                                                               
        ed=dt.datetime(2009, 1, 1),                                                                                               
        sv=10000,                                                                                             
    ):                                                                                                
        """
        Trains the strategy learner on in-sample data.
        """                                                                                       
        # 1. Get price data
        dates = pd.date_range(sd, ed)
        prices_all = ut.get_data([symbol], dates)
        prices_df = prices_all[[symbol]].fillna(method='ffill').fillna(method='bfill')

        # 2. Generate features X (Indicators)
        indicators_df = self.get_indicators(prices_df)
        X = indicators_df.values # Feature matrix
        
        # 3. Standardization/Discretization (Standardize to improve classifier performance)
        if self.means is None:
            self.means = np.mean(X, axis=0)
            self.stdevs = np.std(X, axis=0)
            self.stdevs[self.stdevs == 0] = 1 # Avoid division by zero

        X_norm = (X - self.means) / self.stdevs

        # 4. Generate target Y (Prediction labels)
        # Target: Price change in the next N days
        future_prices = prices_df.loc[indicators_df.index, symbol].shift(-self.prediction_window)
        current_prices = prices_df.loc[indicators_df.index, symbol]

        # Returns
        returns = (future_prices - current_prices) / current_prices

        # Create labels Y
        Y = pd.Series(index=indicators_df.index, data=0) # 0: Hold/Close Position

        # Calculate the total cost of a round-trip trade (buy + sell)
        round_trip_cost = 2 * self.impact # Commission is 0.00 for Experiment 2

        # 1: Strong Buy signal (Future price increase > Threshold + Round Trip Cost)
        Y[returns > (self.threshold + round_trip_cost)] = 1
        # -1: Strong Sell signal (Future price decrease > Threshold + Round Trip Cost)
        # Note: returns is already negative for a loss, so we compare its magnitude
        Y[returns < -(self.threshold + round_trip_cost)] = -1

        # Remove NaN rows introduced by shift
        Y = Y.dropna()
        X_final = X_norm[:len(Y), :]

        # 5. Train the learner (Note: The classifier needs to handle -1/0/1 labels. BagLearner is regression by default and needs to be converted to mode classification)
        # Assumes your BagLearner/RTLearner has been modified for classification mode, using mode instead of mean
        self.learner.add_evidence(X_final, Y.values)

    def get_indicators(self, prices_df):
        """Get indicator data and handle NaNs"""
        prices = prices_df.iloc[:, 0] # Assumes only one column of price data

        # 1. Commodity Channel Index
        cci = commodity_channel_index(prices, window=self.cci_window)
        # 2. Percentage Price Oscillator
        ppo = percentage_price_oscillator(prices, short_window=self.ppo_short, long_window=self.ppo_long)
        # 3. Momentum
        mom = momentum(prices, window=self.mom_window)

        indicators = pd.DataFrame(index=prices.index)
        indicators['CCI'] = cci
        indicators['PPO'] = ppo
        indicators['MOM'] = mom

        # Drop rows where all indicators are NaN, or only keep rows after the first indicator value is calculated
        return indicators.dropna()                                                                                                                
                                                                                              
    # this method should use the existing policy and test it against new data                                                                                             
    def testPolicy(                                                                                               
        self,                                                                                             
        symbol="IBM",                                                                                             
        sd=dt.datetime(2009, 1, 1),                                                                                               
        ed=dt.datetime(2010, 1, 1),                                                                                               
        sv=10000,                                                                                             
    ):                                                                                        
        """
        Generates trading signals using the learned strategy.
        """                                                                                               
                                                                                              
        # 1. Get price data
        dates = pd.date_range(sd, ed)
        prices_all = ut.get_data([symbol], dates)
        prices_df = prices_all[[symbol]].fillna(method='ffill').fillna(method='bfill')
        
        # 2. Generate features X (Indicators)
        indicators_df = self.get_indicators(prices_df)
        X = indicators_df.values
        
        # 3. Standardize features X (using mean and standard deviation from the training set)
        X_norm = (X - self.means) / self.stdevs
        
        # 4. Predict strategy signal (-1, 0, 1)
        # learner.query() should return a NumPy array containing the predicted labels
        predictions = self.learner.query(X_norm) 
        
        # 5. Generate trades DataFrame
        trades = pd.DataFrame(data=0, index=indicators_df.index, columns=[symbol])
        holdings = 0
        
        for i in range(len(predictions)):
            current_date = indicators_df.index[i]
            signal = int(predictions[i]) # Predicted signal: -1, 0, 1
            trade_amount = 0

            # Maximum holding quantity, inferred to be 1000 shares from testing error messages
            MAX_HOLDINGS = 1000
            
             # Current holding 0 (No position):
            if holdings == 0:
                if signal == 1: # Predict Y=1 (Buy): Go long (Trade = 1000).
                    trade_amount = MAX_HOLDINGS  # Buy 1000 shares
                elif signal == -1: # Predict Y=-1 (Sell): Go short (Trade = -1000).
                    trade_amount = -MAX_HOLDINGS # Sell 1000 shares
                # Predict Y=0 (Hold/Close Position): Remain flat (Trade = 0).
            
            # Current holding 1000 (Long):
            elif holdings == MAX_HOLDINGS: # Long position
                if signal == -1: # Predict Y=-1 (Sell): Close position and go short (Trade = -2000).
                    trade_amount = -2 * MAX_HOLDINGS # Reverse from long to short
                # If signal == 1 or signal == 0, remain unchanged (trade_amount = 0)   
                # elif signal == 0: # Hold/Close position, maintain current holding (Optional, if prediction is 0 and currently long)
                #     trade_amount = -1000 # Sell 1000 shares
                # # Predict Y=1 (Buy): Continue holding (Trade = 0).
            
            # Current holding -1000 (Short):
            elif holdings == -1000: # Short position
                if signal == 1: # Predict Y=1 (Buy): Close position and go long (Trade = 2000).
                    trade_amount = 2000 # Reverse from short to long
                # If signal == -1 or signal == 0, remain unchanged (trade_amount = 0)
                # elif signal == 0: # Predict Y=0 (Hold/Close Position): Maintain current holding (Trade = 0).
                #     trade_amount = 1000 # Buy 1000 shares
                # Predict Y=-1 (Sell): Continue holding (Trade = 0).

            # Record trade and update holdings
            trades.loc[current_date, symbol] = trade_amount
            holdings += trade_amount // 1000

        return trades                                                                                                 
                                                                                              
                                                                                              
if __name__ == "__main__":                                                                                                
    print("One does not simply think up a strategy")