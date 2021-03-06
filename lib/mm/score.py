# -*- python -*-
"""Encapsulates the concept of scores in MasterMind, providing basic
algorithm for calculating scores, and a lookup table for looking up
scores quickly.
"""

from . import *
from . import singleton as singleton
from . import loader as loader

import collections

_CODES= CODETABLE.CODES
"""A table mapping numeric codes to the tuple representation."""

NCODES     = CodeTable.NCODES
NPOSITIONS = CodeTable.NPOSITIONS
NCOLORS    = CodeTable.NCOLORS
NSCORES    = CodeTable.NSCORES

VERSION = 1
STORAGE_PATH = 'var/scoretable'

NamedScoreTuple = collections.namedtuple('NamedScoreTuple',
                                        ['exact', 'approx', 'value'])

class Score(NamedScoreTuple):
    """Class representing Mastermind scores.

    **Fields**

    exact
      Exact component of score: count of pegs that match in 
      position and color.

    approx
      Approximate component of score: count of pegs that match in color,
        but disagree in position.  This count excludes the exact matches.

    value
      Numeric encoding of score.  0 is the perfect score.
    """

    def __new__(cls, exact=None, approx=None):
        """score calculations.

        :param exact: exact matches.
        :param approx: approximate matches.
        """
        e = exact
        a = approx
        if e < 0 or e > NPOSITIONS or a < 0 or a > NPOSITIONS or \
                (e+a) > NPOSITIONS:
            raise MMException, \
                ("Invalid score:(exact={0},approx={1}); " +
                 "range for each: [0,{2}), " +
                 "range for sum:[0,{2}), for exact={3}, approx must be 0.").\
                 format(e, a, NPOSITIONS, NPOSITIONS-1)

        return NamedScoreTuple.__new__(cls, e, a, CODETABLE.encode_score(e, a))

    def __repr__(self):
        return "{}.{}(exact={}, approx={}, value={})".format(
            self.__class__.__module__,
            self.__class__.__name__, 
            *self)

    def to_string(self):
        return '(e={}, a={})'.format(self.exact, self.approx)

    @staticmethod
    def from_encoded(c1, c2):
        """Calculates the score of two codes, using numeric codes.

        :param c1: first code.
        :param c2: second code.
        :return: :py:class:`.score`.
        """
        return Score.from_vectors(_CODES[c1], _CODES[c2])

    @staticmethod
    def from_vectors(v1, v2):
        """Static method; calculates the score of two codes; using
        vectors of color numbers.

        :param v1: first vector of color numbers.
        :param v2: second vector of color numbers.
        :return: :py:class:`.score`.
        """
        if len(v1) != NPOSITIONS or len(v2) != NPOSITIONS:
            raise MMException, \
                "Invalid length; required:{}, v1={}, v2={}.". \
                format(NPOSITIONS, v1, v2)

        cc1 = [0] * NCOLORS
        cc2 = [0] * NCOLORS
        e = 0
        for (a,b) in zip(v1,v2):
            if a in range(0, NCOLORS) and b in range(NCOLORS):
                cc1[a] = cc1[a] + 1
                cc2[b] = cc2[b] + 1
                if a == b:
                    e = e + 1
            else:
                raise MMException, \
                    ("Out of range color. a={}, b={}; " + \
                         "range:[0,{}); v1:{}, v2:{}.").\
                    format(a, b, NCOLORS, v1, v2)

        a = 0
        for (x,y) in zip(cc1, cc2):
            a = a + min(x, y)

        a = a - e
        return Score(exact=e, approx=a)


def _genscores():
    s = [0] * NSCORES
    for e in range(0, NPOSITIONS+1):
        for a in range(0, NPOSITIONS+1-e):
            i = CODETABLE.encode_score(e, a)
            s[i] = Score(e, a)
    return tuple(s)


def _genscoretable():
    return tuple(tuple(Score.from_vectors(_CODES[c1], _CODES[c2]).value \
                           for c1 in range(0, NCODES)) \
                     for c2 in range(0, NCODES))


class ScoreTable(singleton.SingletonBehavior):
    """Precalculated scores."""
    __metaclass__ = singleton.Singleton


    def __init__(self):
        self.SCORES = _genscores()
        """Table mapping numeric scores to :py:class:`.Score` objects."""

        self.SCORE_TABLE = _genscoretable()
        """A matrix storing scores of all possible code pairs.  The width
        and height are both :py:data:`.CODETABLE.NCODES`, and the contents
        are small integers representing mastermind scores.
        """

        self.ENCODED_SCORES = {s: i for (i, s) in enumerate(self.SCORES)}
        """Mapping from tuple-scores to numeric encoding; used like
        this:

        .. code-block:: python

          table.ENCODED_SCORES[(exactmatches, nearmatches)]
        """


    def lookup_score(self, s):
        """Decodes a numeric score into a pair of numnbers (exact, approx).

        :param s: score to be translated to a pair of numbers.
        :return: score as a pair.
        """
        return self.SCORES[s]


    def score(self, c1, c2):
        """Looks up the match score between two numeric codes, returning
        a numerically encoded score value.

        :param c1: a code in numeric form.
        :type c1: int
        :param c2: a code in numeric form.
        :type c2: int
        :return: mastermind score of *c1* against *c2*, in numeric form.
        """
        return self.SCORE_TABLE[max(c1, c2)][min(c1, c2)]


SCORE_TABLE = None #scoretable()
"""The single instance of :py:class:`.ScoreTable`."""

LOOKUP_TABLE = None
"""Score lookup table."""


def initialize():
    """Initialize global tables."""

    global SCORE_TABLE
    global LOOKUP_TABLE

    if SCORE_TABLE is not None:
        return

    spec = loader.StorageSpec(VERSION, STORAGE_PATH)
    ldr = loader.Loader(ScoreTable, spec)

    tbl = ldr.get()

    SCORE_TABLE = tbl
    LOOKUP_TABLE = SCORE_TABLE.SCORE_TABLE


def score(c1, c2):
    """Returns the scope of *c1* against *c2* encoded as a small integer.

    :param c1: a mastermind code in numeric form.
    :param c2: a mastermind code in numeric form.
    :return: score, a small integer in the range 0 .. :py:data:`.CODETABLE.NSCORES`
    """
    return LOOKUP_TABLE[c1][c2]
