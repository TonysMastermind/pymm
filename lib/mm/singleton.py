# -*- python -*-
"""Singleton metaclass."""

class Singleton(type):
    """A singleton metaclass.

    Usage:

    .. code-block:: python

      class X(object):
          __metaclass__ = singleton
      
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
