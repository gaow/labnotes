#!/usr/bin/env python
import sys, os, subprocess

from sys import version_info
if not version_info >= (3, 4, 0):
    sys.exit("This program requires Python 3.5")

import yaml
from distutils.core import setup
from distutils.command.build_py import build_py
REV = subprocess.check_output('git rev-list --count HEAD', shell = True).decode().strip()
VERSION = '0.0.1'
FULL_VERSION = '0.0.1-rev{}'.format(REV)

# init
bookdown_out = yaml.load(open('src/assets/bookdown/_output.yml'))
bookdown_cfg = yaml.load(open('src/assets/bookdown/_bookdown.yml'))
bookdown_idx = yaml.load(open('src/assets/bookdown/_index.yml'))
bookdown_tex = open('src/assets/bookdown/preamble.tex').read()
bookdown_style = open('src/assets/bookdown/css/style.css').read()
bookdown_toc = open('src/assets/bookdown/css/toc.css').read()

with open('src/__init__.py', 'w') as f:
    f.write('#!/usr/bin/env python\n# -*- coding: utf-8 -*-\n')
    f.write('VERSION = "{}"\n'.format(VERSION))
    f.write('FULL_VERSION = "{}"\n'.format(FULL_VERSION))
    f.write('BOOKDOWN_CFG = {}\n'.format(str(bookdown_cfg)))
    f.write('BOOKDOWN_OUT = {}\n'.format(str(bookdown_out)))
    f.write('BOOKDOWN_IDX = {}\n'.format(str(bookdown_idx)))
    f.write('BOOKDOWN_TEX = r"""\n{}\n"""\n'.format(bookdown_tex))
    f.write('BOOKDOWN_STYLE = r"""\n{}\n"""\n'.format(bookdown_style))
    f.write('BOOKDOWN_TOC = r"""\n{}\n"""\n'.format(bookdown_toc))
#
setup(name = 'tigernotes',
    version = VERSION,
    description = "tigernotes",
    author = 'Gao Wang',
    author_email = 'gaow@uchicago.edu',
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
        'libtigernotes.markdown',
        'libtigernotes.markdown_toclify',
        'libtigernotes.bookdown'
    ],
    scripts = ['src/tigernotes', 'src/tigerjournal'],
    cmdclass = {'build_py': build_py },
    package_dir = {'libtigernotes': 'src'},
    packages = ['libtigernotes'],
    )
