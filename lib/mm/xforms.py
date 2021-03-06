"""Transformations on Mastermind codes used to implement case-equivalence.
Described in the paper by Koyama and Lai.

See :doc:`Case Equivalence <../casequiv>`
"""

from . import *
from . import loader as loader
from . import singleton as singleton

import collections
import itertools
import math



EMPTY_TUPLE  = tuple()
"""Empty tuple."""

EMPTY_SET  = frozenset()
"""Empty tuple."""

VERSION = 1
STORAGE_PATH = 'var/xftable'

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
    """Transform.new(pp=<pp>, cp=<cp>)

    A transformation consisting of two permuations, one for positions,
    and one for colors.

    :param pp: position permutation index.
    :type pp: int
    :param cp: color permutation index.
    :type cp: int
    """

    def __new__(cls, **kwargs):
        """Creates an instance of the class.

        :param kwargs: keyword args.  Must include the names ``pp`` and ``cp``.
        :return: instance of :py:class:`.Transform`.
        """
        return NamedPermutationPair.__new__(cls,
                                            kwargs['pp'],
                                            kwargs['cp'])

    def __repr__(self):
        return "{}.{}(pp={}, cp={})".format(
            self.__class__.__module__,
            self.__class__.__name__, 
            self.pp, self.cp)


class TransformTable(singleton.SingletonBehavior):
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

    IDENTITY = Transform(cp=0, pp=0)
    """The identity transformation."""


    CODESET = frozenset(CODETABLE.CODES)
    """All codes, in vector form, as a set."""

    ALL = None
    """All transformations."""

    def __init__(self):
        """Initialize contents."""

        self.posperms = tuple(p for p in permutations(self.POSITIONS))
        """All position permutations."""

        self.colorperms = tuple(c for c in permutations(self.COLORS))
        """All color permutations."""

        self.ALL = frozenset(Transform(pp=pp, cp=cp)
                             for pp in xrange(self.NPOSPERMS)
                             for cp in xrange(self.NCOLORPERMS))

        TransformTable.ALL = self.ALL


    def apply(self, xform, v):
        """Returns a transformed code.

        :param v: mastermind code, in vector form.
        :type v: tuple or list.
        :param xform: a pair of indexes.
        :type xform: :py:class:`.Transform`
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


    def apply_cp(self, cp, v):
        """Applies the color permutation to the input.

        :param cp: color permutation index.
        :type cp: int
        :param v: a mastermind code in tuple form.
        :type v: tupe or list.
        :return: transformed code in tuple form.
        """
        p = self.colorperms[cp]
        return tuple(p[i] for i in v)


    def preserving(self, prefix, seed=None):
        """Transformations that do not vary a mastermind code.

        Recommend for use with the initial code in a solution, 
        then using the result to find case-distinct followers
        with increasing length prefixes.

        :param prefix: mastermind code prefix, in encoded form.
        :type c: iterable of int
        :param seed: initial set of transforms to start with; defaults to
          :py:attr:`.TransformTable.ALL` when input is ``None``.
        :type seed: iterable of :py:class:`.Transform`.
        :return: a set of :py:class:`.Transform` objects that do
          not change any element of ``prefix``.
        """
        inv = seed
        if inv is None:
            inv = self.ALL

        minlen = 0
        if self.IDENTITY in inv:
            minlen = 1

        for c in prefix:
            v = CODETABLE.CODES[c]
            inv = frozenset(t for t in inv if self.apply(t, v) == v)
            if len(inv) <= minlen:
                return inv

        return inv


class TransformLookupTable(singleton.SingletonBehavior):
    """Transformation table with all transformatons, a singleton, using numeric
    codes."""

    __metaclass__ = singleton.Singleton


    COLORS = tuple(range(CODETABLE.NCOLORS))
    """A tuple enumerating the colors"""

    POSITIONS = tuple(range(CODETABLE.NPOSITIONS))
    """A tuple enumerating the positions"""

    NPOSPERMS = math.factorial(CODETABLE.NPOSITIONS)
    """Count of possible position permutations."""

    NCOLORPERMS = math.factorial(CODETABLE.NCOLORS)
    """Count of possible color permutations."""

    IDENTITY = Transform(cp=0, pp=0)
    """The identity transformation."""


    CODESET = frozenset(CODETABLE.ALL)
    """All codes, in numeric form, as a set."""


    POS_LOOKUP_TABLE = None
    """Position permutation lookup table; use as ``POS_LOOKUP_TABLE[code][permindex]``."""


    COLOR_LOOKUP_TABLE = None
    """Color permutation lookup table; use as ``COLOR_LOOKUP_TABLE[code][permindex]``."""


    ALL = None
    """All transformations."""

    def __init__(self):
        self.xftbl = TransformTable()

        TransformLookupTable.POS_LOOKUP_TABLE = tuple(
            tuple(CODETABLE.encode(self.xftbl.apply_pp(i, CODETABLE.CODES[c]))
                  for i in xrange(self.NPOSPERMS))
            for c in CODETABLE.ALL)

        TransformLookupTable.COLOR_LOOKUP_TABLE = tuple(
            tuple(CODETABLE.encode(self.xftbl.apply_cp(i, CODETABLE.CODES[c]))
                  for i in xrange(self.NCOLORPERMS))
            for c in CODETABLE.ALL)

        TransformLookupTable.ALL = self.xftbl.ALL

        self.POS_LOOKUP_TABLE = TransformLookupTable.POS_LOOKUP_TABLE
        self.COLOR_LOOKUP_TABLE = TransformLookupTable.COLOR_LOOKUP_TABLE
        self.ALL = TransformLookupTable.ALL


    def apply(self, t, c):
        """Applies the information to the numeric code.

        :param t: a transformation.
        :type t: :py:class:`.Transform`
        :param c: mastermind code in numeric form.
        :return: a number representing the transformed code.
        """
        return self.POS_LOOKUP_TABLE[self.COLOR_LOOKUP_TABLE[c][t.cp]][t.pp]

    def preserving(self, prefix, seed=None):
        """Transformations that do not vary a mastermind code.

        Recommend for use with the initial code in a solution, 
        then using the result to find case-distinct followers
        with increasing length prefixes.

        :param prefix: mastermind code prefix, in encoded form.
        :type c: iterable of int
        :param seed: initial set of transforms to start with; defaults to
          :py:attr:`.TransformTable.ALL` when input is ``None``.
        :type seed: iterable of :py:class:`.Transform`.
        :return: a set of :py:class:`.Transform` objects that do
          not change any element of ``prefix``.
        """
        inv = seed
        if inv is None:
            inv = self.ALL

        minlen = 0
        if self.IDENTITY in inv:
            minlen = 1

        for c in prefix:
            inv = frozenset(t for t in inv if self.apply(t, c) == c)
            if len(inv) <= minlen:
                return inv

        return inv


XF_LOOKUP_TABLE = None
"""Transformation lookup table; lookup tables for transformations."""

def initialize():
    """Initialize global tables."""

    global XF_LOOKUP_TABLE

    if XF_LOOKUP_TABLE is not None:
        return

    spec = loader.StorageSpec(VERSION, STORAGE_PATH)
    ldr = loader.Loader(TransformLookupTable, spec)

    tbl = ldr.get()

    XF_LOOKUP_TABLE = tbl

