##---------------------------------------------
## PROJECT: dutil   FILE NAME: LightUtil
## USER: sasha              PRODUCT: PyCharm
##---------------------------------------------
## 4/28/17:9:34 AM
##---------------------------------------------

import configparser
import os, logging
from collections import namedtuple
import Config as cf
from Timeit import TimeMe
from collections import OrderedDict
from ast import literal_eval as astEval



logger = logging.getLogger('dutil.MultiOrderedDict')


class MultiOrderedDict(OrderedDict):
	""" Special class for handeling duplicate keys
	from config parser
	"""

	def __setitem__(self, key, value):
		if isinstance(value, list) and key in self:
			self[key].extend(value)
		else:
			super(OrderedDict, self).__setitem__(key, value)




logger = logging.getLogger('dutil.LightGenObjWrapper')
class LightGenObjWrapper(object):
	""" Class dynamically mapps configuration key|value pairs to object attributes
		We are using configparser to parse configurations
	"""

	def __init__(self):
		pass

	def getAppConfig(self):
		return self.__config

	def setAppConfig(self, config):
		self.__config = config


logger = logging.getLogger('dutil.aConfigParser')
class aConfigParser(object):
	""" Simple wrapper for ConfigParser
	"""

	def __init__(self, type=None):
		self.type = type
		if type:
			self.cpRaw = configparser.RawConfigParser(dict_type=MultiOrderedDict, strict=False)
		else:
			self.cp = configparser.ConfigParser(interpolation=configparser.ExtendedInterpolation(), strict=False)
			## Nice hack to get INI options in case sensitive matter
			self.cp.optionxform = str

		## setup configparser object
		##self.cp = configparser.ConfigParser(interpolation = configparser.ExtendedInterpolation())

	@TimeMe.timeitShort
	def read(self, ini):
		## read conf files
		if os.path.exists(ini):
			try:
				self.cp.read(ini)
			except configparser.Error as cpErr:
				logger.info("Exception raised: {}".format(cpErr))
				if cf.d: print("Exception raised: {}".format(cpErr))
		else:
			logger.info("Configuration file missing {}".format(ini))
			if cf.d: print("Configuration file missing {}".format(ini))

		sec = self.cp.sections()
		logger.info("Configuration file sections are: {}".format(sec))
		if cf.d: print("Configuration file sections are: {}".format(sec))

		return sec

	@TimeMe.timeitShort
	def readRaw(self, ini):
		## read conf files
		if os.path.exists(ini):
			self.cpRaw.read(ini)
		else:
			logger.info("Configuration file missing {}".format(ini))
			if cf.d: print("Configuration file missing {}".format(ini))



	@TimeMe.timeitShort
	def dsectionMapper(self, section):
		## Dict mapper for conf sections
		opts = {}
		options = self.cp.options(section)
		for el in options:
			try:
				opts[el] = self.cp.get(section, el)
				if opts[el] == -1:
					logger.info("Skipping: {}".foramt(opts))
					if cf.d: print("Skipping: {}".foramt(opts))
			except:
				logger.info("Exception raised {}!".format(opts))
				if cf.d: print("Exception raised {}!".format(opts))
				opts[opts] = None
		return opts

	@TimeMe.timeitShort
	def tsectionMapper(self, section):
		## Named Tuple mapper for conf sections

		fields = list()
		values = list()

		options = self.cp.options(section)
		for el in options:
			try:
				fields.append(el)
				values.append(self.cp.get(section, el))
			except:
				logger.info("Exception raised {}!".format(el))
				if cf.d: print("Exception raised {}!".format(el))

		try:
			opts = namedtuple('section', fields)
			mapper = opts(*tuple([v for v in values]))
		except RuntimeWarning as rtWarn:
			logger.info("Warning ... {}".format(rtWarn))
			if cf.d: print("Warning ... {}".format(rtWarn))

		return mapper

	@TimeMe.timeitShort
	def getObjectMapper(self, sections):
		## Object mapper for sections
		app = LightGenObjWrapper()

		for sec in sections:
			appSec = LightGenObjWrapper()
			setattr(app, sec, appSec)
			elements = self.cp.options(sec)
			for el in elements:
				setattr(appSec, el, self.cp.get(sec, el))

		return app

	@TimeMe.timeitShort
	def getDupObjectMapper(self, sections, conf=None):
		## Object mapper for sections that have duplicate keys
		app = LightGenObjWrapper()

		for sec in sections:
			if sec.lower() == "ACTIONS".lower():
				actions = aConfigParser(type='dup')
				actions.readRaw(conf)
				setattr(app, sec, self.getObjectMapperRaw(actions, sec))
			else:
				appSec = LightGenObjWrapper()
				setattr(app, sec, appSec)
				elements = self.cp.options(sec)
				for el in elements:
					setattr(appSec, el, self.cp.get(sec, el))

		return app

	@TimeMe.timeitShort
	def getObjectMapperRaw(self, actions, sec):
		## Object mapper for sections
		app = LightGenObjWrapper()
		logger.info("Special actions: {}".format(actions.cpRaw.get(sec, 'cmd')))
		if cf.d: print("Special actions: {}".format(actions.cpRaw.get(sec, 'cmd')))

		setattr(app, 'cmds', actions.cpRaw.get(sec, 'cmd'))
		return app


