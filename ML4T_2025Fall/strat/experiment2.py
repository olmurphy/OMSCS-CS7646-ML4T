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
import StrategyLearner as sl
import marketsimcode as mc 
# import metrics as met

def run_experiment2(symbol="JPM", sv=100000, 
                    sd_in=dt.datetime(2008, 1, 1), ed_in=dt.datetime(2009, 12, 31)):
    """
    Execute Experiment 2: Analyze the effect of changing Impact on StrategyLearner's trading behavior.
    """
    
    # Experimental Impact values (at least 3 measurements)
    impact_values = [0.0, 0.001, 0.01, 0.05]
    commission = 0.00 # Project requires commission to be $0.00
    
    results = {}
    
    for impact in impact_values:
        
        # 1. Initialize and train the Strategy Learner
        learner = sl.StrategyLearner(verbose=False, commission=commission)
        learner.add_evidence(symbol=symbol, sd=sd_in, ed=ed_in, sv=sv)
        
        # 2. Generate in-sample trades
        trades_learner_in = learner.testPolicy(symbol=symbol, sd=sd_in, ed=ed_in, sv=sv)
        
        # 3. Calculate Portfolio Value
        # Note: compute_portvals here should use the current impact and commission
        portvals_learner_in = mc.compute_portvals(trades_learner_in, start_val=sv, commission=commission, impact=impact, symbol=symbol)
        
        # 4. Record Results
        cr, adr, sddr = mc.compute_portfolio_stats(portvals_learner_in)
        num_trades = (trades_learner_in.iloc[:, 0] != 0).sum()
        
        results[impact] = {
            'portvals': portvals_learner_in,
            'CR': cr,
            'NumTrades': num_trades,
            'Trades_df': trades_learner_in # Used to verify if trading behavior differs
        }
        
        print(f"2:  Cumulative Return (CR): {cr:.6f}, Number of Trades: {num_trades}")

    # --- 5. Generate Chart (Portfolio Value) ---
    plt.figure(figsize=(12, 6))
    
    for impact, data in results.items():
        portvals = data['portvals']
        norm_portvals = portvals / portvals.iloc[0]
        plt.plot(norm_portvals, label=f'Impact={impact} (CR: {data["CR"]:.4f})', linewidth=1.5)
        
    plt.title("StrategyLearner In-Sample Performance vs. Impact Value (JPM)")
    plt.xlabel("Date")
    plt.ylabel("Normalized Portfolio Value")
    plt.legend()
    plt.grid(True)
    plt.savefig("images/" + "experiment2_impact_performance.png")
    plt.close()

    # --- 6. Generate Chart (Number of Trades) ---
    impacts = list(results.keys())
    num_trades = [results[i]['NumTrades'] for i in impacts]
    
    plt.figure(figsize=(8, 5))
    plt.bar([str(i) for i in impacts], num_trades, color='skyblue')
    plt.title("StrategyLearner Number of Trades vs. Impact Value (JPM)")
    plt.xlabel("Impact Value")
    plt.ylabel("Number of Trades")
    plt.grid(axis='y')
    plt.savefig("images/" + "experiment2_impact_trades.png")
    plt.close()
    
    # 7. Validate Differences in Trading Strategy (Textual Description)
    # You need to check the difference in 'Trades_df' across different impact values to support statements in the report.
    print("\nPlease compare the 'Trades_df' for different Impact values in your report to demonstrate that the strategy has changed.")
    print("For example, compare the trading dataframes for Impact=0.0 and Impact=0.05.")
    
if __name__ == "__main__":
    run_experiment2()