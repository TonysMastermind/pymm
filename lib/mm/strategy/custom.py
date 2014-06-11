"""Custom candidate selection strategies."""

from . import *

from .. import *
from .. import builder as builder

BaseStrategy = STRATEGIES['min_moves_distinct']

class DebugExhaustiveDistinctLogic(BaseStrategy):

    def _best_candidates(self):
        base = super(DebugExhaustiveDistinctLogic, self)._best_candidates()

        if len(self.problem) == 105 and self.depth == 1:
            root = CODETABLE.encode((4,3,1,0))
            return (partition.PartitionResult(self.problem, root),)

        return base


STRATEGIES['debug_minmoves_distinct'] = DebugExhaustiveDistinctLogic

