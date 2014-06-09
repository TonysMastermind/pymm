"""Collection of strategies."""

from .. import *
from .. import builder as builder
from .. import partition as partition

class MinimizeMoveCount(builder.SolutionEvaluator):
    def initial_state(self):
        """:return: initial evaluator state.

        The state is 3-parts:

        - best tree based on total moves, with depth as a tie-breaker.
        - optimal tree with root chosen outside the problem.
        - optimal tree with root chosen inside the problem.
        """
        return [None, None, None]

    def evaluate(self, ctx, tree, state):
        """:param ctx: ignored.
        :param tree: tree to be evaluated.
        :param state: cumulative state of evaluation.
        :return: False, unless an optimal tree with the root chosen from the
          problem was seen.
        """
        if tree.stats.optimal:
            if tree.root_in_solution:
                state[2] = tree
            else:
                state[1] = tree

        if not state[0]:
            state[0] = tree
        elif state[0].stats.total_moves > tree.stats.total_moves:
            stats[0] = tree
        elif state[0].stats.total_moves == tree.stats.total_moves:
            if state[0].stats.max_depth > tree.stats.max_depth:
                state[0] = tree

        return state[2] is not None

    def best(self, state):
        """:param state: evaluation state.
        :return: the best solution evaluated with *state*.

        Optimal trees are always favored.
        """
        return state[2] or state[1] or state[0]


def _minimize_largest(a, b):
    return \
        cmp(a.stats.largest, b.stats.largest) or \
        cmp(b.stats.n, a.stats.n) or \
        cmp(a.root, b.root)

class MinimizeLargestPartition(builder.BuilderContext):
    SOLUTION_EVALUATOR = MinimizeMoveCount

    def __init__(self, problem, step, candidates=None):
        super(MinimizeLargestPartition, self).__init__(problem, step, candidates=candidates)
        self.answer = None
        self.prefix_set = frozenset(self.prefix)


    def compute_candidates(self):
        """Returns the root that mimimizes the largest subproblem.

        :return: an iterable of :py:class:`.PartitionResult` instances.
        """
        if not self.answer:
            self.answer = self._best_candidate()

        return self.answer


    def _best_candidate(self):
        if self.problem_size <= 2:
            return list(partition.PartitionResult(self.problem, c) for c in (min(self.problem),))

        best = partition.PartitionResult(self.problem, self.problem[0])
        for c in self.problem[1:]:
            pr = partition.PartitionResult(self.problem, c)
            if _minimize_largest(pr, best) < 0:
                best = pr

            if pr.stats.optimal:
                best = pr
                return (best,)

        for c in (CODETABLE.ALL_SET - frozenset(self.problem)) - self.prefix_set:
            pr = partition.PartitionResult(self.problem, c)
            if _minimize_largest(pr, best) < 0:
                best = pr

            if pr.stats.optimal:
                best = pr
                return (best, )

        return (best,)


STRATEGIES = {
    'random': builder.BuilderContext,
    'min_largest': MinimizeLargestPartition,
}
