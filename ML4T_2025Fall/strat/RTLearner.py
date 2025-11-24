import numpy as np
import random

class RTLearner():
    """
    An implementation of a Random Tree (RT) Learner, which is a variation of a Decision Tree.
    """
    def __init__(self, leaf_size=1, verbose=False):
        self.leaf_size = leaf_size
        self.verbose = verbose
        self.tree = None  # Initialize tree structure
    
    def add_evidence(self, data_x, data_y):
        """
        Trains the Random Tree Learner with the provided data.
        """
        # Combine data_x and data_y for easier manipulation
        data = np.hstack((data_x, data_y.reshape(-1, 1)))
        self.tree = self._build_tree(data)

    def _build_tree(self, data):
        def get_mode(arr):
            values, counts = np.unique(arr, return_counts=True)
            if len(values) == 0:
                return 0 # Avoid empty array
            return values[np.argmax(counts)]

        # base case 1: # samples <= leaf_size
        if data.shape[0] <= self.leaf_size:
            return np.array([[-1, np.mean(data[:, -1]), np.nan, np.nan]])
        
        # base case 2: all Y (target) values are the same
        if np.all(data[:, -1] == data[0, -1]):
            return np.array([[-1, data[0, -1], np.nan, np.nan]])
        
        num_features = data.shape[1] - 1

        rand_feature = random.randint(0, num_features - 1)

        # Base case 3: all values in the randomly chosen feature are the same
        if np.all(data[:, rand_feature] == data[0, rand_feature]):
            return np.array([[-1, np.mean(data[:, -1]), np.nan, np.nan]])

        split_val = np.median(data[:, rand_feature])

        # Partition the data
        left_data = data[data[:, rand_feature] <= split_val]
        right_data = data[data[:, rand_feature] > split_val]

        # Base case 4: Split fails to separate data (e.g., all values are equal to the median,
        if left_data.shape[0] == 0 or right_data.shape[0] == 0:
            return np.array([[-1, np.mean(data[:, -1]), np.nan, np.nan]])

        # Recursively build the left and right subtrees
        left_tree = self._build_tree(left_data)
        right_tree = self._build_tree(right_data)
        
        # Calculate the indices for the left and right branches.
        root = np.array([[rand_feature, split_val, 1, left_tree.shape[0] + 1]])

        return np.vstack((root, left_tree, right_tree))

    def query(self, points):
        """
        Estimates a set of point values using the fitted tree.
        """
        # Iterate over each point and query the tree starting from the root (index 0)
        predictions = np.array([self._query_point(point, 0) for point in points])
        return predictions
    
    def _query_point(self, point, node_idx):
        """
        Recursive helper function to traverse the tree for a single point.
        """
        node = self.tree[node_idx]
        
        # Check if it's a leaf node (Feature_Index == -1)
        if node[0] == -1:
            return node[1]
        
        feature_idx = int(node[0])
        split_value = node[1]
        
        if point[feature_idx] <= split_value:
            next_node_idx = node_idx + int(node[2])
        else:
            next_node_idx = node_idx + int(node[3])
        
        return self._query_point(point, next_node_idx)
    
    def author(self):
        return "omurphy8"
    
    def study_group(self):
        return "omurphy8"