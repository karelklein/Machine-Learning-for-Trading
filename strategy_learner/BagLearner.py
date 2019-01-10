''' 
author: Karel Klein Cardena
userID: kkc3 
'''
import numpy as np
from scipy.stats import mode

class BagLearner(object):
	def __init__(self, learner, kwargs, bags, boost=False, verbose=False):
		self.learner = learner
		self.bags = bags
		self.boost = boost
		self.verbose = verbose

		self.learners = []
		for i in range(self.bags):
			self.learners.append(self.learner(**kwargs))

	def author(self):
		return 'kkc3'

	def addEvidence(self, dataX, dataY):
		for l in self.learners:
			randoms = np.random.randint(0, dataX.shape[0], dataX.shape[0])
			sampleX = dataX[randoms]
			sampleY = dataY[randoms]
			l.addEvidence(sampleX, sampleY)

	def query(self, xtest):
		pred = []
		if xtest.ndim == 1: num_rows = 1
		else: num_rows = xtest.shape[0]

		for l in self.learners:
			pred.append(l.query(xtest))
		# return np.sum(np.array(pred), axis=0) / self.bags
		return mode(pred)[0][0]
