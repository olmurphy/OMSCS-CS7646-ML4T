""""""  		  	   		 	 	 		  		  		    	 		 		   		 		  
"""  		  	   		 	 	 		  		  		    	 		 		   		 		  
Test a learner.  (c) 2015 Tucker Balch  		  	   		 	 	 		  		  		    	 		 		   		 		  
  		  	   		 	 	 		  		  		    	 		 		   		 		  
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
"""  		  	   		 	 	 		  		  		    	 		 		   		 		  
  		  	   		 	 	 		  		  		    	 		 		   		 		  
import math  		  	   		 	 	 		  		  		    	 		 		   		 		  
import sys
import random  		  	   		 	 	 		  		  		    	 		 		   		 		  
  		  	   		 	 	 		  		  		    	 		 		   		 		  
import numpy as np  		
import matplotlib.pyplot as plt	   		 	 	 		  		  		    	 		 		   		 		  
  		  	   		 	 	 		  		  		    	 		 		   		 		  
import LinRegLearner as lrl
import DTLearner as dtl
import BagLearner as bl
import RTLearner as rtl

def gtid():  		  	   		 	 	 		  		  		    	 		 		   		 		  
    """  		  	   		 	 	 		  		  		    	 		 		   		 		  
    :return: The GT ID of the student  		  	   		 	 	 		  		  		    	 		 		   		 		  
    :rtype: int  		  	   		 	 	 		  		  		    	 		 		   		 		  
    """  		  	   		 	 	 		  		  		    	 		 		   		 		  
    return 904015662

def experiment_one(features, target):

    # compute how much of the data is training and testing
    train_rows = int(0.6 * features.shape[0])
    train_indices = np.random.choice(features.shape[0], size=train_rows, replace=False)
    test_indices = np.setdiff1d(np.arange(features.shape[0]), train_indices)

    # separate out training and testing data  		  	   		 	 	 		  		  		    	 		 		   		 		  
    train_x = features[train_indices]  		  	   		 	 	 		  		  		    	 		 		   		 		  
    train_y = target[train_indices]  		  	   		 	 	 		  		  		    	 		 		   		 		  
    test_x = features[test_indices]  		  	   		 	 	 		  		  		    	 		 		   		 		  
    test_y = target[test_indices] 

    leaf_sizes = range(1, 100)
    in_sample_rmse = []
    out_of_sample_rmse = [] 

    for leaf_size in leaf_sizes:
        learner = dtl.DTLearner(leaf_size=leaf_size, verbose=False)  # create a DTLearner	
        learner.add_evidence(train_x, train_y)  # train it

        # eval in sample
        pred_y = learner.query(train_x)
        rmse_train = math.sqrt(((train_y - pred_y) ** 2).sum() / train_y.shape[0])
        in_sample_rmse.append(rmse_train)

        # eval out of sample
        pred_y = learner.query(test_x)
        rmse_test = math.sqrt(((test_y - pred_y) ** 2).sum() / test_y.shape[0])
        out_of_sample_rmse.append(rmse_test)

    plt.figure(figsize=(10, 6))
    plt.plot(leaf_sizes, in_sample_rmse, label='In-Sample RMSE')
    plt.plot(leaf_sizes, out_of_sample_rmse, label='Out-of-Sample RMSE')
    plt.title('DTLearner RMSE vs Leaf Size')
    plt.xlabel('leaf_size')
    plt.ylabel('RMSE')
    plt.legend()
    plt.grid(True)
    plt.savefig('images/experiment_1.png', format='png')

    # TODO: might not need. Create and append table to p3_results.txt
    with open('p3_results.txt', 'a') as f:
        f.write("\n\nExperiment 1 Results (DTLearner RMSE vs. Leaf Size)\n")
        f.write("--------------------------------------------------\n")
        f.write("{:<12} {:<20} {:<20}\n".format("Leaf Size", "In-Sample RMSE", "Out-of-Sample RMSE"))
        f.write("{:<12} {:<20} {:<20}\n".format("-----------", "--------------------", "--------------------"))
        for i in range(len(leaf_sizes)):
            f.write("{:<12} {:<20.6f} {:<20.6f}\n".format(leaf_sizes[i], in_sample_rmse[i], out_of_sample_rmse[i]))

