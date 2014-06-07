"""Thin wrapper around :py:func:`resource.getrusage`."""

from . import descr

import resource as res
import timeit

class Timer(descr.WithDescription):
    """A simple timer class, with start/stop methods.

    The timer is reusable, but it is not cumulative.
    """

    class rusage(object):
        """A wrapper around the result of :py:func:`resource.getrusage` that
        adds the attribute :py:attr:`.Timer.rusage.ctime`.

        The result from :py:func:`resource.getrusage` is a native object type
        that cannot be inherited or extended with attributes.

        This class implements an override of ':py:meth:`object.__getattr__` that
        delegates to the embedded *resource.struct_rusage* instance.
        """

        def __init__(self, ru):
            """:param ru: the results of a :py:func:`resource.getrusage` call."""

            self._ru = ru
            self.ctime = timeit.default_timer()
            """Clock time."""


        def __getattr__(self, a):
            """Attribute lookup; forwards to the embedded native struct for unknown
            attribute names.

            Note that this method gets called only for attributes that cannot be found
            on the object.

            :param a: Attribute name.
            :return: Equivalent to *self._ru.<name>*.
            """
            return self._ru.__getattribute__(a)


    class CPUTime(object):
        """CPU time consumed within a start/stop interval.

        The timer captures user and system time.
        """

        def __init__(self, start, end):
            """:param start: rusage results at start of interval.
            :param end: rusage results at end of interval."""

            self.utime = end.ru_utime - start.ru_utime
            """User time between *start* and *end*."""

            self.stime = end.ru_stime - start.ru_stime
            """System time between *start* and *end*."""

            self.ctime = end.ctime - start.ctime
            """Clock time between *start* and *end*."""


        def as_dict(self):
            """Dictionary represenation of the data.

            :return: A dictionary representation."""
            return { 'utime': self.utime, 'stime': self.stime }


        def __str__(self):
            """Printable representation; primarily formatting the floating point
            data, and adding the unit 's' for seconds.

            :return: printable/displayable representation."""
            return "ctime:{:.03f}s, utime:{:.03f}s, stime:{:03f}s".format(
                self.ctime, self.utime, self.stime)



    def __init__(self):
        """Initializes the object, and starts the timer."""
        self._start = self.getrusage(res.RUSAGE_SELF)
        self.delta = None
        """Difference in rusage between the last start/stop rusage instants;
        an instance of :py:class:`.Timer.CPUTime`.
        """


    def getrusage(self, *args):
        """Wrapper around :py:func:`resource.getrusage` that adds wall time.

        :return: 
        """
        return Timer.rusage(res.getrusage(*args))


    def start(self):
        """Start time; equivalent to :py:meth:`.Timer.__init__`."""
        self.__init__()


    def stop(self):
        """Stops the time, and populates the field :py:attr:`.Timer.delta`.

        :return: an instance of :py:class:`.Timer.CPUTime`.
        """
        end = self.getrusage(res.RUSAGE_SELF)
        self.delta = Timer.CPUTime(self._start, end)
        return self.delta


def time(fn):
    """Runs the function *fn*, within a timer start/stop interval.

    :param fn: a function to be executed under a timer.
    :return: a tuple *(delta, r)*, where *delta* is the 
      timer's *delta*, an instance of :py:class:`.Timer.CPUTime`, measured
      around the function execution, and *r* is the value returned from the
      function.
    """

    t = Timer()
    t.start()
    r = fn()
    delta = t.stop()
    return (delta, r)
