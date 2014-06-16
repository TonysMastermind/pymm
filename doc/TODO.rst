TODO list
=========

.. todo::

  Optimize for early failure detection.

While constructing a tree, track cumulative move count and max-depth.
Reject as soon as it becomes worse that current best.  Order candidates 
by asecnding max-partition-size, descending partition-count, so that
the best tree is likely to come up early.

.. code-block:: python

  # use a priority queue for this, should be more efficient.
  candidates = sorted(candidates, 
                      lambda a, b: cmp(a.stats.largest, b.stats.largest) or
		                   cmp(b.stats.n, a.stats.n))

  for c in candidates:
      cur_best = None

      ...

      moves = 0
      max_depth = 0

      parts = ((s, p) for (s, p) in enumerate(c.parts) if len(p))
      parts = sorted(parts, lambda a, b: cmp(b[1].stats.largest, a[1].stats.largest))

      t = tree.Tree(c.root)
      if c.stats.in_solution:
          t.root_in_solution = True
          moves += 1

      for (s, p) in parts:
          ...
          child = self._solve(...)
	  t.add_child(child) # must update stats dynamically.

          if cur_best and self.better_tree(t, cur_best) is not t:
	      t = None
              break

      if t is None:
          continue

      # evaluate
      # set cur_best

  ...

