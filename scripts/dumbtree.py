import mm
import mm.builder as builder
import mm.score

import cProfile as profile
import pstats
import StringIO

def doit(pr):
    b = builder.TreeBuilder(builder.BuilderContext, mm.CODETABLE.ALL)
    pr.enable()
    t = b.build(9, root=8)
    pr.disable()
    print t.as_json_string()

def main():
    mm.score.initialize()

    pr = profile.Profile()
    doit(pr)

    s = StringIO.StringIO()
    ps = pstats.Stats(pr, stream=s).strip_dirs().sort_stats('time')
    ps.print_stats()
    print s.getvalue()

if __name__ == '__main__':
    main()
