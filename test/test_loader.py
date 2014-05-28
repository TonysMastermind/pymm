import mm.loader
import mm.singleton
from mm import *

import glob
import os
import os.path
import random
import unittest as ut


FILE_PATH = 'test/var/CODES'
DATA_VERSION = 1

def make_data():
    return CODETABLE.CODES

class PickledSingleton(mm.singleton.SingletonBehavior):
    __metaclass__ = mm.singleton.Singleton

    def __init__(self):
        self.special_value = random.randint(1, (1 << 32) - 1)


PICKLE_PATH = "/tmp/testpickle"
PICKLE_SPEC = mm.loader.StorageSpec(DATA_VERSION, PICKLE_PATH)

class PickledSingletonTestCase(ut.TestCase):
    def runTest(self):
        for p in glob.glob(PICKLE_PATH + '.v1.pickle*'):
            os.remove(p)

        loader = mm.loader.Loader(PickledSingleton, PICKLE_SPEC)
        s = loader.get()

        # corrupt the file.
        os.remove(loader.path)
        with open(loader.path, 'w+') as fp:
            fp.write('x')

        PickledSingleton.clear()

        ss = loader.get()
        self.assertNotEqual(s.special_value, ss.special_value)

        PickledSingleton.clear()

        sss = PickledSingleton()
        self.assertNotEqual(ss.special_value, sss.special_value)

        ssss = PickledSingleton()



        self.assertEqual(sss.special_value, ssss.special_value)
        self.assertIs(sss, ssss)

        loader.store(s)
        loader.store(ss)
        loader.store(sss)

        self.assertTrue(os.path.exists(loader.path))
        self.assertTrue(os.path.exists(loader.path + '.1'))
        self.assertTrue(os.path.exists(loader.path + '.2'))
        self.assertTrue(os.path.exists(loader.path + '.3'))


class LoaderTest(ut.TestCase):
    def runTest(self):
        spec = mm.loader.StorageSpec(DATA_VERSION, FILE_PATH)
        spec2 = mm.loader.StorageSpec(DATA_VERSION+1, FILE_PATH)

        if os.path.exists(spec.path):
            os.unlink(spec.path)

        if os.path.exists(spec2.path):
            os.unlink(spec2.path)

        self.assertFalse(os.path.exists(spec.path))

        loader = mm.loader.Loader(make_data, spec)
            
        self.assertEqual(loader.load(), None)

        value = loader.get()
        self.assertEqual(make_data(), value)
        self.assertTrue(os.path.exists(spec.path))

        loader = mm.loader.Loader(make_data, spec)
        self.assertEqual(loader.load(), value)

        self.assertTrue(os.path.exists(spec.path))
        loader = mm.loader.Loader(make_data, spec2)
        self.assertEqual(loader.load(), None)
        self.assertFalse(os.path.exists(spec2.path))

        if os.path.exists(spec.path):
            os.unlink(spec.path)

        if os.path.exists(spec2.path):
            os.unlink(spec2.path)


if __name__ == '__main__':
    ut.main(verbosity=2)

