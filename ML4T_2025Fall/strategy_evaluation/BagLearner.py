import numpy as np

class BagLearner:
    """
    This is a Bootstrap Aggregation Learner (BagLearner).

    :param learner: Points to any arbitrary learner class that will be used in the BagLearner.
    :type learner: class
    """
    def __init__(self, learner, kwargs = {}, bags = 20, boost = False, verbose = False):
        self.learner = learner
        self.kwargs = kwargs
        self.bags = bags
        self.boost = boost
        self.verbose = verbose
        self.models = []

    def add_evidence(self, data_x, data_y):
        """
        Add training data to learner

        :param data_x: feature set values used to train learner
        :type data_x: numpy.ndarray
        :param data_y: value we try to predict given X data
        :type data_y: numpy.ndarray
        :return: None
        """

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


    def author(self):
        """
        Returns the GT username of the student

        :return: The GT username of the student
        :rtype: str
        """
        return "omurphy8"

    def study_group(self):
        """
        Returns the GT username of the student

        :return: The GT username of the student
        :rtype: str
        """
        return "omurphy8"

    def query(self, points):
        """
        Estimate a set of test points given the model we built.

        :param points: numpy array w/ each row corresponding to specific query.
        :type points: numpy.ndarray
        :return: predicted result of input data according to trained model
        """

        predictions = []
        for model in self.models:
            prediction = model.query(points)
            predictions.append(prediction)

        predictions = np.array(predictions)
        return np.mean(predictions, axis=0)
        