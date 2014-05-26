"""Transformations on Mastermind codes used to implement case-equivalence.
Described in the paper by Koyama and Lai.

See :doc:`Case Equivalence <../casequiv>`
"""

import collections
import itertools
import math

from . import *
from . import singleton as singleton

EMPTY_TUPLE  = tuple()
"""Empty tuple."""

EMPTY_SET  = frozenset()
"""Empty tuple."""

def permutations(v):
    """Yields all permutation of the input tuple ``v``.
    The permuations are strictly by position.  So, a 
    tuple with :math:`n` identical values will still yield
    :math:`n!` permutations.

    :param v: tuple; the algorithm assumes the values are distinct.
    :return: a generator of tuples, each representing a permutation
             of the elements in ``v``.
    """
    if not v:
        yield EMPTY_TUPLE
        return
    n = len(v)
    for i in range(0, n):
        pre, a, post = v[0:i], v[i], v[i+1:]
        tail = pre + post
        first = (a,)
        for p in permutations(tail):
            yield first + p

NamedPermutationPair = collections.namedtuple('NamedPermutationPair',
                                              ['pp', 'cp'])
class Transform(NamedPermutationPair):
    """Transform(pp=<pp>, cp=<cp>)

    A transformation consisting of two permuations, one for positions,
    and one for colors.

    :param pp: position permutation index.
    :type pp: int
    :param cp: color permutation index.
    :type cp: int
    """

    def __new__(cls, **kwargs):
        return NamedPermutationPair.__new__(Transform, 
                                            kwargs['pp'], 
                                            kwargs['cp'])


class TransformTable(object):
    """Transformation table with all transformatons, a singleton."""

    __metaclass__ = singleton.Singleton

    COLORS = tuple(range(CODETABLE.NCOLORS))
    """A tuple enumerating the colors"""

    POSITIONS = tuple(range(CODETABLE.NPOSITIONS))
    """A tuple enumerating the positions"""

    NPOSPERMS = math.factorial(CODETABLE.NPOSITIONS)
    """Count of possible position permutations."""

    NCOLORPERMS = math.factorial(CODETABLE.NCOLORS)
    """Count of possible color permutations."""

    def __init__(self):
        """Initialize contents."""

        self.posperms = tuple(p for p in permutations(self.POSITIONS))
        """All position permutations."""

        self.colorperms = tuple(c for c in permutations(self.COLORS))
        """All color permutations."""

    def apply(self, v, xform):
        """Returns a transformed code.

        :param v: mastermind code, in vector form.
        :type v: tuple or list.
        :param xform: a pair of indexes.
        :type xform:
        :return: transformed mastermind code, in vector form.
        """
        return self.apply_cp(xform.cp, self.apply_pp(xform.pp, v))


    def apply_pp(self, pp, v):
        """Applies the position permutation to the input.

        :param pp: position permutation index.
        :type pp: int
        :param v: a mastermind code in tuple form.
        :type v: tuple or list.
        :return: transformed code in tuple form.
        """
        p = self.posperms[pp]
        return tuple(v[i] for i in p)


    def apply_cp(cp, v):
        """Applies the color permutation to the input.

        :param cp: color permutation index.
        :type cp: int
        :param v: a mastermind code in tuple form.
        :type v: tupe or list.
        :return: transformed code in tuple form.
        """
        p = self.colorperms[cp]
        return tuple(p[i] for i in v)


