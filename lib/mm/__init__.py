# -*- python -*-
"""Encapsualtes algorithms and objects to solve MasterMind derived problems."""

from mm.singleton import *

import exceptions
import logging

NCOLORS       = 6
"""Number of colors in the Master Mind game."""

NPOSITIONS    = 4
"""Number of position in the Master Mind code."""

NCODES        = NCOLORS ** NPOSITIONS
"""Total number of possiuble codes in the game."""

NSCORES       = (NPOSITIONS+1)*(NPOSITIONS+2)//2
"""Total number of expressable scores (including the (exact=3, approx=1)
invalid score)."""


PERFECT_SCORE = 0
"""The numeric value of the perfect score."""

def initialize_logging(level=logging.DEBUG):
    """initialize_logging(level=logging.DEBUG)
    """
    logging.basicConfig(format='%(asctime)s:%(name)s:%(levelname)s:%(message)s',
                        level=level)

class Exception(exceptions.Exception):
    """Exception class for this namespace."""
    pass

def decode(c):
    """Decodes an integer into a vector of color numbers.

    :param c: numeric code to be decoded.
    :return: tuple with :py:data:`.NPOSITIONS` color numbers.
    """
    if c < 0 or c >= NCODES:
        raise Exception, "Out of range: code:%d, range:[%d, %d)" % \
            (c, 0, NCODES)
    v = []
    t = c
    for i in range(0, NPOSITIONS):
        v.append(t % NCOLORS)
        t = int(t // NCOLORS)
    return tuple(v)

def encode(v):
    """Encodes a vector of color numbers into a numeric value.

    :param v: vector of color numbers.
    :return: an integer encoding of the code.
    """
    if len(v) != NPOSITIONS:
        raise Exception, \
            "Incorrect length:{}, required:{}, v:{}". \
            format(len(v), NPOSITIONS, v)
    c = 0
    t = 1
    for i in v:
        if i < 0 or i >= NCOLORS:
            raise Exception, \
                "Out of range: peg:{}, range:[{}, {}); code:{}". \
                format(i, 0, NCOLORS, v)
        c = c + i*t
        t = t * NCOLORS
    return c

def encode_score(e, a):
    """Function that encodes a score into a numeric value.

    .. warning::

       does not validate inputs.

    :param e: exact matches.
    :param a: approximate matches.

    :return: numeric encoding of the score.
    """
    return int((NPOSITIONS - e)*(NPOSITIONS - e + 1) // 2) + a



class codetable(object):
    """Lookup table mapping numeric codes to vectors of color numbers.
    A singleton class."""
    __metaclass__ = Singleton

    ALL = tuple(i for i in range(0, NCODES))
    """An enumeration of all the codes, in numeric form."""

    ALL_SET = frozenset(ALL)
    """:py:data:`ALL` as a set."""

    CODES = tuple(decode(i) for i in range(0, NCODES))
    """Lookup table, converts numeric codes to vectors of color
    numbers.

    >>> c = codetable().CODE[1295]
    [5, 5, 5, 5]
    """

    FIRST = tuple([encode([0,0,0,0]),
                   encode([1,0,0,0]),
                   encode([1,1,0,0]),
                   encode([2,1,0,0]),
                   encode([3,2,1,0])])
    """First roots: generic representative of all possible
    codes, if permutations of positions and colors are considered
    equivalent.  This is a small set (5 elements), representing all
    possible first moves in a MasterMind game."""

    FIRST_SET = frozenset(FIRST)
    """:py:data:`FIRST` as a set"""

CODETABLE = codetable()
"""Instance of :py:class:`.codetable`. """
