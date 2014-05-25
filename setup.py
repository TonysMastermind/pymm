#!/usr/bin/python
# -*- python -*-
from setuptools import setup

import glob
import sys

if len(sys.argv) < 2:
    sys.argv.append('build')

setup(name='pymm',
      version='0.0',
      description='MasterMind in Python',
      author='Antoun Kanawati',
      author_email='antoun.kanawati@gmail.com',
      packages=['mm'],
      package_dir = {'': 'lib'},
      url='ssh://git/git/pymm',
      scripts=[], #glob.glob('bin/*.py'),
      data_files=[]
     )
