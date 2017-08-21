##---------------------------------------------
## PROJECT: Dutil   FILE NAME: sasha
## USER: sasha              PRODUCT: PyCharm
##---------------------------------------------
## 7/10/17:6:26 PM
##---------------------------------------------

import sys

class parserDescriptor:
	"""
	Class descripotor
	"""
	def __init__(self, name):
		self.name = name


	def __set__(self, instance, value):
		if type(value) != str:
			raise TypeError("Wrong type, expected: %s" % str(str))
		instance.__dict__[self.name] = value

	def __get__(self, instance, cls):
		# Actually performs the default action. Just don't define this
		# method to get the default behavior.
		return instance.__dict__[self.name]





class MetaObjectParser:
	name = parserDescriptor("name")

	def __init__(self, name):
		self.name = name


def main():
	opts = {'1': "10.0.2.15"}
	mpo = MetaObjectParser("direct")
	mpo.name = "direct"


# vp = VaraetyParser()
# vp.run("plainParser")


if __name__ == "__main__":
	main()
	sys.exit(0)
