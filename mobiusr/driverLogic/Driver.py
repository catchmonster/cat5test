##---------------------------------------------
## PROJECT: dutil   FILE NAME: Driver
## USER: sasha              PRODUCT: PyCharm
##---------------------------------------------
## 4/28/17:9:24 AM
##---------------------------------------------

import logging, sys
from LightUtil import aConfigParser
from Nio import nIO
from DynModuleImport import ModuleImport
import Config as cf
import ast, time
from collections import OrderedDict
from Timeit import TimeMe



class IterMixin(object):
	def __iter__(self):
		for attr, value in self.__dict__.items():
			yield attr, value


logger = logging.getLogger('dutil.DriverLogic')
class DriverLogic(object):
	"""
	General bussines logic resides here
	"""

	def __init__(self, thisApp, thisArgs, projectConf):

		self.thisApp = thisApp
		self.thisArgs = thisArgs
		self.projectConf = projectConf
		self.nio = nIO()
		self.project = thisApp.PROJECTS
		self.app = None
		self.genRes = None
		self.nio = nIO()
		self.runTest = None
		self.mObject = type('moduleObject', (object,), {})()
		self.apps = type('appObject', (IterMixin,), {})()
		self.runInstances = dict()
		self.objectInstances = list()
		self.staticModList = list()

	@TimeMe.timeitShort
	def processConf(self):
		appConfig = aConfigParser()
		appSections = appConfig.read(self.projectConf)
		self.app = appConfig.getObjectMapper(appSections)

		## get a object attribs for all clients apps.A, apps.B ...
		appList = [a for a in dir(self.app.CLIENTS) if not a.startswith(('__','get','set'))]
		for app in appList:
			opt = ast.literal_eval(getattr(self.app.CLIENTS,app))
			##setattr(self.apps, app, app)
			setattr(self.apps, app, opt)
		## construct module object names attribs for libraries lib1Client lib2Client
		self.mObject.names = ast.literal_eval(self.app.Modules.libs)
		## construct module object extensions attribs
		self.mObject.ext = self.app.Modules.ext
		## construct module object paths attribs
		self.mObject.modulePath = self.app.Modules.libsPath
		## construct module object paths attribs
		self.mObject.libsVersion = self.app.Modules.libsVersion
		## construct module object calss attribs
		self.mObject.klass = self.app.Modules.klass


	@TimeMe.timeitShort
	def loadModules(self):
		logger.info('Importing dynamically modules {}'.format(self.mObject.names))
		## provide to class configuration specified in runtime
		## load import harness
		dm = ModuleImport(self.mObject, self.thisArgs)
		try:
			## get all modules paths and classNames
			dm.modImport()
		except AttributeError as atrErr:
			if cf.d: print("Error occured - {}".format(atrErr))
			logger.info("Error occured - {}".format(atrErr))
		try:
			## get the dictionary of plugin modules
			mods = dm.getModuleMembers()
			apps = dict(self.apps)
			for instanceName, module in mods.items():
				for name, opts in apps.items():
					if instanceName[:-3] == name:
						self.runInstances[instanceName] = [module,opts]
		except AttributeError as atrErr:
			if cf.d: print("Error occured - {}".format(atrErr))
			logger.info("Error occured - {}".format(atrErr))


	def getConfObj(self):
		return (self.app, self.genRes, self.ws)


	####@TimeMe.timeitShort
	def sortRunInstances(self, rawScanOfInstances):
		d = OrderedDict()
		for el in self.staticModList:
			if el in rawScanOfInstances:
					d[el] = rawScanOfInstances[el]
		return d

	@TimeMe.timeitShort
	def run(self):
		"""
		Load one or more dynamically loaded modules
		"""
		klass = OrderedDict()
		self.staticModList = list()
		aKlasses = self.mObject.klass.split()
		for name in ast.literal_eval(self.app.Modules.libs):
			self.staticModList.append(name + self.app.Modules.ext)

		runInstances = self.sortRunInstances(self.runInstances)
		fullRunInstance = dict()

		for instanceName, instanceModule, in runInstances.items():
			##instantiate classes
			for aKlass in aKlasses:
				if aKlass in [a for a in dir(instanceModule[0]) if not a.startswith('__')]:
					print('Loading Class {} of module {} with configuration {}'.format
		      	(aKlass, instanceName, instanceModule[1]))

					try:
						klass[instanceName[:-3]] = [getattr(instanceModule[0], aKlass), instanceModule[1]]
					except AttributeError as attrErr:
						if cf.d: print(attrErr)
						pass

		for module, runKlass in klass.items():
			klass[module]=runKlass[0](init=runKlass[1])

		self.runAll(klass)

	@TimeMe.timeitShort
	def runAll(self, klass):
		## run them all
		for module, objInstance in klass.items():
			logger.info("Running object instance {} of module {}".format(objInstance, module))
			objInstance.run()














