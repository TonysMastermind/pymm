pymm
====

A python library for building mastermind strategy trees.

Requirements
------------

Current versions as of June 2014.

- Python 2.7
- Sphinx, with extra themes and extensions: see doc/config.py for details.
- nose, with the coverage plugin.
- setuptools

Using pypy
----------

The scripts can run with pypy (tested with 2.2.1 and 2.3.1) by setting the
environment variable `PYTHON` to the command for pypy.

Pypy is 2x, or more, faster than CPython for most tasks in this library.


State of progress
=================

Exhaustive strategies are very slow, and still need work.  The area of focus
is on detecting failed attempts early.
