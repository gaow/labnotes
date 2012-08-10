#!/usr/bin/env python
from distutils.core import setup
try:
    from distutils.command.build_py import build_py_2to3 as build_py
except ImportError:
    from distutils.command.build_py import build_py

import sys, os
if sys.version_info < (3, 2):
    sys.exit('The program requires Python 3.2 or higher. Please upgrade your version (%s) of Python and try again.' % (sys.version.split()[0]))
#
setup(name = 'gw_log',
    version = '1.0',
    py_modules = [
        'gwlog.__init__',
        'gwlog.minted',
        'gwlog.btheme',
        'gwlog.htheme',
        'gwlog.gwlog2tex',
        'gwlog.gwlog2beamer',
        'gwlog.gwlog2html',
        'gwlog.utils'
    ],
    scripts = ['gw_log'],
    cmdclass = {'build_py': build_py },
    package_dir = {'gwlog': 'gwlog'},
    packages = ['gwlog']
    )
