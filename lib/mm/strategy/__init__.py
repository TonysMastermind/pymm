"""Collection of strategies."""

from .. import *
from .. import builder as builder
from .. import partition as partition

class MinimizeMoveCount(builder.SolutionEvaluator):
    """A tree evaluator, picks the tree with the fewest moves.  When there's
    a tie, the evaluator favors lower depth.

    The evaluator recognizes optimal trees, and favors them over other trees.
    """

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
            state[0] = tree
        elif state[0].stats.total_moves == tree.stats.total_moves:
            if state[0].root_in_solution == tree.root_in_solution:
                if state[0].stats.max_depth > tree.stats.max_depth:
                    state[0] = tree
            elif tree.root_in_solution:
                state[0] = tree

        return state[2] is not None


    def best(self, state):
        """:param state: evaluation state.
        :return: the best solution evaluated with *state*.
        """
        return state[2] or state[1] or state[0]

class MinimizeTreeDepth(builder.SolutionEvaluator):
    """A tree evaluator, picks the shallowest tree.  When there's a tie, the
    evaluator favors lower depth.

    The evaluator recognizes optimal trees, and favors them over other trees.
    """

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
        elif state[0].stats.max_depth < tree.stats.max_depth:
            state[0] = tree
        elif state[0].stats.max_depth == tree.stats.max_depth:
            if state[0].stats.total_moves > tree.stats.total_moves:
                state[0] = tree

        return state[2] is not None


    def best(self, state):
        """:param state: evaluation state.
        :return: the best solution evaluated with *state*.
        """
        return state[2] or state[1] or state[0]


def _not_implemented():
    raise MMException("Not implemented.")


class OptimizePartitionResultProperty(builder.BuilderContext):
    """General purpose property optimizer for :py:class:`..partition.PartitionResult`
    
    The method :py:meth:`.OptimizePartitionResultProperty.compare` is the
    primary point of specialization.
    """

    SOLUTION_EVALUATOR = MinimizeMoveCount
    """Tree evaluator class."""

    restrict_to_problem = False
    """When true, candidate comupation is restricted to the problem; otherwise
    the selection examines all possible codes."""


    def __init__(self, problem, step, candidates=None, **kwargs):
        """:param problem: problem under analysis.
        :param step: from parent problem to this problem.
        :param candidates: pre-selected candidates.
        """
        super(OptimizePartitionResultProperty, self).__init__(problem, step, candidates=candidates, **kwargs)

        self._answer = None
        self._prefix_set = frozenset(self.prefix)


    def compute_candidates(self):
        """Returns the root that optimizes the partition result property defined by the *compare*
        method.

        :return: an iterable of :py:class:`..partition.PartitionResult` instances.
        """
        if not self._answer:
            self._answer = self._best_candidate()

        return self._answer


    _comparator_sequence = [lambda a, b: _not_implemented()]


    def compare(self, a, b):
        """Defines an ordering on partition results, with *a < b* equivalent to 
        *a is better than b*.

        This implementation raises an exception, requiring specialization with
        real implementations.

        :param a: a partition result of the problem.
        :type a: :py:class:`..partition.PartitionResult`
        :param b: another partition result of the same problem.
        :type b: :py:class:`..partition.PartitionResult`
        :returns: a negative number if *a is better than b*, a positive number if *b is better than a*,
          zero otherwise.
        """
        for f in self._comparator_sequence:
            r = f(a, b)
            if r:
                return r

        return 0

    def _best_candidate(self):
        if self.problem_size <= 2:
            return list(partition.PartitionResult(self.problem, c) for c in (min(self.problem),))

        best = partition.PartitionResult(self.problem, self.problem[0])
        for c in self.problem[1:]:
            pr = partition.PartitionResult(self.problem, c)
            if self.compare(pr, best) < 0:
                best = pr

            if pr.stats.optimal:
                best = pr
                return (best,)

        if self.restrict_to_problem:
            return (best,)

        for c in (CODETABLE.ALL_SET - frozenset(self.problem)) - self._prefix_set:
            pr = partition.PartitionResult(self.problem, c)
            if self.compare(pr, best) < 0:
                best = pr

            if pr.stats.optimal:
                best = pr
                return (best, )

        return (best,)


class MinimizeLargestPartition(OptimizePartitionResultProperty):
    """Policy to minimize largest partition size.  When partition sizes are
    tied, partition count optimization is used.
    """

    _comparator_sequence = [
        lambda a, b: cmp(a.stats.largest, b.stats.largest),
        lambda a, b: cmp(b.stats.n, a.stats.n),
        lambda a, b: cmp(b.stats.in_solution, a.stats.in_solution),
        lambda a, b: cmp(a.root, b.root)
        ]


class MaximizePartitionCount(OptimizePartitionResultProperty):
    """Policy to maximize partition count.  When partition counts are tied,
    largest partition size optimization is used.
    """

    _comparator_sequence = [
        lambda a, b: cmp(b.stats.n, a.stats.n),
        lambda a, b: cmp(a.stats.largest, b.stats.largest),
        lambda a, b: cmp(b.stats.in_solution, a.stats.in_solution),
        lambda a, b: cmp(a.root, b.root)
        ]



class MinimizeLargestPartition01(OptimizePartitionResultProperty):
    """Policy to minimize largest partition size.  When partition sizes are tied, 
    in-problem choices are favored, then partition count optimization is used.
    """

    _comparator_sequence = [
        lambda a, b: cmp(a.stats.largest, b.stats.largest),
        lambda a, b: cmp(b.stats.in_solution, a.stats.in_solution),
        lambda a, b: cmp(b.stats.n, a.stats.n),
        lambda a, b: cmp(a.root, b.root)
        ]


class MaximizePartitionCount01(OptimizePartitionResultProperty):
    """Policy to maximize partition count.  When partition counts are tied,
    in-problem choices are favored, then largest partition size optimization is used.
    """

    _comparator_sequence = [
        lambda a, b: cmp(b.stats.n, a.stats.n),
        lambda a, b: cmp(b.stats.in_solution, a.stats.in_solution),
        lambda a, b: cmp(a.stats.largest, b.stats.largest),
        lambda a, b: cmp(a.root, b.root)
        ]


class MinimizeLargestPartitionInProblem(MinimizeLargestPartition):
    """A specialization of :py:class:`.MinimizeLargestPartition` restricting
    candidate choices to the problem.
    """
    restrict_to_problem = True

class MaximizePartitionCountInProblem(MaximizePartitionCount):
    """A specialization of :py:class:`.MaximizePartitionCount` restricting
    candidate choices to the problem.
    """
    restrict_to_problem = True


STRATEGIES = {
    'random': builder.BuilderContext,
    'min_largest': MinimizeLargestPartition,
    'max_parts': MaximizePartitionCount,
    'min_largest_in': MinimizeLargestPartitionInProblem,
    'max_parts_in': MaximizePartitionCountInProblem,
    'min_largest_01': MinimizeLargestPartition01,
    'max_parts_01': MaximizePartitionCount01,
}
"""Maps symbolic names to strategy classes."""
