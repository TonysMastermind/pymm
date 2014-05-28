#!/usr/bin/python

from mm import CODETABLE
import mm.xforms as xf
import mm.distinct as distinct


def main():
    g = distinct.PrefixGen()

    for (p, i) in g.prefixes(7, 4):
        print "%2d" % (len(p), ), ":", p, "[{}]".format(len(i))

if __name__ == '__main__':
    main()
