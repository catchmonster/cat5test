##---------------------------------------------
## PROJECT: dutil   FILE NAME: JsonUtil
## USER: sasha              PRODUCT: PyCharm
##---------------------------------------------
## 4/28/17:9:34 AM
##---------------------------------------------

import simplejson as json
import logging, codecs
from collections import defaultdict, OrderedDict
from munch import munchify
import Config as cf
from Timeit import TimeMe

logger = logging.getLogger('dutil.sjWrapper')
class sjWrapper(object):
	"""
	Not so simplejson wrapper
	more to come ...
	"""
	def __init__(self):
		self.normalize = None

	@TimeMe.timeitShort
	def loadFromFile(self, fn):
		try:
			with open(fn) as jsonDataFile:
				data = json.load(jsonDataFile)
		except json.JSONDecodeError as jErr:
			logger.info("Exception raised {}".format(jErr))
			if cf.d: print("Exception raised {}".format(jErr))
		return data

	@TimeMe.timeitShort
	def normalizeString (self, genStr=""):
		self.empty = False
		if self.emptyInstance(genStr):
			self.normalize = genStr.replace("'", "\"")
		else:
			logger.info("Empty string found... "
			            "Json wrapper will not convert this instance...")
			if cf.d: print("Empty string found... "
			               "Json wrapper will not convert this instance...")
			self.empty = True

	@TimeMe.timeitShort
	def emptyInstance(self, ln):
		line = ln.rstrip()
		if line:
			return line

	@TimeMe.timeitShort
	def convertToString(self, pyObj):
		try:
			s = json.dumps(pyObj)
		except json.JSONDecodeError as jsonErr:
			logger.info("Exception raised: {}".format(jsonErr))
			if cf.d: print("Exception raised {}".format(jsonErr))
		return s

	@TimeMe.timeitShort
	def convertToDict(self, genString):
		self.normalizeString(genString)
		if not self.empty:
			try:
				d = json.loads(self.normalize)
				if cf.d: print("convertToDict conversion type is {}".format(type(d)))
				for k,v in d.items():
					if isinstance(v, str):
						newV = codecs.getdecoder("unicode_escape")(v)[0]
						d[k] = newV
			except json.JSONDecodeError as jsonErr:
				logger.info("Exception raised: {}".format(jsonErr))
				if cf.d: print("Exception raised {}".format(jsonErr))
			return d
		else:
			return None

	@TimeMe.timeitShort
	def convertToMultiDict(self, genString):
		self.normalizeString(genString)
		if not self.empty:
			return json.JSONDecoder(object_pairs_hook=
			                        self.multiDict).decode(self.normalize)
		else:
			return None

	@TimeMe.timeitShort
	def multiDict(self, normalize):
		"""Convert duplicate keys values to lists."""
		# read all values into lists

		d = defaultdict(list)

		for k, v in normalize:
			d[k].append(v)

		# unpack lists that have only 1 item
		for k, v in d.items():
			if len(v) == 1:
				d[k] = v[0]
		return dict(d)

	@TimeMe.timeitShort
	def dictToBinary(self, d):
		str = json.dumps(d)
		blo = ' '.join(format(ord(ch), 'b') for ch in str)
		return blo

	@TimeMe.timeitShort
	def binaryToDict(self, blo):
		jsonObj = ''.join(chr(int(x, 2)) for x in blo.split())
		d = json.loads(jsonObj)
		return d

	@TimeMe.timeitShort
	def convertToList(self, genStr):
		return json.loads(genStr)

	@TimeMe.timeitShort
	def munch(self, d):
		return munchify(d)

	@TimeMe.timeitShort
	def getListFromList(self, x):
		l = list()
		for el in x:
			if cf.d: print("Extracted element is: {}".format(el))
			for k, v in el.items():
				if cf.d: print("Key - Value elements are: {} - {}".format(
					k,v))
				l.append(v)
		return l

	@TimeMe.timeitShort
	def getDictFromListOfDicts(self, x):
		d = OrderedDict()
		for el in x:
			d.update(el)
		return d

	@TimeMe.timeitShort
	def getDictFromList(self, x):
		d = OrderedDict(zip(x,x))
		return d
