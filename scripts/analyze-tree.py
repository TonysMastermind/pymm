from mm import CODETABLE
from mm.treewalk import TreeWalker
from mm.xforms import TransformTable

import argparse
from collections import defaultdict
import locale
import os
import sys

ALL_PREFIXES = set()
PREFIX_USE_COUNT = defaultdict(int)
SEEN = set()
LENGTH_SIZE_MAP = defaultdict(lambda: defaultdict(int))
XFTBL = TransformTable()
PRESERVING = {}

RECORDS = []
MAX_PFX_LEN = 0
PRINTED_PFX_LEN = 0

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

    inv = PRESERVING.get(cpfx)
    if not inv:
        if cpfx:
            i0 = PRESERVING.get(cpfx[:-1])
            inv = XFTBL.preserving((cpfx[-1],), i0)
            PRESERVING[cpfx] = inv
        else:
            PRESERVING[cpfx] = XFTBL.ALL
            inv = XFTBL.ALL

    pp = path[:-1]
    if not pp in SEEN:
        ALL_PREFIXES.add(vpfx)
        PREFIX_USE_COUNT[vpfx] += 1
        SEEN.add(pp)
        MAX_PFX_LEN = max(len(vpfx), MAX_PFX_LEN)

    insoln = tree['in_solution']
    RECORDS.append((vpfx, insoln, (mx == 1), len(children), psize, mx, len(inv)))

    return True


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

    tw = TreeWalker(action)

    tw.walkfile(fname)

    global PRINTED_PFX_LEN
    PRINTED_PFX_LEN = (len(str(CODETABLE.CODES[0]))+2) * MAX_PFX_LEN + 2

    columns = (
        ('prefix', PRINTED_PFX_LEN, 'r'),
        ('flags', max(len('flags'), 6), 'l'),
        ('#children', max(len('#children'), 6), 'l'),
        ('problem size', max(len('problem size'), 6), 'l'),
        ('max subproblem', max(len('max subproblem'), 6), 'l'),
        ('#preserving', max(len('#preserving'), 6), 'l'))

    separator = ' '.join(map(lambda c: '=' * c[1], columns))

    header = ' '.join(map(lambda c: pad(c[0], c), columns))

    formats = ("%s", "%s", "%5d", "%5d", "%5d", "%6d")

    locale.setlocale(locale.LC_ALL, 'en_US')

    print title
    print '=' * len(title)
    print ""

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

    for r in sorted(RECORDS, lambda a, b: cmp(a[0], b[0]) or cmp(b[4], a[4])):
        (pfx, insoln, optimal, nchildren, psize, maxprob, ninv) = r
        fields = (format_prefix(pfx),
                  ''.join((('\\$' if psize <= CODETABLE.NSCORES else ''), 
                           ('' if insoln else '\\*'), ('\\+' if optimal else ''))),
                  nchildren,
                  psize,
                  maxprob,
                  ninv)

        printable = map(lambda i: locale.format(i[0], i[1], grouping=True), zip(formats, fields))
        printable = map(lambda i: pad(i[0], i[1]), zip(printable, columns))
        print '  ' + (' '.join(printable))

    print '  ' + separator

if __name__ == '__main__':
    main()
