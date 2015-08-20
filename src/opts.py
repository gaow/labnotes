#!/usr/bin/env python
# -*- coding: utf-8 -*-
import sys, shutil, os
from .argparse import ArgumentParser
import codecs
from .utils import getfname, pdflatex, indexhtml
from .doc import Tex
from .slides import Beamer
from .html import Html
from .dokuwiki import Dokuwiki
from .pmwiki import Pmwiki
from . import VERSION


def doc(args):
    tex = Tex(args.title, args.author, args.date, args.toc, args.footnote, args.font, args.font_size,
                   args.filename, long_ref = args.long_ref, no_num = args.no_section_number, 
                   no_page = args.no_page_number, no_ref = False, twocols = args.twocols,
                   landscape = args.landscape)
    lite = 1 if args.lite else 0
    fname = getfname(args.filename, args.output)
    pdflatex(fname, tex.get(lite), vanilla=args.vanilla)
    return

def slides(args):
    tex = Beamer(args.title, args.author, args.date, args.institute,
                      args.toc, args.stoc, args.mode, args.theme,
                      args.thank, args.filename, long_ref = args.long_ref)
    lite = 1 if args.lite else 0
    fname = getfname(args.filename, args.output)
    pdflatex(fname, tex.get(lite), vanilla = args.vanilla,
             beamer_institute = args.color)
    return

def html(args):
    htm = Html(args.title, args.author, args.toc,
               args.filename, args.columns,
               long_ref = args.long_ref, fig_path = args.figure_path)
    lite = 1 if args.lite else 0
    fname = getfname(args.filename, args.output, suffix='.html')
    body, css, js = htm.get(lite, args.separate, args.plain)
    if body:
        with codecs.open(fname + '.html', 'w', encoding='UTF-8', errors='ignore') as f: f.writelines(body)
    if css:
        with open('style.css', 'w') as f: f.writelines(css)
    if js:
        with open('script.js', 'w') as f: f.writelines(js)
    # woff = os.path.join(os.path.dirname(sys.modules['libtigernotes'].__file__), 'PTSans.woff')
    # if os.path.exists(woff):
    #     shutil.copy2(woff, '.')
    # else:
    #     # cannot find font in current directory either
    #     if not os.path.isfile('PTSans.woff'):
    #         sys.stderr.write("WARNING: font file 'PTSans.woff' might be missing (http://www.google.com/webfonts/specimen/PT+Sans)\n")
    return

def dokuwiki(args):
    htm = Dokuwiki(args.title, args.author, args.filename, args.toc,
                   args.showall, args.prefix, long_ref = args.long_ref)
    lite = 1 if args.lite else 0
    fname = getfname(args.filename, args.output, suffix='.txt')
    if args.filename == fname + '.txt':
        raise ValueError('Cannot write output as "{0}": name conflict with source file. Please rename either of them')
    with codecs.open(fname + '.txt', 'w', encoding='UTF-8', errors='ignore') as f:
        if args.permission:
            f.write('<ifauth !{0}>\nThis post is only visible to authorized members. Please login if you are one of them.\n</ifauth>\n<ifauth {0}>\n'.format(args.permission.strip('\'"')))
        f.writelines(htm.get(lite))
        if args.permission:
            f.write('\n</ifauth>')
    return

def pmwiki(args):
    htm = Pmwiki(args.title, args.author, args.filename, args.toc, args.prefix, long_ref = args.long_ref)
    lite = 1 if args.lite else 0
    fname = getfname(args.filename, args.output, suffix='.txt')
    if args.filename == fname + '.txt':
        raise ValueError('Cannot write output as "{0}": name conflict with source file. Please rename either of them')
    with codecs.open(fname + '.txt', 'w', encoding='UTF-8', errors='ignore') as f:
        f.writelines(htm.get(lite))
    return

def admin(args):
    if args.action == 'index_html':
        fname = 'index.html'
        if args.output:
            fname = getfname([], args.output, suffix='.html') + '.html'
        otext = indexhtml([x for x in args.filename if x != fname])
        with codecs.open(fname, 'w', encoding='UTF-8', errors='ignore') as f:
            f.writelines(otext)
    return

class LogOpts:
    def __init__(self):
        self.master_parser = ArgumentParser(
        description = '''Compile formatted notes into various publishable formats''',
        prog = 'tigernotes',
        fromfile_prefix_chars = '@',
        epilog = '''Copyright 2012 Gao Wang <ewanggao@gmail.com> GNU General Public License''')
        self.master_parser.add_argument('--version', action='version', version='%(prog)s {0}'.format(VERSION))
        subparsers = self.master_parser.add_subparsers()
        # latex
        parser = subparsers.add_parser('doc', help='Generate text document from notes file(s)')
        self.getTexArguments(parser)
        self.getDocArguments(parser)
        parser.set_defaults(func=doc)
        # beamer
        parser = subparsers.add_parser('slides', help='Generate slides from notes file(s)')
        self.getTexArguments(parser)
        self.getSlidesArguments(parser)
        parser.set_defaults(func=slides)
        # html
        parser = subparsers.add_parser('html', help='Generate HTML page from notes file(s)')
        self.getTexArguments(parser)
        self.getHtmlArguments(parser)
        parser.set_defaults(func=html)
        # dokuwiki
        parser = subparsers.add_parser('dokuwiki', help='Generate dokuwiki text from notes file(s)')
        self.getTexArguments(parser)
        self.getDokuwikiArguments(parser)
        parser.set_defaults(func=dokuwiki)
        # pmwiki
        parser = subparsers.add_parser('pmwiki', help='Generate pmwiki text from notes file(s)')
        self.getTexArguments(parser)
        self.getPmwikiArguments(parser)
        parser.set_defaults(func=pmwiki)
        # admin
        parser = subparsers.add_parser('admin', help='A collection of utility features')
        self.getAdminArguments(parser)
        parser.set_defaults(func=admin)

    def run(self):
        args = self.master_parser.parse_args()
        # calling the associated functions
