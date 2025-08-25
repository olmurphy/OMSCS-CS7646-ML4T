import numpy as np
import matplotlib.pyplot as plt
import random

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

def gtid():  		  	   		 	 	 		  		  		    	 		 		   		 		  
    """  		  	   		 	 	 		  		  		    	 		 		   		 		  
    :return: The GT ID of the student  		  	   		 	 	 		  		  		    	 		 		   		 		  
    :rtype: int  		  	   		 	 	 		  		  		    	 		 		   		 		  
    """  		  	   		 	 	 		  		  		    	 		 		   		 		  
    return 904015662  # replace with your GT ID number  

def simulate_episode(num_spins=1000):
    """
    Simulates a single episode of the betting strategy.

    The strategy involves starting with a $1 bet and doubling the bet
    on a loss until a win is achieved. The episode ends when the
    total winnings reach $80.
    
    Args:
        num_spins (int): The number of spins in a single episode.
    
    Returns:
        list: A list of winnings at each spin. The winnings are
              persisted at $80 or greater once the target is hit.
    """
    episode_winnings = 0
    winnings_history = []
    win_prob = 0.4737 
    
    for _ in range(num_spins):
        if episode_winnings >= 80:
            # If the target is reached, the value persists
            winnings_history.append(episode_winnings)
            continue
            
        bet_amount = 1
        won = False
        
        while not won:
            # Simulate a roulette spin (50% chance of winning for simplicity)
            won = get_spin_result(win_prob)
            
            if won:
                episode_winnings += bet_amount
            else:
                episode_winnings -= bet_amount
                bet_amount *= 2
        
        winnings_history.append(episode_winnings)
        
    return winnings_history

def generate_charts():
    """
    Generates the three required charts based on the simulation experiments.
    """
    np.random.seed(gtid())
    # Define plot parameters
    x_range = [0, 300]
    y_limits = [-256, 100]
    
    # === Experiment 1: 10 Episodes ===
    print("Running Experiment 1: 10 episodes...")
    episodes_10 = []
    for _ in range(10):
        episodes_10.append(simulate_episode())
        
    plt.figure(figsize=(10, 6))
    for i, history in enumerate(episodes_10):
        plt.plot(history, label=f'Episode {i+1}')
        
    plt.title('Figure 1: Winnings of 10 Roulette Betting Episodes')
    plt.xlabel('Number of Spins')
    plt.ylabel('Winnings ($)')
    plt.xlim(0, 300)
    plt.ylim(y_limits)
    plt.legend()
    plt.grid(True)
    plt.show()

    # === Experiment 2 & 3: 1000 Episodes ===
    print("Running Experiment 2 & 3: 1000 episodes...")
    episodes_1000 = []
    for _ in range(1000):
        episodes_1000.append(simulate_episode())
        
    # Convert list of lists to a NumPy array for easy calculations
    data_1000 = np.array(episodes_1000)
    
    # Calculate statistics
    mean_winnings = np.mean(data_1000, axis=0)
    std_winnings = np.std(data_1000, axis=0)
    median_winnings = np.median(data_1000, axis=0)
    
    # === Figure 2: Mean Winnings ===
    plt.figure(figsize=(10, 6))
    plt.plot(mean_winnings, label='Mean Winnings', color='blue')
    plt.plot(mean_winnings + std_winnings, '--', label='Mean + Std Dev', color='red')
    plt.plot(mean_winnings - std_winnings, '--', label='Mean - Std Dev', color='green')
    
    plt.title('Figure 2: Mean Winnings over 1000 Episodes')
    plt.xlabel('Number of Spins')
    plt.ylabel('Winnings ($)')
    plt.xlim(x_range)
    plt.ylim(y_limits)
    plt.legend()
    plt.grid(True)
    plt.show()

    # === Figure 3: Median Winnings ===
    plt.figure(figsize=(10, 6))
    plt.plot(median_winnings, label='Median Winnings', color='blue')
    plt.plot(median_winnings + std_winnings, '--', label='Median + Std Dev', color='red')
    plt.plot(median_winnings - std_winnings, '--', label='Median - Std Dev', color='green')
    
    plt.title('Figure 3: Median Winnings over 1000 Episodes')
    plt.xlabel('Number of Spins')
    plt.ylabel('Winnings ($)')
    plt.xlim(x_range)
    plt.ylim(y_limits)
    plt.legend()
    plt.grid(True)
    plt.show()

if __name__ == '__main__':
    generate_charts()