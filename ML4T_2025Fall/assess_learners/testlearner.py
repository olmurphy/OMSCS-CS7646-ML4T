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
  		  	   		 	 	 		  		  		    	 		 		   		 		  
import numpy as np  		
import matplotlib.pyplot as plt	   		 	 	 		  		  		    	 		 		   		 		  
  		  	   		 	 	 		  		  		    	 		 		   		 		  
import LinRegLearner as lrl
import DTLearner as dtl

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

if __name__ == "__main__":  		  	   		 	 	 		  		  		    	 		 		   		 		  
    if len(sys.argv) != 2:  		  	   		 	 	 		  		  		    	 		 		   		 		  
        print("Usage: python testlearner.py <filename>")  		  	   		 	 	 		  		  		    	 		 		   		 		  
        sys.exit(1)  		  	   		 	 	 		  		  		    	 		 		   		 		  
    inf = open(sys.argv[1]) 
    data = np.genfromtxt(inf, delimiter=',', skip_header=1)
    
    # selecting all rows, and all columns except the 1st column
    features = data[:, 1:-1]
    target = data[:, -1]

    experiment_one(features, target)

    # compute how much of the data is training and testing
    train_rows = int(0.6 * features.shape[0])
    train_indices = np.random.choice(features.shape[0], size=train_rows, replace=False)

    # this does a left join, return indices not in train_indices
    test_indices = np.setdiff1d(np.arange(features.shape[0]), train_indices)

    # separate out training and testing data  		  	   		 	 	 		  		  		    	 		 		   		 		  
    train_x = features[train_indices]  		  	   		 	 	 		  		  		    	 		 		   		 		  
    train_y = target[train_indices]  		  	   		 	 	 		  		  		    	 		 		   		 		  
    test_x = features[test_indices]  		  	   		 	 	 		  		  		    	 		 		   		 		  
    test_y = target[test_indices]  

    print(f"{test_x.shape}")  		  	   		 	 	 		  		  		    	 		 		   		 		  
    print(f"{test_y.shape}")

    # create a learner and train it  		  	   		 	 	 		  		  		    	 		 		   		 		  
    # learner = lrl.LinRegLearner(verbose=True)  # create a LinRegLearner  
    learner = dtl.DTLearner(leaf_size=1, verbose=False)  # create a DTLearner	
     		  		    	 		 		   		 		  
    learner.add_evidence(train_x, train_y)  # train it  		  	   		 	 	 		  		  		    	 		 		   		 		  
    print(learner.author())  		  	   		 	 	 		  		  		    	 		 		   		 		  
  		  	   		 	 	 		  		  		    	 		 		   		 		  
    # evaluate in sample  		  	   		 	 	 		  		  		    	 		 		   		 		  
    pred_y = learner.query(train_x)  # get the predictions  		  	   		 	 	 		  		  		    	 		 		   		 		  
    rmse = math.sqrt(((train_y - pred_y) ** 2).sum() / train_y.shape[0])  		  	   		 	 	 		  		  		    	 		 		   		 		  
    print()  		  	   		 	 	 		  		  		    	 		 		   		 		  
    print("In sample results")  		  	   		 	 	 		  		  		    	 		 		   		 		  
    print(f"RMSE: {rmse}")  		  	   		 	 	 		  		  		    	 		 		   		 		  
    c = np.corrcoef(pred_y, y=train_y)  		  	   		 	 	 		  		  		    	 		 		   		 		  
    print(f"corr: {c[0,1]}")  		  	   		 	 	 		  		  		    	 		 		   		 		  
  		  	   		 	 	 		  		  		    	 		 		   		 		  
    # evaluate out of sample  		  	   		 	 	 		  		  		    	 		 		   		 		  
    pred_y = learner.query(test_x)  # get the predictions  		  	   		 	 	 		  		  		    	 		 		   		 		  
    rmse = math.sqrt(((test_y - pred_y) ** 2).sum() / test_y.shape[0])  		  	   		 	 	 		  		  		    	 		 		   		 		  
    print()  		  	   		 	 	 		  		  		    	 		 		   		 		  
    print("Out of sample results")  		  	   		 	 	 		  		  		    	 		 		   		 		  
    print(f"RMSE: {rmse}")  		  	   		 	 	 		  		  		    	 		 		   		 		  
    c = np.corrcoef(pred_y, y=test_y)  		  	   		 	 	 		  		  		    	 		 		   		 		  
    print(f"corr: {c[0,1]}")  		  	   		 	 	 		  		  		    	 		 		   		 		  

