import unittest as ut

import mm
import mm.score

class ScoreTableTestCase(ut.TestCase):
    def runTest(self):
        s = mm.score.score(0, mm.CODETABLE.NCODES-1)
        self.assertTrue(mm.score.ScoreTable.exists())

        tbl = mm.score.ScoreTable()
        self.assertIs(mm.score.SCORE_TABLE, tbl)

        t = tbl.SCORES[s]
        self.assertEqual(0, t.exact)
        self.assertEqual(0, t.approx)

        s = tbl.lookup_score(mm.CODETABLE.PERFECT_SCORE)
        self.assertEqual(mm.score.NPOSITIONS, s[0])
        self.assertEqual(0, s[1])

        for i in xrange(mm.CODETABLE.NCODES):
            self.assertEqual(mm.CODETABLE.PERFECT_SCORE, 
                             tbl.score(i, i))



if __name__ == '__main__':
    ut.main(verbosity=2)