def experiment_two(features, target):
    
    # compute how much of the data is training and testing
    train_rows = int(0.6 * features.shape[0])
    train_indices = np.random.choice(features.shape[0], size=train_rows, replace=False)
    test_indices = np.setdiff1d(np.arange(features.shape[0]), train_indices)

    # separate out training and testing data  		  	   		 	 	 		  		  		    	 		 		   		 		  
    train_x = features[train_indices]  		  	   		 	 	 		  		  		    	 		 		   		 		  
    train_y = target[train_indices]  		  	   		 	 	 		  		  		    	 		 		   		 		  
    test_x = features[test_indices]  		  	   		 	 	 		  		  		    	 		 		   		 		  
    test_y = target[test_indices] 

    leaf_sizes = range(1, 100)
    num_bags = 20

    in_sample_rmse_dt = []
    out_of_sample_rmse_dt = [] 
    in_sample_rmse_bl = []
    out_of_sample_rmse_bl = [] 

    for leaf_size in leaf_sizes:
        # DTLearner
        dt_learner = dtl.DTLearner(leaf_size=leaf_size, verbose=False)	
        dt_learner.add_evidence(train_x, train_y)

        # eval in sample
        pred_y = dt_learner.query(train_x)
        rmse_train = math.sqrt(((train_y - pred_y) ** 2).sum() / train_y.shape[0])
        in_sample_rmse_dt.append(rmse_train)

        # eval out of sample
        pred_y = dt_learner.query(test_x)
        rmse_test = math.sqrt(((test_y - pred_y) ** 2).sum() / test_y.shape[0])
        out_of_sample_rmse_dt.append(rmse_test)

        learner_bl = bl.BagLearner(learner=dtl.DTLearner, kwargs={'leaf_size': leaf_size}, bags=num_bags, boost=False, verbose=False)
        learner_bl.add_evidence(train_x, train_y)

        # eval in sample
        pred_y = learner_bl.query(train_x)
        rmse_train = math.sqrt(((train_y - pred_y) ** 2).sum() / train_y.shape[0])
        in_sample_rmse_bl.append(rmse_train)

        # eval out of sample
        pred_y = learner_bl.query(test_x)
        rmse_test = math.sqrt(((test_y - pred_y) ** 2).sum() / test_y.shape[0])
        out_of_sample_rmse_bl.append(rmse_test)

    # Plotting
    plt.figure(figsize=(12, 8))
    plt.plot(leaf_sizes, in_sample_rmse_dt, label='DTLearner In-Sample RMSE', color='orange', linestyle='--')
    plt.plot(leaf_sizes, out_of_sample_rmse_dt, label='DTLearner Out-of-Sample RMSE', color='orange')
    plt.plot(leaf_sizes, in_sample_rmse_bl, label='BagLearner In-Sample RMSE', color='red', linestyle='--')
    plt.plot(leaf_sizes, out_of_sample_rmse_bl, label='BagLearner Out-of-Sample RMSE', color='red')

    plt.title('DTLearner vs. BagLearner RMSE vs Leaf Size (Bags=20)')
    plt.xlabel('leaf_size')
    plt.ylabel('RMSE')
    plt.legend()
    plt.grid(True)
    plt.savefig('images/experiment_2.png', format='png')

