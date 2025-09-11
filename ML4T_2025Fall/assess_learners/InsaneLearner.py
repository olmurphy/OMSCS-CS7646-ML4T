import BagLearner as bl
import LinRegLearner as lrl

class InsaneLearner:
    """
    This is a Insane Learner (InsaneLearner).
    """

    def __init__(self, verbose=False):
        """
        :param verbose: If "verbose" is True, your code can print out information for debugging.
                        If verbose = False your code should not generate ANY output. When we test your code, verbose will be False.
        """
        self.learner = bl.BagLearner(learner=bl.BagLearner, kwargs={"learner": lrl.LinRegLearner, "bags": 20}, bags=20, verbose=verbose)

    def add_evidence(self, data_x, data_y):
        """
        Add training data to learner

        :param data_x: A set of feature values used to train the learner
        :type data_x: numpy.ndarray
        :param data_y: The value we are attempting to predict given the X data
        :type data_y: numpy.ndarray
        """
        self.learner.add_evidence(data_x, data_y)

    def author(self):
        """
        Returns the GT username of the student

        :return: The GT username of the student
        :rtype: str
        """
        return "omurphy8"

    def query(self, Xtest):
        """
        Estimate a set of test points given the model we built.

        :param Xtests: numpy array w/ each row corresponding to specific query.
        :type points: numpy.ndarray
        :return: predicted result of input data according to trained model
        :rtype: numpy.ndarray
        """
        # Implement your prediction logic here
        return self.learner.query(Xtest)
