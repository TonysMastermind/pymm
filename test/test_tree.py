import unittest as ut

from mm import *
import mm.builder as builder
import mm.partition as partition

import json

class TreeTestCase(ut.TestCase):
    def testTreeBuild(self):
        b = builder.TreeBuilder(builder.BuilderStrategy, CODETABLE.ALL, progress=None)
        t = b.build(10, root=8)
        self.verifyTree(t.tree, 10, CODETABLE.ALL)

        d = t.as_dict()
        js = json.dumps(d, skipkeys=True, check_circular=True, indent=2, sort_keys=True)
        ts = t.as_json_string()

        t.to_json_file('/dev/null')

        self.assertEqual(js, ts)

        t = t.tree
        js = json.dumps(t.as_dict(), skipkeys=True, check_circular=True, indent=2, sort_keys=True)
        ts = t.as_json_string()

        s = str(t.stats)
        self.assertGreater(s.find(str(CODETABLE.NCODES)), 0)

    def testCantBuild(self):
        b = builder.TreeBuilder(builder.BuilderStrategy, CODETABLE.ALL, progress=None)
        t = b.build(3, root=8)
        self.assertIs(None, t.tree)


    def testDescription(self):
        b = builder.TreeBuilder(builder.BuilderStrategy, CODETABLE.ALL, progress=None)
        d = b.description()
        self.assertGreater(d.find(str(CODETABLE.NCODES)), 0)


    def verifyTree(self, tree, remaining, problem):
        self.assertEqual(len(problem), tree.stats.problem_size)
        self.assertLess(0, remaining)
        
        pr = partition.PartitionResult(problem, tree.root)

        child_sizes = list(child.stats.problem_size for child in tree.children if child)
        total_sizes = sum(child_sizes)
        if tree.root_in_solution:
            total_sizes += 1
            child_sizes .append(1)

        child_sizes = tuple(reversed(sorted(child_sizes)))

        self.assertEqual(len(problem), total_sizes)
        self.assertEqual(pr.stats.in_solution, tree.root_in_solution)
        self.assertEqual(pr.stats.optimal, tree.stats.optimal)
        self.assertEqual(pr.sorted_sizes, child_sizes)

        for (score, child) in enumerate(tree.children):
            self.assertTrue( ((not pr.parts[score]) and (not child)) 
                             or
                             (pr.parts[score] and child)
                             or
                             (score == CODETABLE.PERFECT_SCORE and pr.stats.in_solution)
                             )

            if child:
                self.assertEqual(len(pr.parts[score]), child.stats.problem_size)
                self.verifyTree(child, remaining-1, pr.parts[score])


if __name__ == '__main__':
    ut.main(verbosity=2)
