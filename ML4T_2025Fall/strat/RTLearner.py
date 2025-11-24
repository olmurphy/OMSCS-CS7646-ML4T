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

        :param data_x: The training data features as a numpy array.
        :type data_x: numpy.ndarray
        :param data_y: The training data target values as a numpy array.
        :type data_y: numpy.ndarray
        """
        # Combine data_x and data_y for easier manipulation
        # data format: [feature_1, feature_2, ..., feature_N, Y_value]
        data = np.hstack((data_x, data_y.reshape(-1, 1)))
        self.tree = self._build_tree(data)

    def _build_tree(self, data):
        # Helper function: compute the mode (used to be in a previous version, kept for reference)
        def get_mode(arr):
            # arr is the array of Y values
            values, counts = np.unique(arr, return_counts=True)
            if len(values) == 0:
                return 0 # Avoid empty array
            # Return the value with the highest count
            return values[np.argmax(counts)]

        # base case 1: # samples <= leaf_size
        # The node becomes a leaf, the prediction is the mean of the Y values in the data
        if data.shape[0] <= self.leaf_size:
            # Structure: [-1 (leaf marker), prediction_value, NaN, NaN]
            return np.array([[-1, np.mean(data[:, -1]), np.nan, np.nan]])
        
        # base case 2: all Y (target) values are the same
        # The node becomes a leaf, the prediction is that common Y value
        if np.all(data[:, -1] == data[0, -1]):
            # Structure: [-1 (leaf marker), prediction_value, NaN, NaN]
            return np.array([[-1, data[0, -1], np.nan, np.nan]])
        
        num_features = data.shape[1] - 1

        # Randomly select a feature index to split on (RT key step)
        rand_feature = random.randint(0, num_features - 1)

        # Base case 3: all values in the randomly chosen feature are the same
        if np.all(data[:, rand_feature] == data[0, rand_feature]):
            # The node becomes a leaf, the prediction is the mean of the Y values
            return np.array([[-1, np.mean(data[:, -1]), np.nan, np.nan]])

        # The split value is the median of the chosen feature's values (RT key step)
        split_val = np.median(data[:, rand_feature])

        # Partition the data
        left_data = data[data[:, rand_feature] <= split_val]
        right_data = data[data[:, rand_feature] > split_val]

        # Base case 4: Split fails to separate data (e.g., all values are equal to the median,
        # leading to one empty set and causing infinite recursion).
        if left_data.shape[0] == 0 or right_data.shape[0] == 0:
            # Create a leaf node with the mean of the current data's Y values
            return np.array([[-1, np.mean(data[:, -1]), np.nan, np.nan]])

        # Recursively build the left and right subtrees
        left_tree = self._build_tree(left_data)
        right_tree = self._build_tree(right_data)
        
        # Calculate the indices for the left and right branches.
        # Structure of a non-leaf node: [Feature_Index, Split_Value, Left_Tree_Size (1), Right_Tree_Size (left_tree.shape[0] + 1)]
        root = np.array([[rand_feature, split_val, 1, left_tree.shape[0] + 1]])

        # Combine the current node (root) with the subtrees vertically
        return np.vstack((root, left_tree, right_tree))

    def query(self, points):
        """
        Estimates a set of point values using the fitted tree.

        :param points: A numpy array of test data features.
        :type points: numpy.ndarray
        :return: A numpy array of predicted values.
        :rtype: numpy.ndarray
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
            # If leaf, return the prediction value (node[1])
            return node[1]
        
        # Not a leaf, check the split condition
        feature_idx = int(node[0])
        split_value = node[1]
        
        if point[feature_idx] <= split_value:
            # Move to the left child (index current + 1)
            next_node_idx = node_idx + int(node[2])
        else:
            # Move to the right child (index current + 1 + size_of_left_tree)
            next_node_idx = node_idx + int(node[3])
        
        # Recursively call the query on the next node
        return self._query_point(point, next_node_idx)
    
    def author(self):
        return "omurphy8"
    
    def study_group(self):
        return "omurphy8"