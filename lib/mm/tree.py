"""Game Tree construction."""

from . import *
from . import score

import json
import platform

_SCORE_LIST = range(CODETABLE.NSCORES)

class TreeResult(object):
    """The result of calculating a game tree.  Non-null entity encapsulating
    the result of calculation, the strategy used during generating, and
    some metrics about the cost of calculation.

    The game tree, itself, may be null.
    """

    def __init__(self, tree, max_levels, strategy, rusage):
        """
        :param tree: game tree, may be null.
        :param max_levels: depth constraint on the contsruction.
        :param strategy: strategy for building the tree.
        :param rusage: cputime/usertime consumed during construction.
        """

        self.tree = tree
        """Game tree; may be null."""

        self.max_levels = max_levels
        """Depth constraint on the construction algorithm."""

        self.strategy = strategy
        """Strategy controlling the tree algorithm."""

        self.rusage = rusage
        """Time resource used during tree construction."""


    def to_json_file(self, fname):
        """Writes a JSON representation of the tree to a file.

        :param fname: name, or path, of output file.
        """
        fp = open(fname, 'w')
        json.dump(self.as_dict(), fp, skipkeys=True, 
                  check_circular=True, indent=2)

    def as_json_string(self):
        """Returns a JSON represtation of the tree as a string.

        :return: JSON string representation.
        """
        return json.dumps(self.as_dict(), skipkeys=True, 
                          check_circular=True, indent=2)

    def as_dict(self):
        """Dictionary representation of the tree result.

        :return: representation as a dictionary; typically for generating JSON.
        """
        return {
            'tree': self.tree.as_dict() if self.tree else None,
            'metrics': {
                'rusage': self.rusage.as_dict(),
                'python': platform.python_implementation()
                },
            'strategy': self.strategy.description(),
            'max_levels': self.max_levels
            }

class Tree(object):
    """MasterMind strategy tree."""

    class Stats(object):
        """Tree stats.  Basic quality attributes of a game tree."""

        def __init__(self, 
                     problem_size = None,
                     min_depth    = None,
                     max_depth    = None,
                     total_moves  = None,
                     optimal      = None,
                     in_solution  = None,
                     pr_stats     = None):
            """
            :param problem_size: size of problem sovled in the tree.
            :param min_depth: length of shortest path to a leaf.
            :param max_depth: length of longest path to a leaf.
            :param total_moves: total number of all possible games 
              playable against the tree.
            :param optimal: true when the tree os an optimal strategy (all subproblems are
              of size 1).
            :param in_solution: true when the root guess is in the tree's problem; false
              otherwise.
            :param pr_stats: partition result stats for the root and the problem of the tree.
            """

            self.problem_size = problem_size 
            self.min_depth    = min_depth
            self.max_depth    = max_depth 
            self.total_moves  = total_moves
            self.in_solution  = in_solution
            self.optimal      = optimal
            self.pr_stats     = pr_stats
            self.rusage       = None

        def set_timing(self, rusage):
            self.rusage = rusage

        @property
        def average_game_length(self):
            return float(self.total_moves)/self.problem_size
        
        def as_dict(self):
            """Returns a dictionary representing the tree stats. 
            Suitable for serialization to JSON and similar formats."""
            d = dict((a, getattr(self, a)) \
                         for a in ['problem_size', 'min_depth', 
                                   'max_depth', 'total_moves', 
                                   'average_game_length',
                                   'in_solution', 'optimal'])
            if self.rusage != None:
                d['rusage'] = self.rusage.as_dict()

            return d        

        def __str__(self):
            """Printable (informal) string format."""
            b = super(tree.stats, self).__str__()
            d = ("---------------------------------------\n" +
                 "   problem_size:{:7d}; min_depth:{:4d}\n" +
                 "    total_moves:{:7d}; max_depth:{:4d}\n" +
                 "avg_game_length:{:7.4f}; optimal: {}\n" +
                 "    in_solution: {}\n").\
                 format(self.problem_size,
                        self.min_depth,
                        self.total_moves,
                        self.max_depth,
                        self.avg_game_length,
                        (self.optimal if hasattr(self, 'optimal') \
                             else 'n/a'),
                        (self.in_solution if hasattr(self, 'in_solution') \
                             else 'n/a'))
            if self.rusage:
                d += 'rusage: ' + str(self.rusage) + "\n"
            d += "---------------------------------------\n"

            return b + "\n" + d

    def __init__(self, rc):
        """Initializes the tree object with a root code.

        :param rc: Root code of the tree.
        """
        self.children = [None] * CODETABLE.NSCORES
        """subtrees, one for each possible score against the root."""

        self.root = rc
        """root code of the tree."""

        self.root_in_solution = False
        """True when the root code is in the problem."""

        self.stats = Tree.Stats()
        """Tree stats."""

    def add_child(self, score, child):
        """:param score: score where the subtree is attached.
           :param child: a subtree.
           """
        self.children[score] = child

    def as_dict(self):
        """Returns a representation of the tree as a dictionary."""
        d = { }
        d['root'] = self.root
        d['in_solution'] = self.root_in_solution
        d['problem_size'] = self.stats.problem_size
        d['stats'] = self.stats.as_dict()
        d['pr_stats'] = self.pr_stats.as_dict()
        children = filter(lambda p: p[1], zip(_SCORE_LIST, self.children))
        if len(children) == 0:
            return d

        d['children'] = {s: c.as_dict() for (s, c) in children}
        return d


    def as_json_string(self):
        """Returns a JSON represtation of the tree as a string.

        :return: JSON string representation.
        """
        return json.dumps(self.as_dict(), skipkeys=True, 
                          check_circular=True, indent=2)


    def update_stats(self, pr):
        """Derives the tree stats from the stats of the subtrees, and
        the root's properties.

        :param pr: Partition results.
        """
        s = self.stats
        if pr:
            self.pr_stats = pr.stats
            self.root_in_solution = s.in_solution = pr.stats.in_solution
            s.optimal = pr.stats.optimal

        children = filter(lambda p: p[1], zip(_SCORE_LIST, self.children))
        if len(children) == 0:
            s.total_moves = 1
            s.min_depth = s.max_depth = 1
            s.problem_size = 1
            return

        mn = min(c.stats.min_depth for (_, c) in children)
        mx = 1 + max(c.stats.max_depth for (_, c) in children)
        sz = sum(c.stats.problem_size for (_, c) in children)
        tot = sum(c.stats.total_moves+c.stats.problem_size for (_, c) in children)
        if self.root_in_solution:
            sz  = sz + 1
            tot = tot + 1
        else:
            mn  = mn + 1

        s.total_moves  = tot
        s.min_depth    = mn
        s.max_depth    = mx
        if (s.problem_size is not None) and (s.problem_size != sz):
            raise MMException, \
                "Problem size inconsistency: calculated:{:d}, stored:{:d}".\
                format(sz, s.problem_size)
        s.problem_size = sz

