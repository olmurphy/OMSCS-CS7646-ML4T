import numpy as np  		  	   		 	 	 		  		  		    	 		 		   		 		  
class LinRegLearner(object):  		  	   		 	 	 		  		  		    	 		 		   		 		  
	   		 	 	 		  		  		    	 		 		   		 		  
    def __init__(self, verbose=False):  		  	   		 	 	 		  		  		    	 		 		   		 		  
        pass  # move along, these aren't the drones you're looking for  		  	   		 	 	 		  		  		    	 		 		   		 		  
  		  	   		 	 	 		  		  		    	 		 		   		 		  
    def author(self):  		  	   		 	 	 		  		  		    	 		 		   		 		  
        return "tb34"  # replace tb34 with your Georgia Tech username  		  	   		 	 	 		  		  		    	 		 		   		 		  
  		  	   		 	 	 		  		  		    	 		 		   		 		  
    def add_evidence(self, data_x, data_y):  		  	   		 	 	 		  		  		    	 		 		   		 		  
	 	 	 		  		  		    	 		 		   		 		  
        # slap on 1s column so linear regression finds a constant term  		  	   		 	 	 		  		  		    	 		 		   		 		  
        new_data_x = np.ones([data_x.shape[0], data_x.shape[1] + 1])  		  	   		 	 	 		  		  		    	 		 		   		 		  
        new_data_x[:, 0 : data_x.shape[1]] = data_x  		  	   		 	 	 		  		  		    	 		 		   		 		  
  		  	   		 	 	 		  		  		    	 		 		   		 		  
        # build and save the model  		  	   		 	 	 		  		  		    	 		 		   		 		  
        self.model_coefs, residuals, rank, s = np.linalg.lstsq(  		  	   		 	 	 		  		  		    	 		 		   		 		  
            new_data_x, data_y, rcond=None  		  	   		 	 	 		  		  		    	 		 		   		 		  
        )  		  	   		 	 	 		  		  		    	 		 		   		 		  
  		  	   		 	 	 		  		  		    	 		 		   		 		  
    def query(self, points):  		  	   		 	 	 		  		  		    	 		 		   		 		  
        return (self.model_coefs[:-1] * points).sum(axis=1) + self.model_coefs[  		  	   		 	 	 		  		  		    	 		 		   		 		  
            -1  		  	   		 	 	 		  		  		    	 		 		   		 		  
        ]  		  	   		 	 	 		  		  		    	 		 		   		 		  
  		  	   		 	 	 		  		  		    	 		 		   		 		  
  		  	   		 	 	 		  		  		    	 		 		   		 		  
if __name__ == "__main__":  		  	   		 	 	 		  		  		    	 		 		   		 		  
    print("the secret clue is 'zzyzx'")  		  	   		 	 	 		  		  		    	 		 		   		 		  
