from mm import *
import mm.score    as score
import mm.treewalk as treewalk
import mm.xforms   as xforms

import argparse
import time
import sys

ROOT_ID = None

def initialize():
    score.initialize()
    xforms.initialize()

def node_id(ctx):
    if not ctx.parent:
        return ROOT_ID

    spfx = map(lambda cs: '.'.join(map(str, cs)), ctx.path)
    pfx = ':'.join(spfx)
    return "{}.{}".format(ROOT_ID, pfx)


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

    ctx.tree_id = node_id(ctx)

    parent_id = 'NULL'
    if ctx.parent:
        parent_id = "'" + ctx.tree_id + "'"

    score = 'NULL'
    if ctx.path:
        score = ctx.path[-1][1]


    sizes = ()
    children = tree.get('children')
    if children:
        sizes = tuple(reversed(sorted(child['problem_size'] for child in children.itervalues())))

    stats = tree['stats']
    print "insert into tree_node values('{}',{},{},{},{},{},{},{},{},{},{},{});".format(
        ctx.tree_id,
        parent_id,
        tree['root'],
        score,
        len(ctx.path),
        tree['problem_size'], 
        (sizes[0] if len(sizes) else 'NULL'),
        len(sizes),
        (1 if tree['in_solution'] else 0),
        (1 if stats['optimal'] else 0), 
        stats['total_moves'], 
        stats['max_depth'])

    return True


def print_tree(tree):
    w = treewalk.TreeWalker(action)
    w.walktree(tree)


def parser():
    p = argparse.ArgumentParser(description="Tree to librebase tree_node table.")
    p.add_argument('--input', '-i', help="JSON input file",
                   type=str, action='store', dest='fname', default=None)
    p.add_argument('--name', '-n', help="Tree name",
                   type=str, action='store', dest='name', required=True)
    return p

def main():
    initialize()

    p = parser()
    args = p.parse_args()

    fname = args.fname

    global ROOT_ID
    ROOT_ID = args.name

    tree = treewalk.loadfile(fname)

    tree = populate_stats(tree)
    print_tree(tree)


if __name__ == '__main__':
    main()
