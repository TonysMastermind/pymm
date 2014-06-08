from mm import CODETABLE
from mm.partition import PartitionResult
from mm.treewalk import TreeWalker, TreeWalkerContext, play, loadfile
from mm.xforms import TransformTable
from mm.distinct import PrefixGen

import argparse
from collections import defaultdict
import locale
import os
import sys

PFXGEN = None

ALL_PREFIXES = set()
PREFIX_USE_COUNT = defaultdict(int)
SEEN = set()
LENGTH_SIZE_MAP = defaultdict(lambda: defaultdict(int))
XFTBL = TransformTable()

RECORDS = []
MAX_PFX_LEN = 0
PRINTED_PFX_LEN = 0

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

        self.distinct_followers = None
        self.preserving = None
        if self.parent:
            self.preserving = XFTBL.preserving(self.prefix, parent.preserving)
        else:
            self.preserving = XFTBL.preserving(self.prefix, XFTBL.ALL)

        self.distinct_followers = PFXGEN.distinct_subset(self.preserving, CODETABLE.ALL, self.prefix)
        self.distinct_followers_in_problem = PFXGEN.distinct_subset(self.preserving, self.problem,
                                                                    self.prefix)
        self.reduced_followers = PFXGEN.reduce_codeset(self.preserving, self.problem, self.prefix)

        fp = frozenset(self.problem)
        if self.distinct_followers_in_problem != self.reduced_followers:
            print >>sys.stderr, "Different reductions at {}; {} {}".format(
                self.prefix, 
                len(self.problem),
                len(self.reduced_followers & fp))

        if len(self.reduced_followers & fp) != len(self.reduced_followers):
            print >>sys.stderr, "Reduced dropped some items at {}.".format(prefix)


def pad(s, c):
    delta = max(0, c[1] - len(s))
    padding = ' ' * delta
    if c[2] == 'l':
        return padding + s
    else:
        return s + padding


def format_prefix(p):
    s = str(p)
    s += ' ' * (PRINTED_PFX_LEN - len(s))
    return s

def action(ctx):
    global ALL_PREFIXES
    global PREFIX_USE_COUNT
    global SEEN
    global MAX_PFX_LEN
    global RECORDS

    tree = ctx.tree
    path = ctx.path
    cpfx = ctx.prefix

    psize = tree['problem_size']
    if psize <= 2:
        return False

    children = tree.get('children')
    subsizes = []
    if children:
        subsizes = map(lambda t: t['problem_size'], children.itervalues())
        mx = max(subsizes)
    else:
        children = {}
        mx = 0

    vpfx = tuple(map(lambda c: CODETABLE.CODES[c], cpfx))

    inv = ctx.preserving
    i0 = None
    if ctx.parent:
        i0 = ctx.parent.preserving
    else:
        i0 = XFTBL.ALL

    nd_in = len(ctx.distinct_followers_in_problem)
    nd_all = len(ctx.distinct_followers)

    pp = path
    if not pp in SEEN:
        ALL_PREFIXES.add(vpfx)
        PREFIX_USE_COUNT[vpfx] += 1
        SEEN.add(pp)
        MAX_PFX_LEN = max(len(vpfx), MAX_PFX_LEN)

    insoln = tree['in_solution']
    RECORDS.append((vpfx, insoln, (mx == 1), len(children), psize, mx, len(inv), nd_in, nd_all))

    return True

class Summary(object):
    def __init__(self, tree):
        games = map(lambda c: play(c, tree), CODETABLE.ALL)
        self.maxlen = max(map(len, games))
        self.moves = sum(map(len, games))

    def mean_game(self):
        return float(self.moves)/CODETABLE.NCODES

    def longest_game(self):
        return self.maxlen


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument('--input', '-i', help="Input file, default: stdin.",
                        default=None, type=str, dest='fname')

    args = parser.parse_args()
    if args.fname:
        args.title = 'Tree analysis for ' + args.fname
    else:
        args.title = 'Tree analysis process ' + str(os.getpid())

    legend = '(\\$: problem size <= possible scores, \\+: optimal split, \\*: root code not a solution.)'
    title = args.title

    fname = args.fname

    global PFXGEN
    PFXGEN = PrefixGen()
    PFXGEN.skip_non_reducing = True

    tw = TreeWalker(action, Ctx)

    tree = loadfile(fname)
    tw.walktree(tree)
    summary = Summary(tree)

    global PRINTED_PFX_LEN
    PRINTED_PFX_LEN = (len(str(CODETABLE.CODES[0]))+2) * MAX_PFX_LEN + 2

    columns = (
        ('prefix', PRINTED_PFX_LEN, 'r'),
        ('flags', max(len('flags'), 6), 'l'),
        ('#children', max(len('#children'), 6), 'l'),
        ('problem size', max(len('problem size'), 6), 'l'),
        ('max subproblem', max(len('max subproblem'), 6), 'l'),
        ('#preserving', max(len('#preserving'), 6), 'l'),
        ('#distinct/in', max(len('#distinct/in'), 4), 'l'),
        ('#distinct/all', max(len('#distinct/all'), 4), 'l'))

    separator = ' '.join(map(lambda c: '=' * c[1], columns))

    header = ' '.join(map(lambda c: pad(c[0], c), columns))

    formats = ("%s", "%s", "%5d", "%5d", "%5d", "%6d", "%4d", "%4d")

    locale.setlocale(locale.LC_ALL, 'en_US')

    print title
    print '=' * len(title)
    print "\nAverage game: {:.4f} moves, Longest game: {} moves\n\n".format(
        summary.mean_game(), 
        locale.format("%d", summary.longest_game(), grouping=True))

    print """.. table:: Prefix properties of a game tree %s
  :widths: %s
  :column-wrapping: %s
  :column-alignment: %s
  :column-dividers: %s

""" % (legend,
       ('1 ' * len(columns)),
       ('false' + ' true' * len(columns[1:])),
       ('left' + ' right' * len(columns[1:])),
       'single' + ' single' * len(columns))


    print '  ' + separator
    print '  ' + header
    print '  ' + separator

    for r in sorted(RECORDS, lambda a, b: cmp(len(a[0]), len(b[0])) or cmp(a[0], b[0]) or cmp(b[4], a[4])):
        (pfx, insoln, optimal, nchildren, psize, maxprob, ninv, nd_in, nd_all) = r
        fields = (format_prefix(pfx),
                  ''.join((('\\$' if psize <= CODETABLE.NSCORES else ''), 
                           ('' if insoln else '\\*'), ('\\+' if optimal else ''))),
                  nchildren,
                  psize,
                  maxprob,
                  ninv,
                  nd_in,
                  nd_all)

        printable = map(lambda i: locale.format(i[0], i[1], grouping=True), zip(formats, fields))
        printable = map(lambda i: pad(i[0], i[1]), zip(printable, columns))
        print '  ' + (' '.join(printable))

    print '  ' + separator

if __name__ == '__main__':
    main()
