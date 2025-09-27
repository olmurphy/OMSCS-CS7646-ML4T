import numpy as np
class DTLearner(object):

    def __init__(self, leaf_size=1, verbose=False):
        self.leaf_size = leaf_size
        self.verbose = verbose
        self.tree = None  # Initialize tree structure

    def author(self):
        return "omurphy8"
    
    def study_group(self):
        return "omurphy8"

    def add_evidence(self, data_x, data_y):
        # Combine data_x and data_y for easier manipulation
        data = np.hstack((data_x, data_y.reshape(-1, 1)))
        self.tree = self._build_tree(data)

    def _build_tree(self, data):
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
        predictions = np.array([self._query_point(point, 0) for point in points])
        return predictions
    
    def _query_point(self, point, node_idx):
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