#        args.func(args)
        try:
            args.func(args)
        except Exception as e:
            sys.exit('Unexpected error occurred while processing {0}: {1}'.format('-'.join(args.filename), e))

    def getTexArguments(self, parser):
        parser.add_argument('filename',
                        metavar = 'FN',
                        nargs = '+',
                        help='''name of the input notes file(s)''')
        parser.add_argument('-o', '--output',
                        metavar='name',
                        type=str,
                        help='''name of output file''')
        parser.add_argument('--toc',
                        action='store_true',
                        default = '',
                        help='''generate table of contents''')
        parser.add_argument('-a', '--author',
                        action='store',
                        default = '',
                        help='''author's name''')
        parser.add_argument('-t', '--title',
                        action='store',
                        default = '',
                        help='''title of document''')
        parser.add_argument('--lite',
                        action='store_true',
                        default = '',
                        help='''mask commented-out text from output''')
        parser.add_argument('--long_ref',
                        action='store_true',
                        help='''additionally include DOI and HTTP links in reference paper''')
#        parser.add_argument('--no_reference',
#                        action='store_true',
#                        help='''do not include reference in the document''')


    def getDocArguments(self, parser):
        parser.add_argument('-d', '--date',
                        action='store',
                        default = '',
                        help='''date, leave empty for current date''')
        parser.add_argument('--no_section_number',
                        action='store_true',
                        help='''generate un-numbered sections''')
        parser.add_argument('--no_page_number',
                        action='store_true',
                        help='''generate un-numbered pages''')
        parser.add_argument('--twocols',
                        action='store_true',
                        help='''two columns per page''')
        parser.add_argument('--landscape',
                        action='store_true',
                        help='''landscape orientation''')
        parser.add_argument('--footnote',
                        action='store_true',
                        default = '',
                        help='''generate footnote instead of reference''')
        parser.add_argument('--font',
                        default = 'bch',
                        choices = ['bch', 'default', 'serif', 'tt', 'roman'],
                        help='''font type, default to "bch"''')
        parser.add_argument('--font_size',
                        type=int,
                        default = 10,
                        help='''font size, default to 10''')
        parser.add_argument('-v', '--vanilla',
                        action='store_true',
                        default = '',
                        help='''build document from scratch without using cached data''')

    def getSlidesArguments(self, parser):
        parser.add_argument('-i', '--institute',
                        action='store',
                        default = '',
                        help='''institute of author''')
        parser.add_argument('-d', '--date',
                        action='store',
                        default = '',
                        help='''date, leave empty for current date''')
        parser.add_argument('--theme',
                        type = str,
                        choices = ['heavy', 'compact', 'plain'],
                        default = 'compact',
                        help='''slides style theme''')
        parser.add_argument('--color',
                        type = str,
                        choices = ['rice', 'uchicago'],
                        default = 'rice',
                        help='''color theme for non-plain slides''')
        parser.add_argument('--stoc',
                        action='store_true',
                        default = '',
                        help='''generate table of contents for each section''')
        parser.add_argument('--thank',
                        action='store_true',
                        help='''generate last 'thank you' page''')
        parser.add_argument('--mode',
                        type = str,
                        choices = ['presentation', 'notes', 'handout'],
                        default = 'presentation',
                        help='''output document mode (default set to 'presentation')''')
        parser.add_argument('-v', '--vanilla',
                        action='store_true',
                        default = '',
                        help='''build document from scratch without using cached data''')

    def getHtmlArguments(self, parser):
        parser.add_argument('--columns',
                        type = int,
                        choices = [1,2,3],
                        default = 1,
                        help='''number of columns in html page (1 ~ 3)''')
        parser.add_argument('-s', '--separate',
                        action='store_true',
                        help='''use separate files for css and js scripts''')
        parser.add_argument('-p', '--plain',
                        action='store_true',
                        help='''plain html code for text body (no style, no title / author, etc.)''')
        parser.add_argument('--figure_path',
                        metavar = 'PATH',
                        default = '',
                        help='''path to where figures are saved''')


    def getPmwikiArguments(self, parser):
        parser.add_argument('--prefix',
                        metavar='PATH',
                        type=str,
                        help='''remote relative path for image, usually is the namespace a dokuwiki page belongs to''')

    def getDokuwikiArguments(self, parser):
        self.getPmwikiArguments(parser)
        parser.add_argument('--showall',
                        action='store_true',
                        default = '',
                        help='''unfold source code / output fields in page by default''')
        parser.add_argument('--permission',
                        metavar='user',
                        type=str,
                        help='''authorized user name or group name of this page''')


    def getAdminArguments(self, parser):
        parser.add_argument('filename',
                        metavar = 'FN',
                        nargs = '+',
                        help='''name of the input file(s)''')
        parser.add_argument('-a', '--action',
                        type=str,
                        choices=['index_html'],
                        help='''action to be applied to input files''')
        parser.add_argument('-o', '--output',
                        metavar='name',
                        type=str,
                        help='''name of output file''')
