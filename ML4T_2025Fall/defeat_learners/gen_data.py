""""""  		  	   		 	 	 		  		  		    	 		 		   		 		  
"""  		  	   		 	 	 		  		  		    	 		 		   		 		  
template for generating data to fool learners (c) 2016 Tucker Balch  		  	   		 	 	 		  		  		    	 		 		   		 		  
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
  		  	   		 	 	 		  		  		    	 		 		   		 		  
Student Name: Tucker Balch (replace with your name)  		  	   		 	 	 		  		  		    	 		 		   		 		  
GT User ID: tb34 (replace with your User ID)  		  	   		 	 	 		  		  		    	 		 		   		 		  
GT ID: 900897987 (replace with your GT ID)  		  	   		 	 	 		  		  		    	 		 		   		 		  
"""  		  	   		 	 	 		  		  		    	 		 		   		 		  
  		  	   		 	 	 		  		  		    	 		 		   		 		  
import math  		  	   		 	 	 		  		  		    	 		 		   		 		  
  		  	   		 	 	 		  		  		    	 		 		   		 		  
import numpy as np  
import random		  	   		 	 	 		  		  		    	 		 		   		 		  
  		  	   		 	 	 		  		  		    	 		 		   		 		  
  		  	   		 	 	 		  		  		    	 		 		   		 		  
# this function should return a dataset (X and Y) that will work  		  	   		 	 	 		  		  		    	 		 		   		 		  
# better for linear regression than decision trees  		  	   		 	 	 		  		  		    	 		 		   		 		  
def best_4_lin_reg(seed=1489683273):  		  	   		 	 	 		  		  		    	 		 		   		 		  	 	 	 		  		  		    	 		 		   		 		  
    np.random.seed(seed)
    random.seed(seed)
    
    n_samples = 100
    n_features = 5

    X = np.random.uniform(-5.0, 5.0, size=(n_samples, n_features))

    # initalize weights and biases
    weights = np.array([1.5, -0.8, 3.0, 0.2, -4.5])
    bias = 10.0

    # linear combination of inputs + noise
    y_lin = X @ weights + bias

    noise = np.random.normal(0, 0.1, size=n_samples)
    Y = y_lin + noise

    return X, Y	  	   		 	 	 		  		  		    	 		 		   		 		  
  		  	   		 	 	 		  		  		    	 		 		   		 		  
  		  	   		 	 	 		  		  		    	 		 		   		 		  
def best_4_dt(seed=1489683273):  		  	   		 	 	 		  		  		    	 		 		   		 		   		  	   		 	 	 		  		  		    	 		 		   		 		  
    np.random.seed(seed)
    random.seed(seed)

    n_samples = 100
    n_features = 5

    X = np.random.uniform(-5.0, 5.0, size=(n_samples, n_features))

    Y = np.zeros(n_samples)

    # set up piecewise function, with split at x= -2.0
    Y[X[:, 0] < -2.0] = 70.0  
    Y[X[:, 0] >= -2.0] = -20.0

    # small gaussian noise
    noise = np.random.normal(0, 0.1, size=n_samples)
    Y = Y + noise

    return X, Y  	   		 	 	 		  		  		    	 		 		   		 		  
  		  	   		 	 	 		  		  		    	 		 		   		 		  
def author():  		  	   		 	 	 		  		  		    	 		 		   		 		  
    """  		  	   		 	 	 		  		  		    	 		 		   		 		  
    :return: The GT username of the student  		  	   		 	 	 		  		  		    	 		 		   		 		  
    :rtype: str  		  	   		 	 	 		  		  		    	 		 		   		 		  
    """  		  	   		 	 	 		  		  		    	 		 		   		 		  
    return "omurphy8"

def study_group(self):
    """
    Returns
        A comma separated string of GT_Name of each member of your study group
        # Example: "gburdell3, jdoe77, tbalch7" or "gburdell3" if a single individual working alone
    """
    return "omurphy8"


if __name__ == "__main__":  		  	   		 	 	 		  		  		    	 		 		   		 		  
    print("they call me Tim.")  		  	   		 	 	 		  		  		    	 		 		   		 		  
