"""Mastermind Strategy Tree builder."""

from . import *
from . import descr 
from . import partition 
from . import progress
from . import score
from . import tree
from . import usage
from . import xforms

from partition import PartitionResult
from progress import ReportingCalculationStatus

from collections import namedtuple
import datetime
import os
import random
import sys

SOCKET_NAME_TEMPLATE = 'unix://default//tmp/mm.progress.{}'
"""Default datagram socket address template, instantiated with a process id."""

_MAX_PARTS = CODETABLE.NSCORES - 1

_PROBLEM_SIZE_LIMITS = [ -1, 1 ]
_MAX_REMAINING = 1000

_SCORE_LIST = range(CODETABLE.NSCORES)

def size_limit(remaining):
    """Calculates an upper bound on problem size for the given number of guesses.

    This upper bound is a hypothetical number based on the number of possible score values,
    and the number of guesses, using arithmetic.  For a maximum problem size of :math:`N`, 
    and :math:`P` possible score values, the limit :math:`L(i)` for *i* moves is:

    - :math:`L(0) = 0`
    - :math:`L(i+1) = min(1 + (P-1)L(i), N)`


    For example, given 4 positions, there are 14 possible scores, and the limits on 
    problem sizes are:

    - For 2 guesses: :math:`1 + 13 = 14`
    - For 3 guesses: :math:`1 + 13(1 + 13)= 183` 
    - For 4 guesses: the upper limit on problem is :math:`1 + 13(1 + 13(1 + 13)) = 2380`,
      which exceeds the maximum problem size in the *(6color, 4pos)* mastermind problem.

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



BuilderStep = namedtuple('BuilderStep', ['root', 'score', 'origin'])
"""Derivation step from a :py:class:`.BuilderContext` to a child instance.

