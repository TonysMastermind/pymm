import unittest as ut

from mm import *
import mm.xforms as xforms

class IdentityTestTestCase(ut.TestCase):
    def runTest(self):
        t = xforms.TransformTable.IDENTITY
        xftbl = xforms.TransformTable()
        for c in CODETABLE.CODES:
            self.assertEqual(xftbl.apply(t, c), c)

class ReversePPTestCase(ut.TestCase):
    def runTest(self):
        rev = -1
        xftbl = xforms.TransformTable()
        revperm = tuple(reversed(xrange(CODETABLE.NPOSITIONS)))
        for i in xrange(xftbl.NPOSPERMS):
            if xftbl.posperms[i] == revperm:
                rev = i
                break

        t = xforms.Transform(cp=0, pp=rev)
        for c in CODETABLE.CODES:
            r = xftbl.apply(t, c)
            self.assertEqual(tuple(reversed(c)), r)

class InvariantAfterTestCase(ut.TestCase):
    def runTest(self):
        xftbl = xforms.TransformTable()
        inv = xftbl.preserving([])
        self.assertIs(xftbl.ALL, inv)

        seed = xftbl.ALL - frozenset((xftbl.IDENTITY,))
        inv = xftbl.preserving([], seed)
        self.assertIs(seed, inv)

        i1 = inv

        c = 48
        v = CODETABLE.CODES[c]
        inv = xftbl.preserving([c], seed)
        diff = seed - inv
        for t in inv:
            self.assertEqual(v, xftbl.apply(t, v))
        for t in diff:
            self.assertNotEqual(v, xftbl.apply(t, v))

        self.assertEqual(inv, i1 & inv)
        self.assertNotEqual(inv, i1)

class ReprTestCase(ut.TestCase):
    def runTest(self):
        i = xforms.Transform(cp=1, pp=0)
        s = str(i)
        self.assertEqual('mm.xforms.Transform(pp=0, cp=1)', s)

if __name__ == '__main__':
    ut.main(verbosity=2)
