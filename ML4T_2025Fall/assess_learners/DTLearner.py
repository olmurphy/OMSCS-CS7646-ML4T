import numpy as np

class DTLearner(object):
    """
    This is a Decision Tree Learner.

    :param leaf_size: The max number of samples to be aggregated into one leaf
        (i.e., the minimum number of samples required to split a node)
    :type leaf_size: int
    :param verbose: If “verbose” is True, your code can print out information for debugging.
                    If verbose = False your code should not generate ANY output. When we test
                    your code, verbose will be False.
    :type verbose: bool
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

    def _build_tree(self, data):
        """
        Recursively build the decision tree.

        :param data: Combined feature and target values
        :type data: numpy.ndarray
        :return: The decision tree represented as a nested list
        :rtype: list
        """
        # base case 1: # samples <= leaf_size
        if data.shape[0] <= self.leaf_size:
            return np.array([[-1, np.mean(data[:, -1]), np.nan, np.nan]])
        
        # base case 2: all target values same
        if np.all(data[:, -1] == data[0, -1]):
            return np.array([[-1, np.mean(data[:, -1]), np.nan, np.nan]])
        
        num_features = data.shape[1] - 1
        best_feature = -1
        max_abs_corr = -1

        for i in range(num_features):
            feature = data[:, i]
            target = data[:, -1]

            # avoid divizion by zero if feature no variance    
            if np.std(feature) == 0:
                continue
            corr = np.corrcoef(feature, target)[0, 1]

            if abs(corr) > max_abs_corr:
                max_abs_corr = abs(corr)
                best_feature = i

        # no correlation found (all features constant), return leaf w/ mean
        if best_feature == -1:
            return np.array([[-1, np.mean(data[:, -1]), np.nan, np.nan]])
        
        split_val = np.median(data[:, best_feature])

        # case where all avlues same, leading to infinite recursion
        left_data = data[data[:, best_feature] <= split_val]
        right_data = data[data[:, best_feature] > split_val]

        # split creates two non-distinct subsets, create leaft to prevent infinite recursion
        if left_data.shape[0] == 0 or right_data.shape[0] == 0:
            return np.array([[-1, np.mean(data[:, -1]), np.nan, np.nan]])

        left_tree = self._build_tree(left_data)
        right_tree = self._build_tree(right_data)
        
        root = np.array([[best_feature, split_val, 1, left_tree.shape[0] + 1]])

        return np.vstack((root, left_tree, right_tree))

        
    def query(self, points):
        """
        Estimate set of test points given the model we built.

        :param points: A numpy array with each row corresponding to a specific query.
        :type points: numpy.ndarray
        :return: The predicted result of input data according to the trained model
        :rtype: numpy.ndarray
        """

        predictions = np.array([self._query_point(point, 0) for point in points])
        return predictions
    
    def _query_point(self, point, node_idx):
        """
        Recursively query a single point through the decision tree.

        :param point: A single feature vector
        :type point: numpy.ndarray
        :param tree: The decision tree
        :type tree: numpy.ndarray
        :return: The predicted target value for the input point
        :rtype: float
        """
        node = self.tree[node_idx]
        
        # If leaf node, return the prediction
        if node[0] == -1:
            return node[1]
        
        feature_idx = int(node[0])
        split_value = node[1]
        
        if point[feature_idx] <= split_value:
            next_node_idx = node_idx + int(node[2])
        else:
            next_node_idx = node_idx + int(node[3])
        
        return self._query_point(point, next_node_idx)  # Fallback (should not reach here)