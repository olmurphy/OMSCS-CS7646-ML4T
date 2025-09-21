import BagLearner as bl
import LinRegLearner as lrl

class InsaneLearner:
    def __init__(self, verbose=False):
        self.learner = bl.BagLearner(learner=bl.BagLearner, kwargs={"learner": lrl.LinRegLearner, "bags": 20}, bags=20, verbose=verbose)

    def add_evidence(self, data_x, data_y):
        self.learner.add_evidence(data_x, data_y)

    def author(self):
        return "omurphy8"

    def query(self, Xtest):
        return self.learner.query(Xtest)
