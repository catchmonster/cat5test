##---------------------------------------------
## PROJECT: dutil   FILE NAME: Nio
## USER: sasha              PRODUCT: PyCharm
##---------------------------------------------
## 4/28/17:9:36 AM
##---------------------------------------------

import os, fileinput, logging, glob, subprocess, io, shutil, time
import Config as cf


logger = logging.getLogger('dutil.nIO')
class nIO():
	""" The new IO librarary convinience methods for NYSE
	"""

	def __init__(self):
		pass

	def convertSizes(self, num, suffix='B'):
		for unit in ['', 'Ki', 'Mi', 'Gi', 'Ti', 'Pi', 'Ei', 'Zi']:
			if abs(num) < 1024.0:
				return "%3.1f%s%s" % (num, unit, suffix)
			num /= 1024.0
		return "%.1f%s%s" % (num, 'Yi', suffix)

	def listPart(self, lpath):
		if self.ifFolderExists(lpath):
			from os import walk
			metaF = []
			for (dirpath, dirnames, filenames) in walk(lpath):
				metaF.extend(filenames)
				break

			return metaF

	def ifExists(self, path):
		if os.path.exists(path):
			logger.info('Absolute path found... {}'.format(path))
			return True
		else:
			logger.info('Absolute path NOT found...'.format(path))
			return False

	def deleteContent(self, fh):
		try:
			fh.seek(0)
			fh.truncate()
		except IOError as ioErr:
			logger.info("Error: {}".format(ioErr))

	def ifFolderExists(self, path):
		if os.path.isdir(path):
			logger.info('Absolute path found... {}'.format(path))
			return True
		else:
			logger.info('Absolute path NOT found... {}'.format(path))
			return False

	def createLocalPartition(self, lpath):
		## To creatge a local partition
		bool = True
		try:
			if not os.path.exists(lpath):
				os.makedirs(lpath)
		except os.error as oserr:
			logger.error("Exception: {}".format(oserr))
			return False

		return bool

	def moveFolder(self, src, dst):
		if src != None or dst != None:
			try:
				shutil.move(src, dst)
			except shutil.Error as shutilErr:
				logger.info("Error: {}".format(shutilErr))
		else:
			logger.info("Ether source or destination path are missing!")
			return False
		return True

	def copyFolder(self, src, dst):
		if src != None or dst != None:
			if os.path.exists(dst):
				shutil.rmtree(dst)
				shutil.copytree(src, dst)
			else:
				shutil.copytree(src, dst)
		else:
			logger.info("Ether source or destination path are missing!")
			return False
		return True

	# TODO implement marshaling method to chain any number of files
	def chain(self, listOfFiles, outputFile=None):
		## To cahin filename strings for usage in manifests
		try:
			with open(outputFile, 'w') as fout:
				for line in fileinput.input(listOfFiles):
					fout.write(line)
		except RuntimeError as fie:
			logger.error("Exception: {}".format(fie))

	def clean(self, folder):
		## For cleaning up directory structures like log files
		try:
			os.chdir(folder)
			fileList = glob.glob("*")
			logger.info("File list to remove {}".format(fileList))
			for x in fileList:
				logger.info("Removing following log file: {}".format(x))
				os.remove(x)
		except OSError as oserr:
			logger.error("exception: {}".format(oserr))

	def pickleObj(self, fName, mode):
		## Object pickling
		f = open(fName, mode)
		return f

	def fileObj(self, fName, mode):
		## Wrapper method for different mode types
		try:
			f = open(fName, mode)
		except:
			f = open(fName, 'w')
			pass
		return f

	##due to windows engineering stupididty I got to code work around for detecting mime type ...
	def specMimeType(self, file):
		##We are only checking for plain and x-gzip formats

		type = subprocess.check_output(['file', '-ib', file]).strip().decode('ascii')
		if "plain" in type:
			return "plain"
		elif "x-gzip" in type:
			return "x-gzip"
		else:
			return None

	def manifestIO(self, mfFile, mfFolder=None, idx=None, slice=None):
		## Path manipulation
		nio = nIO()
		##Create manifest folder on the fly
		##Assumption here is that if manifest folder is None full path to manifest file is supplied by developer via mFile
		if mfFolder != None:
			manifest = os.path.join(mfFolder, mfFile)
			try:
				nio.createLocalPartition(mfFolder)
			except OSError as ioExc:
				if cf.d: logger.info("Error: Manifest folder could not be created!")
				raise

		if idx:
			##open a manifest file it always write
			fh = nio.fileObj(manifest, 'w')
			##crerate manifest partition indexes
			for x in range(0, idx + 1):
				try:
					fh.write(str(x) + '\n')

				except io.UnsupportedOperation as ioErr:
					logger.info("Error in writing manifest file: {}".format(ioErr))
					raise
			fh.close()
		elif slice:  ## if no index is supplied, eg. idx is None update manifest file with slice number if exist
			##just update done work on the manifest file
			##I am done with this slice prefix index with !
			newSlice = "!" + str(slice)
			try:
				fh = nio.fileObj(manifest, 'r')
				curData = fh.read()
				fh.close()
				newData = curData.replace(slice, newSlice)
				fh = nio.fileObj(manifest, 'w')
				fh.write(newData)
				fh.close()
			except io.UnsupportedOperation as ioErr:
				logger.info("Error in writing manifest file: {}".format(ioErr))
				raise

	def manifestPlain(self, mfFile, mfFolder, action='aw', payload=None):
		## Path manipulation
		rPyaload = None
		##Create manifest folder on the fly
		##Assumption here is that if manifest folder is None full path to manifest file is supplied by developer via mFile
		if mfFolder != None:
			manifest = os.path.join(mfFolder, mfFile)
			try:
				self.createLocalPartition(mfFolder)
				fh = self.fileObj(manifest, action)
			except OSError as ioExc:
				if cf.d: logger.info("Error: Manifest folder could not be created!")
				raise
		try:
			if action == 'r':
				rPyaload = fh.read()
			elif action == 'a':
				fh.write(payload + '\n')
			else:
				logger.info("Error: incorect file action passed! {}".format(action))
		except Exception as ex:
			logger.info("Error: exception {}".format(ex))

		fh.close()
		return rPyaload
