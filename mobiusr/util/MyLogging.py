##---------------------------------------------
## PROJECT: dutil   FILE NAME: MyLogging
## USER: sasha              PRODUCT: PyCharm
##---------------------------------------------
## 4/28/17:9:36 AM
##---------------------------------------------

import logging.config
import logging.handlers
import configparser
from Nio import nIO
import Config as cf
from io import StringIO
import socket, os



logger = logging.getLogger("dutil.MyLogger")
class MyLogger:
	""" This class deals with logger setup and all
			manipulations necessery with log handelers
	"""

	def __init__(self, myLogger, dateTime):
		## Setting up log object (namedtuple) and host name for log name ...
		self.clog = myLogger
		self.whoamI = socket.gethostname().split('.')[0]
		self.dateTime = '-' + dateTime

	def changeLogHandlers(self, logConfig, myName):
		##This is medium hack
		##Please be cognisant of changes in app-log*.conf file
		##They will affect this method ...

		nutil = nIO()
		nutil.createLocalPartition(os.path.join(self.clog.myRoot, myName))
		HANDLER = "log_file"
		LOGFILE = os.path.join(self.clog.myRoot, myName, (self.whoamI + self.dateTime + self.clog.myLogExt))
		config = configparser.ConfigParser()
		try:
			config.read(logConfig)
		except configparser.Error as cpe:
			logger.info("Exception raised: {}".format(cpe))
			if cf.d: print("Exception raised: {}".format(cpe))

		sections = config.sections()
		if cf.d: logger.info("Logger configuration sections are {}".format(sections))

		section = "handler_%s" % HANDLER
		opt = "args"
		oldargs = eval(config.get(section, opt))
		newargs = "(" + "'" + LOGFILE + "'" + "," + "'" + "w" + "'" ")"
		##write new log entry to clog pbject so that we can use it later
		self.clog.logFile = LOGFILE
		if cf.d: logger.info("Substituting current {} with {}".format(oldargs, newargs))
		try:
			config.set(section, "args", newargs)
			outstream = StringIO()
			config.write(outstream)
			outstream.seek(0)
		except configparser.Error as cpe:
			logger.info("Exception raised: {}".format(cpe))

		logging.config.fileConfig(outstream)
		return LOGFILE

	def setupLoggers(self):
		# Setup file based logger handle
		## delete previous log for now
		try:
			os.unlink(self.mainLogFH)  ##windows only
			## os.truncate(path, lenght) is better for tail -f in linux
		except os.error as ioe:
			logger.info("Exception raised: {}".format(ioe))

		try:
			log = logging.getLogger(self.logMainAppName)
			fileHandeler = logging.FileHandler(self.mainLogFH)
			formatSpec = logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s')
			fileHandeler.setFormatter(formatSpec)
			fileHandeler.setLevel(logging.DEBUG)
			log.addHandler(fileHandeler)
			log.debug('Logger initiated successfully!')  # Create INFO message
		except Exception as gle:
			logger.info("Exception: {}".format(gle))

		return (log)
