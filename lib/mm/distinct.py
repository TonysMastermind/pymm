"""Distinct prefix enumeration."""

from . import *
from . import xforms as xforms

import sys

class PrefixGen(object):
    """Pefix geneator."""

    def __init__(self):
        self.xftbl = xforms.TransformLookupTable()
        """Transformation table."""

        self.seed = self.xftbl.ALL
        """Initial transformation set for prefix generation; :py:attr:`.xforms.TransformTable.ALL`
        without the identity transformation.
        """

        self.skip_non_reducing = False
        """When *True*, the generator skips some *inefficient* codes.  The default is *False*.

        Given:

          - input prefix *p*,
          - the set *P* representing the preserving transforms for *p*, 
          - the set *D* of distinct followers of *p*
          - for each *d* in *D*: if the preserving transforms of *p+(d)* are the same as *P*, then
            *d* is considered *inefficient*.
        """

    def distinct_subset(self, xfset, codeset, exclusions):
        """Distinct subset of a set of codes under a set of transformations.

        :param xfset: a set of transformations; instances of :py:class:`.xforms.Transfrom`.
        :param codeset: a set of codes, in numeric form.
        :param exclusions: a set of codes, in numeric form, to exclude from the results.
        :return: a subset of *codeset* representing the codes that are distinct
          under the proposet set of equivalence transformations *xfset*.  Not that the
          output codes are not guaranteed to be in the input set.
        """
        if not xfset:
            return frozenset(codeset) - frozenset(exclusions)
        if len(xfset) == 1 and self.xftbl.IDENTITY in xfset:
            return frozenset(codeset) - frozenset(exclusions)
        return frozenset(min(self.xftbl.apply(t, v) for t in xfset)
                         for v in codeset) - frozenset(exclusions)

    def reduce_codeset(self, xfset, codeset, exclusions):
        """Reduced subset of a set of codes under a set of transformations.

        :param xfset: a set of transformations; instances of :py:class:`.xforms.Transfrom`.
        :param codeset: a set of codes, in numeric form.
        :param exclusions: a set of codes, in numeric form, to exclude from the results.
        :return: a subset of *codeset* representing the codes that are distinct
          under the proposet set of equivalence transformations *xfset*.  Unlike the
          method :py:meth:`.PrefixGen.distinct_subset`, this method will ensure that
          the output results are in the input codeset, using costlier calculations.

        This method may throw an exception if the result is empty.  Including the
        identity transformation in *xfset* will prevent such events.
        """
        codeset = frozenset(codeset)

        if not xfset:
            return codeset - frozenset(exclusions)
        if len(xfset) == 1 and self.xftbl.IDENTITY in xfset:
            return codeset - frozenset(exclusions)


        return frozenset(min(w
                             for w in (self.xftbl.apply(t, v) for t in xfset)
                             if w in codeset)
                         for v in codeset) - frozenset(exclusions)


    def _distinct(self, xfset, exclusions):
        return self.distinct_subset(xfset, CODETABLE.ALL, exclusions)

    def prefixes(self, first, maxlen):
        """Generator of distinct prefixes, starting with a specific code.

        :param first: First code in the prefix.
        :param maxlen: maximum distinct prefix length.
        :return: yields prefixes, generated recursively.
        """
        first = (first,)

        for p in self._prefixes(first, self.xftbl.preserving(first, self.seed), maxlen):
            yield p

    def distinct_after(self, pfx):
        """Distinct codes after a particular prefix.

        :param pfx: a set of codes, in numeric form.
        :return: a set of codes that are distinct after the prefix.
        """
        xfset = self.seed
        if pfx:
            xfset = self.xftbl.preserving(pfx, xfset)

        return self._distinct(xfset, pfx)


    def _prefixes(self, p, invp, maxlen, d=None):
        if d is None:
            d = self._distinct(invp, p)

        yield (p, invp, d)

        if (len(invp) == 1) or (len(p) >= maxlen) or (len(d) == (CODETABLE.NCODES-len(p))):
            return

        dprev = d
        lendprev = len(dprev)
        for c in dprev:
            nxt = p + (c,)
            invnxt = self.xftbl.preserving(nxt, invp)
            dnxt = self._distinct(invnxt, nxt)

            if self.skip_non_reducing:
                if (len(invnxt) == len(invp)) or (len(dnxt) <= lendprev):
                    yield (nxt, invnxt, dnxt)
                    continue

            for (q, i, d) in self._prefixes(nxt, invnxt, maxlen, dnxt):
                yield (q, i, d)

