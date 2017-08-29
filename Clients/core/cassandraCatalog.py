##---------------------------------------------
## PROJECT: Cattest   FILE NAME: cassandraCatalog
## USER: sasha              PRODUCT: PyCharm
##---------------------------------------------
## 8/28/17:5:19 PM
##---------------------------------------------


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

class Perm(IterMixin):
	def __init__(self, role, username, resource, permission):
		self.role = role
		self.username = username
		self.resource = resource
		self.permission = permission