#!/usr/bin/python

from mm import CODETABLE
import mm.xforms as xf
import mm.distinct as distinct

import sys

def main():
    maxlen = 3
    if len(sys.argv) > 1:
        maxlen = int(sys.argv[1])

    g = distinct.PrefixGen()

    for (p, i, d) in g.prefixes(7, maxlen):
        print "{}, {}, {}, {}".format(len(p), len(i), len(d), p) 

if __name__ == '__main__':
    main()
