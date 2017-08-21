##---------------------------------------------
## PROJECT: Dutil   FILE NAME: Dill
## USER: sasha              PRODUCT: PyCharm
##---------------------------------------------
## 5/19/17:10:15 AM
##---------------------------------------------

import dill


class MSGpack(object):
	"""
	We want to be able to ship Python object to different type of infrastructure -
	heterogeneous programming - byte streams
	"""

	def __init__(self):
		##print("License {}".format(dill.license()))
		pass

	@staticmethod
	def pack(obj):
		"Pack it to bytes as object"
		_f = dill.dumps(obj)
		return _f


	@staticmethod
	def unpack(bf):
		"Unpack it to dill object and get back original object from packed dill"
		obj = dill.loads(bf)
		return obj

## for test purposes
class Foo(object):
	def bar(self, x):
		return x + self.y

	y = 1


def main():
	f = Foo()
	d = MSGpack()
	bf = d.pack(f)
	newObj = d.unpack(bf)
	print("unpacked {}".format(newObj))
	print(newObj.y)

	from TD.util.PSUtil import PSInterrogate
	nstat = PSInterrogate()
	res = nstat.run()
	bres = d.pack(res)
	newObj = d.unpack(bres)
	print("unpacked {}".format(newObj))
	print(newObj[0]._fields)



if __name__ == '__main__':
	main()
