from mm import *

import mm.distinct as distinct
import mm.score as score
import mm.treewalk as tw
import mm.xforms as xforms

import sys


def initialize():
    score.initialize()
    xforms.initialize()


def populate_stats(tree):
    if tree.get('stats') and 'total_moves' in tree.get('stats'):
        return tree

    children = tree.get('children') or {}
    children = { int(s): populate_stats(c) for (s, c) in children.iteritems() }
    
    stats = { 'problem_size': tree['problem_size'],
              'in_solution': tree['in_solution'], }
    tree['stats'] = stats

    if tree['problem_size'] == 1:
        stats.update({
                'total_moves': 1,
                'min_depth': 1,
                'max_depth': 1,
                'optimal': True
                })
        return tree

    total_moves = sum(child['problem_size'] + child['stats']['total_moves'] for child in children.itervalues())
    if tree['in_solution']:
        total_moves += 1

    max_depth = 1 + max(child['stats']['max_depth'] for child in children.itervalues())
    min_depth = 1 if tree['in_solution'] else 1 + min(child['stats']['min_depth'] for child in children.itervalues())
    optimal   = (1 == max(child['problem_size'] for child in children.itervalues()))

    stats.update({
            'total_moves': total_moves,
            'min_depth': min_depth,
            'max_depth': max_depth,
            'optimal': optimal
            })

    subsum = sum(child['problem_size'] for child in children.itervalues())
    if tree['in_solution']:
        subsum += 1

    if subsum != tree['problem_size']:
        raise MMException('problem_size at parent ({}) does not match sum of child sizes ({}).'.format(
                tree['problem_size'], subsum))

    return tree


def action(ctx):
    tree = ctx.tree
    pfx  = ctx.prefix

    vpfx = (CODETABLE.CODES[c] for c in pfx)
    pfxstr = ''.join(map(str, vpfx))
    vpath = ((CODETABLE.CODES[c], s) for (c, s) in ctx.path)
    pathstr = '.'.join(map(lambda p: str(p[0])+str(score.SCORE_TABLE.SCORES[p[1]].to_string()), vpath))

    sizes = ()
    children = tree.get('children')
    if children:
        sizes = reversed(sorted(child['problem_size'] for child in children.itervalues()))

    stats = tree['stats']
    print "'{}',{},{},{},{},{},{},{}".format(
        pathstr, len(pfx), tree['problem_size'], stats['total_moves'], stats['max_depth'],
        (1 if tree['in_solution'] else 0), (1 if stats['optimal'] else 0), 
        ','.join(map(str, sizes)))

    return True


def print_tree(tree):
    print ','.join(('prefix', 'prefix_length', 'problem_size', 'total_moves', 'max_depth',
                    'in_solution', 'optimal', 'child_sizes'))
    w = tw.TreeWalker(action)
    w.walktree(tree)

def main():
    initialize()

    fname = None
    if len(sys.argv) > 1:
        fname = sys.argv[1]
    tree = tw.loadfile(fname)

    tree = populate_stats(tree)
    print_tree(tree)


if __name__ == '__main__':
    main()
