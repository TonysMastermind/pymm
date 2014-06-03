=========================
 Case-Equivalent analysis
=========================


Contents
========

.. toctree::
   :maxdepth: 2

   tree-analysis
   tree-analysis-2


Terms
=====


:math:`T`
  All the the possible transformations on mastermind codes; 
  a set of 17,280 distinct elements.

:math:`C`
  All the possible mastermind codes.

:math:`preserving(x)`
  The subset of :math:`T` that does not vary the code :math:`x`; or

  :math:`\left\{ t \in T: t(x) = x \right\}`

:math:`preserving(\vec{x})`
  The subset of transformations that do not vary any of the codes 
  :math:`x_1`, :math:`x_2`, ...;  

  :math:`preserving(x_1) \cap preserving(x_2) \cap ...`.

Case equivalent: :math:`eqv(x, y)_{\vec{g}}`
  We say that :math:`x` and :math:`y` are *case equivalent after a sequence
  of guesses (codes)* :math:`\vec{g}` when there is a transformation in 
  :math:`preserving(\vec{g})` mapping :math:`x` to :math:`y`; or

  :math:`eqv(x,y)_{\vec{g}} \iff \exists t \in preserving(\vec{g}): t(x) = y`, or

  :math:`eqv(x,y)_{\vec{g}} \iff \exists t \in T: t(\vec{g}) = \vec{g} \land t(x) = y`

:math:`distinct(\vec{g})`
  The smallest set of case equivalent codes following :math:`\vec{g}`:

  :math:`\left\{\forall x \in (C - \vec{g}): min(t(x) \forall t \in preserving(\vec{g})) \right\}`, or

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
  ================= ==================


Interesting numbers
~~~~~~~~~~~~~~~~~~~ 

The code *[2100]* remains invariant under 24 transformations (out of 17,280).  Under these 24
transformations, the canonical set of distinct followers has 129 members, of which

- 19 achieve full resolution: only the identity transformation preserves both codes in the 
  prefix.
- 2 achieve no extra resolution: the same transformations that preserve the initial code
  also preserve them.
     
The code *[1100]* remains invariant under 192 transformations (out of 17,280).  Under these
192 transformations, the canonical set of distinct followers has 38 members, of which

- none acheive full resolution.
- 1 achieves no extra resolution.


.. table:: Prefixes starting with *[2100]*, summary stats.
  :widths: 1 1
  :column-wrapping: true true true true true true true true
  :column-alignment: right right right right right right right right 
  :column-dividers: single single single single single single single single single

  ================= ======== =================== ================ ================= ============== ============== ===============
  Prefix length     count    min # preserving    max # preserving mean # preserving min # distinct max # distinct mean # distinct
  ================= ======== =================== ================ ================= ============== ============== ===============
  1                 1        24                  24               24.000            129            129            129.000
  2                 129      1                   24               4.395             128            1,294          636.984
  3                 57,329   1                   12               1.609             196            1,293          1,063.542
  ================= ======== =================== ================ ================= ============== ============== ===============



Usefulness
==========

Case equivalence simplifies exhaustive approaches by reducing the number of 
codes to be examined for the first two to three guesses.