logger = logging.getLogger('dutil.sConfigParser')
class sConfigParser(object):
	""" Not so simple wrapper for ConfigParser
	"""

	def __init__(self, type=None):
		## setup configparser object
		self.type = type
		if type:
			self.cpRaw = configparser.RawConfigParser(dict_type=MultiOrderedDict, strict=False)
		else:
			self.cp = configparser.ConfigParser(strict=False)

	@TimeMe.timeitShort
	def read(self, ini):
		## read conf files
		if os.path.exists(ini):
			self.cp.read(ini)
		else:
			logger.info("Configuration file missing {}".format(ini))
			if cf.d: print("Configuration file missing {}".format(ini))

		sec = self.cp.sections()
		logger.info("Configuration file sections are: {}".format(sec))
		if cf.d: print("Configuration file sections are: {}".format(sec))
		return sec

	@TimeMe.timeitShort
	def readRaw(self, ini):
		## read conf files
		if os.path.exists(ini):
			self.cpRaw.read(ini)
		else:
			logger.info("Configuration file missing {}".format(ini))
			if cf.d: print("Configuration file missing {}".format(ini))

	@TimeMe.timeitShort
	def dSecItemMapper(self, section):
		## Dict mapper for items in one section
		opts = dict()
		opts[section] = dict()

		for k,v in self.cp.items(section):
			try:
				opts[section][k] = astEval(v)
			except:
				logger.info("Exception raised {}!".format(opts))
				if cf.d: print("Exception raised {}!".format(opts))
				opts[opts] = None
		return opts

	@TimeMe.timeitShort
	def dsectionMapper(self, section):
		## Dict mapper for conf sections
		opts = {}
		options = self.cp.options(section)
		for el in options:
			try:
				opts[el] = self.cp.get(section, el)
				if opts[el] == -1:
					logger.info("Skipping: {}".foramt(opts))
					if cf.d: print("Skipping: {}".foramt(opts))
			except:
				logger.info("Exception raised {}!".format(opts))
				if cf.d: print("Exception raised {}!".format(opts))
				opts[opts] = None
		return opts

	@TimeMe.timeitShort
	def tsectionMapper(self, section):
		## Named Tuple mapper for conf sections

		fields = list()
		values = list()

		options = self.cp.options(section)
		for el in options:
			try:
				fields.append(el)
				values.append(self.cp.get(section, el))
			except:
				logger.info("Exception raised {}!".format(el))
				if cf.d: print("Exception raised {}!".format(el))

		try:
			opts = namedtuple('section', fields)
			mapper = opts(*tuple([v for v in values]))
		except RuntimeWarning as rtWarn:
			logger.info("Warning ... {}".format(rtWarn))
			if cf.d: print("Warning ... {}".format(rtWarn))

		return mapper

	@TimeMe.timeitShort
	def getObjectMapper(self, sections):
		## Object mapper for sections
		app = LightGenObjWrapper()

		for sec in sections:
			appSec = LightGenObjWrapper()
			setattr(app, sec, appSec)
			elements = self.cp.options(sec)
			for el in elements:
				setattr(appSec, el, self.cp.get(sec, el))

		return app

	@TimeMe.timeitShort
	def getDupObjectMapper(self, sections, dupSections, dupActions, conf=None):
		## Object mapper for sections that have duplicate keys
		app = LightGenObjWrapper()

		for sec in sections:
			if sec in dupSections:
				## for duplicate keys in sections we need to take alternate approach
				dupParser = sConfigParser(type='dup')
				dupParser.readRaw(conf)
				if dupParser.cpRaw.has_section(sec):
					for act in dupActions:
						try:
							##logger.info(dupParser.cpRaw.get(sec, act))
							setattr(app, sec, dupParser.cpRaw.get(sec, act))
						except:
							pass
			else:
				appSec = LightGenObjWrapper()
				setattr(app, sec, appSec)
				elements = self.cp.options(sec)
				for el in elements:
					setattr(appSec, el, self.cp.get(sec, el))

		return app

	@TimeMe.timeitShort
	def getObjectMapperRaw(self, dupParser, sec, key):
		## Object mapper for sections
		app = LightGenObjWrapper()
		logger.info("Sections {}".format(dupParser.cpRaw.get(sec, key)))
		if cf.d: print("Sections {}".format(dupParser.cpRaw.get(sec, key)))
		setattr(app, key, dupParser.cpRaw.get(sec, key))
		return app
