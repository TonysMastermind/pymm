"""Tree walker for anlayzing game trees, represented as dictionaries.

The tree walker can operates on tree dictionaries, or produce the trees from
JSON data files.
"""
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

    .. note::

      Note that a tree walk can occur while constructing a tree, in addition
      to traversing a pre-constructed tree; for example, in the *__init__* method
      of a the tree node.
      
    """

    def __init__(self, parent, path, tree):
        """:param parent: parent context; None for initial tree.
        :param path: a sequence of *(code, score)*  pairs that leads to the subtree.
        :param tree: subtree associated with the context.

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

        self.tree = tree
        """Subtree associated with the context."""

        self.root = tree['root']
        """Root of the subtree associated with the context."""

        self.prefix = (parent.prefix \
                           if parent \
                           else tuple(map(lambda p: p[0], path))) \
                           + (self.root,)
        """Code prefix sequence to the tree, including own root.  This is 
        one element longer than the path, and does not include scores."""


    def child(self, score, subtree):
        """Children of the class must implement this method.  The method 
        creates a context suitable for visiting the subtree specified by *score*
        with a root code of *root*.

        :param subtree: numeric code at the root of the subtree.
        :return: an instance of the object.
        """
        return self.__class__(self, 
                              (self.path + ((self.root, score),)), 
                              subtree)

class TreeWalker(object):
    """Encapsulation of a depth-first tree traversal algorithm."""

    def __init__(self, action, context=Context):
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
        ctx = self.context(None, tuple(), tree)
        self.walk(ctx)

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
                    self.walk(ctx.child(int(score), child))

