TODO list
=========

.. todo::

  Optimize for early failure detection.

While constructing a tree, track cumulative move count and max-depth.
Reject as soon as it becomes worse that current best.  Order candidates 
by asecnding max-partition-size, descending partition-count, so that
the best tree is likely to come up early.

Adjust tree evaluator state to use a tracker similar to this:

.. code-block:: python

  class Tracker(object):
      def __init__(self):
          self.available_moves = MAX_INT
          self.max_depth = MAX_INT
	  self.best_tree = None

      def add_child(self, child):
          self.available_moves -= (child.stats.total_moves + child.problem_size)
          self.max_depth = min(self.max_depth, 1 + child.max_depth)
	  return self.available_moves < 0 or self.max_depth < child.max_depth

      def reset(self, t):
          self.available_moves = t.stats.total_moves
          self.max_depth = t.max_depth


.. todo::

   Use a pre-linked array of status objects instead of creating new ones.
   Add a ``reset()`` method to reinitialize them.
