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



class IterMixin(object):
	def __iter__(self):
		for attr, value in self.__dict__.items():
			yield attr, value


class User(IterMixin):
	def __init__(self, user, super):
		self.user = user
		self.super = super

class Role(IterMixin):
	def __init__(self, role, super, login, options):
		self.role = role
		self.super = super
		self.login = login
		self.options = options



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
		self.protocol = self.c.protocol
		self.queries = self.conf.QUERIES

		self.session = None
		try:
			self.bootStrap()
		except RuntimeError as rtErr:
			print("Error occurred: {}".format(rtErr))
			sys.exit(1)
		try:
			self.getUsersRoles(self.queries.users, self.queries.roles)
		except RuntimeError as rtErr:
			print("Error occurred: {}".format(rtErr))
			sys.exit(1)

	def bootStrap(self,):
		if self.auth:
			auth_provider = PlainTextAuthProvider(username=self.user,
																						password=self.mask.decrypt(self.passwd))
			cluster = Cluster([self.cluster], auth_provider=auth_provider,
												protocol_version=int(self.protocol))
			self.session = cluster.connect()
		else:
			cluster = Cluster([self.cluster])
			self.session = cluster.connect()

	def getUsersRoles(self, qUser, qRoles ):
		if qUser:
			users = self.session.execute(qUser)

			for user in users:
				self.users.append(User(user.name, user.super))
				##self.users.append(setattr(type('genObject', (IterMixin,), {})(), 'superPrivs', user.super))
				##self.users.append(self.genObj)
				print("User:{}\t\tSuper: {}".format(user.name,user.super))
				print('--------------------------')
				if qRoles:
					userRoles = self.session.execute(qRoles, [user.name])
					for roleOfUser in userRoles:
						self.roles.append(Role(roleOfUser.role,
																	 roleOfUser.super, roleOfUser.login, roleOfUser.options))
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