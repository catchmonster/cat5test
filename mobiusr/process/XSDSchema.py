##---------------------------------------------
## PROJECT: XMLDiamond   FILE NAME: XSDSchema
## USER: sasha              PRODUCT: PyCharm
##---------------------------------------------
## 8/15/17:5:27 PM
##---------------------------------------------

# import pyxb
# import diamond_schema
#
# rbacx = diamond_schema.rbacx()
# rbacx.namespace = pyxb.BIND()
# rbacx.attributeValues = pyxb.BIND()
# rbacx.accounts = pyxb.BIND()
#
# rbacx.namespace. = 'Cassandra'
#
# el = diamond_schema.domain('MAL CODE')
#
# ##print(el.rbacx('utf-8'))
# ##print(el.nameSpace('utf-8'))
# print(el.toxml('utf-8'))

import sys
import td as api

def test():

	rbacx = api.rbacx()
	comment = api.comments()

	account = api.account(
		id=1, name='Aleksandar Kacanski', endPoint=None, domain='Cassandra', comments="user one",
		suspended=None, locked=None, createDate=None, updateDate=None, createUser=None, attributes=None)


	namespace = api.namespace(namespaceShortName='Cassandra', namespaceName='MALCode')
	rbacx.set_accounts(account)

	rbacx.export(sys.stdout, 0)

test()