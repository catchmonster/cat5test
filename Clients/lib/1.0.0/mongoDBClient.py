##---------------------------------------------
## PROJECT: Cattest   FILE NAME: cassandraClient.py
## USER: sasha              PRODUCT: PyCharm
##---------------------------------------------
## 8/17/17:7:04 PM
##---------------------------------------------

from cassandra.cluster import Cluster
from cassandra.auth import PlainTextAuthProvider
import sys
from messageHash import Mask
from AbstractCore import Core


class MDBDriver(Core):
	"""
	Cassandra Driver
	"""
	name = 'mongoDB'
	app = 'app'
	cluster = 'cluster'
	user = 'user'
	passwd = 'passwd'
	auth = 'auth'

	def run(self):
		for k, v in self.init.items():
			if k == MDBDriver.app and v == MDBDriver.name: print("Running {} client".format(MDBDriver.name))
			if k == MDBDriver.passwd: self.psw = Mask(v)
			if k == MDBDriver.user: self.user = v
			if k == MDBDriver.cluster: self.cluster = v
			if k == MDBDriver.auth: self.auth = v
		## encrypted passwd
		try:
			self.passwd = self.psw.encrypt()
		except:
			sys.exit(0)

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

	def getMaskedPasswd(self):
		return self.passwd

	def bootStrap(self, ):
		if self.auth:
			auth_provider = PlainTextAuthProvider(username=self.user,
																						password=self.psw.decrypt(self.getMaskedPasswd()))
			cluster = Cluster(['192.168.1.9'], auth_provider=auth_provider, protocol_version=3)
			self.session = cluster.connect()
		else:
			cluster = Cluster(['192.168.1.9'])
			self.session = cluster.connect()

	def getUsersRoles(self, qUser, qRoles):
		if qUser:
			users = self.session.execute(qUser)

			for user in users:
				print("User:{}\t\tSuper: {}".format(user.name, user.super))
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
	mdbDriver = MDBDriver()
	mdbDriver \

		.run({'app': 'cassandra', 'cluster': '192.168.1.9', 'user': 'cassandra', 'passwd': 'cassandra', 'auth': True})


##cDriver.bootStrap()
##cDriver.getUsersRoles('LIST users', 'LIST roles of %s')


if __name__ == "__main__":
	main()
	sys.exit(0)