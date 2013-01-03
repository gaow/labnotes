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
setup(name = 'tigernotes',
    version = '1.0',
    py_modules = [
        'libtigernotes.__init__',
        'libtigernotes.minted',
        'libtigernotes.ltheme',
        'libtigernotes.htheme',
        'libtigernotes.utils',
        'libtigernotes.logtranslator',
        'libtigernotes.logopts',
        'libtigernotes.argparse'
    ],
    scripts = ['tigernotes'],
    cmdclass = {'build_py': build_py },
    package_dir = {'libtigernotes': 'libtigernotes'},
    packages = ['libtigernotes'],
    package_data = {'libtigernotes': ['PTSans.woff']}
    )
