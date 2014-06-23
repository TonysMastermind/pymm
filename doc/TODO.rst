TODO list
=========

.. todo::

  Optimize for early failure detection.

While constructing a tree, track cumulative move count and max-depth.
Reject as soon as it becomes worse that current best.  Order candidates 
by asecnding max-partition-size, descending partition-count, so that
the best tree is likely to come up early.


.. code-block:: python

  class BuilderStrategy(...):
      ...
          self.max_levels = ...
	  self.max_moves = ...
      ...

  class TreeBuilder(...):
      ...
      def _solve(strategy):
          ...

          for pr in candidates:
              remaining_moves = strategy.max_moves	      
              ...
              for (score, part) in ...:
                  ... # skip empty parts
                  if score == CODETABLE.PERFECT_SCORE:
                      remaining_moves -= 1
		      continue
                  else:
                      remaining_moves -= len(part)

                      # no moves left to solve the problem?
                      if remaining_moves <= 0:
                          ... # go to next candidate
			  break

                  ...
                  child = self._solve(self.strategy(part, ..., strategy.max_levels-1, max_moves, ...))
                  if not child:
                      ... # go to next candidate

                  max_moves -= child.stats.total_moves
                  ...
            

.. todo::

   Use a pre-linked array of status objects instead of creating new ones.
   Add a ``reset()`` method to reinitialize them.
