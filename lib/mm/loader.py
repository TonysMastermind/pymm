"""Utilities to load and store pickled data."""

import collections
import cPickle as pickle
import logging
# import pickle
import os
import os.path
import traceback

_StorageSpecBase = collections.namedtuple('_LoaderSpecBase', ['version', 'path'])

class StorageSpec(_StorageSpecBase):
    """A specifiction of storage location, consisting of a path prefix, and 
    a version."""

    def __new__(cls, version, path_prefix):
        """Constructs an instsance.

        :param cls: Class being instantiated.
        :param version: version of the schema associated with the data.
        :param path_prefix: path_prefix of the storage path.
        :return: an instance of L{StorageSpec}, with the path set to 
          *path_prefix*``.v``*version*``.pickle``
        """
        path = '{}.v{}.pickle'.format(path_prefix, version)
        """Path to the file used for storing/loading data."""

        return _StorageSpecBase.__new__(cls, version, path)

    def __repr__(self):
        """:return: printable reprsentation of the object."""
        return super(StorageSpec, self).__repr__().replace(
            _StorageSpecBase.__name__,
            StorageSpec.__name__,
            1)

class Loader(object):
    """Data loader.  Associates the method of construction the data with
    a storage path.  Unpickling the file is expected to yield the result
    faster than calling the data constructor.  In case the file loading
    fails, the data is constructed by computation."""

    def __init__(self, make, pathspec):
        """:param make: creates the data computationally with the expression ``make()``.
        :param pathspec: path specification to pre-stored result.
        """
        self._make = tuple([make])

        self.version = pathspec.version
        """Representation version."""

        self.path = pathspec.path
        """Storage path."""


    def load(self):
        """Attempts to unpickle the data at the specified path.

        The file, if it exists, is expected to contain the schema version
        followed by th data.

        If file exists and the stored version matches the version specified
        to the loader, the loader unpickles the data and returns it.

        Exceptions and version mistmatches will result in the file being
        deleted, and a null return value.

        :return: unpickled stored data upon success, *None* otherwise.
        """
        if os.path.exists(self.path):
            try:
                with open(self.path, 'rb') as inp:
                    try:
                        version = pickle.load(inp)
                        if version == self.version:
                            return pickle.load(inp)
                    except (pickle.UnpicklingError, AttributeError, 
                            EOFError, ImportError, IndexError):
                        pass
                    except: # unfortunately, corrupt files raise all sorts of error.
                        logging.error("Error loading data: " + traceback.format_exc())
                        
            except IOError:
                pass
            os.unlink(self.path)
        return None


    def make(self):
        """Calculate an instance of the associated data.

        :return: The data associated with the loader."""
        return self._make[0]()

    def store(self, value):
        """Store data at the associated path.

        :param value: the data to be stored.
        :return: *value*

        If the loader file exists, it will be renamed with a
        numeric suffix, *path*.*number*, where *number* is
        chosen to ensure that the file is new.  Then, the new
        data is written to *path*.

        The directory hierarchy needed to store the file will
        be created, if necessary.
        """
        if os.path.exists(self.path):
            i = 1
            p = '{}.{}'.format(self.path, i)
            while os.path.exists(p):
                i += 1
                p = '{}.{}'.format(self.path, i)
            os.rename(self.path, p)
        else:
            d = os.path.dirname(self.path)
            if not os.path.exists(d):
                os.makedirs(d)

        with open(self.path, 'wb+') as out:
            import stat
            pickle.dump(self.version, out)
            pickle.dump(value, out)
        os.chmod(self.path, stat.S_IRUSR|stat.S_IRGRP|stat.S_IROTH)
        return value

    def get(self):
        """Returns the data associated with the loader.

        :return: the data associated with the loader.

        If the loader's file does not existed, the data will be
        calculated and stored before returning.
        """
        return self.load() or self.store(self.make())
