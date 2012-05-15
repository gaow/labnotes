#!/usr/bin/env python

from distutils.core import setup
try:
   from distutils.command.build_py import build_py_2to3 as build_py
except ImportError:
   from distutils.command.build_py import build_py

import sys, os
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
