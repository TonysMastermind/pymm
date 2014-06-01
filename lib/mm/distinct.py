"""Distinct prefix enumeration."""

from . import *
from . import xforms as xforms

import sys

class PrefixGen(object):
    """Pefix geneator."""

    def __init__(self):
        self.xftbl = xforms.TransformTable()
        """Transformation table."""

        self.seed = self.xftbl.ALL
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

    def distinct_after(self, pfx):
        """Distinct codes after a particular prefix.

        :param pfx: a set of codes, in numeric form.
        :return: a set of codes that are distinct after the prefix.
        """
        xfset = self.seed
        if pfx:
            xfset = self.xftbl.invariant_after(pfx, xfset)

        return self._distinct(xfset, frozenset(pfx))

    def _vset(self, pfx):
        return frozenset(CODETABLE.CODES[c] for c in pfx)

    def _prefixes(self, p, invp, maxlen, d=None):
        if d is None:
            d = self._distinct(invp, self._vset(p))

        yield (p, invp, d)

        if (len(invp) == 1) or (len(p) >= maxlen) or (len(d) == (CODETABLE.NCODES-len(p))):
            return

        dprev = d
        lendprev = len(dprev)
        for c in dprev:
            nxt = p + (c,)
            invnxt = self.xftbl.invariant_after(nxt, invp)
            dnxt = self._distinct(invnxt, self._vset(nxt))

            if self.skip_non_reducing:
                if (len(invnxt) == len(invp)) or (len(dnxt) <= lendprev):
                    yield (nxt, invnxt, dnxt)
                    continue

            for (q, i, d) in self._prefixes(nxt, invnxt, maxlen, dnxt):
                yield (q, i, d)

