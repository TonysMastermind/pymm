import json
import sys

_EMPTY_PREFIX = tuple()

class Unimplemented(Exception):
    pass


def _visit(path, tree, action):
    if action(path, tree):
        root = tree['root']
        children = tree.get('children')
        if children:
            for (score, child) in children.iteritems():
                _visit(path + (root, score,), child, action)


def path2prefix(path):
    return tuple(x for (i, x) in zip(range(len(path)), path) if i % 2 == 0)

def visit(tree, action):
    """:param tree: tree, expressed as a dictionary.
    :type tree: dict.
    :param action: callable action function, invoked as ``action(tree)``, should return
      *True* for deeper recursion, *False* to stop deeper recursion.
    :type action: callable.
    """
    _visit(tuple(), tree, action)


def loadfile(fname=None):
    fp = sys.stdin
    if fname:
        fp = open(fname, 'r')

    d = json.load(fp)
    fp.close()

    if 'tree' in d:
        d = d['tree']

    return d


def visitfile(action, fname=None):
    d = loadfile(fname)
    visit(d, action)


class Context(object):
    """Traversal context for a recursive tree walk. Minimal parent."""

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
    def __init__(self, action, context=Context):
        self.action = action
        self.context = context


    def walkfile(self, fname=None):
        tree = loadfile(fname)
        self.walktree(tree)


    def walktree(self, tree):
        ctx = self.context(None, tuple(), tree)
        self.walk(ctx)

    def walk(self, ctx):
        if self.action(ctx):
            root = ctx.root
            children = ctx.tree.get('children')
            if children:
                for (score, child) in children.iteritems():
                    self.walk(ctx.child(int(score), child))

