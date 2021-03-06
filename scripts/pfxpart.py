#!/usr/bin/python2.7

from mm import CODETABLE
import mm.distinct as distinct
import mm.partition as partition

import argparse
import math
import sys

PREFIX_LENGTH = 2
FLOAT_FUZZ = sys.float_info.epsilon * 16
MARKERS = { True: '*', False: ' ' }

def printablecode(c):
    return str(CODETABLE.CODES[c])

def hdrs():
    print "prefix           ndistinct total count  max  min   mean    entropy     stddev   sorted sizes"
    print "================ ========= ===== ===== ==== ==== ======== ========== ========== ======================"

def main():
    p = argparse.ArgumentParser()
    p.add_argument('--first', '-i', help='Initial code',
                   default=8, # [2100]
                   type=int, action='store', dest='first')

    args = p.parse_args()
    first = args.first

    pgen = distinct.PrefixGen()
    
    prefixes = tuple((p, len(d)) for (p, _, d) in pgen.prefixes(first, PREFIX_LENGTH))
    pfx0 = prefixes[0]
    prefixes = sorted(prefixes[1:], lambda a, b: cmp(b[1], a[1]))

    pr0 = partition.PartitionResult(CODETABLE.ALL, first)
    s0 = pr0.stats

    subproblems = map(tuple, sorted(filter(lambda l: len(l) > 1, pr0.parts),
                                    lambda a, b: cmp(len(b), len(a))))

    results = { 
        (pfx, prob): partition.PartitionResult(prob, pfx[0][1])
        for pfx in prefixes 
        for prob in subproblems 
        }

    

    hdrs()
    print "(%s) %9d %5d %4d%s %3d%s %4d %8.3f %9.3f%s %9.3f%s %s" % \
        (printablecode(first) + '  ' + (' ' * len(printablecode(first))),
         pfx0[1],
         s0.total,
         s0.n, ' ',
         s0.largest, ' ',
         s0.smallest,
         s0.mean,
         s0.entropy, ' ',
         math.sqrt(s0.variance), ' ',
         str(pr0.sorted_sizes))

    print "----"
    for prob in subproblems:
        subset = (results[(pfx, prob)] for pfx in prefixes)

        subset = sorted(subset, lambda a, b: cmp(b.stats.n, a.stats.n))
        n_max = subset[0].stats.n
        for r in subset:
            if r.stats.n < n_max:
                r.stats.max_partitions = False
            else:
                r.stats.max_partitions = True

        subset = sorted(subset, lambda a, b: cmp(a.stats.variance, b.stats.variance))
        variance_min = subset[0].stats.variance
        for r in subset:
            if (r.stats.variance + FLOAT_FUZZ) > variance_min:
                r.stats.min_variance = False
            else:
                r.stats.min_variance = True


        subset = sorted(subset, lambda a, b: cmp(b.stats.entropy, a.stats.entropy))
        entropy_max = subset[0].stats.entropy
        for r in subset:
            if (r.stats.entropy + FLOAT_FUZZ) < entropy_max:
                r.stats.max_entropy = False
            else:
                r.stats.max_entropy = True


        subset = sorted(subset, lambda a, b: cmp(a.stats.largest, b.stats.largest))
        largest_min = subset[0].stats.largest
        for r in subset:
            if r.stats.largest > largest_min:
                r.stats.min_largest = False
            else:
                r.stats.min_largest = True

        ordered_prefixes = sorted(prefixes,
                                  lambda a, b:
                                      cmp(results[(b, prob)].stats.max_partitions,
                                          results[(a, prob)].stats.max_partitions) or \
                                      cmp(results[(b, prob)].stats.min_largest,
                                          results[(a, prob)].stats.min_largest) or \
                                      cmp(results[(b, prob)].stats.max_entropy,
                                          results[(a, prob)].stats.max_entropy) or \
                                      cmp(results[(b, prob)].stats.n, results[(a, prob)].stats.n) or \
                                      cmp(results[(a, prob)].stats.largest, results[(b, prob)].stats.largest) or \
                                      cmp(results[(b, prob)].stats.entropy, results[(a, prob)].stats.entropy) or \
                                      cmp(results[(a, prob)].stats.variance, results[(b, prob)].stats.variance) or \
                                      cmp(b[1], a[1]))


        hdrs()
        for pfx in ordered_prefixes:
            (p, ndistinct) = pfx
            pr = results[(pfx, prob)]
            s = pr.stats
            print "(%s) %9d %5d %4d%s %3d%s %4d %8.3f %9.3f%s %9.3f%s %s" % \
                (', '.join(map(printablecode, p)),
                 ndistinct,
                 s.total,
                 s.n, MARKERS[s.max_partitions],
                 s.largest, MARKERS[s.min_largest],
                 s.smallest,
                 s.mean,
                 s.entropy, MARKERS[s.max_entropy],
                 math.sqrt(s.variance), MARKERS[s.min_variance],
                 str(pr.sorted_sizes))
        print "----"



if __name__ == '__main__':
    main()
