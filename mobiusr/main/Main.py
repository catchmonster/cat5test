##---------------------------------------------
## PROJECT: dutil   FILE NAME: Main
## USER: sasha              PRODUCT: PyCharm
##---------------------------------------------
## 4/28/17:9:28 AM
##---------------------------------------------

from ArgParse import parseArgs
import Config as cf
import logging, time, datetime
from MyLogging import MyLogger
from Nio import nIO
from LightUtil import aConfigParser
from getBaseOfProject import getBase
from Driver import DriverLogic
import os, sys
from time import sleep

logger = logging.getLogger('dutil')

if cf.d:
	print(
"""Dutil app:
	1. Dutil - Dutil application wrapper tool written in Python3.x.x
	2. Tool provides dynamic framework for hooks for custom project libraries
	3. Extensive configuration, template, and run time argument options
	4. Combine power of python and template engines to create on the fly hooks 
	for the applications to execute specific modules and templates for degugging
	sockets, ports and applications
"""
	)


def main():
	dateTime = datetime.datetime.now().strftime("%m.%d.%Y.%H.%M.%S")
	## Any aplication has mandatory configuration file called
	## app-unix.conf -- DO NOT CHANGE NAME OF THE FILE --

	myappConf = "app.conf"
	## conf directory will always be part of the application
	## Everything is relative to application stack -- DO NOT CHANGE NAME OF THE FOLDER --
	conf = "conf"

	##get base path of project - always relative to where porject is placed ... (POSIX only - no windows)
	appBase = getBase()
	appConfFolder = os.path.join(str(appBase), conf)

	## Init class to create all mandatory folders if not already created
	nio = nIO()

	## Here we deal with arguments passed to cmd line interface
	## Let's talk a bit about what could be passed to this executable...
	## First program is called: dutil
	## Mandatory options are:
	## -d = debug (turns a lot of logging statments)
	## -p --projectName", help="execute on configuration file of the project", required=True)
	## -v --projectVersion", help="project version libraries that we want to use", required=True)
	##
	## Before you start playing with applications arguments and options
	## study app.conf configuration

	thisArgs = parseArgs()
	## look at python singletons if you want to undrestand how this diebug flag is working ...
	if cf.d: print(thisArgs)
	## Here we start to meassure time of execution
	startTime = time.time()
	if cf.d: print("Application start time in seconds since the "
	               "epoch as a floating point number {}".format(startTime))
	## Here we read main configuration files
	## get utility class to process static and template workflows
	appConfig = aConfigParser()
	appSections = appConfig.read(os.path.join(appConfFolder, myappConf))

	thisApp = appConfig.getObjectMapper(appSections)

	## convert py object to dict
	project = dict((name, getattr(thisApp.PROJECTS, name)) for name in dir(thisApp.PROJECTS) if not name.startswith('__'))

	## search for project template in case insesitive way
	projectInsensitive = { k.lower():v for k,v in project.items()}


	## Here we deal with loggin modules
	mylogImplementation = MyLogger(thisApp.LOG, dateTime)
	logFile = mylogImplementation.changeLogHandlers(os.path.join(str(appBase),
	            conf, thisApp.LOG.myConfig), thisApp.APP.myName)
	if cf.d: print("Logging file is stashed in following path:{}".format(
		logFile))
	## create logger
	logger = logging.getLogger(thisApp.APP.myName.lower())
	if cf.d: print("Starting file based logging")
	logger.info("Starting file based logging")

	if (thisArgs.projectName.lower() in projectInsensitive.keys()):
		projectTemplate = projectInsensitive.get(thisArgs.projectName.lower())
		projectT = os.path.join(thisApp.PROJECTS.projectTemplateFolder,projectTemplate)
		if nio.ifExists(projectT):
			if cf.d: print("For project {} found template {}".format
			               (thisArgs.projectName, projectT))
			logger.info("For project {} found template {}".format
			            (thisArgs.projectName, projectT))
		else:
			if cf.d: print(
				"""\n
							Project template for project {} was not found in path {}!
						Please ensure that you add your project template to 'PROJECTS' section of app-unix.conf configuration file and that
						template exist in the 'ProjectTemplates' folder.
						Please follow guidelines provided in Example.template file for creating of your application template.
						Refuse to proceed...""".format(thisArgs.projectName, projectT))
			logger.info("""\n
			Project template for project {} was not found in path {}!
		Please ensure that you add your project template to 'PROJECTS' section of app-unix.conf configuration file and that
		template exist in the 'ProjectTemplates' folder.
		Please follow guidelines provided in Example.template file for creating of your application template.
		Refuse to proceed...""".format(thisArgs.projectName, projectT))
	else:
		if cf.d: print(
			"""\n
					Project template for project {} was not found in app.conf configuration file!
					Please ensure that you add your project template to 'PROJECTS' section of app-unix.conf configuration file and that
					template exist in the 'ProjectTemplates' folder.
					Please follow guidelines provided in Example.template file for creating of your application template.

					Refuse to proceed...""".format(thisArgs.projectName))
		logger.info("""\n
		Project template for project {} was not found in app.conf configuration file!
		Please ensure that you add your project template to 'PROJECTS' section of app-unix.conf configuration file and that
		template exist in the 'ProjectTemplates' folder.
		Please follow guidelines provided in Example.template file for creating of your application template.

		Refuse to proceed...""".format(thisArgs.projectName))

		sys.exit(1)


	## Here we call buisness logic module and the app takes from there
	d = DriverLogic(thisApp, thisArgs, projectT)
	d.processConf()
	d.loadModules()
	## now let's run app modules
	d.run()
	d.publish()



	##Done
	if cf.d: print("\n\nMain program finished processing in "
	               "{} seconds ---".format(time.time() - startTime))
	logger.info("\n\nMain program finished processing in "
	            "{} seconds ---".format(time.time() - startTime))


if __name__ == "__main__":
	main()
	sys.exit(0)