def experiment_three(features, target):
    
    # compute how much of the data is training and testing
    train_rows = int(0.6 * features.shape[0])
    train_indices = np.random.choice(features.shape[0], size=train_rows, replace=False)
    test_indices = np.setdiff1d(np.arange(features.shape[0]), train_indices)

    # separate out training and testing data  		  	   		 	 	 		  		  		    	 		 		   		 		  
    train_x = features[train_indices]  		  	   		 	 	 		  		  		    	 		 		   		 		  
    train_y = target[train_indices]  		  	   		 	 	 		  		  		    	 		 		   		 		  
    test_x = features[test_indices]  		  	   		 	 	 		  		  		    	 		 		   		 		  
    test_y = target[test_indices]

    # range and step value of 5
    leaf_sizes = range(1, 101, 5)

    dt_in_sample_mape = []
    dt_out_of_sample_mape = []
    dt_nodes = []

    rt_in_sample_mape = []
    rt_out_of_sample_mape = []
    rt_nodes = []

    for leaf_size in leaf_sizes:
        # DTLearner
        dt_learner = dtl.DTLearner(leaf_size=leaf_size, verbose=False)
        dt_learner.add_evidence(train_x, train_y)

        # calc MAPE & # of node for DTLearner
        dt_pred_train = dt_learner.query(train_x)
        dt_mape_train = np.mean(np.abs((train_y - dt_pred_train) / train_y)) * 100
        dt_in_sample_mape.append(dt_mape_train)
        dt_nodes.append(dt_learner.tree.shape[0])

        dt_pred_test = dt_learner.query(test_x)
        dt_mape_test = np.mean(np.abs((test_y - dt_pred_test) / test_y)) * 100
        dt_out_of_sample_mape.append(dt_mape_test)

        # RTLearner
        rt_learner = rtl.RTLearner(leaf_size=leaf_size, verbose=False)
        rt_learner.add_evidence(train_x, train_y)
        
        # Calculate MAPE and number of nodes for RTLearner
        rt_pred_train = rt_learner.query(train_x)
        rt_mape_train = np.mean(np.abs((train_y - rt_pred_train) / train_y)) * 100
        rt_in_sample_mape.append(rt_mape_train)
        rt_nodes.append(rt_learner.tree.shape[0])

        rt_pred_test = rt_learner.query(test_x)
        rt_mape_test = np.mean(np.abs((test_y - rt_pred_test) / test_y)) * 100
        rt_out_of_sample_mape.append(rt_mape_test)
    
    # Plotting MAPE
    plt.figure(figsize=(10, 6))
    plt.plot(leaf_sizes, dt_out_of_sample_mape, label='DTLearner MAPE', color='blue')
    plt.plot(leaf_sizes, dt_in_sample_mape, label='DTLearner In-Sample MAPE', color='blue', linestyle='--')
    plt.plot(leaf_sizes, rt_out_of_sample_mape, label='RTLearner MAPE', color='red')
    plt.plot(leaf_sizes, rt_in_sample_mape, label='RTLearner In-Sample MAPE', color='red', linestyle='--')
    plt.title('Out-of-Sample MAPE vs. Leaf Size')
    plt.xlabel('Leaf Size')
    plt.ylabel('MAPE (%)')
    plt.legend()
    plt.grid(True)
    plt.savefig('images/experiment_3_mape.png')

    # Plotting number of nodes
    plt.figure(figsize=(10, 6))
    plt.plot(leaf_sizes, dt_nodes, label='DTLearner Nodes', color='blue')
    plt.plot(leaf_sizes, rt_nodes, label='RTLearner Nodes', color='red')
    plt.title('Tree Complexity (Nodes) vs. Leaf Size')
    plt.xlabel('Leaf Size')
    plt.ylabel('Number of Nodes')
    plt.legend()
    plt.grid(True)
    plt.savefig('images/experiment_3_nodes.png')

if __name__ == "__main__":  	
    random.seed(gtid())

    if len(sys.argv) != 2:  		  	   		 	 	 		  		  		    	 		 		   		 		  
        print("Usage: python testlearner.py <filename>")  		  	   		 	 	 		  		  		    	 		 		   		 		  
        sys.exit(1)  		  	   		 	 	 		  		  		    	 		 		   		 		  
    inf = open(sys.argv[1]) 
    data = np.genfromtxt(inf, delimiter=',', skip_header=1)
    
    # selecting all rows, and all columns except the 1st column
    features = data[:, 1:-1]
    target = data[:, -1]

    experiment_one(features, target)
    experiment_two(features, target)
    experiment_three(features, target)