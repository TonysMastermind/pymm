import mm
import mm.distinct as distinct
import mm.partition as partition
import mm.score as score
import mm.xforms as xforms

def main():
    mm.score.initialize()
    mm.xforms.initialize()

    pr = mm.partition.PartitionResult(mm.CODETABLE.ALL, 8)

    parts = filter(lambda p: p and len(p) > 1, pr.parts)

    pfxgen = mm.distinct.PrefixGen()

    d = pfxgen.distinct_after([8])
    i = mm.xforms.XF_LOOKUP_TABLE.preserving([8])
    for p in parts:
        s = pfxgen.distinct_subset(i, p, [8])
        r = pfxgen.reduce_codeset(i, p, [8])
        x = frozenset(sorted(mm.xforms.XF_LOOKUP_TABLE.apply(t, c) for t in i for c in p))
        fp = frozenset(p)

        print "len(i)={}, len(problem)={}, len(d)={}, s={}, r={}".format(
            len(i), len(p), len(d), tuple(sorted(s)), tuple(sorted(r)))
        print "              problem = {}".format(tuple(sorted(fp)))
        print "  problem * invariant = {}".format(tuple(sorted(x)))
        print ("  distinct & problem = {}\n"+
               "  distinct & s       = {}\n"+
               "  distinct & r       = {}\n"+
               "  problem  & s       = {}\n"+
               "  problem  & r       = {}").format(
            *map(lambda x: tuple(sorted(x)), (d&fp, d&s, d&r, fp&s, fp&r)))

        if x != fp:
            print "*** problem != preserving*problem ***"

        if s != r:
            print "*** s != r ***"
            delta = r - s
            xp = { c: frozenset(mm.xforms.XF_LOOKUP_TABLE.apply(t, c) for t in i) for c in p }
            yp = { c: frozenset(w for w in (mm.xforms.XF_LOOKUP_TABLE.apply(t, c) for t in i)
                                if w in fp)
                   for c in fp }

            print "  r - s = {}".format(tuple(sorted(delta)))
            for (c, cp) in sorted(xp.iteritems()):
                ycp = yp[c]
                print "   {:4d} => {:4d}, all={}, all-problem={}".format(c, min(cp), tuple(sorted(cp)), tuple(sorted(cp-fp)))
                print "   {:4s} => {:4d}, all={}, all-problem={}".format(' ', min(ycp), tuple(sorted(ycp)), tuple(sorted(ycp-fp)))
                print ""

        print "=========================================================================="

if __name__ == '__main__':
    main()
