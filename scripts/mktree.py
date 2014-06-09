from mm import *
from mm.strategy import STRATEGIES

import mm.score as score
import mm.xforms as xforms


import argparse
import sys

def initialize():
    score.initialize()
    xforms.initialize()


def parser():
    p = argparse.ArgumentParser(description='Mastermind tree builder.')

    p.add_argument('--strategy', '-s', type=str, 
                   help='Strategy name',
                   action='store', dest='strategy',
                   default=None)

    p.add_argument('--max-depth', '-m', type=int,
                   help='Maximum tree depth',
                   action='store', dest='maxdepth',
                   default=6)

    p.add_argument('--list', '-l',
                   help='List strategies',
                   action='store_true', dest='list_strategies',
                   default=False)

    p.add_argument('--root', '-r', type=int,
                   help='Initial guess',
                   action='store', dest='root',
                   default=None)

    p.add_argument('--output', '-o',
                   help='Output file (json format); default to stdout.',
                   action='store', dest='output',
                   default=None)

    return p

def list_strategies(output=sys.stdout):
    for s in sorted(STRATEGIES.keys()):
        print >>output, s


def main():
    p = parser()
    args = p.parse_args()

    if args.list_strategies:
        list_strategies()
        sys.exit(0)

    if not args.strategy:
        p.print_help(sys.stderr)
        print >>sys.stderr, "Strategy name not specified."
        sys.exit(1)

    s = STRATEGIES.get(args.strategy)
    if not s:
        p.print_help(sys.stderr)
        print >>sys.stderr, "Unknown strategy name: '{}', available names are:".format(args.strategy)
        list_strategies(sys.stderr)
        sys.exit(1)

    if args.maxdepth <= 0:
        print >>sys.stderr, "Tree height constraint must be a positive integer."
        sys.exit(1)

    if args.root is not None and args.root not in CODETABLE.ALL_SET:
        print >>sys.stderr, "Initial guess must be in the range [{}, {}]; input: {}".format(
            0, CODETABLE.NCODES-1, args.root)
        sys.exit(1)

    initialize()

    t = s.build_tree(CODETABLE.ALL, args.maxdepth, args.root)

    if args.output:
        t.to_json_file(args.output)
    else:
        print t.as_json_string()


if __name__ == '__main__':
    main()
