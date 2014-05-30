#!/usr/bin/python2.7

import mm

import argparse
import sys

MAX_LEN = 7
INV_COL = 0
DIST_COL = 1

def main():
    for line in sys.stdin:
        parts = line.split(', ', 3)
        pfxstr = parts[-1]
        pfxstr = pfxstr.replace('\n','').replace('(','').replace(')','')
        codes = map(lambda i: mm.CODETABLE.CODES[i], map(int, pfxstr.split(', ')))
        codes = map(lambda v: ''.join(map(str, v)), codes)
        print ', '.join(parts[:-1]) + ', (' + ', '.join(codes) + ')'

if __name__ == '__main__':
    main()
