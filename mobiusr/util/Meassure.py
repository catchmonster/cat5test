##---------------------------------------------
## PROJECT: dutil   FILE NAME: Meassure
## USER: sasha              PRODUCT: PyCharm
##---------------------------------------------
## 4/28/17:9:35 AM
##---------------------------------------------

import logging
import Config as cf
from Timeit import TimeMe

logger = logging.getLogger('dutil.Accuracy')
class Accuracy():

	def __init__(self, trainTestInstance, *args):
		logger.info("""
Why can’t you train your machine learning algorithm on your dataset and use predictions from
this same dataset to evaluate machine learning algorithms? The simple answer is overfitting.
Imagine an algorithm that remembers every observation it is shown during training. If you
evaluated your machine learning algorithm on the same dataset used to train the algorithm, then
an algorithm like this would have a perfect score on the training dataset. But the predictions it
made on new data would be terrible. We must evaluate our machine learning algorithms on
data that is not used to train the algorithm. The evaluation is an estimate that we can use to
talk about how well we think the algorithm may actually do in practice. It is not a guarantee
of performance. Once we estimate the performance of our algorithm, we can then re-train the final
algorithm on the entire training dataset and get it ready for operational use. Next up we are
going to look at four different techniques that we can use to split up our training dataset and
create useful estimates of performance for our machine learning algorithms:

Train and Test Sets.
k-fold Cross Validation.
Leave One Out Cross Validation.
Repeated Random Test-Train Splits.
		""")

		self.tti = trainTestInstance
		self.inputArrays = args

	@TimeMe.timeitShort
	def setupTrainTestSplit(self, test_size = 0, seed = 1):
		res = self.tti(*self.inputArrays, test_size=test_size, random_state = seed)
		return res

	@TimeMe.timeitShort
	def setupKFold(self, nSplits = 0, randomState = 0):
		res = self.tti(n_splits=nSplits, random_state=randomState)
		return res

	@TimeMe.timeitShort
	def score(self, impModule, *args):
		return impModule.score(*args)

	@TimeMe.timeitShort
	def crossValScore(self, model, cv):
		return self.tti(model, *self.inputArrays, cv=cv)