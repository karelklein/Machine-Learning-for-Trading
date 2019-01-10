import BagLearner as bl
import LinRegLearner as lrl
import numpy as np

class InsaneLearner(object):
    def __init__(self, verbose=False):
        self.verbose = verbose
        self.learners = []
        for i in range(20):
            self.learners.append(bl.BagLearner(learner=lrl.LinRegLearner, kwargs={}, bags=20, boost=False, verbose=False))

    def author(self): print 'kkc3'

    def addEvidence(self, dataX, dataY):
        for learner in self.learners: learner.addEvidence(dataX, dataY)

    def query(self, xtest):
        preds = [learner.query(xtest) for learner in self.learners]
        return np.mean(np.array(preds), axis=0)