:param origin: the :py:class:`.BuilderContext` where the problem resides.
:param root: a mastermind numeric code representing a guess againts the origin's problem.
:param score: a score resulting from guessing *root* against the origin's problem.
"""

class BuilderContext(descr.WithDescription):
    """Tree construction context."""

    SOLUTION_EVALUATOR = SolutionEvaluator
    """Solution evaluator class."""

    STEP_CLASS = BuilderStep
    """Step class."""

    def __init__(self, problem, step, candidates=None, status_socket=None):
        """
        :param parent: parent context.
        :param problem: problem to be solved.
        :param step: a *(guess, score)* pair indicating the derivation of the problem from
          its parent.
        :param candidates: a preselected collection of candidates to use for solving
          the problem.
        :type candidates: collection of :py:class:`.partition.PartitionResult`
        :param status_socket: optional address to report status to.
        :type status_socket: str.
        """

        self.status_socket = status_socket or SOCKET_NAME_TEMPLATE.format(os.getpid())
        """Socket address where progress messages sent.  Initialized from the input
        parameter by the same name when not null/empty, otherwise, instantiates
        :py:data:`.SOCKET_NAME_TEMPLATE` with the process id, and uses the result.

        The syntax for this attribute is: ``unix://<id>/<path>``, or ``ip://<id>/<host>:<port>``.

        For IP addresses, the host will be resolved and its address used for the lifetime 
        of the program.   This may be an issue with long-lived solvers and dynamically 
        changing addresses.

        The ``<id>`` component identifies the message source.  Since ``/`` is the syntactic delimiter,
        an ``<id>`` cannot contain that character.

        If ``<path>`` component is an absolute path, then it must start with a ``/``; 
        see :py:data:`.SOCKET_NAME_TEMPLATE`, which uses an absolute path.
        """

        self.candidates = candidates
        """Preselected initial guess candidats."""

        self.parent = None
        """Parent context."""

        self.problem = problem
        """Problem being solved."""

        self.path = None
        """A sequence of *(code, score)* pairs from the root problem to the current problem."""

        self.prefix = None
        """A sequence of numeric codes, representing the first elements :py:attr:`.BuilderContext.path` items."""

        if step:
            self.parent = step.origin
            self.path = self.parent.path + (step,)
            self.prefix = self.parent.prefix + (step.root,)
            self.status = ReportingCalculationStatus(step.origin.status, len(self.problem))
        else:
            self.parent = None
            self.path = tuple()
            self.prefix = tuple()
            self.status = ReportingCalculationStatus(None, len(self.problem), root_ctx=self)


    def step(self, root, score):
        """Constructs a solution step.

        :param root: mastermind code in numeric form.
        :param score: match score in numeric form.
        :return: an instance of :py:class:`.BuilderStep`
        """
        return self.STEP_CLASS(root, score, self)


    @property
    def depth(self):
        """:return: the length of the parent chain above."""
        return len(self.path)


    @property
    def problem_size(self):
        """:return: the size of the mastermind problem."""
        return len(self.problem)


    @classmethod
    def preselected(clazz, problem, root):
        return (PartitionResult(problem, root),)

    def candidate_guesses(self):
        """Returns a selection of guesses suitable for solving the current problem.

        :return: an iterable of :py:class:`.PartitionResult` instances.

        If the attribute :py:attr:`.candidates`, then method returns its value.
        Otherwise, it delegates to the method :py:meth:`.BuilderContext.compute_candidates`.
        """
        if self.candidates:
            return self.candidates

        return self.compute_candidates()


    def compute_candidates(self):
        """Returns a collection of candidate guesses suitable for use on the context's problem.

        :return: an iterable of :py:class:`.PartitionResult` instances.

        This method is expected to derive the candidates algorithmically from the problem, and is
        the critical specialization point of this class.

        The default implementation picks a random member of the problem, and returns it.

        .. note::

          Given a problem of size *n*, using a member of the problem set that is not
          on the path to the current problem guarantees that the next largest 
          subproblem has at most *n-1* elements, since the partition result will
          always get populated at the perfect score.
        """
        # Since the strategy consistely chooses from the problem set, the
        # members of the prefix are always excluded from subproblems, making
        # the choice below safe.
        c = random.choice(self.problem)
        return (PartitionResult(self.problem, c), )


    def solution_evaluator(self):
        """:return: a solution evaulator, a instance of :py:class:`.SolutionEvaluator`.

        This method can be specialized to provide more interesting evaluation algorithms.
        """
        return self.SOLUTION_EVALUATOR()


    def possible(self, remaining):
        """:return: false if the problem cannot be solved with the given number of guesses.
        :param remaining: maximum number of guesses allowed for the problem.

        This calculation is based on problem size, and not its composition.  Consequently, a 
        true response does not imply the existence of a solution within the specified number of
        guesses.  However, a false result means that it's impossible split the current problem
        into subproblems of size 1 with the given budget of moves.
        """
        return remaining > 0 and self.problem_size <= size_limit(remaining)


    @classmethod
    def description(clazz):
        return descr.base_description(clazz)

    @classmethod
    def build_tree(clazz, problem, maxdepth, root=None, progress=None):
        return TreeBuilder(clazz, problem, progress).build(maxdepth, root=root)



class TreeBuilder(descr.WithDescription):
    """Tree builder framework."""

    def __init__(self, strategy, problem, progress):
        """:param strategy: strategy/context class.
        :param problem: the master mind problem, a collection of codes in numeric form.
        :type problem: list, or tuple.
        :param progress: destination of progress messages.  See :py:module:`.progress` for details.
        """

        self.strategy = strategy
        """Builder strategy."""

        self.root_problem = problem
        """Root problem."""

        self.entry_count = 0
        """Number of times the recursive solver has been entered."""

        self.reporting_cycle = 10000
        """Progress sampling cycle, once per :py:attr:`.TreeBuilder.reporting_cycle` entries
        into recursive solver."""

        self.progress = progress
        """Destination of progress messages."""

    def description_qualifiers(self):
        return {
            'strategy': self.strategy.description(),
            'problem_size': len(self.root_problem)
            }


    def build(self, maxdepth, root=None):
        """Build a tree.

        :param maxdepth: maximum game length.
        :param root: optional initial guess.
        :return: an instance of :py:class:`.tree.TreeResult` representating a strategy.
        """
        candidates = None
        if root:
            candidates = self.strategy.preselected(self.root_problem, root)

        ctx = self.strategy(self.root_problem, None, candidates, status_socket=self.progress)
        (u, t) = usage.time(lambda: self._solve(ctx, maxdepth))
        if t:
            t.stats.set_timing(u)

        t = tree.TreeResult(t, maxdepth, self.strategy, u, root)
        return t


    def _solve(self, ctx, remaining):
        self.entry_count += 1
        if self.entry_count % self.reporting_cycle == 0:
            ctx.status.report(self.entry_count)

        if not ctx.possible(remaining):
            return None

        n = ctx.problem_size
        if n == 1:
            return tree.one_element_tree(ctx.problem[0])
        if n == 2:
            return tree.two_element_tree(ctx.problem)

        candidates = ctx.candidate_guesses()
        if not candidates:
            return None

        ctx.status.candidate_count = len(candidates)

        evaluator = ctx.solution_evaluator()
        state = evaluator.initial_state()

        for pr in candidates:
            ctx.status.next_candidate(pr)

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

                # Proceed thru parts in descending size.  Larger partitions
                # are more likely to fail under a depth constraint than smaller
                # ones.
                for score in sorted(_SCORE_LIST, lambda a, b: cmp(len(pr.parts[b]), 
                                                                  len(pr.parts[a]))):
                    prob = pr.parts[score]
                    if not prob: # we hit the zeros, exit loop.
                        break

                    # count a non-empty child
                    ctx.status.cur_child += 1

                    if score == CODETABLE.PERFECT_SCORE:
                        continue

                    child = self._solve(self.strategy(prob, ctx.step(pr.root, score)),
                                        remaining - 1)
                    if not child:
                        subtrees = None
                        break

                    subtrees[score] = child

                if not subtrees: # failed building subtrees.
                    continue # to next candidate

                t = tree.Tree(pr.root)
                for score in _SCORE_LIST:
                    t.add_child(score, subtrees[score])
                t.update_stats(pr)

                if evaluator.evaluate(ctx, t, state):
                    return evaluator.best(state)

        result = evaluator.best(state)
        return result
