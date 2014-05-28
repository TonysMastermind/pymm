"""Distinct prefix enumeration."""

from . import *
from . import xforms as xforms

import sys

class PrefixGen(object):
    """Pefix geneator."""

    def __init__(self):
        self.xftbl = xforms.TransformTable()
        """Transformation table."""

        self.seed = self.xftbl.ALL - frozenset([self.xftbl.IDENTITY])
        """Initial transformation set for prefix generation; :py:attr:`.xforms.TransformTable.ALL`
        without the identity transformation.
        """

        self.skip_non_reducing = False
        """When *True*, the generator skips some *inefficient* codes.  The default is *False*.

        Given:

          - input prefix *p*,
          - the set *I* representing the invariant transforms for *p*, 
          - the set *D* of distinct followers of *p*
          - for each *d* in *D*: if the invariant transforms of *p+(d)* are the same as *I*, then
            *d* is consideredn *inefficient*.
        """

    def _distinct(self, xfset, exclusions):
        codeset = (self.xftbl.CODESET - exclusions)
        if not xfset:
            return codeset
        return frozenset(min(CODETABLE.encode(self.xftbl.apply(t, v)) for t in xfset)
                         for v in codeset) - exclusions


    def prefixes(self, first, maxlen):
        """Generator of distinct prefixes, starting with a specific code.

        :param first: First code in the prefix.
        :param maxlen: maximum distinct prefix length.
        :return: yields prefixes, generated recursively.
        """
        first = (first,)

        for p in self._prefixes(first, self.xftbl.invariant_after(first, self.seed), maxlen):
            yield p

    def _vset(self, pfx):
        return frozenset(CODETABLE.CODES[c] for c in pfx)

    def _prefixes(self, p, invp, maxlen):
        d = self._distinct(invp, self._vset(p))
        yield (p, invp, d)

        if (not invp) or (len(p) >= maxlen) or (len(d) == (CODETABLE.NCODES-len(p))):
            return

        for c in d:
            nxt = p + (c,)
            invnxt = self.xftbl.invariant_after(nxt, invp)
            if self.skip_non_reducing and (len(invnxt) == len(invp)):
                continue
            for (q, i, d) in self._prefixes(nxt, invnxt, maxlen):
                yield (q, i, d)

