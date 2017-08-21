##---------------------------------------------
## PROJECT: Dutil   FILE NAME: MultiObjParser
## USER: sasha              PRODUCT: PyCharm
##---------------------------------------------
## 7/11/17:1:14 PM
##---------------------------------------------

from TD.util.PSUtil import PSInterrogate
from functools import wraps

def accepts(*types):
	def checkAccepts(f):
		assert len(types) == 2
		@wraps(f)
		def newF(*args, **kwds):
			for (a, t) in zip(args, types):
				assert isinstance(a, t), "argument {} does not match {}".format(a, t)
			return f(*args, **kwds)
		return newF
	return checkAccepts



class ObjectParser(object):
	"""
	Multi object parser
	"""

	def __init__(self):
		self.ps = PSInterrogate()

	@accepts(object,object)
	def parseSSH(self, output):
		print("Working with {} parser".format(output['parser']))
		for h in output['ssh']:
			for host, hostOutput in h.items():
				for el in hostOutput.stdout:
					print(" Remote end {} command output is {}".format(hostOutput['host'], el))


	@accepts(object,object)
	def parsePyro4(self, output):
		print("Working with {} parser".format(output['parser']))
		self.ps.setup(output)
		for out in output['pyro4']:
			self.ps.parseOnly(out, 'laddr')


	@accepts(object, object)
	def parseDirect(self, output):
		print("Working with {} parser".format(output['parser']))
		if output['parser'] == 'psParser':
			self.ps.setup(output)
			for out in output['direct']:
				self.ps.parseOnly(out, 'raddr')
		elif output['parser'] == 'dictParser':
			for out in output['direct']:
				for port, connStatus in out.items():
					if connStatus == 0:
						print("Port: {}\nStatus: {}".format(port,'Success'))
					else:
						print("Port: {}\nStatus: {}".format(port, 'Failure'))
				print("------------------------------------------")
