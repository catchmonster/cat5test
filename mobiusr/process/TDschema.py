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
		self.perms = dict()


	def run(self):
		for m,payload in self.payload.items():
			print("Publishing XML for application {}".format(m))
			self.data, self.xml = payload.data, payload.xml
			for a in self.xml.allPermissions.split():
				self.perms[a] = a

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
	def getPermissions(self):
		return self.data['permissions']


	def init(self):
		self.rbacx = api.rbacx()
		self.namespace = api.namespace()


	def setup(self):
		self.namespace.set_namespaceShortName(self.xml.namespaceShortName)
		self.namespace.set_namespaceName(self.xml.namespaceName)
		self.rbacx.set_namespace(self.namespace)

		attVals = api.attributeValues()
		atts = api.attributes()


		for el in self.getPermissions():
			acc = api.attributeValue(id= self.xml.roleSyntax + el.role, value= el.username)
			attrGlossary = api.attribute(name=self.xml.glossary)
			atts.add_attribute(attrGlossary)

			acc.set_attributes(atts)
			attVals.add_attributeValue(acc)

		self.rbacx.set_attributeValues(attVals)
		##self.rbacx.set_accounts(self.account)

	def export(self):
		sys.stdout.write('<?xml version="1.0" ?>\n')
		self.rbacx.export(sys.stdout, 0)




