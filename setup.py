#!/usr/bin/env python
import sys, os, subprocess
from distutils.core import setup
try:
    from distutils.command.build_py import build_py_2to3 as build_py
except ImportError:
    from distutils.command.build_py import build_py
# Update version
from src import VERSION
main_version = VERSION.split('-')[0]
revision = subprocess.check_output('cat src/.revision', shell = True).strip()
version = '{}-rev{}'.format(main_version, revision)
full_version = '{}, revision {}'.format(main_version, revision)
content = []
with open('{}/__init__.py'.format("src"), 'r') as init_file:
    for x in init_file.readlines():
        if x.startswith('VERSION'):
            content.append("VERSION = '{}'".format(version))
        elif x.startswith("FULL_VERSION"):
            content.append("FULL_VERSION = '{}'".format(full_version))
        else:
            content.append(x.rstrip())
with open('{}/__init__.py'.format("src"), 'w') as init_file:
    init_file.write('\n'.join(content))
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
