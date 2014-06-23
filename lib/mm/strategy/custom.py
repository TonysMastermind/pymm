"""Custom candidate selection strategies."""

from . import *

from .. import *
from .. import builder as builder
from .. import partition

import sys

BaseStrategy = STRATEGIES['min_moves_distinct']

PATH_RESPONSE = {
    (): (8, 3),
    #((8, 3),): (58, 11, 12),
    ((8, 3),): (58, 12), # focus on the 23-element problem
    }


def _preselected(pth, problem, root):
    pre_choice = PATH_RESPONSE.get(pth)
    if not pre_choice:
        return (partition.PartitionResult(problem, root),)

    print >>sys.stderr, "# placing pre-selected choice: {} at {}, probsize={}".format(
        pre_choice[0], pth, len(problem))
    pr = partition.PartitionResult(problem, pre_choice[0])
    scores = pre_choice[1:]
    if scores:
        stub_problem = (0,)
        parts = list(pr.parts)
        for i in xrange(CODETABLE.NSCORES):
            if i == CODETABLE.PERFECT_SCORE:
                pass
            elif i in scores:
                pass
            elif not parts[i]:
                pass
            else:
                parts[i] = stub_problem
        pr.parts = tuple(parts)

    print >>sys.stderr, "# stubbed partition result: {}".format(map(len, pr.parts))
    return (pr, )

def fmt_tree(label, t, pth):
    if not t:
        print >>sys.stderr, '--{} - -'.format(label)
        return
    for s in (('--{} {} {}.({}, *)'.format(label, t, pth, t.root),
               '  probsize={}, moves={}, opt={}, in={}'.format(t.stats.problem_size,
                                                               t.stats.total_moves,
                                                               t.stats.optimal,
                                                               t.root_in_solution))):
        print >>sys.stderr, s


class DebugMinimizeMoveCount(MinimizeMoveCount):
    def evaluate(self, strat, tree, state):
        self.log_conditions('Before', strat, tree, state, None)
        result = super(DebugMinimizeMoveCount, self).evaluate(strat, tree, state)
        self.log_conditions('After', strat, tree, state, result)
        return result

    def best(self, state):
        base = super(DebugMinimizeMoveCount, self).best(state)
        fmt_tree('best: ', base, '-')
        for (i, s) in enumerate(state):
            fmt_tree('--state['+str(i)+']', s, '-')
        return base

    def log_conditions(self, label, strat, tree, state, result):
        if not strat.debug_enabled:
            return

        pth = tuple((s.root, s.score) for s in strat.path)

        if result is None:
            result = '-'


        print >>sys.stderr, ">>", label, pth, result
        if label == 'Before':
            fmt_tree('input', tree, pth)
        for (i, s) in enumerate(state):
            fmt_tree('state['+str(i)+']', s, pth)


class DebugExhaustiveDistinctLogic(BaseStrategy):
    SOLUTION_EVALUATOR = DebugMinimizeMoveCount

    @classmethod
    def preselected(clazz, problem, root):
        return _preselected((), problem, root)

    @classmethod
    def build_tree(clazz, problem, maxdepth, root=None):
        return builder.TreeBuilder(clazz, problem).build(maxdepth, PATH_RESPONSE[()][0])


    def __init__(self, *args, **kwargs):
        super(DebugExhaustiveDistinctLogic, self).__init__(*args, **kwargs)
        pth = tuple((s.root, s.score) for s in self.path)
        self.debug_enabled = False

        while pth:
            if PATH_RESPONSE.get(pth) is not None:
                self.debug_enabled = True
                break
            pth = pth[:-1]

    def _best_candidates(self):
        base = super(DebugExhaustiveDistinctLogic, self)._best_candidates()
        pth = tuple((s.root, s.score) for s in self.path)
        pre_choice = PATH_RESPONSE.get(pth)
        if pre_choice:
            return _preselected(pth, self.problem, None)

        print >>sys.stderr, "# returning base result of size {} at path {}, probsize={}; #distinct={}, #preserving={}, #root_problem={}".format(
            len(base), pth, len(self.problem), len(self._distinct_candidates), len(self._preserving), len(self._root_problem))

        return base


STRATEGIES['debug_minmoves_distinct'] = DebugExhaustiveDistinctLogic

