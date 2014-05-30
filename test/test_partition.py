import unittest as ut

from mm import *
import mm.partition as partition
import mm.score as score

class PartitionResultTestCase(ut.TestCase):
    def test_TopLevelSplit(self):
        all = CODETABLE.ALL

        pr = partition.PartitionResult(all, 0)
        self.assertEqual((625, 500, 150, 20, 1), pr.sorted_sizes)

        s = pr.stats
        self.assertTrue(s.in_solution)
        self.assertEqual(625, s.largest)
        self.assertEqual(1, s.smallest)
        self.assertEqual(CodeTable.NCODES, s.total)
        self.assertEqual(5, s.n)

        pr = partition.PartitionResult(all, 1)
        self.assertEqual((317, 308, 256, 156, 123, 61, 27, 24, 20, 3, 1),
                         pr.sorted_sizes)

        s = pr.stats
        self.assertTrue(s.in_solution)
        self.assertEqual(317, s.largest)
        self.assertEqual(1, s.smallest)
        self.assertEqual(CodeTable.NCODES, s.total)
        self.assertEqual(11, s.n)


        pr = partition.PartitionResult(all, 7)
        self.assertEqual((256, 256, 256, 208, 114, 96, 36, 32, 20, 16, 4, 1, 1),
                         pr.sorted_sizes)

        s = pr.stats
        self.assertTrue(s.in_solution)
        self.assertEqual(256, s.largest)
        self.assertEqual(1, s.smallest)
        self.assertEqual(CodeTable.NCODES, s.total)
        self.assertEqual(13, s.n)
        self.assertEqual(13, s.as_dict()['n'])

        self.assertLess(0, str(s).find('count:'))
        sig = pr.signature
        self.assertEqual((1, (256, 256, 256, 208, 114, 96, 36, 32, 20, 16, 4, 1, 1)),
                         sig)

        sig = pr.long_signature
        self.assertEqual(1, sig[0])
