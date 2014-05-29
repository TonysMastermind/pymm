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

    return p

def main():
    class options(object):
        pass

    opt = options()
    p = parser()
    args = p.parse_args(namespace=opt)

    maxlen = args.maxlen
    first = args.initial

    g = distinct.PrefixGen()
    g.skip_non_reducing = True

    for (p, i, d) in g.prefixes(first, maxlen):
        print "{}, {}, {}, {}".format(len(p), len(i), len(d), p) 

if __name__ == '__main__':
    main()
