import unittest as ut

import mm

class CodeTableTestCase(ut.TestCase):
    def runTest(self):
        mm.initialize_logging()
        tbl = mm.CODETABLE

        v = tbl.decode(0)
        self.assertEqual((0,0,0,0), v)

        v = tbl.decode(51)
        self.assertEqual((3,2,1,0), v)

        c = tbl.encode([3,2,1,0])
        self.assertEqual(51, c)

        c = tbl.encode((3,2,1,1))
        self.assertEqual(51+216, c)

        s = tbl.encode_score(4, 0)
        self.assertEqual(tbl.PERFECT_SCORE, s)


class ExceptionsTestCase(ut.TestCase):
    def runTest(self):
        tbl = mm.CODETABLE

        
        self.assertRaises(mm.Exception, tbl.decode, -1)
        self.assertRaises(mm.Exception, tbl.decode, tbl.NCODES)

        prefix = (0,) * (tbl.NPOSITIONS - 1)
        self.assertRaises(mm.Exception, tbl.encode, prefix)
        self.assertRaises(mm.Exception, tbl.encode, prefix + (0, 0))
        self.assertRaises(mm.Exception, tbl.encode, prefix + (-1,))
        self.assertRaises(mm.Exception, tbl.encode, prefix + (tbl.NCOLORS,))

if __name__ == '__main__':
    ut.main(verbosity=2)
