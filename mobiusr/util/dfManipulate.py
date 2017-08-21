##---------------------------------------------
## PROJECT: dutil   FILE NAME: dfManipulate
## USER: sasha              PRODUCT: PyCharm
##---------------------------------------------
## 4/28/17:9:33 AM
##---------------------------------------------


import logging
import Config as cf
from Timeit import TimeMe

logger = logging.getLogger('dutil.DFmanipulate')
class DFmanipulate(object):
	"""
	Some hacks to manipulate dataframe for ML
	"""
	def __init__(self, df):
		if not df.empty:
			self.df = df
			self.ndf = None
		else:
			if cf.d: print("Data Frame missing...")

	@TimeMe.timeitShort
	def removeBadRecords(self, reject):
		self.ndf = self.ndf.drop(reject)
		if len(reject) != 0:
			self.ndf.reset_index
		else:
			if cf.d: print("Data frame not reindexed... "
			               "No bad records encountered!")
			logger.info("Data frame not reindexed... "
			               "No bad records encountered!")

	@TimeMe.timeitShort
	def deleteDF(self):
		try:
			del self.df
		except RuntimeError as rtErr:
			logger.info("Data Frame removal faield!")
			if cf.d: print("Data Frame removal faield!")

	@TimeMe.timeitShort
	def extractDFbyColumnLabel(self, columnList):
		self.ndf = self.df.loc[:,columnList]

	def getNDF(self):
		return self.ndf
