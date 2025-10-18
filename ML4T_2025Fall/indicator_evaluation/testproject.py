import datetime as dt
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import os

# 导入其他文件中的函数/模块
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
    计算投资组合的性能指标。
    """
    # 归一化：所有值除以第一个值 (已在绘图时处理，但此处为确保准确性再次处理)
    normed_port_val = port_val / port_val.iloc[0]
    
    # 累计收益 (CR)
    cr = normed_port_val.iloc[-1] - normed_port_val.iloc[0]
    
    # 每日收益 (DR)
    daily_returns = port_val.copy()
    daily_returns[1:] = (port_val[1:] / port_val[:-1].values) - 1
    daily_returns.iloc[0] = 0 # 将第一天的每日收益设置为 0
    
    # 每日收益平均值 (Mean DR)
    mean_dr = daily_returns.mean()
    
    # 每日收益标准差 (Stdev DR)
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
        f.write(f"time: {sd.strftime('%Y-%m-%d')} 至 {ed.strftime('%Y-%m-%d')}\n")
        f.write(f"stock symbol: {symbol}\n\n")
        
        # 格式化输出到小数点后 6 位
        f.write("performance indicator (to 6 sig digits):\n")
        f.write("----------------------------------------------------------------\n")
        f.write(f"| indicator | (TOS) | Benchmark | \n")
        f.write("----------------------------------------------------------------\n")
        f.write(f"| cumulative return | {tos_cr:.6f} | {bench_cr:.6f} |\n")
        f.write(f"| stdev daily return | {tos_stdev_dr:.6f} | {bench_stdev_dr:.6f} |\n")
        f.write(f"| mean daily return mean daily return | {tos_mean_dr:.6f} | {bench_mean_dr:.6f} |\n")
        f.write("----------------------------------------------------------------\n\n")
        
    

    # general files
    # 3. 生成性能对比图表
    # ------------------------------------------
    
    # 归一化投资组合价值
    normed_tos = tos_port_val / tos_port_val.iloc[0]
    normed_bench = benchmark_port_val / benchmark_port_val.iloc[0]
    
    plt.figure(figsize=(10, 6))
    plt.plot(normed_bench, label='基准 (Benchmark)', color='purple') # 基准：紫线
    plt.plot(normed_tos, label='理论最优策略 (TOS)', color='red')    # TOS：红线
    
    plt.title(f"理论最优策略 (TOS) 与基准对比 ({symbol})", fontsize=16)
    plt.xlabel("日期", fontsize=12)
    plt.ylabel("投资组合价值 (归一化)", fontsize=12)
    plt.legend(loc='best')
    plt.grid(True)
    
    # 确保保存到 ./images 文件夹
    if not os.path.exists('images'):
        os.makedirs('images')
    
    plt.savefig("images/TOS_Performance_Comparison.png")
    plt.close()
    
    print("✅ TOS 性能对比图表已保存到 images/TOS_Performance_Comparison.png")


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
    
    # 1.4. 生成 TOS 报告 (图表和表格)
    generate_tos_report(tos_port_val, benchmark_port_val)

    # ==========================================================================
    # 第 2 部分：技术指标
    # ==========================================================================
    
    # 2.1. 运行并生成指标图表
    df_indicator_results = ind.run_all_indicators(symbol=symbol, sd=sd, ed=ed)
    
    print("\n--- 所有项目任务已完成。请检查 images/ 文件夹中的图表以及 p6_results.txt 中的统计数据。---")