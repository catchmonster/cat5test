##---------------------------------------------
## PROJECT: Dutil   FILE NAME: PSUtil
## USER: sasha              PRODUCT: PyCharm
##---------------------------------------------
## 5/15/17:1:41 PM
##---------------------------------------------

import psutil
from collections import OrderedDict as od
import ast



class PSInterrogate(object):

	def __init__(self):
		self.attr = od([('fd','socket file descriptor or -1'),
           ('family','the address family = AF_INET, AF_INET6 or AF_UNIX'),
           ('type','the address type, either SOCK_STREAM or SOCK_DGRAM'),
           ('laddr','the local address as a (ip, port) tuple or a path in case of AF_UNIX sockets'),
           ('raddr', 'the remote address as a (ip, port) tuple or a path in case of AF_UNIX sockets'),
           ('status','represents the status of a TCP connection - for UDP and UNIX sockets return is psutil.CONN_NONE'),
           ('pid','the PID of the process which opened the socket, if retrievable, else None')])
		self.parser = None
		self.pyro = None
		self.runFilter = None

	def setup(self, retrn):
		self.parser = retrn['parser']
		if 'pyro4' in retrn:
			self.pyro = retrn['pyro4']
		elif 'direct' in retrn:
			self.direct = retrn['direct']
		else:
			print('Error in type of parser')
		self.runFilter = retrn['runFilter']

	def run(self):
		try:
			psRun = psutil.net_connections()
		except psutil.Error as psErr:
			print(psErr)
			psRun = None

		return psRun


	def isEmpty(self, any):
		if any:
			return False
		else:
			return True

	def extractStats(self, name, el):
		##todo use lambda here
		host = getattr(el, name)[0]
		family = str(getattr(el, 'family'))
		if not self.isEmpty(getattr(el, 'raddr')):
			rPort = getattr(el, 'raddr')[1]
		else:
			rPort = None
		if not self.isEmpty(getattr(el, 'laddr')):
			lPort = getattr(el, 'laddr')[1]
		else:
			lPort = None

		status = getattr(el,'status')

		return (host, family, rPort, lPort, status)


	def parseAll(self, result):
		for el in result:
			print(el)
			for name in el._fields:
				print("Attribute {} = {} > {}".format(name, str(getattr(el, name)), self.attr[name]))
			print('END-OF-ATTR----------------------------------------------------------END-OF-ATTR')
		print('END-OF-RUN----------------------------------------------------------END-OF-RUN')

	def parseOnly(self, result, nameFilter):
		filter = self.runFilter
		ports = filter['ports']
		for el in result:
			##print(el)
			## match local address name of attrib
			for name in el._fields:
				if name == nameFilter:
					##match port oin the local address tuple second arg
					try:
						##print(getattr(el, 'laddr')[1])
						if getattr(el, name)[1] in ports:
							print(el)
							host, family, rPort, lPort, status = self.extractStats(name, el)
							print("Host IP:{}\nSocket Family:{}\nRPORT:{}\nLPORT :{}\nStatus:{}\n".format(
								host, family, rPort, lPort, status))
							print('END-OF-ATTR----------------------------------------------------------END-OF-ATTR')
					except:
						pass
		print('END-OF-SCAN----------------------------------------------------------END-OF-SCAN')

def main():
	nstat = PSInterrogate()
	res = nstat.run()
	nstat.parse(res)

if __name__ == '__main__':
	main()
