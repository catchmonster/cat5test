##---------------------------------------------
## PROJECT: dutil   FILE NAME: ArgParse
## USER: sasha              PRODUCT: PyCharm
##---------------------------------------------
## 4/28/17:9:31 AM
##---------------------------------------------


import argparse, sys
import Config as cf
import logging
from Timeit import TimeMe

logger = logging.getLogger('dutil.parseArgs')


@TimeMe.timeitShort
def parseArgs():
	""" Here we deal with inputs
			this is strictly import module """

	argParser = argparse.ArgumentParser(prog='dutil (Main.py)')
	argParser.add_argument("-p", "--projectName", help="What tests (project) we want execute", required=True)
	argParser.add_argument("-v", "--projectVersion", help="What version of libraries we want to execute", required=True)
	argParser.add_argument("-d", action='store_true', help='Enable debugging')


	try:
		args = argParser.parse_args()
		if args:
			if args.d:
				logger.info("Debugging enabled!")
				cf.d = True
				if cf.d: logger.info(
					"Argument Name Space: {}".format(args))  # # if debug flag engaged Please check singleton pattern
			else:
				logger.info("Debugging disabled!")

		if args.projectName:
			if cf.d:  logger.info("Project name: {}".format(args.projectName))
		if args.projectVersion:
			if cf.d:  logger.info("Version of project libraries: {}".format(args.projectVersion))
	except SystemExit:
		if cf.d: logger.info("Mandatory argument required")
		sys.exit(0)

	return args
