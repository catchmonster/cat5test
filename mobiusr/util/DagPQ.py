##---------------------------------------------
## PROJECT: Dutil   FILE NAME: DagPQ
## USER: sasha              PRODUCT: PyCharm
##---------------------------------------------
## 6/5/17:12:00 PM
##---------------------------------------------

import queue, logging, sys
from JsonUtil import sjWrapper
from getBaseOfProject import getBase
from Nio import nIO
from LightUtil import sConfigParser



class PEntry(object):
	""" priority of actions {dict}"""

	def __init__(self, priority, input):
		self.priority = priority
		self.input = input

	def __lt__(self, other):
		return self.priority < other.priority



logger = logging.getLogger('dutil.SoftQueue')
class SoftQueue(object):
	"""
	Ordered queue - simple state machine
	"""

	def __init__(self):
		self.pQueue = queue.PriorityQueue()


	def show(sd):
		for k, v in sd.items():
			print("key : {}\nvalue: {}".format(k, v))


	def pushQ(self, pl):
		if len(pl) != 0:
			for act in pl:
				self.pQueue.put(act)


	def pullQ(self, pl):
		while not pl.empty():
			item = pl.get()
			##print(type(item))
			print("Traversing Queue FIFO - priority: {} item {}".format(item.priority, item.input))

	def getpQueue(self):
		return self.pQueue



def main():

	nio = nIO()
	## get base of the project
	appBase = getBase()
	## init json wrapper
	jw = sjWrapper()
	## get path to running configuration (what do you want to do!!)
	run = '/core/apps/dutil/projectTaskActions/cassandraTest.conf'

	tProjConf = sConfigParser()
	projSec = tProjConf.read(run)

	actions = tProjConf.dSecItemMapper('ACTIONS')

	print("Raw actons are {}".format(actions))

	klassObjList = list()
	for k,v in actions['ACTIONS'].items():
		print(v)
		action = PEntry(v[0],v[1])
		klassObjList.append(action)

	print(klassObjList)

	sq = SoftQueue()
	sq.pushQ(klassObjList)
	priorityQ = sq.getpQueue()
	sq.pullQ(priorityQ)



if __name__ == "__main__":
	main()
	sys.exit(0)
