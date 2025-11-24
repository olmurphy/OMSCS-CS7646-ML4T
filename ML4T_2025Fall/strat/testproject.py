import datetime as dt
import experiment1
import experiment2

def run_all():
    """
    Runs all experiments and generates all charts and data required for the report.
    """
    # Experiment parameters
    symbol = "JPM"
    sv = 100000
    sd_in = dt.datetime(2008, 1, 1)
    ed_in = dt.datetime(2009, 12, 31)
    sd_out = dt.datetime(2010, 1, 1)
    ed_out = dt.datetime(2011, 12, 31)

    experiment1.run_experiment1(
        symbol=symbol, sv=sv, 
        sd_in=sd_in, ed_in=ed_in, 
        sd_out=sd_out, ed_out=ed_out
    )
    experiment2.run_experiment2(
        symbol=symbol, sv=sv, 
        sd_in=sd_in, ed_in=ed_in
    )
    
def author():                                                                                             
    return "omurphy8"   

def study_group():
    return "omurphy8"

if __name__ == "__main__":
    run_all()