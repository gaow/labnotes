#!/usr/bin/env python
from distutils.core import setup
try:
    from distutils.command.build_py import build_py_2to3 as build_py
except ImportError:
    from distutils.command.build_py import build_py
from src import VERSION
import sys, os
#if sys.version_info < (3, 1):
#    sys.exit('The program requires Python 3.1 or higher. Please upgrade your version (%s) of Python and try again.' % (sys.version.split()[0]))
#
setup(name = 'tigernotes',
    version = VERSION,
    description = "tigernotes",
    author = 'Gao Wang',
    author_email = 'ewanggao@gmail.com',
    url = 'http://tigerwang.org/software/tigernotes',
    py_modules = [
        'libtigernotes.__init__',
        'libtigernotes.minted',
        'libtigernotes.style',
        'libtigernotes.utils',
        'libtigernotes.doi',
        'libtigernotes.opts',
        'libtigernotes.base',
        'libtigernotes.doc',
        'libtigernotes.slides',
        'libtigernotes.html',
        'libtigernotes.dokuwiki',
        'libtigernotes.pmwiki',
        'libtigernotes.ordereddict',
        'libtigernotes.argparse'
    ],
    scripts = ['src/tigernotes', 'src/tigerjournal'],
    cmdclass = {'build_py': build_py },
    package_dir = {'libtigernotes': 'src'},
    packages = ['libtigernotes'],
    package_data = {'libtigernotes': ['PTSans.woff']}
    )
