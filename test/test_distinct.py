import unittest as ut

from mm import *
import mm.distinct as distinct
import mm.xforms as xforms

import sys

class IdentityTestTestCase(ut.TestCase):
    def testTopLevel(self):
        pgen = distinct.PrefixGen()
        prefixes = map(lambda x: x[0], pgen.prefixes(8, 1))
        self.assertEqual([(8,)], prefixes)

    def testDistinctAfter(self):
        pgen = distinct.PrefixGen()
        observed = pgen.distinct_after((8,))
        inv = pgen.xftbl.invariant_after((8,))
        expected = set()
        for v in pgen.xftbl.CODESET - frozenset((CODETABLE.CODES[8],)):
            c = min(map(lambda v: CODETABLE.encode(v), 
                        map(lambda xf: pgen.xftbl.apply(xf, v), inv)))
            expected.add(c)
        expected -= set((8,))
        expected = frozenset(expected)
        self.assertEqual(expected, observed)

        prefix_data = tuple(pgen.prefixes(8, 2))
        followers = (x[0][1] for x in prefix_data[1:])
        for f in followers:
            self.assertIn(f, observed)
            self.assertIn(f, expected)

    def testPrefixesWithNonReducing(self):
        pgen = distinct.PrefixGen()
        observed = pgen.distinct_after((8,))
        inv = pgen.xftbl.invariant_after((8,))
        expected = set()
        for v in pgen.xftbl.CODESET - frozenset((CODETABLE.CODES[8],)):
            c = min(map(lambda v: CODETABLE.encode(v), 
                        map(lambda xf: pgen.xftbl.apply(xf, v), inv)))
            expected.add(c)
        expected -= set((8,))
        expected = frozenset(expected)
        self.assertEqual(expected, observed)

        prefix_data = tuple(pgen.prefixes(8, 2))
        followers = (x[0][1] for x in prefix_data[1:])
        for f in followers:
            self.assertIn(f, observed)
            self.assertIn(f, expected)

        pgen.skip_non_reducing = True
        prefix_data = tuple(pgen.prefixes(8, 2))
        followers = (x[0][1] for x in prefix_data[1:])
        for f in followers:
            self.assertIn(f, observed)
            self.assertIn(f, expected)
        


if __name__ == '__main__':
    ut.main(verbosity=2)
