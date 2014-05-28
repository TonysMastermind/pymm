from . import *
from .xforms import TransformTable


class PrefixGen(object):
    def __init__(self):
        self.xftbl = TransformTable()
        self.seed = self.xftbl.ALL - frozenset([self.xftbl.IDENTITY])

    def _distinct(self, xfset, exclusions):
        return frozenset(min(CODETABLE.encode(self.xftbl.apply(t, v)) for t in xfset)
                         for v in (self.xftbl.CODESET - exclusions)) - exclusions


    def prefixes(self, first, maxlen):
        first = (first,)

        for p in self._prefixes(first, self.xftbl.invariant_after(first, self.seed), maxlen):
            yield p

    def _prefixes(self, p, invp, maxlen):
        yield (p, invp)
        if not invp:
            return

        if len(p) >= maxlen:
            return

        d = self._distinct(invp, frozenset(p))
        for c in d:
            nxt = p + (c,)
            for (q, i) in self._prefixes(nxt, self.xftbl.invariant_after(nxt, invp), maxlen):
                yield (q, i)