_ONE_ELEMENT_PR_STATS = partition.Stats([1], 1)
_TWO_ELEMENT_PR_STATS = partition.Stats([1, 1], 1)

_ONE_ELEMENT_STATS = Tree.Stats(problem_size = 1,
                                min_depth    = 1,
                                max_depth    = 1,
                                total_moves  = 1,
                                optimal      = True,
                                in_solution  = True,
                                pr_stats     = _ONE_ELEMENT_PR_STATS)

_TWO_ELEMENT_STATS = Tree.Stats(problem_size = 2,
                                min_depth    = 1,
                                max_depth    = 2,
                                total_moves  = 3,
                                optimal      = True,
                                in_solution  = True,
                                pr_stats     = _TWO_ELEMENT_PR_STATS)


def one_element_tree(code):
    """Trivial one-element tree.

    :param code: the tree root.
    :return: a strategy tree for a 1-code problem.
    """
    t = Tree(code)
    t.root_in_solution = True
    t.stats = _ONE_ELEMENT_STATS
    t.pr_stats = _ONE_ELEMENT_PR_STATS
    return t

def two_element_tree(codes):
    """Trivial two-element tree.

    :param codes: the 2-element problem.
    :return: a strategy tree for a 2-code problem.
    """
    c1, c2 = min(codes), max(codes)
    s = score.score(c1, c2)

    t = Tree(c1)
    t.root_in_solution = True
    t.add_child(s, one_element_tree(c2))
    t.stats = _TWO_ELEMENT_STATS
    t.pr_stats = _TWO_ELEMENT_PR_STATS
    return t


def optimal_tree(pr):
    """Build an optimal tree from an optimal partition result.

    :param pr: An instance of :py:class:`.partition.PartitionResult`
    :return: a tree.
    """
    t = Tree(pr.root)
    for (score, prob) in zip(_SCORE_LIST, pr.parts):
        if prob:
            if len(prob) != 1:
                raise MMException("Partition of size {} is not legal in an optimal partition result.".format(
                        len(prob)))

            t.add_child(score, one_element_tree(prob[0]))
    t.update_stats(pr)
    if type(t.stats.total_moves) is not int:
        raise MMException("Improperly set stats.")
    return t
