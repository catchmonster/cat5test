##---------------------------------------------
## PROJECT: dutil   FILE NAME: Timeit
## USER: sasha              PRODUCT: PyCharm
##---------------------------------------------
## 4/28/17:9:37 AM
##---------------------------------------------

import time
import logging


logger = logging.getLogger("dutil.TimeMe")
class TimeMe():
    """This class is used for timing any algorithm for the constructor timeit
    Learn differences between classmethod and staticmethod
    here you are doing something similar to overload in C++
    """

    def __init__(self):
        logger.info('Log for class {} initiated successfully!'.format(type(self).__name__))

    @classmethod
    def timeit(self, method):
        def timed(*args, **kw):
            ts = time.time()
            result = method(*args, **kw)
            te = time.time()
            logger.info('%r (%r, %r) method executed in %2.2f sec' % (method.__name__, args, kw, te - ts))
            print('%r (%r, %r) method executed in %2.2f sec' % (method.__name__, args, kw, te - ts))
            return result

        return timed

    @classmethod
    def timeitShort(self, method):
        def timed(*args, **kw):
            ts = time.time()
            result = method(*args, **kw)
            te = time.time()
            logger.info('%r method executed in %2.2f sec' % (method.__name__, te - ts))
            logger.info('%r method executed in %2.2f sec' % (method.__name__, te - ts))
            return result

        return timed