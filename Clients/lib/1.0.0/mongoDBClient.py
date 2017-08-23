##---------------------------------------------
## PROJECT: Cattest   FILE NAME: cassandraClient.py
## USER: sasha              PRODUCT: PyCharm
##---------------------------------------------
## 8/17/17:7:04 PM
##---------------------------------------------

from cassandra.cluster import Cluster
from cassandra.auth import PlainTextAuthProvider
import sys, ast
from messageHash import Mask
from AbstractCore import Core

class CDriver(Core):
	"""
	Cassandra Driver
	"""

	def run(self):
		self.c = self.conf.CASSANDRA
		print("Running {} client".format(self.c.app))
		passwdList = ast.literal_eval(self.c.passwd)
		self.passwd = passwdList[0]
		self.mask = Mask(self.passwd)
		self.user = self.c.user
		self.cluster = self.c.cluster
		self.auth = self.c.auth
		## encrypted passwd
		##try:
		##	self.passwd = self.psw.encrypt()
		##except:
		##	sys.exit(0)

		self.session = None
		try:
			self.bootStrap()
		except RuntimeError as rtErr:
			print("Error occurred: {}".format(rtErr))
			sys.exit(1)
		try:
			self.getUsersRoles('LIST users', 'LIST roles of %s')
		except RuntimeError as rtErr:
			print("Error occurred: {}".format(rtErr))
			sys.exit(1)

	def bootStrap(self,):
		if self.auth:
			auth_provider = PlainTextAuthProvider(username=self.user,
																						password=self.mask.decrypt(self.passwd))
			cluster = Cluster([self.cluster], auth_provider=auth_provider, protocol_version=3)
			self.session = cluster.connect()
		else:
			cluster = Cluster([self.cluster])
			self.session = cluster.connect()

	def getUsersRoles(self, qUser, qRoles ):
		if qUser:
			users = self.session.execute(qUser)

			for user in users:
				print("User:{}\t\tSuper: {}".format(user.name,user.super))
				print('--------------------------')
				if qRoles:
					userRoles = self.session.execute(qRoles, [user.name])
					for roleOfUser in userRoles:
						print("Role {}\nSuper {}\nLogin {}\nOptions {}\n".format(roleOfUser.role,
																												roleOfUser.super,
																												roleOfUser.login,
																												roleOfUser.options))
			print('--------------------------')


def main():
	cDriver = CDriver({'app': 'cassandra', 'cluster': '10.0.2.15', 'user': 'cassandra', 'passwd': 'cassandra', 'auth': True})
	cDriver.run()


if __name__ == "__main__":
	main()
	sys.exit(0)