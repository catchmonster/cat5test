##---------------------------------------------
## PROJECT: Cattest   FILE NAME: AbstractCore
## USER: sasha              PRODUCT: PyCharm
##---------------------------------------------
## 8/18/17:12:20 PM
##---------------------------------------------

import logging
from LightUtil import aConfigParser
from collections import OrderedDict as od


class IterMixin(object):
	def __iter__(self):
		for attr, value in self.__dict__.items():
			yield attr, value



logger = logging.getLogger('cattest.MLCore')
class Core(object):
	"""
	General intake class for lib modules
	"""

	def __init__(self, init=None):

		self.init = init
		self.conf = None
		self.users = list()
		self.roles = list()
		self.groups = list()
		self.permissions = list()
		self.attestDataContainer = od()
		##self.genObj = type('genObject', (IterMixin,), {})()

		self.processConf()



	def processConf(self):
		appConfig = aConfigParser()
		appSections = appConfig.read(self.init)
		self.conf = appConfig.getObjectMapper(appSections)
		self.xml = self.conf.XML

	def getUsers(self): return self.users
	def	getRoles(self):	return self.roles
	def getGroups(self):	return self.groups
	def getXMLGenData(self): return self.xml
	def getPermissions(self): return self.permissions

	def getAttestationData(self):
		self.attestDataContainer['users'] = self.getUsers()
		self.attestDataContainer['roles'] = self.getRoles()
		self.attestDataContainer['groups'] = self.getGroups()
		self.attestDataContainer['permissions'] = self.getPermissions()
		return (self.attestDataContainer, self.getXMLGenData())