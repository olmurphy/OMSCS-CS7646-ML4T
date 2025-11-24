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

# Import strategy and market simulation code
# Assume your files are located under the strategy_evaluation directory
import StrategyLearner as sl
import ManualStrategy as ms
import marketsimcode as mc 
# import metrics as met # Assume metrics is included in marketsimcode.py

def run_experiment1(symbol="JPM", sv=100000, 
                    sd_in=dt.datetime(2008, 1, 1), ed_in=dt.datetime(2009, 12, 31),
                    sd_out=dt.datetime(2010, 1, 1), ed_out=dt.datetime(2011, 12, 31)):
    """
    Execute Experiment 1: Compare the performance of ManualStrategy and StrategyLearner 
    both in-sample and out-of-sample.
    """
    
    # Trading costs (set according to project requirements)
    commission = 9.95
    impact = 0.005
    
    # --- 1. Initialize and train the Strategy Learner ---
    learner = sl.StrategyLearner(verbose=False, impact=impact, commission=commission)
    learner.add_evidence(symbol=symbol, sd=sd_in, ed=ed_in, sv=sv)
    
    manual_strategy = ms.ManualStrategy(verbose=False, impact=impact, commission=commission)
    
    # --- 2. In-Sample Data ---
    print(f"--- In-Sample ({sd_in.date()} - {ed_in.date()}) ---")
    
    # Benchmark
    bench_trades_in = mc.create_benchmark_trades(symbol, sd_in, ed_in)
    portvals_bench_in = mc.compute_portvals(bench_trades_in, start_val=sv, commission=commission, impact=impact, symbol=symbol)
    
    # Manual Strategy
    trades_manual_in = manual_strategy.testPolicy(symbol=symbol, sd=sd_in, ed=ed_in, sv=sv)
    portvals_manual_in = mc.compute_portvals(trades_manual_in, start_val=sv, commission=commission, impact=impact, symbol=symbol)
    
    # Strategy Learner
    trades_learner_in = learner.testPolicy(symbol=symbol, sd=sd_in, ed=ed_in, sv=sv)
    portvals_learner_in = mc.compute_portvals(trades_learner_in, start_val=sv, commission=commission, impact=impact, symbol=symbol)
    
    # Generate Chart and Table (In-Sample)
    generate_plot_and_stats(
        [portvals_manual_in, portvals_learner_in, portvals_bench_in], 
        [trades_manual_in, trades_learner_in],
        ["Manual Strategy (Red)", "Strategy Learner (Green)", "Benchmark (Purple)"],
        "JPM In-Sample Strategy Comparison", "experiment1_in_sample.png"
    )

    # --- 3. Out-of-Sample Data ---
    print(f"--- Out-of-Sample ({sd_out.date()} - {ed_out.date()}) ---")
    
    # Benchmark
    bench_trades_out = mc.create_benchmark_trades(symbol, sd_out, ed_out)
    portvals_bench_out = mc.compute_portvals(bench_trades_out, start_val=sv, commission=commission, impact=impact, symbol=symbol)
    
    # Manual Strategy
    trades_manual_out = manual_strategy.testPolicy(symbol=symbol, sd=sd_out, ed=ed_out, sv=sv)
    portvals_manual_out = mc.compute_portvals(trades_manual_out, start_val=sv, commission=commission, impact=impact, symbol=symbol)
    
    # Strategy Learner
    trades_learner_out = learner.testPolicy(symbol=symbol, sd=sd_out, ed=ed_out, sv=sv)
    portvals_learner_out = mc.compute_portvals(trades_learner_out, start_val=sv, commission=commission, impact=impact, symbol=symbol)
    
    # Generate Chart and Table (Out-of-Sample)
    generate_plot_and_stats(
        [portvals_manual_out, portvals_learner_out, portvals_bench_out], 
        [trades_manual_out, trades_learner_out],
        ["Manual Strategy (Red)", "Strategy Learner (Green)", "Benchmark (Purple)"],
        "JPM Out-of-Sample Strategy Comparison", "experiment1_out_of_sample.png"
    )

def generate_plot_and_stats(portvals_list, trades_list, labels, title, filename):
    """
    Generates the chart and outputs performance metrics to the console.
    """
    plt.figure(figsize=(12, 6))
    
    # Colors
    colors = ['r', 'g', 'm']
    
    # Plot Portfolio Values (Normalized)
    for portvals, label, color in zip(portvals_list, labels, colors):
        norm_portvals = portvals / portvals.iloc[0]
        plt.plot(norm_portvals, label=label, color=color, linewidth=1.5)
        
        # Calculate and print statistics
        cr, adr, sddr = mc.compute_portfolio_stats(portvals)
        print(f"  {label}: CR={cr:.6f}, ADR={adr:.6f}, SDDR={sddr:.6f}")
    
    # Plot Trading Signals (Only for ManualStrategy and StrategyLearner)
    # For ManualStrategy (Red) and StrategyLearner (Green)
    # Signal line colors: Blue (Buy/Long Entry), Black (Sell/Short Entry)
    # The signal lines only need to show trades of 1000/-1000/2000/-2000, 
    # but the vertical lines should be based on entry.
    
    trades_manual = trades_list[0]
    trades_learner = trades_list[1]
    
    # Extract entry signals (trades where the amount is non-zero)
    # Only plot signals for ManualStrategy to satisfy ManualStrategy plot requirements
    
    # Plot ManualStrategy's trading signals (entry points)
    manual_signal_dates = trades_manual[trades_manual.iloc[:, 0] != 0].index
    
    for date in manual_signal_dates:
        trade = trades_manual.loc[date].iloc[0]
        
        # Simplification: Focus on Long Entry (Buy 1000, Blue) and Short Entry (Sell 1000, Black)
        # Note: The logic here requires Marketsimcode to accurately determine holding status.
        # To meet project requirements, we simplify to: Buy/Go Long = Blue Line, Sell/Go Short = Black Line
        
        if trade > 0: # Buy or transition from short to long
            # Only label the first signal for the legend
            label_text = 'Long Entry' if date == manual_signal_dates[0] and trade > 0 else ""
            plt.axvline(date, color='blue', linestyle='--', linewidth=0.5, label=label_text)
        elif trade < 0: # Sell or transition from long to short
            # Only label the first signal for the legend
            label_text = 'Short Entry' if date == manual_signal_dates[0] and trade < 0 else ""
            plt.axvline(date, color='black', linestyle='--', linewidth=0.5, label=label_text)

    plt.title(title)
    plt.xlabel("Date")
    plt.ylabel("Normalized Portfolio Value")
    plt.legend()
    plt.grid(True)
    plt.savefig("images/" + filename)
    plt.close()

def author():                                                                                             
    return "omurphy8"   

def study_group():
    return "omurphy8"

if __name__ == "__main__":
    run_experiment1()