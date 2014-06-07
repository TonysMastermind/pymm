"""Mastermind Strategy Tree builder."""

from . import *
from . import partition 
from . import descr 
from . import score
from . import tree
from . import usage

from partition import PartitionResult

import random

_MAX_PARTS = CODETABLE.NSCORES - 1

_PROBLEM_SIZE_LIMITS = [ -1, 1 ]
_MAX_REMAINING = 1000

_SCORE_LIST = range(CODETABLE.NCODES)

def size_limit(remaining):
    """
    A problem of size 2 requires 2 moves.  

    Given 4 positions, there are 14 possible scores, and the limits on problem sizes are:

    - For 2 guesses: :math:`1 + 13 = 14`
    - For 3 guesses: :math:`1 + 13(1 + 13)= 183` 
    - For 4 guesses: the upper limit on problem is :math:`1 + 13(1 + 13(1 + 13)) = 2380`,
      which exceeds the maximum problem size in the *(6color, 4pos)* mastermind problem.

    Given a maximum problem size of :math:`N`, and a maximum partition count of :math:`P`, we have:

    - :math:`L(0) = 0`
    - :math:`L(i+1) = max(1 + (P-1)L(i), N)`

    """

    global _PROBLEM_SIZE_LIMITS
    global _MAX_REMAINING

    remaining = max(0, remaining)
    if remaining < len(_PROBLEM_SIZE_LIMITS):
        return _PROBLEM_SIZE_LIMITS[remaining]

    if remaining >= _MAX_REMAINING:
        return CODETABLE.NCODES

    while remaining >= len(_PROBLEM_SIZE_LIMITS):
        m = len(_PROBLEM_SIZE_LIMITS)
        x = _PROBLEM_SIZE_LIMITS[-1]
        y = 1 + x * (_MAX_PARTS - 1)
        if y >= CODETABLE.NCODES:
            _MAX_REMAINING = m
            return CODETABLE.NCODES
        _PROBLEM_SIZE_LIMITS.append(y)

    return size_limit(remaining)


class SolutionEvaluator(descr.WithDescription):
    """Strategy tree evaluator.

    The base implementation considers a non-null strategy tree to be the best
    possible result.
    """

    def initial_state(self):
        """:return: initial evaluation state.

        The evaluation state is updated with each evaluation.  At every
        evaluation, the state is updated.  The best solution can be chosen
        by calling :py:meth:`.SolutionEvaluator.best` on the state.
        """
        return [None]


    def evaluate(self, ctx, tree, state):
        """Evaluate the strategy tree in the given context, and update evaluation
        state.

        :param ctx: problem context.
        :param tree: subject of evaluation.
        :param state: state of the evaluation.
        :return: True to indicate that the best possible solution was found, and futher
          evaluations cannot improve the current best; False otherwise.
        """
        if tree:
            state[0] = tree
            return True
        return False


    def best(self, state):
        """:param state: evaluation state.
        :return: the best solution evaluated with *state*.
        """
        return state[0]

    @classmethod
    def description(clazz):
        return descr.base_description(clazz)


