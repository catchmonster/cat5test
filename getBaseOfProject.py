##---------------------------------------------
## PROJECT: Dutil   FILE NAME: getBaseOfProject
## USER: sasha              PRODUCT: PyCharm
##---------------------------------------------
## 6/1/17:9:56 AM
##---------------------------------------------

import os
import Config as cf

class getBase(object):
    '''
    For all Resources under application root define the root of application
    '''

    def __init__(self):
        self.root = __file__

    def __str__(self):
        ##if cf.d: logger.info(os.path.dirname(self.root))
        return os.path.dirname(self.root)