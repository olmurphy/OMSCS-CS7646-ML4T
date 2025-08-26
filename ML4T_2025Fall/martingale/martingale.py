""""""
"""Assess a betting strategy.

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
  		  	   		 	 	 		  		  		    	 		 		   		 		  
Student Name: Owen Murphy	  	   		 	 	 		  		  		    	 		 		   		 		  
GT User ID: omurphy8		  	   		 	 	 		  		  		    	 		 		   		 		  
GT ID: 904015662	  	   		 	 	 		  		  		    	 		 		   		 		  
"""  		  	   		 	 	 		  		  		    	 		 		   		 		  
  		  	   		 	 	 		  		  		    	 		 		   		 		  
import numpy as np  	
import matplotlib.pyplot as plt
  		  	   		 	 	 		  		  		    	 		 		   		 		  
  		  	   		 	 	 		  		  		    	 		 		   		 		  
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

def gtid():  		  	   		 	 	 		  		  		    	 		 		   		 		  
    """  		  	   		 	 	 		  		  		    	 		 		   		 		  
    :return: The GT ID of the student  		  	   		 	 	 		  		  		    	 		 		   		 		  
    :rtype: int  		  	   		 	 	 		  		  		    	 		 		   		 		  
    """  		  	   		 	 	 		  		  		    	 		 		   		 		  
    return 904015662		  	   		 	 	 		  		  		    	 		 		   		 		  
  		  	   		 	 	 		  		  		    	 		 		   		 		  
  		  	   		 	 	 		  		  		    	 		 		   		 		  
def get_spin_result(win_prob):  		  	   		 	 	 		  		  		    	 		 		   		 		  
    """  		  	   		 	 	 		  		  		    	 		 		   		 		  
    Given a win probability between 0 and 1, the function returns whether the probability will result in a win.  		  	   		 	 	 		  		  		    	 		 		   		 		  
  		  	   		 	 	 		  		  		    	 		 		   		 		  
    :param win_prob: The probability of winning  		  	   		 	 	 		  		  		    	 		 		   		 		  
    :type win_prob: float  		  	   		 	 	 		  		  		    	 		 		   		 		  
    :return: The result of the spin.  		  	   		 	 	 		  		  		    	 		 		   		 		  
    :rtype: bool  		  	   		 	 	 		  		  		    	 		 		   		 		  
    """  		  	   		 	 	 		  		  		    	 		 		   		 		  
    result = False  		  	   		 	 	 		  		  		    	 		 		   		 		  
    if np.random.random() <= win_prob:  		  	   		 	 	 		  		  		    	 		 		   		 		  
        result = True  		  	   		 	 	 		  		  		    	 		 		   		 		  
    return result  		  	   		 	 	 		  		  		    	 		 		   		 		  

def plot_data(df, title="Stock prices"):
    """Plot stock prices with a custom title and meaningful axis labels."""
    ax = df.plot(title=title, fontsize=12)
    ax.set_xlabel("Date")
    ax.set_ylabel("Price")
    plt.show()

def save_plot(filename):
    """Save the current figure using the provided filename."""
    plt.savefig("images/" + filename + ".png", format="png")
    plt.close()

def run_episode_with_bankroll(win_prob, initial_bankroll=256):
    episode_winnings = 0
    winnings = [0]
    num_spins = 0
    bankroll = initial_bankroll
    bet_amnt = 1

    while num_spins < 1000:
        if episode_winnings >= 80 or bankroll <= 0:
            final_winnings = episode_winnings if episode_winnings >= 80 else -256
            while num_spins < 1000:
                winnings.append(final_winnings)
                num_spins += 1
            return winnings
            
        current_bet = bet_amnt
        if bankroll < bet_amnt:
            current_bet = bankroll
        
        won = get_spin_result(win_prob)
        num_spins += 1
        if won == True:
            episode_winnings += current_bet
            bankroll += current_bet
            bet_amnt = 1
        else:
            episode_winnings -= current_bet
            bankroll -= current_bet
            bet_amnt = bet_amnt * 2
        winnings.append(episode_winnings)
    return winnings

def run_episode(win_prob):
    episode_winnings = 0
    winnings = [0]
    num_spins = 0

    while num_spins < 1000:
        if episode_winnings >= 80:
            # If the target is reached, the value persists
            winnings.append(episode_winnings)
            num_spins += 1
            continue
            
        bet_amnt = 1
        won = False
        while not won:
            won = get_spin_result(win_prob)
            num_spins += 1
            
            if won == True:
                episode_winnings += bet_amnt
            else:
                episode_winnings -= bet_amnt
                bet_amnt = bet_amnt * 2
            winnings.append(episode_winnings)
    return winnings

def generate_figure_1(win_prob):
    """Create Figure 1."""
    num_episodes = 10
    for i in range(num_episodes):
        winnings = run_episode(win_prob)
        plt.plot(winnings, label=f'Episode {i+1}')
    
    plt.plot(winnings)
    plt.title("10 Episodes of the Martingale Betting Strategy")
    plt.xlabel("Spin Number")
    plt.ylabel("Winnings ($)")
    plt.ylim(-256, 100)
    plt.xlim(0, 300)
    plt.legend()
    plt.grid(True)
    save_plot("Figure-1")


