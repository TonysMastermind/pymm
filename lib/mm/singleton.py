# -*- python -*-
"""Singleton metaclass."""

class Singleton(type):
    """A singleton metaclass.

    Usage:

    .. code-block:: python

      class X(object):
          __metaclass__ = Singleton
      
      x = X() # X() => singleton.__call__(X, (), {})
      y = X()
      assert(x is y)

    The class variable _instances is shared among all singletons."""

    _instances = {}
    def __call__(cls, *args, **kwargs):
        """
        :param cls: class delegating to this metaclass.
        :type cls: type.
        :param args: positional args passed upwards.
        :type args: list.
        :param kwargs: keywoard args passsed upwards.
        :type kwargs: dict.
        :return: singleton instance of the specified class.
        """
        if cls not in cls._instances:
            cls._instances[cls] = \
                super(Singleton, cls).__call__(*args, **kwargs)
        return cls._instances[cls]


class SingletonBehavior(object):

    @classmethod
    def exists(cls):
        return Singleton._instances.get(cls) is not None

    @classmethod
    def clear(cls):
        """For testing."""
        if cls.exists():
            del Singleton._instances[cls]

    def __setstate__(self, state):
        self.__dict__.update(state)

        cls = self.__class__
        r = Singleton._instances.get(cls)
        if r:
            r.__dict__.update(state)
        Singleton._instances[cls] = self