class BuilderContext(object):
    """Tree construction context."""

    SOLUTION_EVALUATOR = SolutionEvaluator

    def __init__(self, parent, problem, step, candidates=None):
        """
        :param parent: parent context.
        :param problem: problem to be solved.
        :param step: a *(guess, score)* pair indicating the derivation of the problem from
          its parent.
        :param candidates: a preselected collection of candidates to use for solving
          the problem.
        :type candidates: collection of :py:class:`.partition.PartitionResult`
        """

        score.initialize()

        self.candidates = candidates
        """Preselected initial guess candidats."""

        self.parent = parent
        """Parent context."""

        self.problem = problem
        """Problem being solved."""

        self.path = None
        """A sequence of *(code, score)* pairs from the root problem to the current problem."""

        self.prefix = None
        """A sequence of numeric codes, representing the first elements :py:attr:`.BuilderContext.path` items."""

        if parent:
            self.path = parent.path + (step,)
            self.prefix = parent.prefix + (step[0],)
        else:
            self.path = tuple()
            self.prefix = tuple()


    @property
    def depth(self):
        """:return: the length of the parent chain above."""
        return len(self.path)

    @property
    def problem_size(self):
        """:return: the size of the mastermind problem."""
        return len(self.problem)

    def candidate_guesses(self):
        """Returns a selection of guesses suitable for solving the current problem.

        :return: an iterable collection of :py:class:`.PartitionResult` instances.

        If the attribute :py:attr:`.candidates`, then method returns its value.
        Otherwise, the method picks a random member of the problem, and returns it.

        The default implementation picks a random member of the problem, unless
        the is set to a non-null value. 

        .. note::

          Given a problem of size *n*, using a member of the problem set that is not
          on the path to the current problem guarantees that the next largest 
          subproblem has at most *n-1* elements, since the partition result will
          always get populated at the perfect score.
        """
        if self.candidates:
            return self.candidates

        # Since the strategy consistely chooses from the problem set, the
        # members of the prefix are always excluded from subproblems, making
        # the choice below safe.
        c = random.choice(self.problem)
        return (PartitionResult(self.problem, c), )


    def solution_evaluator(self):
        """:return: a solution evaulator, a instance of :py:class:`.SolutionEvaluator`.

        This method can be specialized to provide more interesting evaluation algorithms.
        """
        return self.__class__.SOLUTION_EVALUATOR()
    

    def possible(self, remaining):
        """:return: false if the problem cannot be solved with the given number of guesses.
        :param remaining: maximum number of guesses allowed for the problem.

        This calculation is based on problem size, and not its composition.  Consequently, a 
        true response does not imply the existence of a solution within the specified number of
        guesses.  However, a false result means that it's impossible split the current problem
        into subproblems of size 1 with the given budget of moves.
        """
        return self.problem_size <= size_limit(remaining)

    @classmethod
    def description(clazz):
        return descr.base_description(clazz)


class TreeBuilder(descr.WithDescription):
    """Tree builder framework."""

    def __init__(self, strategy, problem):
        """:param strategy: strategy/context class.
        :param problem: the master mind problem, a collection of codes in numeric form.
        :type problem: list, or tuple.
        """
        self.strategy = strategy
        self.root_problem = problem


    def build(self, maxdepth, root=None):
        """Build a tree.

        :param maxdepth: maximum game length.
        :param root: optional initial guess.
        :return: an instance of :py:class:`.tree.TreeResult` representating a strategy.
        """
        candidates = None
        if root:
            candidates = (PartitionResult(self.root_problem, root),)

        ctx = self.strategy(None, self.root_problem, None, candidates)
        (u, t) = usage.time(lambda: self._solve(ctx, maxdepth))
        return tree.TreeResult(t, maxdepth, self.strategy, u)


    def _solve(self, ctx, remaining):
        if not ctx.possible(remaining):
            return None

        n = ctx.problem_size
        if n == 1:
            return tree.one_element_tree(ctx.problem[0])
        if n == 2:
            return tree.two_element_tree(ctx.problem)

        candidates = ctx.candidate_guesses()
        evaluator = ctx.solution_evaluator()
        state = evaluator.initial_state()

        for pr in candidates:
            s = pr.stats
            if s.n < 2: # not a usable guess.
                continue

            t = None
            if pr.stats.optimal:
                t = tree.optimal_tree(pr)
                if evaluator.evaluate(ctx, t, state):
                    return evaluator.best(state)
            else:
                subtrees = [None] * CODETABLE.NSCORES
                for (score, prob) in zip(_SCORE_LIST, pr.parts):
                    if (not prob) or (score == CODETABLE.PERFECT_SCORE):
                        continue

                    child = self._solve(self.strategy(ctx, prob, (pr.root, score)), 
                                        remaining - 1)
                    if not child:
                        subtrees = None
                        break

                    subtrees[score] = child

                if not subtrees: # failed building subtrees.
                    continue

                t = tree.Tree(pr.root)
                for (score, child) in zip(_SCORE_LIST, subtrees):
                    t.add_child(score, child)
                t.update_stats(pr)

                if evaluator.evaluate(ctx, t, state):
                    return evaluator.best(state)

        result = evaluator.best(state)
        return result
