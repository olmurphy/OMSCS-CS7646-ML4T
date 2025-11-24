import numpy as np

class BagLearner:
    """
    This is a Bootstrap Aggregation Learner (BagLearner).
    """
    def __init__(self, learner, kwargs = {}, bags = 20, boost = False, verbose = False):
        self.learner = learner
        self.kwargs = kwargs
        self.bags = bags
        self.boost = boost
        self.verbose = verbose
        self.models = []

    def add_evidence(self, data_x, data_y):
        # numb data points n
        n = data_x.shape[0]

        self.models = []
        
        for _ in range(self.bags):
            # new learner and add it to list
            new_learner = self.learner(**self.kwargs)
            self.models.append(new_learner)

            # bootstrap sample of data w/ replacement
            bag_indices = np.random.choice(n, size=n, replace=True)

            bag_x = data_x[bag_indices]
            bag_y = data_y[bag_indices]

            new_learner.add_evidence(bag_x, bag_y)

    def query(self, points):
        predictions = []
        for model in self.models:
            prediction = model.query(points)
            predictions.append(prediction)

        predictions = np.array(predictions)


        mean_predictions = np.mean(predictions, axis=0)
        return mean_predictions

    def author(self):
        return "omurphy8"

    def study_group(self):
        return "omurphy8"