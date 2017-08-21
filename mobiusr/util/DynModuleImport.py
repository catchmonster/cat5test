##---------------------------------------------
## PROJECT: dutil   FILE NAME: DynModuleImport
## USER: sasha              PRODUCT: PyCharm
##---------------------------------------------
## 4/28/17:9:33 AM
##---------------------------------------------

from importlib.machinery import SourceFileLoader
import os, logging, sys
import Config as cf
from Nio import nIO
from Timeit import TimeMe

class IterMixin(object):
	def __iter__(self):
		for attr, value in self.__dict__.items():
			yield attr, value


logger = logging.getLogger('dutil.ModuleSkeleton')
class ModuleSkeleton(IterMixin):
	pass

logger = logging.getLogger('dutil.ModuleImport')
class ModuleImport(object):
	"""
	Dynamic import of the module machinery
	There are strict rules on how the classes should be setup...
	"""

	def __init__(self, modObj, thisArgs):
		self.module = modObj
		self.thisArgs = thisArgs
		self.nio = nIO()
		self.modules = list()
		self.genModLoader = ModuleSkeleton()
		self.module.fullNames = list()
		for name in self.module.names:
			self.module.fullNames.append(name + self.module.ext)

	@TimeMe.timeitShort
	def modImport(self):
		## All modules in specific directory import
		logger.info(self.module.modulePath)
		if self.nio.ifFolderExists(self.module.modulePath):
			if self.module.libsVersion == self.thisArgs.projectVersion:
				logger.info("Version modules folder {} exist - "
					"We will try to load all modules...".format(
					self.thisArgs.projectVersion))
				if cf.d: print("Version modules folder {} exist - "
					"We will try to load all modules...".format(
					self.thisArgs.projectVersion))
				moduleABSPath = os.path.join(self.module.modulePath,
					self.module.libsVersion)
				self.modules = [f for f in
					os.listdir(moduleABSPath)
					if os.path.isfile(os.path.join(moduleABSPath, f))]

				if len(self.modules) != 0:
					modules =  self.compareBitwise(self.modules, self.module.fullNames)
					logger.info("Sorted list of dynamic modules... {}".format(modules))
					if cf.d: print("Sorted list of dynamic modules... {}".format(modules))
					for imodule in modules:
						try:
							##setattr(self.genModLoader, 'n'+imodule, imodule)
							setattr(self.genModLoader, imodule,
								SourceFileLoader(imodule[:-3],
								os.path.join(moduleABSPath, imodule)).load_module())
						except Exception as aErr:
							logger.info("Exception raised {}".format(aErr))
							if cf.d: print("Exception raised {}".format(aErr))
				else:
					logger.info("There is no modules in this version of project "
					            "{}...".format(moduleABSPath))
					logger.info("Bailing out ...")
					if cf.d: print("There is no modules in this version of project "
					                "{}...".format(moduleABSPath))
					sys.exit(1)

			else:
				logger.info("""This version of dynamic modules ether does not exist 
				or specified configuration is mismatched: \nConfig version is: {}
				\nModule version argument is {}""".format(self.module.libsVersion,
				self.thisArgs.projectVersion))

				logger.info("Bailing out...")
				if cf.d: print("""This version of dynamic modules ether does not exist 
				or specified configuration is mismatched: \nConfig version is: {}
				\nModule version argument is {}""".format(self.module.libsVersion,
				self.thisArgs.projectVersion))
				sys.exit(1)
		else:
			logger.info('Module absolut path {} is incorrect or it does not '
			'exists!'.format(self.module.modulePath))
			if cf.d: print('Module absolut path {} is incorrect or it does not '
			'exists!'.format(self.module.modulePath))
			logger.info("Bailing out...")
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

