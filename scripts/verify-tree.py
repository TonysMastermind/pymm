from mm import CODETABLE
from mm.partition import PartitionResult
from mm.treewalk import TreeWalker, TreeWalkerContext, play, loadfile

import argparse
from collections import defaultdict
import locale
import os
import sys

class Ctx(TreeWalkerContext):
    def __init__(self, parent, path, root, tree=None):
        super(Ctx, self).__init__(parent, path, root, tree=tree)

        if parent is None:
            self.problem = CODETABLE.ALL
        else:
            score = path[-1][1]
            self.problem = parent.subproblems[score]

        p = PartitionResult(self.problem, self.root)
        self.subproblems = p.parts

        problem_size = self.tree['problem_size']
        stats = self.tree.get('stats')
        optimal = 'n/a'
        if stats:
            optimal = stats.get('optimal', 'n/a')

        if problem_size != len(self.problem):
            print "Problem size mismatch: path:{}, insoln:{}, optimal:{}, stat value:{}, len(problem):{}".format(
                self.path,
                self.tree['in_solution'],
                optimal,
                problem_size,
                len(self.problem))
            return

        children = self.tree.get('children')
        if not children:
            return

        total = 1 if self.tree['in_solution'] else 0
        for t in children.itervalues():
            total += t['problem_size']

        if total != problem_size:
            print "Problem size mismatch: path:{}, insoln:{}, optimal:{}, len(problem):{}, sum over children:{}".format(
                self.path,
                self.tree['in_solution'],
                optimal,
                len(self.problem),
                total)


def action(ctx):
    return True

def main():
    parser = argparse.ArgumentParser()
    parser.add_argument('--input', '-i', help="Input file, default: stdin.",
                        default=None, type=str, dest='fname')

    args = parser.parse_args()
    fname = args.fname

    tw = TreeWalker(action, Ctx)

    tree = loadfile(fname)
    tw.walktree(tree)

if __name__ == '__main__':
    main()
