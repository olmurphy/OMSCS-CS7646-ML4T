import datetime as dt
import experiment1
import experiment2

# 实现 author() 函数
def author():
    # 请替换为您的佐治亚理工学院用户 ID
    return 'your_gt_username' 

# 您也需要在所有文件中添加 author() 函数

def run_all():
    """
    运行所有实验，生成报告所需的所有图表和数据。
    """
    # 实验参数
    symbol = "JPM"
    sv = 100000
    sd_in = dt.datetime(2008, 1, 1)
    ed_in = dt.datetime(2009, 12, 31)
    sd_out = dt.datetime(2010, 1, 1)
    ed_out = dt.datetime(2011, 12, 31)

    print("--- 运行 experiment1.py ---")
    experiment1.run_experiment1(
        symbol=symbol, sv=sv, 
        sd_in=sd_in, ed_in=ed_in, 
        sd_out=sd_out, ed_out=ed_out
    )
    print("experiment1.py 完成，图表已保存。")

    print("\n--- 运行 experiment2.py ---")
    experiment2.run_experiment2(
        symbol=symbol, sv=sv, 
        sd_in=sd_in, ed_in=ed_in
    )
    print("experiment2.py 完成，图表已保存。")
    
    # 如果 ManualStrategy.py 和 StrategyLearner.py 也需要直接生成图表，
    # 您需要在这里调用相应的函数，例如：
    # ms.ManualStrategy().generate_report_charts(sd_in, ed_in, sd_out, ed_out)
    
    print("\n--- 所有实验和图表生成完成。---")

if __name__ == "__main__":
    run_all()
    # 确保在所有 Python 文件中都添加了 author() 函数
    print(f"\nAuthor: {author()}")