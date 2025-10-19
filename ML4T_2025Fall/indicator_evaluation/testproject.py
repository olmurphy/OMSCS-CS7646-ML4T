import datetime as dt
import pandas as pd
import matplotlib.pyplot as plt

from util import get_data
from marketsimcode import compute_portfolio_values
import TheoreticallyOptimalStrategy as tos
import indicators as ind

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

def compute_performance_metrics(port_val):
    """
    Calculate portfolio performance metrics.
    """
    # Normalization: All values divided by the first value (Already handled when plotting, but processed again here for accuracy)
    normed_port_val = port_val / port_val.iloc[0]
    
    # Cumulative Return (CR)
    cr = normed_port_val.iloc[-1] - normed_port_val.iloc[0]
    
    # Daily Returns (DR)
    daily_returns = port_val.copy()
    daily_returns[1:] = (port_val[1:] / port_val[:-1].values) - 1
    daily_returns.iloc[0] = 0 # Set the first day's daily return to 0
    
    # Mean Daily Return (Mean DR)
    mean_dr = daily_returns.mean()
    
    # Standard Deviation of Daily Return (Stdev DR)
    stdev_dr = daily_returns.std()
    
    return cr, mean_dr, stdev_dr

def generate_tos_report(tos_port_val, benchmark_port_val):
    # calc
    tos_cr, tos_mean_dr, tos_stdev_dr = compute_performance_metrics(tos_port_val)
    bench_cr, bench_mean_dr, bench_stdev_dr = compute_performance_metrics(benchmark_port_val)

    # p6_results.txt
    output_filename = 'p6_results.txt'
    with open(output_filename, 'w') as f:
        f.write("--- (TOS) and benchmark performance comparison ---\n")
        f.write(f"time: {sd.strftime('%Y-%m-%d')} to {ed.strftime('%Y-%m-%d')}\n")
        f.write(f"stock symbol: {symbol}\n\n")
        
        # Format output to 6 decimal places
        f.write("performance indicator (to 6 sig digits):\n")
        f.write("----------------------------------------------------------------\n")
        f.write(f"| Metric | (TOS) | Benchmark | \n")
        f.write("----------------------------------------------------------------\n")
        f.write(f"| cumulative return | {tos_cr:.6f} | {bench_cr:.6f} |\n")
        f.write(f"| stdev daily return | {tos_stdev_dr:.6f} | {bench_stdev_dr:.6f} |\n")
        f.write(f"| mean daily return | {tos_mean_dr:.6f} | {bench_mean_dr:.6f} |\n")
        f.write("----------------------------------------------------------------\n\n")

    # general chart files
    # Norm portfolio value
    normed_tos = tos_port_val / tos_port_val.iloc[0]
    normed_bench = benchmark_port_val / benchmark_port_val.iloc[0]
    
    plt.figure(figsize=(10, 6))
    plt.plot(normed_bench, label='Benchmark', color='purple')
    plt.plot(normed_tos, label='Theoretically Optimal Strategy (TOS)', color='red')
    
    plt.title(f"Theoretically Optimal Strategy (TOS) vs Benchmark Comparison ({symbol})", fontsize=16)
    plt.xlabel("Date", fontsize=12)
    plt.ylabel("Portfolio Value (Normalized)", fontsize=12)
    plt.legend(loc='best')
    plt.grid(True)
    
    plt.savefig("images/TOS_Performance_Comparison.png")
    plt.close()


if __name__ == "__main__":
    symbol = "JPM"
    sd = dt.datetime(2008, 1, 1)
    ed = dt.datetime(2009, 12, 31)
    sv = 100000.0
    
    # trade costs
    commission = 0.00
    impact = 0.00

    # TOS
    df_tos_trades = tos.testPolicy(symbol=symbol, sd=sd, ed=ed, sv=sv)
    
    # calc TOS
    tos_port_val = compute_portfolio_values(
        df_tos_trades, 
        start_val=sv, 
        commission=commission, 
        impact=impact
    )

    tos_port_val = tos_port_val['Value'] 

    dates = pd.date_range(sd, ed)
    prices_all = get_data([symbol], dates)
    prices = prices_all[[symbol]].dropna() # NaN

    df_benchmark_trades = pd.DataFrame(0.0, index=prices.index, columns=[symbol])
    
    # day 1 buy
    df_benchmark_trades.loc[df_benchmark_trades.index[0], symbol] = 1000 
    
    benchmark_port_val = compute_portfolio_values(
        df_benchmark_trades, 
        start_val=sv, 
        commission=commission, 
        impact=impact
    )
    benchmark_port_val = benchmark_port_val['Value'] 
    
    # generate TOS Report, chart & table
    generate_tos_report(tos_port_val, benchmark_port_val)

    # Run and generate indicator charts
    df_indicator_results = ind.run_all_indicators(symbol=symbol, sd=sd, ed=ed)
    