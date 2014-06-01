import unittest as ut

from mm import *
import mm.distinct as distinct
import mm.xforms as xforms

class IdentityTestTestCase(ut.TestCase):
    def testTopLevel(self):
        pgen = distinct.PrefixGen()
        prefixes = frozenset(pgen.prefixes, 1)
        


if __name__ == '__main__':
    ut.main(verbosity=2)
