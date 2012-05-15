#!/usr/bin/env python
from distutils.core import setup
try:
   from distutils.command.build_py import build_py_2to3 as build_py
except ImportError:
   from distutils.command.build_py import build_py
import sys, os
try:
    import argparse
except ImportError:
    sys.exit('The program requires Python 2.7.2 or higher, or Python 3.2 or higher. Please upgrade your version (%s) of Python and try again.' % (sys.version.split()[0]))
#
setup(name = 'gw_log',
    version = '1.0',
    py_modules = [
        '__init__',
        'minted',
        'gwlog2tex'
    ],
    scripts = ['gw_log'],
    cmdclass = {'build_py': build_py }
    )
