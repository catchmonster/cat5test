##---------------------------------------------
## PROJECT: XMLDiamond   FILE NAME: XSDSchema
## USER: sasha              PRODUCT: PyCharm
##---------------------------------------------
## 8/15/17:5:27 PM
##---------------------------------------------

import sys
import td as api





class Assemble(object):
	"""
	Assemble class to privide XML schema for creation of output feed
	"""
	def __init__(self, payload):
		self.payload = payload
		self.data = None
		self.xml = None


	def run(self):
		for m,payload in self.payload.items():
			print("Publishing XML for application {}".format(m))
			self.data, self.xml = payload.data, payload.xml
			self.init()
			self.setup()
			self.setup()
			self.export()



	def getGroups(self):
		return self.data['groups']
	def getRoles(self):
		return self.data['roles']
	def getUsers(self):
		return self.data['users']


	def init(self):
		self.rbacx = api.rbacx()
		self.comment = api.comments()
		self.account = api.account()
		self.namespace = api.namespace()

		##self.attributeValue = api.attributeValue()
		self.value = api.value()


	def setup(self):
		##sys.stdout.write('<?xml version="1.0" ?>\n')
		self.namespace.set_namespaceShortName(self.xml.namespaceShortName)
		self.namespace.set_namespaceName(self.xml.namespaceName)


		self.rbacx.set_namespace(self.namespace)
		##self.accSetup()


		avs = api.attributeValues()

		for el in self.getRoles():
			acc = api.attributeValue(id= "Role=" + el.role, value= el.role)
			avs.add_attributeValue(acc)

		self.rbacx.set_attributeValues(avs)
		##self.rbacx.set_accounts(self.account)

	def export(self):
		sys.stdout.write('<?xml version="1.0" ?>\n')
		self.rbacx.export(sys.stdout, 0)

	def accSetup(self):
		pass
		# for  el in self.getRoles():
		# 	attributeValue.set_id("Role=" + el.role)
		# 	attributeValue.set_value(el.role)
		# 	self.attributeValues.set_attributeValue(attributeValue)

			# self.account = api.account(
			# id=1, name='Aleksandar Kacanski', endPoint=None, domain='Cassandra', comments="user one",
			# suspended=None, locked=None, createDate=None, updateDate=None, createUser=None, attributes=None)



