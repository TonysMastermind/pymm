"""Advanced candidate selection strategies using case-equivalence to reduce choices."""

from . import *

from .. import *
from .. import builder as builder
from .. import distinct as distinct
from .. import partition as partition
from .. import xforms as xforms


class ScanDistinctFollowers(builder.BuilderContext):
    """General purpose property optimizer for :py:class:`..partition.PartitionResult`
    that reduces the initial code set using case-equivalence, and may yield multiple
    results.
    
    The method :py:meth:`.OptimizePartitionResultProperty.compare` is the
    primary point of specialization.
    """

    SOLUTION_EVALUATOR = MinimizeMoveCount
    """Tree evaluator class."""

    restrict_to_problem = False
    """When true, candidate comupation is restricted to the problem; otherwise
    the selection examines all possible codes."""


    def __init__(self, problem, step, candidates=None):
        """:param problem: problem under analysis.
        :param step: from parent problem to this problem.
        :param candidates: pre-selected candidates.
        """
        super(ScanDistinctFollowers, self).__init__(problem, step, candidates=candidates)

        self._answer = None
        self._prefix_set = frozenset(self.prefix)
        self._problem_set = frozenset(problem)

        self._set_distinct_candidates()


    def _set_distinct_candidates(self):
        self._set_root_problem()
        self._set_preserving()

        if len(self._preserving) == 1:
            if self.restrict_to_problem:
                self._distinct_candidates = tuple(self._problem_set - self._prefix_set)
            else:
                self._distinct_candidates = tuple(self._root_problem - self._prefix_set)
            return

        if not self.parent:
            if len(self.problem) == CODETABLE.NCODES:
                self._distinct_candidates = CODETABLE.FIRST
                return

        pg = distinct.PrefixGen()

        p = self._root_problem
        if self.restrict_to_problem:
            p = self._problem_set
        self._distinct_candidates = tuple(pg.distinct_subset(self._preserving, p, self._prefix_set))


    def _set_preserving(self):
        XFTBL = xforms.XF_LOOKUP_TABLE # must have been initialized.
        if not self.parent:
            self._preserving = XFTBL.ALL
            return

        p0 = self.parent._preserving
        if len(p0) == 1:
            self._preserving = p0
            return

        c = self.path[-1].root
        self._preserving = XFTBL.preserving((c,), seed=p0)


    def _set_root_problem(self):
        self._root_problem = None

        if self.parent:
            self._root_problem = self.parent._problem_set
        else:
            self._root_problem = self._problem_set


    def compute_candidates(self):
        """Returns the root that optimizes the partition result property defined by the *compare*
        method.

        :return: an iterable of :py:class:`..partition.PartitionResult` instances.
        """
        if not self._answer:
            self._answer = self._best_candidates()

        return self._answer


    def _best_candidates(self):
        if self.problem_size <= 2:
            return list(partition.PartitionResult(self.problem, c) for c in (min(self.problem),))

        candidates = []
        optimal = None
        for c in self._distinct_candidates:
            pr = partition.PartitionResult(self.problem, c)
            if pr.stats.optimal:
                if pr.stats.in_solution:
                    return (pr,)
                elif not optimal:
                    optimal = pr
                elif optimal.root > c:
                    optimal = pr

            candidates.append(pr)

        if optimal:
            return (optimal,)

        return tuple(candidates)


class MinimizeMoveCountUsingDistinctInProblem(ScanDistinctFollowers):
    restrict_to_problem = True
    SOLUTION_EVALUATOR = MinimizeMoveCount


class MinimizeMoveCountUsingDistinct(ScanDistinctFollowers):
    restrict_to_problem = False
    SOLUTION_EVALUATOR = MinimizeMoveCount


class MinimizeDepthUsingDistinctInProblem(ScanDistinctFollowers):
    restrict_to_problem = True
    SOLUTION_EVALUATOR = MinimizeTreeDepth


class MinimizeDepthUsingDistinct(ScanDistinctFollowers):
    restrict_to_problem = False
    SOLUTION_EVALUATOR = MinimizeTreeDepth


STRATEGIES.update({
        'min_moves_distinct_in': MinimizeMoveCountUsingDistinctInProblem,
        'min_moves_distinct':  MinimizeMoveCountUsingDistinct,
        'min_depth_distinct_in': MinimizeDepthUsingDistinctInProblem,
        'min_depth_distinct': MinimizeDepthUsingDistinct,
        })
