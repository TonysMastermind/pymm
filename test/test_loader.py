import os
import os.path
import random
import unittest as ut

import mm.loader
import mm.singleton
from mm import *

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
        if os.path.exists(PICKLE_PATH):
            os.remove(PICKLE_PATH)

        loader = mm.loader.Loader(PickledSingleton, PICKLE_SPEC)
        s = loader.get()

        PickledSingleton.clear()

        ss = loader.get()
        sss = PickledSingleton()
        ssss = PickledSingleton()

        self.assertEqual(s.special_value, ss.special_value)
        self.assertEqual(ss.special_value, sss.special_value)
        self.assertEqual(sss.special_value, ssss.special_value)
        self.assertIs(sss, ssss)


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

