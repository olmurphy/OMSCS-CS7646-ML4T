import numpy as np

class RTLearner():
    """
    This is a Random Tree Learner (RTLearner)

    :param leaf_size: Is the number of samples required for a potential split
    :type leaf_size: int
    :param verbose: If “verbose” is True, your code can print out information for debugging.
                    If verbose = False your code should not generate ANY output. When we test
                    your code, verbose will be False.
    """

    def __init__(self, leaf_size=1, verbose=False):
        """
        Constructor method

        :param leaf_size: The maximum number of samples to be aggregated into one leaf
            (i.e., the minimum number of samples required to split a node)
        :type leaf_size: int
        :param verbose: If “verbose” is True, your code can print out information for debugging.
            If verbose = False your code should not generate ANY output. When we test your code, verbose will be False.
        :type verbose: bool
        """
        self.leaf_size = leaf_size
        self.verbose = verbose
        self.tree = None  # Initialize tree structure

    def author(self):
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
    
    def add_evidence(self, data_x, data_y):
        """
        Add train data to learner

        :param data_x: A set of feature values used to train the learner
        :type data_x: numpy.ndarray
        :param data_y: The value we are attempting to predict given the X data
        :type data_y: numpy.ndarray
        """
        # Combine data_x and data_y for easier manipulation
        data = np.hstack((data_x, data_y.reshape(-1, 1)))
        self.tree = self._build_tree(data)

    def query(self, points):
        """
        Estimate set of test points given the model we built.

        :param points: A numpy array with each row corresponding to a specific query.
        :type points: numpy.ndarray
        :return: The predicted result of input data according to the trained model
        :rtype: numpy.ndarray
        """
        
        # TODO: Placeholder implementation
        if self.tree is None:
            raise ValueError("The model has not been trained yet. Please call add_evidence first.")
        
        # For demonstration purposes, return zeros
        return np.zeros(points.shape[0])

# class RTLearner.RTLearner(leaf_size=1, verbose=False)

#     This is a Random Tree Learner (RTLearner). You will need to properly implement this class as necessary.

#     Parameters
#         leaf_size (int)  - Is the number of samples required for a potential split
#         verbose (bool)   - If “verbose” is True, your code can print out information for debugging.
#                            If verbose = False your code should not generate ANY output. When we test your code, verbose will be False.

#     add_evidence(data_x, data_y)

#         Add training data to learner

#         Parameters
#             data_x (numpy.ndarray) – A set of feature values used to train the learner
#             data_y (numpy.ndarray) – The value we are attempting to predict given the X data


#     author()

#         Returns
#             The GT username of the student

#         Return type
#             str

#      study_group()
    
#         Returns
#             A comma separated string of GT_Name of each member of your study group
#             # Example: "gburdell3, jdoe77, tbalch7" or "gburdell3" if a single individual working alone

#         Return type
#             str
 
#     query(points)

#         Estimate a set of test points given the model we built.

#         Parameters
#             points (numpy.ndarray) – A numpy array with each row corresponding to a specific query.

#         Returns
#             The predicted result of the input data according to the trained model

#         Return type
#             numpy.ndarray