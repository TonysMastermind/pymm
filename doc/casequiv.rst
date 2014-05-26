
==========================
 Case-Equivalent analysis
==========================

Terms
=====


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
  We say that :math:`x` and :math:`y` are *case equivalent after a sequence
  of guesses (codes)* :math:`\vec{g}` when there is a transformation in 
  :math:`invariant(\vec{g})` mapping :math:`x` to :math:`y`; or

  :math:`eqv(x,y)_{\vec{g}} \iff \exists t \in invariant(\vec{g}): t(x) = y`, or

  :math:`eqv(x,y)_{\vec{g}} \iff \exists t \in T: t(\vec{g}) = \vec{g} \land t(x) = y`

:math:`distinct(\vec{g})`
  The smallest set of case equivalent codes following :math:`\vec{g}`:

  :math:`\left\{\forall x \in (C - \vec{g}): min(t(x) \forall t \in invariant(\vec{g})) \right\}`, or

  :math:`\bigcup_{x \in (C - \vec{g})} min(y \in C: eqv(x, y)_{\vec{g}})`


Interesting stats
=================


Using case-equivalence analysis, we have:

.. table:: Prefixes for length 2 or less (count).
  :widths: 1 1
  :column-wrapping: true true
  :column-alignment: right right
  :column-dividers: single single single

  ================= ==================
  prefix            distinct followers
  ================= ==================
  *empty*           5
  [0000]            11
  [1000]            52 
  [1100]            38
  [2100]            129
  [3210]            56
  [:math:`c_1,c_2`] 43,600
  ================= ==================


**Case-distinct stats:** There is only one empty prefix, five canonical prefixes
of size 1 (0000, 1000, 1100, 2100, 3210), and 286 distinct 2-code prefixes
generated from the first 5, each paired with its case-distinct set elements.
Of the 286 2-element prefixes, 31 provide full resolution; meaning that all
codes are case-distinct after them, and consequently after any prefix that
starts with them.

Usefulness
==========

Case equivalence simplifies exhaustive approaches by reducing the number of 
codes to be examined.

