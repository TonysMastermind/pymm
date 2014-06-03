#!/usr/bin/python2.7

import sys

class Summary(object):
    def __init__(self, name):
        self.name = name
        self.count = 0
        self.min = 0
        self.max = 0
        self.sum = 0

    def add(self, v):
        self.count += 1
        self.sum += v

        if self.count == 1:
            self.min = self.max = v
        else:
            self.min = min(v, self.min)
            self.max = max(v, self.max)


    @property
    def avg(self):
        if self.count:
            return self.sum / 1.0 / self.count
        return 0


    def __repr__(self):
        return '{}(name={}, count={}, min={}, max={}, avg={})'.format(
            self.__class__.__name__, self.name,
            self.count, self.min, self.max, self.avg)


MAX_LEN = 7
INV_COL = 0
DIST_COL = 1

def main():
    colnames = ['n(preserving)', 'n(distinct)']

    summaries = [None] + \
        [ [Summary("{}.{}".format(i, nm)) for nm in colnames]
          for i in range(1, MAX_LEN+1) ]

    counts = [0] * (MAX_LEN+1)

    for line in sys.stdin:
        (pfxlen, n_inv, n_dist) = map(int, line.split(', ', 3)[0:3])
        counts[pfxlen] += 1
        if pfxlen > MAX_LEN:
            print >>sys.stderr, "Ignoring prefix length: ", pfxlen
        else:
            summaries[pfxlen][INV_COL].add(n_inv)
            summaries[pfxlen][DIST_COL].add(n_dist)

    for (i, row) in zip(range(MAX_LEN+1), summaries):
        if not counts[i]:
            continue

        for s in row:
            print s

if __name__ == '__main__':
    main()
