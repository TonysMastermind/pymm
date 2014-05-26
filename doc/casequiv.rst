
Case-Equivalent analysis
========================

Interesting stats
_________________

Using case-equivalence analysis, we have

    - 1 empty prefix.
    - 5 distinct prefixes of length 1.
    - 286 distinct 2-code prefixes, starting with the first 5.
        - (0000), or 0; 11 distinct codes.
        - (1000), or 1; 52 distinct codes.
        - (1100), or 7; 38 distinct codes.
        - (2100), or 8; 129 distinct codes.
        - (3210), or 51; 56 distinct codes.

We can generate the subproblems as follows:

.. code-block:: python

   for c in FIRST:
       pr = partition.result(pr, c)
       second_guesses = distinct_after_prefix((c,))
       for s in range(1, NSCORES):
           if not pr.parts[s]:
               continue
           for c2 in second_guesses:
               pr2 = partition.result(pr.parts[s], c2)
               for s2 in range(1, NSCORES):
                   if not pr2.parts[s2]:
                       continue
                   emit(problem=pr2.parts[s2], path=((c, c2), (s, s2)))


Calculating invariant transformations and distinct sets
=======================================================

:math:`T`
  All the the possible transformations on mastermind codes; 
  a set of 17,280 distinct elements.

:math:`C`
  All the possible mastermind codes.

:math:`invariant(x)`
  The subset of :math:`T` that does not vary the code :math:`x`; or

  :math:`\left\{ t \in T: t(x) = x \right\}`

:math:`invariant(\vec{x})`
  The subset of transformations that do not vary any of the codes 
  :math:`x_1`, :math:`x_2`, ...;  

  :math:`invariant(x_1) \cap invariant(x_2) \cap ...`.

Case equivalent: :math:`eqv(x, y)_{\vec{g}}`
  We say that :math:`x` and :math:`y` are case equivalent after a sequence
  of guesses (codes) :math:`\vec{g}` when there is a transformation in 
  :math:`invariant(\vec{g})` mapping :math:`x` to :math:`y`; or

  :math:`\exists t \in invariant(\vec{g}): t(x) = y`

:math:`distinct(\vec{g})`
  The smallest set of case equivalent codes following :math:`\vec{g}`
  
**Case-distinct stats:** There is only one empty prefix, five canonical prefixes
of size 1 (0000, 1000, 1100, 2100, 3210), and 286 distinct 2-code prefixes
generated from the first 5, each paired with its case-distinct set elements.
Of the 286 2-element prefixes, 31 provide full resolution; meaning that all
codes are case-distinct after them, and consequently after any prefix that
starts with them.  For 3-code prefixes, we skipped over prefixes that have
degenerate invariant sets, with the results shown below::

  prefix |  all   | wild
  length |  count | count
  -------+--------+-------
       0 |      1 |    n/a
       1 |      5 |      0
       2 |    286 |      0
       3 |  43660 |     31

**Invariant transform stats:** For these, we go as far as 3-element prefixes.
For these, the trivial case is a one-element result containing the identity
transfomration.  For prefixes that lead to a trivial result, all longer
prefixes are also trivial.  At the 3-element level, more than half of the
prefixes lead to trivial results::

  prefix |  all   | wild
  length |  count | count
  -------+--------+-------
       0 |      1 |    n/a
       1 |      5 |      0
       2 |    286 |      0
       3 | 110289 |     31
       4 |    n/a |  66629

*Size problems:*  Storing data for 3-element prefixes is expensive.  The
program grows over 2GB in memory.  The pickle files are: 150MB for the
case-distinct data, and 8MB for the invariants.  Currently, the case-distinct
tables are restricted to 2-elements to keep the sizes down.

With a 2-element limit on both case-distinct and invariant tables, the 
program's resident footprint is approximately 153MB.

With the invariant tables allowed to use three-element prefixes, the footprint
is approximately 401MB.


Policy Driven partition result collector
========================================

  Basic policies controlling collectors:
    - root selection controls whether case-distinct logic is applied.
    - thus, at this level, we look at:
      - structural equivalence: :py:class:`mm.partition.result.signature` and 
      :py:class:`mm.partition.result.long_signature`
      - ranking and selection:

          - pick best (only one).
          - pick best (one and its equivalents).
          - picking multiple based on ranking:

            - pick best N ranks (each, with its equivalents).
            - pick best P% ranks.
            - pick best ranks based on a *distance* based on
              the worst and best ranks.

  Something like:

.. code-block:: python

    collector_class(
        equivalence= 'long_sig'|'short_sig'|None,
        mode= 'single'|'multi',
        input_ranking= None|callable,
        output_ranking= None|callable,
        output_selection= None|callable
    )

