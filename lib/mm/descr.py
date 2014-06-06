"""For implementing self-describing objects.

A description has two components:

- symbolic prefix: a list of identifiers jointed by dots.
- qualifies: an optional list of name/value pairs.

"""

from types import ModuleType

def base_description(obj, **qualifiers):
    """The base implementation of descriptions.

    :param obj: the object to be described.
    :param qualifiers:  a dictionary with name/value pairs.
    :return: a string that describes the object.
    """
    q = ''
    if len(qualifiers):
        q = "({})".format(
            ", ".join(["{}={}".\
                           format(k,v) for (k,v) in qualifiers.iteritems()]))

    if isinstance(obj, type):
        return "{}.{}{}".format(obj.__module__, obj.__name__, q)

    if isinstance(obj, ModuleType):
        return "{}{}".format(obj.__name__, q)

    mod = '<unknown_module>'
    nm  = '<unknown_name>'

    if hasattr(obj, '__name__'):
        nm = obj.__name__
    elif hasattr(obj, '__class__'):
        nm = obj.__class__.__name__

    if hasattr(obj, '__module__'):
        mod = obj.__module__
    elif hasattr(obj, '__class__'):
        mod = obj.__class__.__module__

    return "{}.{}{}".format(mod, nm, q)

class WithDescription(object):
    """Base class for self-describing objects.

    The default implementation is to call :py:func:`.base_description` with the object
    and a qualifier dictionary.

    This behavior can be specialized at two points:

    - :py:meth:`.WithDescription.description_qualifiers`: provide qualifiers specific
      to the child class or specific instance, without changing the implementation.
    - :py:meth:`.WithDescription.description`: custom implementation.
    """

    def basic_description(self, **kwargs):
        """Base-implementation, delegates to L{base_description}.

        :param kwargs: keyword args, passed as-is to :py:func:`.base_description.base_description`.
        :return: a string containing the description.
        """
        return base_description(self, **kwargs)


    def description(self):
        """Default implementation.  Delegates to :py:meth:`.WithDescription.basic_description`,
        passing the value of *self.description_qualifiers()* along.

        :return: a string containing a description.
        """
        return self.basic_description(**self.description_qualifiers())

    def description_qualifiers(self):
        """Default implementation, returns an empty dictionary.
   
        :return: empty dictionary.
        """
        return { }
