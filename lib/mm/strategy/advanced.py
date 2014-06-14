"""Advanced candidate selection strategies using case-equivalence to reduce choices."""

from . import *

from .. import *
from .. import builder as builder
from .. import distinct as distinct
from .. import partition as partition
from .. import xforms as xforms

MAX_PROBLEM_SIZE = (CODETABLE.NCODES,           # 0, 1296
                    CODETABLE.NCODES/4,         # 1, 324
                    CODETABLE.NCODES/4/4,       # 2, 81
                    CODETABLE.NCODES/4/4/4,     # 3, 20
                    CODETABLE.NCODES/4/4/4/4,   # 4, 5
                    CODETABLE.NCODES/4/4/4/4/4) # 5, 1

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

    restrict_problem_size = False
    """When true, candidate comupation fails when the problem size exceeds pre-specified
    thresholds (at each depth)."""


    def __init__(self, problem, step, candidates=None, **kwargs):
        """:param problem: problem under analysis.
        :param step: from parent problem to this problem.
        :param candidates: pre-selected candidates.
        """
        super(ScanDistinctFollowers, self).__init__(problem, step, candidates=candidates, **kwargs)

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
        self._root_problem = self._problem_set

        if self.parent:
            self._root_problem = self.parent._root_problem


    def compute_candidates(self):
        """Returns the root that optimizes the partition result property defined by the *compare*
        method.

        :return: an iterable of :py:class:`..partition.PartitionResult` instances.
        """
        if self._answer is None:
            if self.restrict_problem_size and \
                    self.depth < len(MAX_PROBLEM_SIZE) and \
                    self.problem_size > MAX_PROBLEM_SIZE[self.depth]:
                self._answer = ()
            else:
                self._answer = self._best_candidates()


        return self._answer


    def _best_candidates(self):
        if self.problem_size <= 2:
            return (partition.PartitionResult(self.problem, min(self.problem)), )

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
    """Strategy to minimize move count in tree, using case-equivalence to reduce
    candidates.  Restricts candidates to current problem."""
    restrict_to_problem = True
    SOLUTION_EVALUATOR = MinimizeMoveCount


class MinimizeMoveCountUsingDistinct(ScanDistinctFollowers):
    """Strategy to minimize move count in tree, using case-equivalence to reduce
    candidates.  Uses all codes as candidates."""
    restrict_to_problem = False
    SOLUTION_EVALUATOR = MinimizeMoveCount

class MinimizeMoveCountUsingDistinctOpt(MinimizeMoveCountUsingDistinct):
    """Strategy to minimize move count in tree, using case-equivalence to reduce
    candidates.  Uses all codes as candidates.  Fails when the problem size exceeds
    a pre-specified threshold based on the path to the tree's problem."""
    restrict_problem_size = True

class MinimizeDepthUsingDistinctInProblem(ScanDistinctFollowers):
    """Strategy to minimize tree depth, uses case-equivalence to reduce candidates.
    Restricts candidates to current problem."""
    restrict_to_problem = True
    SOLUTION_EVALUATOR = MinimizeTreeDepth


class MinimizeDepthUsingDistinct(ScanDistinctFollowers):
    """Strategy to minimize tree depth, uses case-equivalence to reduce candidates.
    Restricts candidates to current problem. Considers all codes as candidates."""
    restrict_to_problem = False
    SOLUTION_EVALUATOR = MinimizeTreeDepth


class MinimizeDepthUsingDistinctOpt(MinimizeDepthUsingDistinct):
    """Strategy to minimize tree depth, uses case-equivalence to reduce candidates.
    Restricts candidates to current problem. Considers all codes as candidates.
    Fails when the problem size exceeds a pre-specified threshold based on the 
    path to the tree's problem."""
    restrict_problem_size = True

STRATEGIES.update({
        'min_moves_distinct_in': MinimizeMoveCountUsingDistinctInProblem,
        'min_moves_distinct':  MinimizeMoveCountUsingDistinct,
        'min_moves_distinct_opt':  MinimizeMoveCountUsingDistinctOpt,
        'min_depth_distinct_in': MinimizeDepthUsingDistinctInProblem,
        'min_depth_distinct': MinimizeDepthUsingDistinct,
        'min_depth_distinct_opt': MinimizeDepthUsingDistinctOpt,
        })
