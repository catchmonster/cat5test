##---------------------------------------------
## PROJECT: Dutil   FILE NAME: DynSingleModuleImport
## USER: sasha              PRODUCT: PyCharm
##---------------------------------------------
## 6/8/17:10:14 AM
##---------------------------------------------

from importlib.machinery import SourceFileLoader
import os, logging, sys
import Config as cf
from Nio import nIO
from Timeit import TimeMe


class ModuleSkeleton(object):
	pass

logger = logging.getLogger('dutil.ModuleImport')
class ModuleImport(object):
	"""
		Dynamic import of the module machinery
		There are strict rules on how the classes should be setup...
		"""

	def __init__(self, moduleName, modulePath):
		self.moduleName = moduleName + '.py'
		self.modulePath = modulePath
		self.nio = nIO()
		self.genModLoader = ModuleSkeleton()


	@TimeMe.timeitShort
	def modImport(self):
		## All modules in specific directory import
		logger.info(self.modulePath)
		if self.nio.ifFolderExists(self.modulePath):
			logger.info("Module folder {} exist - "
				            "We will try to load module...".format(self.modulePath))
			module = os.path.join(self.modulePath, self.moduleName)
			try:
				setattr(self.genModLoader, module,
							        SourceFileLoader(module[:-3], module).load_module())
			except Exception as aErr:
				logger.info("Exception raised {}".format(aErr))
				if cf.d: print("Exception raised {}".format(aErr))
		else:
					logger.info("Could not find module path "
					            "{}...".format(self.modulePath))
					logger.info("Bailing out ...")
					if cf.d: print("Could not find module "
					               "{}...".format(self.modulePath))
					sys.exit(1)


	def getModuleMembers(self):
		return self.genModLoader.__dict__

	@TimeMe.timeitShort
	def compareBitwise(self, x, y):
		## if you don't understand this don't program, period ... leave it alone
		## this is very fast way of comparing set of values in two list objects
		## I am using to establish order according to what you put into
		# configuration file check *.txt file for order of libraries ...
		setX = set(x)
		setY = frozenset(y)
		return setY & setX