def generate_figure_2(win_prob):

    num_episodes = 1000
    equal_80 = 0
    greater_than_80 = 0
    winning_data = []
    for _ in range(num_episodes):
        winning_data.append(run_episode(win_prob))
        if winning_data[-1][-1] >= 80:
            greater_than_80 += 1
        
        if winning_data[-1][-1] == 80:
            equal_80 += 1
    
    winnings_arr = np.array(winning_data)
    means = np.mean(winnings_arr, axis=0)
    stds = np.std(winnings_arr, axis=0)

    upper_band, lower_band = get_bollinger_bands(np.array(means), np.array(stds))

    prob_greater_than_80 = greater_than_80 / num_episodes
    prob_equal_80 = equal_80 / num_episodes

    # Print the results in a format suitable for a table
    print("--------------------------------------------------")
    print("Simulation Results for Experiment 1")
    print("--------------------------------------------------")
    print(f"| Total Episodes Simulated      | {num_episodes: <23} |")
    print(f"| Episodes with Winnings >= $80 | {greater_than_80: <23} |")
    print(f"| Episodes with Winnings = $80  | {equal_80: <23} |")
    print(f"| Probability of Winnings >= $80| {prob_greater_than_80: <23.4f} |")
    print(f"| Probability of Winnings = $80 | {prob_equal_80: <23.4f} |")
    print("--------------------------------------------------")

    plt.plot(means, label='Mean')
    plt.plot(upper_band, label='Upper Band')
    plt.plot(lower_band, label='Lower Band')
    plt.title("Mean Winnings per Episode with Bollinger Bands using 1 STDEV")
    plt.xlabel("Spin Number")
    plt.ylabel("Mean Winnings")
    plt.xlim(0, 300)
    plt.ylim(-256, 100)
    plt.grid(True)
    plt.legend()
    save_plot("Figure-2")

def generate_figure_3(win_prob):
    winning_data = []
    for _ in range(1000):
        winning_data.append(run_episode(win_prob))
    
    winnings_arr = np.array(winning_data)
    median = np.median(winnings_arr, axis=0)
    stds = np.std(winnings_arr, axis=0)
    
    upper_band, lower_band = get_bollinger_bands(np.array(median), np.array(stds))

    plt.plot(median, label='Median')
    plt.plot(upper_band, label='Upper Band')
    plt.plot(lower_band, label='Lower Band')
    plt.title("Median Winnings per Episode with Bollinger Bands using 1 STDEV")
    plt.xlabel("Spin Number")
    plt.ylabel("Median Winnings")
    plt.xlim(0, 300)
    plt.ylim(-256, 100)
    plt.grid(True)
    plt.legend()
    save_plot("Figure-3")

def generate_figure_4(win_prob):

    winning_data = []
    for _ in range(1000):
        winning_data.append(run_episode_with_bankroll(win_prob))
    
    winnings_arr = np.array(winning_data)
    means = np.mean(winnings_arr, axis=0)
    stds = np.std(winnings_arr, axis=0)

    upper_band, lower_band = get_bollinger_bands(np.array(means), np.array(stds))

    plt.plot(means, label='Mean')
    plt.plot(upper_band, label='Upper Band')
    plt.plot(lower_band, label='Lower Band')
    plt.title("Mean Winnings per Episode with Bollinger & Bankroll Limit")
    plt.xlabel("Spin Number")
    plt.ylabel("Mean Winnings")
    plt.xlim(0, 300)
    plt.ylim(-256, 100)
    plt.grid(True)
    plt.legend()
    save_plot("Figure-4")

def generate_figure_5(win_prob):
    winning_data = []
    for _ in range(1000):
        winning_data.append(run_episode_with_bankroll(win_prob))
    
    winnings_arr = np.array(winning_data)
    median = np.median(winnings_arr, axis=0)
    stds = np.std(winnings_arr, axis=0)
    
    upper_band, lower_band = get_bollinger_bands(np.array(median), np.array(stds))

    plt.plot(median, label='Median')
    plt.plot(upper_band, label='Upper Band')
    plt.plot(lower_band, label='Lower Band')
    plt.title("Median Winnings per Episode with Bollinger & Bankroll Limit")
    plt.xlabel("Spin Number")
    plt.ylabel("Median Winnings")
    plt.xlim(0, 300)
    plt.ylim(-256, 100)
    plt.grid(True)
    plt.legend()
    save_plot("Figure-5")



def get_bollinger_bands(mean, stdev):
    """Return **1 stdev** upper and lower Bollinger Bands."""
    upper_band = mean + stdev
    lower_band = mean - stdev
    return upper_band, lower_band
     		  		  		    	 		 		   		 		  
  		  	   		 	 	 		  		  		    	 		 		   		 		  
def test_code():  		  	   		 	 	 		  		  		    	 		 		   		 		  
    """  		  	   		 	 	 		  		  		    	 		 		   		 		  
    Method to test your code  		  	   		 	 	 		  		  		    	 		 		   		 		  
    """  		  	   
    # source: https://www.primedope.com/american-roulette-odds/		 	 	 		  		  		    	 		 		   		 		  
    win_prob = 0.4737  # set appropriately to the probability of a win (47.37% chance of winning)	  	   		 	 	 		  		  		    	 		 		   		 		  
    np.random.seed(gtid())  # do this only once
    
    generate_figure_1(win_prob)
    generate_figure_2(win_prob)
    generate_figure_3(win_prob)
    generate_figure_4(win_prob)
    generate_figure_5(win_prob)
    	 		   		 		  
  		  	   		 	 	 		  		  		    	 		 		   		 		  
if __name__ == "__main__":  	
    test_code()  		  	   		 	 	 		  		  		    	 		 		   		 		  
