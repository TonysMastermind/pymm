# -*- python -*-
"""Encapsualtes algorithms and objects to solve MasterMind derived problems."""

from . import singleton as singleton

import exceptions
import logging

def initialize_logging(**kwargs):
    """Initialize logging with defaults.

    :param kwargs: arguments passed to :py:func:`logging.basicConfig`.

    Defaults:
      - format: ``%(asctime)s:%(name)s:%(levelname)s:%(message)s``
      - level: :py:const:`logging.DEBUG`
    """
    args = {
        'format': '%(asctime)s:%(name)s:%(levelname)s:%(message)s',
        'level': logging.DEBUG
        }
    args.update(kwargs)
    logging.basicConfig(**args)


class MMException(exceptions.Exception):
    """Exception class for this namespace (also aliased as *MasterMindException*)."""
    pass

MasterMindException = MMException

class Code(tuple):
    """A refinement of :py:class:`tuple` for printability."""

    def __repr__(self):
        return '[{}]'.format(''.join(map(str, self)))


class CodeTable(object):
    """Lookup table mapping numeric codes to vectors of color numbers.
    A singleton class."""
    __metaclass__ = singleton.Singleton

    NCOLORS = 6
    """Number of colors in the Master Mind game."""

    NPOSITIONS = 4
    """Number of position in the Master Mind code."""

    NCODES = NCOLORS ** NPOSITIONS
    """Total number of possiuble codes in the game."""

    NSCORES = (NPOSITIONS+1)*(NPOSITIONS+2)//2
    """Total number of expressable scores (including the (exact=3, approx=1)
    invalid score)."""


    PERFECT_SCORE = 0
    """The numeric value of the perfect score."""


    def __init__(self):
        self.ALL = tuple(i for i in range(0, self.NCODES))
        """An enumeration of all the codes, in numeric form."""

        self.ALL_SET = frozenset(self.ALL)
        """:py:data:`ALL` as a set."""

        self.CODES = tuple(self.decode(i) for i in range(0, self.NCODES))
        """Lookup table, converts numeric codes to vectors of color
        numbers.

        >>> c = codetable().CODE[1295]
        [5, 5, 5, 5]
        """

        self.FIRST = tuple(map(self.encode,
                               ([0,0,0,0],
                                [1,0,0,0],
                                [1,1,0,0],
                                [2,1,0,0],
                                [3,2,1,0])))

        """First roots: generic representative of all possible
        codes, if permutations of positions and colors are considered
        equivalent.  This is a small set (5 elements), representing all
        possible first moves in a MasterMind game."""

        self.FIRST_SET = frozenset(self.FIRST)
        """:py:data:`FIRST` as a set"""


    def decode(self, c):
        """Decodes an integer into a vector of color numbers.

        :param c: numeric code to be decoded.
        :return: tuple with :py:data:`codetable.NPOSITIONS` color numbers.
        """
        if c < 0 or c >= self.NCODES:
            raise MMException, "Out of range: code:%d, range:[%d, %d)" % \
                (c, 0, self.NCODES)
        v = []
        t = c
        for i in range(0, self.NPOSITIONS):
            v.append(t % self.NCOLORS)
            t = int(t // self.NCOLORS)
        return Code(v)

    
    def encode(self, v):
        """Encodes a vector of color numbers into a numeric value.

        :param v: vector of color numbers.
        :return: an integer encoding of the code.
        """
        if len(v) != self.NPOSITIONS:
            raise MMException, \
                "Incorrect length:{}, required:{}, v:{}". \
                format(len(v), self.NPOSITIONS, v)
        c = 0
        t = 1
        for i in v:
            if i < 0 or i >= self.NCOLORS:
                raise MMException, \
                    "Out of range: peg:{}, range:[{}, {}); code:{}". \
                    format(i, 0, self.NCOLORS, v)
            c = c + i*t
            t = t * self.NCOLORS
        return c

    def encode_score(self, e, a):
        """Function that encodes a score into a numeric value.

        .. warning::
          does not validate inputs.

        :param e: exact matches.
        :param a: approximate matches.

        :return: numeric encoding of the score.
        """
        return int((self.NPOSITIONS - e)*(self.NPOSITIONS - e + 1) // 2) + a


CODETABLE = CodeTable()
"""Instance of :py:class:`.CodeTable`. """
