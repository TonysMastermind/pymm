"""Tree walker for anlayzing game trees, represented as dictionaries.

The tree walker can operates on tree dictionaries, or produce the trees from
JSON data files.
"""

from . import CODETABLE
from . import score

import json
import sys

_EMPTY_PREFIX = tuple()

class Unimplemented(Exception):
    pass


def loadfile(fname=None):
    """Reads a JSON file from a named file or stadnard input.

    :param fname: name of the file, an empty or null file name indicates
      that input is from :py:data:`sys.stdin`.
    :return: dictionary reprsenting a strategy tree.
    """
    fp = sys.stdin
    if fname:
        fp = open(fname, 'r')

    d = json.load(fp)
    fp.close()

    if 'tree' in d:
        d = d['tree']

    return d


class Context(object):
    """Traversal context for a recursive tree walk.

    A *tree* represents a strategy for solving a specific 
    *mastermind problem*.  The problem is a set of codes.  The root
    node of the tree has a root code representing the initial guess
    against the tree's problem, and edges to subtrees labeled by the
    possible responses to that initial guess.

    The traversal context contains information about the path, from
    the root of the tree, to the subtree being analyzed, a reference
    to the parent context, and a reference to the subtree itself.

    The :py:attr:`.Context.prefix` attribute contains the code sequence
    prefix to the root, including the root.

    The :py:attr:`.Context.path` attribute contains the sequence of
    *(guess, score)* defining the path to the current subtree.
    """

    def __init__(self, parent, path, root):
        """:param parent: parent context; None for initial tree.
        :param path: a sequence of *(code, score)*  pairs that leads to the subtree.
        :param root: root code of subtree associated with the context.

        A child class's initializer would look like:

        .. code-block:: python

          class MyContext(mm.treewalk.Context):
              def __init__(self, *args, **kwargs):
                  super(MyContext, self).__init__(*args, **kwargs)
                  self.depth = self.parent.depth + 1
                  # etc...

              ## alternatively
              def child(self, *args, **kwargs):
                  c = super(MyContext, self).child(*args, **kwargs)
                  # make changes.
                  return c
        """

        self.parent = parent
        """Parent context; may be null."""

        self.path = path
        """Path to the tree; a sequence of (Code, Score) pairs leading to the tree."""

        self.root = root
        """Root of the subtree associated with the context."""

        self.prefix = (parent.prefix \
                           if parent \
                           else tuple(map(lambda p: p[0], path))) \
                           + (self.root,)
        """Code prefix sequence to the tree, including own root.  This is 
        one element longer than the path, and does not include scores."""


    def child(self, score, root, *args, **kwargs):
        """Children of the class must implement this method.  The method 
        creates a context suitable for visiting the subtree specified by *score*
        with a root code of *root*.

        :param root: numeric code at the root of the subtree.
        :param args: optional unnamed args passed from child implementation.
        :param kwargs: optional named args passed from child implementation.
        :return: an instance of the object.
        """
        return self.__class__(self, 
                              (self.path + ((self.root, score),)), 
                              root, *args, **kwargs)


class TreeWalkerContext(Context):
    """A specialization of :py:class:`.Context` for walking pre-built
    trees with a dictionary representation."""

    def __init__(self, parent, path, root, tree=None):
        """
        :param parent: see :py:class:`.Context`.
        :param path: see :py:class:`.Context`.
        :param root: see :py:class:`.Context`.
        :param tree: optional prebuilt tree to process.
        """
        super(TreeWalkerContext, self).__init__(parent, path, root)
        self.tree = tree


    def child(self, score, root):
        """Override of parent implementation to pass the subtree.
        """
        children = self.tree['children']
        subtree = children.get(score, children.get(str(score)))
        return super(TreeWalkerContext, self).child(score, root, tree=subtree)


class TreeWalker(object):
    """Encapsulation of a depth-first tree traversal algorithm."""

    def __init__(self, action, context=TreeWalkerContext):
        """
        :param action: a callable function with one argument, which will be an
          instance of :py:class:`.Context`.  If the function returns *True*, the
          tree walk algorithm will recurse into the children of the visited tree,
          otherwise, otherwise, the traversal returns.
        :param context: the class of traversal context, must be a subclass of
          :py:class:`.Context`, or have a duck-type compatible interface.
        """

        self.action = action
        """Action function, invoked with a context object."""

        self.context = context
        """Class to use for creating traversal context."""


    def walkfile(self, fname=None):
        """
        :param fname: name of the file to read the JSON encoding of the tree from.
          If null, the loader will use :py:data:`sys.stdin`.
        """
        tree = loadfile(fname)
        self.walktree(tree)


    def walktree(self, tree):
        """Starts a tree walk for the input tree.

        :param tree: the strategy to be traversed.
        """
        ctx = self.context(None, tuple(), tree['root'], tree=tree)
        self.walk(ctx)


    def _childctx(self, ctx, score, child):
        c = ctx.child(score, child['root'])
        return c


    def walk(self, ctx):
        """The recursive step of the tree walk.  Given a traversal
        context, the method will apply the action at the context.
        If the supplied :py:data:`.TreeWalker.action` function returns
        *True*, the method will recurse into the subtrees of the 
        current tree; otherwise, the traversal stops.

        :param ctx: A traversal context.
        """
        if self.action(ctx):
            root = ctx.root
            children = ctx.tree.get('children')
            if children:
                for (score, child) in children.iteritems():
                    self.walk(self._childctx(ctx, int(score), child))


def play(secret, tree):
    """Play the strategy tree against the secret code.

    :param secret: numeric code to use as the hidden code.
    :param tree: strategy tree, expressed as a dictionary.
    :return: a sequence of *(code, score)* pairs, terminating
      with perfect score and the secret code.
    """
    path = []
    cur = tree
    while cur:
        root = cur['root']
        s = score.score(root, secret)
        path.append((root, s))
        if s == CODETABLE.PERFECT_SCORE:
            break

        children = cur.get('children')
        if children:
            cur = children.get(s, children.get(str(s)))

    return tuple(path)

