#!/usr/bin/python

from mm import CODETABLE
import mm.xforms as xf
import mm.distinct as distinct

import argparse
import sys

def parser():
    p = argparse.ArgumentParser(description='Enumerate Mastermind prefixes.')
    p.add_argument('--initial', '-i', type=int, dest='initial',
                   help='Initial code in the prefix.',
                   action='store', default=8)
    p.add_argument('--maxlen', '-m', type=int, dest='maxlen',
                   help='Maximum prefix length.',
                   action='store', default=3)

    p.add_argument('--skip-non-reducing', '-o', 
                   help='Optimize',
                   action='store_true',
                   dest='skip_non_reducing')

    p.add_argument('--allow-non-reducing', '-a', 
                   help='Do not optimize.',
                   action='store_false',
                   dest='skip_non_reducing')

    return p

def main():
    class options(object):
        def __init__(self):
            self.skip_non_reducing = True

    opt = options()

    p = parser()
    args = p.parse_args(namespace=opt)

    maxlen = args.maxlen
    first = args.initial

    g = distinct.PrefixGen()
    g.skip_non_reducing = args.skip_non_reducing

    for (p, i, d) in g.prefixes(first, maxlen):
        print "{}, {}, {}, {}".format(len(p), len(i), len(d), p) 

if __name__ == '__main__':
    main()
