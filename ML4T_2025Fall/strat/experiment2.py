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

import pandas as pd
import numpy as np
import datetime as dt
import matplotlib.pyplot as plt

# 导入策略和市场模拟代码
import StrategyLearner as sl
import marketsimcode as mc 
# import metrics as met

def run_experiment2(symbol="JPM", sv=100000, 
                    sd_in=dt.datetime(2008, 1, 1), ed_in=dt.datetime(2009, 12, 31)):
    """
    执行实验 2：分析改变影响值 (Impact) 对 StrategyLearner 交易行为的影响。
    """
    
    # 实验影响值 (至少 3 个测量值)
    impact_values = [0.0, 0.001, 0.01, 0.05]
    commission = 0.00 # 项目要求佣金为 0.00 美元
    
    results = {}
    
    print("--- 实验 2：不同影响值对 StrategyLearner 的影响 ---")
    
    for impact in impact_values:
        print(f"\n测试影响值: {impact}")
        
        # 1. 初始化和训练策略学习器
        learner = sl.StrategyLearner(verbose=False, impact=impact, commission=commission)
        learner.add_evidence(symbol=symbol, sd=sd_in, ed=ed_in, sv=sv)
        
        # 2. 生成样本内交易
        trades_learner_in = learner.testPolicy(symbol=symbol, sd=sd_in, ed=ed_in, sv=sv)
        
        # 3. 计算投资组合价值
        # 注意：这里的 compute_portvals 应该使用当前的 impact 和 commission
        portvals_learner_in = mc.compute_portvals(trades_learner_in, start_val=sv, commission=commission, impact=impact, symbol=symbol)
        
        # 4. 记录结果
        cr, adr, sddr = mc.compute_portfolio_stats(portvals_learner_in)
        num_trades = (trades_learner_in.iloc[:, 0] != 0).sum()
        
        results[impact] = {
            'portvals': portvals_learner_in,
            'CR': cr,
            'NumTrades': num_trades,
            'Trades_df': trades_learner_in # 用于验证交易行为是否不同
        }
        
        print(f"  累计收益 (CR): {cr:.6f}, 交易次数: {num_trades}")

    # --- 5. 生成图表 (投资组合价值) ---
    plt.figure(figsize=(12, 6))
    
    for impact, data in results.items():
        portvals = data['portvals']
        norm_portvals = portvals / portvals.iloc[0]
        plt.plot(norm_portvals, label=f'Impact={impact} (CR: {data["CR"]:.4f})', linewidth=1.5)
        
    plt.title("StrategyLearner 样本内性能随 Impact 值变化 (JPM)")
    plt.xlabel("Date")
    plt.ylabel("Normalized Portfolio Value")
    plt.legend()
    plt.grid(True)
    plt.savefig("experiment2_impact_performance.png")
    plt.close()

    # --- 6. 生成图表 (交易次数) ---
    impacts = list(results.keys())
    num_trades = [results[i]['NumTrades'] for i in impacts]
    
    plt.figure(figsize=(8, 5))
    plt.bar([str(i) for i in impacts], num_trades, color='skyblue')
    plt.title("StrategyLearner 交易次数随 Impact 值变化 (JPM)")
    plt.xlabel("Impact Value")
    plt.ylabel("Number of Trades")
    plt.grid(axis='y')
    plt.savefig("experiment2_impact_trades.png")
    plt.close()
    
    # 7. 验证交易策略差异 (文字描述)
    # 您需要检查 trades_df 在不同影响值下的差异，以支持报告中的声明。
    print("\n请在报告中对比不同 Impact 值下的 'Trades_df'，以证明策略发生了改变。")
    print("例如，比较 Impact=0.0 和 Impact=0.05 的交易数据框。")
    
if __name__ == "__main__":
    run_experiment2()