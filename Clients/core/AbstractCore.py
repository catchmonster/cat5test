##---------------------------------------------
## PROJECT: Cattest   FILE NAME: AbstractCore
## USER: sasha              PRODUCT: PyCharm
##---------------------------------------------
## 8/18/17:12:20 PM
##---------------------------------------------

import logging

logger = logging.getLogger('mlm.MLCore')

class Core(object):
	"""
	General intake class for lib modules
	"""

	def __init__(self, init=None):
		self.init = init

	def show(self, pyD):
		for k,v in pyD.items():
			logger.info("key : {}\nvalue: {}".format(k,v))
