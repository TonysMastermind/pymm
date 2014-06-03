from mm import CODETABLE
from mm.treewalk import walkfile, path2prefix

import argparse
from collections import defaultdict
import sys

def prefix(path):
    return tuple(map(lambda c: CODETABLE.CODES[c], path2prefix(path)))

ALL_PREFIXES = set()
PREFIX_USE_COUNT = defaultdict(int)

SEEN = set()

LENGTH_SIZE_MAP = defaultdict(lambda: defaultdict(int))

def action(path, tree):
    global ALL_PREFIXES
    global PREFIX_USE_COUNT
    global SEEN

    psize = tree['problem_size']
    if psize <= 2:
        return False

    children = tree.get('children')
    subsizes = [0]
    if children:
        subsizes = map(lambda t: t['problem_size'], children.itervalues())
    mx = max(subsizes)
    pfx = prefix(path)

    pp = path[:-1]
    if not pp in SEEN:
        ALL_PREFIXES.add(pfx)
        PREFIX_USE_COUNT[pfx] += 1
        SEEN.add(pp)

    if mx:
        if mx <= 3:
            print " {} {} => {}".format(pfx,
                                        psize, list(reversed(sorted(subsizes))))
            return mx > 1
        elif psize <= 14:
            print "*{} {} => {}".format(pfx,
                                        psize, list(reversed(sorted(subsizes))))
            return True

    return True


def length_size(path, tree):
    global LENGTH_SIZE_MAP
    psize = tree['problem_size']
    LENGTH_SIZE_MAP[len(path)//2][psize] += 1
    return True

ACTIONS = { False: action, True: length_size }

def main():
    parser = argparse.ArgumentParser()
    parser.add_argument('--input', '-i', help="Input file, default: stdin.",
                        default=None, type=str, dest='fname')
    parser.add_argument('--simple', '-s', help="Simple prefix-length/problem size printout",
                        action='store_true', dest='simple')
    parser.add_argument('--deeper', '-d', help="More complex analysis at node.",
                        action='store_false', dest='simple')

    args = parser.parse_args()

    fname = args.fname

    walkfile(ACTIONS[args.simple], fname=fname)

    print "========================"
    if args.simple:
        for l in sorted(LENGTH_SIZE_MAP.keys()):
            d = LENGTH_SIZE_MAP[l]
            for sz in sorted(d.keys()):
                print "{}, {}, {}".format(l, sz, d[sz])
    else:
        for p in sorted(ALL_PREFIXES, 
                        lambda a, b: cmp(PREFIX_USE_COUNT[b], PREFIX_USE_COUNT[a]) or \
                            cmp(a, b)):
            print PREFIX_USE_COUNT[p], ":", p

if __name__ == '__main__':
    main()
