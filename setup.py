#!/usr/bin/env python
from distutils.core import setup
try:
    from distutils.command.build_py import build_py_2to3 as build_py
except ImportError:
    from distutils.command.build_py import build_py

import sys, os
#if sys.version_info < (3, 1):
#    sys.exit('The program requires Python 3.1 or higher. Please upgrade your version (%s) of Python and try again.' % (sys.version.split()[0]))
#
setup(name = 'gw_log',
    version = '1.0',
    py_modules = [
        'gwlog.__init__',
        'gwlog.minted',
        'gwlog.ltheme',
        'gwlog.htheme',
        'gwlog.utils',
        'gwlog.logtranslator',
        'gwlog.logopts',
        'gwlog.argparse'
    ],
    scripts = ['gw_log'],
    cmdclass = {'build_py': build_py },
    package_dir = {'gwlog': 'gwlog'},
    packages = ['gwlog'],
    package_data = {'gwlog': ['PTSans.woff']}
    )
