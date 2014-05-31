# -*- python -*-
"""Handles the partitioning of code sets by their score against a specified
code, called the root code.
"""

import math
import sys

from . import *
from . import score as score

PERFECT_SCORE = CodeTable.PERFECT_SCORE
NSCORES = CodeTable.NSCORES

def safelog(n):
    """Safe logarithm calcuation.  Returns 0 for non-positive inputs.

    :param n: a number.
    :return: binary logarithm of :math:`n` when :math:`n` is positive, zero otherwise.
    """
    if n > 0:
        return math.log(n, 2)
    return 0


class Stats(object):
    """Basic partitition stats."""

    def __init__(self, sizes, perfect):
        """Construct sats from a size vector.

        :param sizes: sizes of the partitions, indexed by numeric score.
        :type sizes: list.
        :param perfect: size of the perfect score partition.
        :type perfect: int.
        """
        total  = sum(sizes)
        count  = sum(1 if n > 0 else 0 for n in sizes)
        totsq  = sum(n*n for n in sizes)
        mean   = float(total)/count
        var    = float(totsq)/count - mean*mean
        if var < 0: var = 0.0 # in case of rounding issues.
        s_xlgx = sum(float(n) * safelog(n) for n in sizes)
        ntrpy  = safelog(total) - s_xlgx/total
        if abs(ntrpy) <= sys.float_info.epsilon*4:
            ntrpy = 0
        mx = max(sizes)
        mn = min((n if n > 0 else mx) for n in sizes)

        self.totsq = totsq
        """Sum of squares, used in the Irving strategy."""

        self.total = total
        """Sum of sizes."""

        self.n = count
        """number of non-zero sizes."""

        self.mean = mean
        """average size."""

        self.variance = var
        """variance."""

        self.entropy = ntrpy
        """entropy of the distribution."""

        self.largest  = mx
        """size of smallest non-empty partition."""

        self.smallest = mn
        """size of largest partition."""

        self.optimal = (mx == 1) and (total > 2)
        """True when the partitionning result is optimal."""

        self.in_solution = (perfect != 0)
        """True when the partitionning result contains a non-empty
        partition for the perfect score."""

        self.degenerate = self.total > 2 and self.n == 1
        """True when the partitionning result has only one partition,
        when the input set has 2 or more members."""

    def as_dict(self):
        """:return: a dictionary representation of the stats."""
        return dict((k, getattr(self, k)) \
                        for k in ['n', 'variance',
                                  'total',
                                  'smallest', 'largest',
                                  'entropy', 'in_solution',
                                  'optimal', 'degenerate'])

    def __repr__(self):
        """Printable (informal) string format.

        :return: printable representation of the stats.
        """
        b = super(Stats, self).__repr__()
        d = ("-----------------------------\n" +
             "  sum:{:5d};    mean: {:7.3f}\n" + 
             "count:{:5d};   sigma: {:7.3f}\n" +
             "  min:{:5d}; entropy: {:7.3f}\n" +
             "  max:{:5d};\n"    +
             "    optimal: {}\n" +
             " degenerate: {}\n" +
             "in_solution: {}\n" +
             "-----------------------------\n"). \
             format(self.total,
                    self.mean,
                    self.n,
                    math.sqrt(self.variance),
                    self.smallest,
                    self.entropy,
                    self.largest,
                    self.optimal,
                    self.degenerate,
                    self.in_solution)
        return b + "\n" + d


class PartitionResult(object):
    """Parition result. Groups a set of codes by their scores
    against a *root* code.
    """

    def __init__(self, codes, rootcode):
        """Constructs the partition result, and calculates the stats.

        :param codes: a set of codes, in numeric encoding.
        :param rootcode: code against which to split the code set.
        """

        self.root = rootcode
        """Root code; the codes are partition by score against the root code."""

        p = tuple([] for i in range(0, NSCORES))
        for c in codes:
            s = score.score(c, rootcode)
            p[s].append(c)

        self.parts = p
        """The partitions, an array indexable by score."""

        self.sizes = tuple(len(x) for x in p)
        """The sizes of the partitions, indexable by score."""

        n = sum(1 if sz > 0 else 0 for sz in self.sizes)
        ss = tuple(reversed(sorted(self.sizes)))[:n]

        self.sorted_sizes = ss
        """Sizes of non-empty partitions, in descending order."""

        self.stats = Stats(ss, self.sizes[0])
        """Paritionning stats; see :py:class:`.Stats`"""

        # from old C++;
        #   <root-in-soln>:<sizes in descending order>
        self.signature = (self.sizes[0], self.sorted_sizes)
        """Short structural signature of result.

        A summary of the partition result structure with two items:

          * a boolean indicating whether the root code is a member of the
            input code set.
          * the sorted size list in descending order.
        """

        self._long_signature = None

        if len(codes) <= 2:
            self._long_signature = self.signature 


    @property
    def long_signature(self):
        """From old C++ implementation (ca. 2005)

        :return: long signature.

        For problem size <=2, use regular signature.  Otherwise:

          * <root-membership>:<long-entry>:...:<short-entry>:...
          * <root-membership> is 0 or 1.
          * <long-entry> is a pair (score, size), used for size > 2.
          * <short-entry> is just size, for size == 1 or 2.

        The long signature summarizes the structure of the partitionning
        result by enumerating the sizes *and* the score of each non empty 
        parition.
        """
        if self._long_signature is not None:
            return self._long_signature

        big, one, two = [], [], []
        for score in range(0, NSCORES):
            n = self.sizes[score]
            if n > 2:
                big.append((score, n))
            elif n == 2:
                two.append(n)
            elif n == 1:
                one.append(n)

        lsig = (self.sizes[PERFECT_SCORE], ) + \
            tuple(big) + tuple(two) + tuple(one)
        self._long_signature = lsig

        return self._long_signature
