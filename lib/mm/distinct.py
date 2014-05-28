from . import *
from .xforms import TransformTable

import sys

class PrefixGen(object):
    def __init__(self):
        self.xftbl = TransformTable()
        self.seed = self.xftbl.ALL - frozenset([self.xftbl.IDENTITY])

    def _distinct(self, xfset, exclusions):
        codeset = (self.xftbl.CODESET - exclusions)
        if not xfset:
            return codeset
        return frozenset(min(CODETABLE.encode(self.xftbl.apply(t, v)) for t in xfset)
                         for v in codeset) - exclusions


    def prefixes(self, first, maxlen):
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
            for (q, i, d) in self._prefixes(nxt, self.xftbl.invariant_after(nxt, invp), maxlen):
                yield (q, i, d)

