import mm
import mm.builder as builder
import mm.score

def main():
    mm.score.initialize()
    b = builder.TreeBuilder(builder.BuilderContext, mm.CODETABLE.ALL)
    t = b.build(9, root=8)
    print t.as_json_string()

if __name__ == '__main__':
    main()
