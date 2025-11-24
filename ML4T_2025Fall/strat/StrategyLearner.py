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
        
        # 超参数
        self.prediction_window = 20 # 预测未来 N 天的价格变化
        self.threshold = 0.0015 # 强买/强卖的百分比阈值 (0.5%)
        
        # 指标参数 (可优化)
        self.cci_window = 14
        self.ppo_short = 12
        self.ppo_long = 26
        self.mom_window = 10
        
        # 分类器参数
        self.leaf_size = 10 # 必须 >= 5
        self.bags = 20     # BagLearner 的包数
        self.learner = BagLearner(learner=RTLearner, kwargs={"leaf_size": self.leaf_size}, bags=self.bags, boost=False, verbose=False)
        
        # 用于特征标准化的变量
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
        在样本内数据上训练策略学习器。
        """  	   		 	 	 		  		  		    	 		 		   		 		  
        # 1. 获取价格数据
        dates = pd.date_range(sd, ed)
        prices_all = ut.get_data([symbol], dates)
        prices_df = prices_all[[symbol]].fillna(method='ffill').fillna(method='bfill')

        # 2. 生成特征 X (指标)
        indicators_df = self.get_indicators(prices_df)
        X = indicators_df.values # 特征矩阵
        
        # 3. 标准化/离散化 (标准化以提高分类器性能)
        if self.means is None:
            self.means = np.mean(X, axis=0)
            self.stdevs = np.std(X, axis=0)
            self.stdevs[self.stdevs == 0] = 1 # 避免除以零

        X_norm = (X - self.means) / self.stdevs

        # 4. 生成目标 Y (预测标签)
        # 目标: 未来 N 天的价格变化
        future_prices = prices_df.loc[indicators_df.index, symbol].shift(-self.prediction_window)
        current_prices = prices_df.loc[indicators_df.index, symbol]

        # 收益率
        returns = (future_prices - current_prices) / current_prices

        # 创建标签 Y
        Y = pd.Series(index=indicators_df.index, data=0) # 0: 持有/平仓

        # 1: 强买信号 (未来价格上涨 > 阈值)
        Y[returns > self.threshold] = 1
        # -1: 强卖信号 (未来价格下跌 > 阈值 + 市场影响)
        Y[returns < -self.threshold] = -1

        # 删除由于 shift 引入的 NaN 行
        Y = Y.dropna()
        X_final = X_norm[:len(Y), :]

        # 5. 训练学习器 (注意：分类器需要处理 -1/0/1 标签，BagLearner 默认是回归，需要转换为众数分类)
        # 假设您的 BagLearner/RTLearner 已修改为分类模式，使用众数而不是均值
        self.learner.add_evidence(X_final, Y.values)

    def get_indicators(self, prices_df):
        """获取指标数据, 并处理NaNs"""
        prices = prices_df.iloc[:, 0] # 假设只有一列价格数据

        # 商品通道指数
        cci = commodity_channel_index(prices, window=self.cci_window)
        # 2. 价格百分比振荡器
        ppo = percentage_price_oscillator(prices, short_window=self.ppo_short, long_window=self.ppo_long)
        # 3. 动量
        mom = momentum(prices, window=self.mom_window)

        indicators = pd.DataFrame(index=prices.index)
        indicators['CCI'] = cci
        indicators['PPO'] = ppo
        indicators['MOM'] = mom

        # 删除所有指标都为 NaN 的行，或只保留从第一个指标计算出值后的行
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
        使用学习到的策略生成交易信号。
        """  		  	   		 	 	 		  		  		    	 		 		   		 		  
  		  	   		 	 	 		  		  		    	 		 		   		 		  
        # 1. 获取价格数据
        dates = pd.date_range(sd, ed)
        prices_all = ut.get_data([symbol], dates)
        prices_df = prices_all[[symbol]].fillna(method='ffill').fillna(method='bfill')
        
        # 2. 生成特征 X (指标)
        indicators_df = self.get_indicators(prices_df)
        X = indicators_df.values
        
        # 3. 标准化特征 X (使用训练集上的均值和标准差)
        X_norm = (X - self.means) / self.stdevs
        
        # 4. 预测策略信号 (-1, 0, 1)
        # learner.query() 应该返回一个包含预测标签的 NumPy 数组
        predictions = self.learner.query(X_norm) 
        
        # 5. 生成交易数据框
        trades = pd.DataFrame(data=0, index=indicators_df.index, columns=[symbol])
        holdings = 0
        
        for i in range(len(predictions)):
            current_date = indicators_df.index[i]
            signal = int(predictions[i]) # 预测信号: -1, 0, 1
            trade_amount = 0

            # 最大持仓量，从测试结果的错误信息推断是 1000 股
            MAX_HOLDINGS = 1000
            
             # 当前持仓 0（空仓）：
            if holdings == 0:
                if signal == 1: # 预测 Y=1 (买)：做多 (Trade = 1000)。
                    trade_amount = MAX_HOLDINGS  # 买入 1000 股
                elif signal == -1: # 预测 Y=-1 (卖)：做空 (Trade = -1000)。
                    trade_amount = -MAX_HOLDINGS # 卖出 1000 股
                # 预测 Y=0 (持有/平仓)：保持空仓 (Trade = 0)。
            
            # 当前持仓 1000（多头）：
            elif holdings == MAX_HOLDINGS: # 多头
                if signal == -1: # 预测 Y=-1 (卖)：平仓并做空 (Trade = -2000)。
                    trade_amount = -2 * MAX_HOLDINGS # 从多头转空头
                # 如果 signal == 1 或 signal == 0，保持不变 (trade_amount = 0)   
                # elif signal == 0: # 持有/平仓，保持当前持仓 (可选，如果预测为 0 且当前持有多头)
                #     trade_amount = -1000 # 卖出 1000 股
                # # 预测 Y=1 (买)：继续持有 (Trade = 0)。
            
            # 当前持仓 -1000（空头）：
            elif holdings == -1000: # 空头
                if signal == 1: # 预测 Y=1 (买)：平仓并做多 (Trade = 2000)。
                    trade_amount = 2000 # 从空头转多头
                # 如果 signal == -1 或 signal == 0，保持不变 (trade_amount = 0)
                # elif signal == 0: # 预测 Y=0 (持有/平仓)：保持当前持仓 (Trade = 0)。
                #     trade_amount = 1000 # 买入 1000 股
                # 预测 Y=-1 (卖)：继续持有 (Trade = 0)。

            # 记录交易并更新持仓
            trades.loc[current_date, symbol] = trade_amount
            holdings += trade_amount // 1000

        return trades	  		  	   		 	 	 		  		  		    	 		 		   		 		  
  		  	   		 	 	 		  		  		    	 		 		   		 		  
  		  	   		 	 	 		  		  		    	 		 		   		 		  
if __name__ == "__main__":  		  	   		 	 	 		  		  		    	 		 		   		 		  
    print("One does not simply think up a strategy")  		  	   		 	 	 		  		  		    	 		 		   		 		  
