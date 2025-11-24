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
# 假设您的文件位于 strategy_evaluation 目录下
import StrategyLearner as sl
import ManualStrategy as ms
import marketsimcode as mc 
# import metrics as met # 假设 metrics 包含在 marketsimcode.py 中

def run_experiment1(symbol="JPM", sv=100000, 
                    sd_in=dt.datetime(2008, 1, 1), ed_in=dt.datetime(2009, 12, 31),
                    sd_out=dt.datetime(2010, 1, 1), ed_out=dt.datetime(2011, 12, 31)):
    """
    执行实验 1：比较 ManualStrategy 和 StrategyLearner 在样本内和样本外的表现。
    """
    
    # 交易成本 (根据项目要求设置)
    commission = 9.95
    impact = 0.005
    
    # --- 1. 初始化和训练策略学习器 ---
    learner = sl.StrategyLearner(verbose=False, impact=impact, commission=commission)
    learner.add_evidence(symbol=symbol, sd=sd_in, ed=ed_in, sv=sv)
    
    manual_strategy = ms.ManualStrategy(verbose=False, impact=impact, commission=commission)
    
    # --- 2. 样本内数据 (In-Sample) ---
    print(f"--- 样本内 ({sd_in.date()} - {ed_in.date()}) ---")
    
    # 基准
    bench_trades_in = mc.create_benchmark_trades(symbol, sd_in, ed_in)
    portvals_bench_in = mc.compute_portvals(bench_trades_in, start_val=sv, commission=commission, impact=impact, symbol=symbol)
    
    # 手动策略
    trades_manual_in = manual_strategy.testPolicy(symbol=symbol, sd=sd_in, ed=ed_in, sv=sv)
    portvals_manual_in = mc.compute_portvals(trades_manual_in, start_val=sv, commission=commission, impact=impact, symbol=symbol)
    
    # 策略学习器
    trades_learner_in = learner.testPolicy(symbol=symbol, sd=sd_in, ed=ed_in, sv=sv)
    portvals_learner_in = mc.compute_portvals(trades_learner_in, start_val=sv, commission=commission, impact=impact, symbol=symbol)
    
    # 生成图表和表格 (样本内)
    generate_plot_and_stats(
        [portvals_manual_in, portvals_learner_in, portvals_bench_in], 
        [trades_manual_in, trades_learner_in],
        ["Manual Strategy (Red)", "Strategy Learner (Green)", "Benchmark (Purple)"],
        "JPM 样本内策略比较", "experiment1_in_sample.png"
    )

    # --- 3. 样本外数据 (Out-of-Sample) ---
    print(f"--- 样本外 ({sd_out.date()} - {ed_out.date()}) ---")
    
    # 基准
    bench_trades_out = mc.create_benchmark_trades(symbol, sd_out, ed_out)
    portvals_bench_out = mc.compute_portvals(bench_trades_out, start_val=sv, commission=commission, impact=impact, symbol=symbol)
    
    # 手动策略
    trades_manual_out = manual_strategy.testPolicy(symbol=symbol, sd=sd_out, ed=ed_out, sv=sv)
    portvals_manual_out = mc.compute_portvals(trades_manual_out, start_val=sv, commission=commission, impact=impact, symbol=symbol)
    
    # 策略学习器
    trades_learner_out = learner.testPolicy(symbol=symbol, sd=sd_out, ed=ed_out, sv=sv)
    portvals_learner_out = mc.compute_portvals(trades_learner_out, start_val=sv, commission=commission, impact=impact, symbol=symbol)
    
    # 生成图表和表格 (样本外)
    generate_plot_and_stats(
        [portvals_manual_out, portvals_learner_out, portvals_bench_out], 
        [trades_manual_out, trades_learner_out],
        ["Manual Strategy (Red)", "Strategy Learner (Green)", "Benchmark (Purple)"],
        "JPM 样本外策略比较", "experiment1_out_of_sample.png"
    )

def generate_plot_and_stats(portvals_list, trades_list, labels, title, filename):
    """
    生成图表并将性能指标输出到控制台。
    """
    plt.figure(figsize=(12, 6))
    
    # 颜色
    colors = ['r', 'g', 'm']
    
    # 绘制投资组合价值 (归一化)
    for portvals, label, color in zip(portvals_list, labels, colors):
        norm_portvals = portvals / portvals.iloc[0]
        plt.plot(norm_portvals, label=label, color=color, linewidth=1.5)
        
        # 计算和打印统计数据
        cr, adr, sddr = mc.compute_portfolio_stats(portvals)
        print(f"  {label}: CR={cr:.6f}, ADR={adr:.6f}, SDDR={sddr:.6f}")
    
    # 绘制交易信号 (仅适用于 ManualStrategy 和 StrategyLearner)
    # 对于 ManualStrategy (红色) 和 StrategyLearner (绿色)
    # 信号线颜色: 蓝色 (买/多头入场), 黑色 (卖/空头入场)
    # 信号行仅需要 1000/-1000/2000/-2000 的交易，但垂直线应基于入场
    
    trades_manual = trades_list[0]
    trades_learner = trades_list[1]
    
    # 提取入场信号（从 0 或 -1000 变为 1000，或从 0 或 1000 变为 -1000）
    # 仅绘制 ManualStrategy 的信号，以满足 ManualStrategy 的图表要求
    
    # 绘制 ManualStrategy 的交易信号（入场点）
    manual_signal_dates = trades_manual[trades_manual.iloc[:, 0] != 0].index
    
    for date in manual_signal_dates:
        trade = trades_manual.loc[date].iloc[0]
        
        # 简化: 仅关注多头入场 (买入 1000, 蓝色) 和空头入场 (卖出 1000, 黑色)
        # 注意: 这里的逻辑需要 Marketsimcode 来准确确定持仓状态
        # 为了满足项目要求，我们简化为：买入/转多头为蓝线，卖出/转空头为黑线
        
        if trade > 0: # 买入或从空头转多头
            plt.axvline(date, color='blue', linestyle='--', linewidth=0.5, label='Long Entry' if date == manual_signal_dates[0] and trade > 0 else "")
        elif trade < 0: # 卖出或从多头转空头
            plt.axvline(date, color='black', linestyle='--', linewidth=0.5, label='Short Entry' if date == manual_signal_dates[0] and trade < 0 else "")

    plt.title(title)
    plt.xlabel("Date")
    plt.ylabel("Normalized Portfolio Value")
    plt.legend()
    plt.grid(True)
    plt.savefig(filename)
    plt.close()

if __name__ == "__main__":
    run_experiment1()