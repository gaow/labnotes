#!/usr/bin/env python
# -*- coding: utf-8 -*-
import sys, shutil, os, re, argparse
import codecs
from .utils import env, regulate_output, pdflatex, indexhtml
from .encoder import LaTeX, Beamer, Html, Dokuwiki
from .parser import ParserCore

def doc(args, unknown_args):
    runner = ParserCore(args.filename, 'tex', 'long' if args.long_ref else 'short', args.lite)
    worker = LaTeX(args.title, args.author, args.date, args.toc, args.footnote, args.font, args.font_size,
                   table_font_size = 'footnotesize', no_num = args.no_section_number,
                   no_page = args.no_page_number, no_ref = False, twocols = args.twocols,
                   landscape = args.landscape)
    pdflatex(regulate_output(args.filename, args.output), runner(worker), vanilla=args.vanilla)
    return

def slides(args, unknown_args):
    runner = ParserCore(args.filename, 'tex', 'long' if args.long_ref else 'short', args.lite)
    worker = Beamer(args.title, args.author, args.date, args.institute,
                      args.toc, args.stoc, False, table_font_size = 'tiny',
                      mode = args.mode, theme = args.theme, thank = args.thank)
    pdflatex(regulate_output(args.filename, args.output), runner(worker), vanilla = args.vanilla,
             beamer_institute = args.color)

def html(args, unknown_args):
    runner = ParserCore(args.filename, 'html', 'long' if args.long_ref else 'short', args.lite,
                        figure_path = args.figure_path)
    worker = Html(args.title, args.author, args.date, args.toc, args.columns, separate_css = args.separate,
                  text_only = args.plain)
    fname = regulate_output(args.filename, args.output, suffix='.html')
    #
    body, css = runner(worker)
    if body:
        with codecs.open(fname + '.html', 'w', encoding='UTF-8', errors='ignore') as f:
            f.writelines(body)
    if css:
        with open('style.css', 'w') as f:
            f.writelines(css)
    env.logger.info('Done! ``{}.html`` should display in PTSans font if available.'.format(fname))
    env.logger.info('http://www.google.com/webfonts/specimen/PT+Sans')
    return

def dokuwiki(args, unknown_args):
    toc = 0
    if args.toc:
        toc = 2
    if args.compact_toc:
        toc = 1
    runner = ParserCore(args.filename, 'dokuwiki', 'long' if args.long_ref else 'short', args.lite,
                        figure_path = args.figure_path)
    worker = Dokuwiki(args.title, args.author, args.date, toc, args.showall, args.permission,
                      args.disqus)
    fname = regulate_output(args.filename, args.output, suffix='.txt')
    if args.filename == fname + '.txt':
        raise ValueError('Cannot write output to ``{0}`` due to name conflict with input!')
    with codecs.open(fname + '.txt', 'w', encoding='UTF-8', errors='ignore') as f:
        f.writelines(runner(worker))
    return


class Main:
    def __init__(self, version):
        self.master_parser = argparse.ArgumentParser(
        description = '''Dynamically compile formatted notes into various publishable formats''',
        prog = 'labnotes',
        fromfile_prefix_chars = '@',
        epilog = '''Copyright 2012 Gao Wang <gaow@uchicago.edu> GNU General Public License''')
        self.master_parser.add_argument('--version', action='version', version='%(prog)s {0}'.format(version))
        subparsers = self.master_parser.add_subparsers(dest = 'command-name')
        subparsers.required = True
        # latex
        parser = subparsers.add_parser('doc', formatter_class=argparse.ArgumentDefaultsHelpFormatter,
                                       help='Generate text document from notes file(s)')
        self.getCommonArguments(parser)
        self.getDocArguments(parser)
        parser.set_defaults(func=doc)
        # beamer
        parser = subparsers.add_parser('slides', formatter_class=argparse.ArgumentDefaultsHelpFormatter,
                                       help='Generate slides from notes file(s)')
        self.getCommonArguments(parser)
        self.getSlidesArguments(parser)
        parser.set_defaults(func=slides)
        # html
        parser = subparsers.add_parser('html', formatter_class=argparse.ArgumentDefaultsHelpFormatter,
                                       help='Generate HTML page from notes file(s)')
        self.getCommonArguments(parser)
        self.getHtmlArguments(parser)
        parser.set_defaults(func=html)
        # dokuwiki
        parser = subparsers.add_parser('dokuwiki', formatter_class=argparse.ArgumentDefaultsHelpFormatter,
                                       help='Generate dokuwiki text from notes file(s)')
        self.getCommonArguments(parser)
        self.getDokuwikiArguments(parser)
        parser.set_defaults(func=dokuwiki)
        # # markdown
        # parser = subparsers.add_parser('markdown', formatter_class=argparse.ArgumentDefaultsHelpFormatter,
        #                                help='Generate markdown text from notes file(s)')
        # self.getCommonArguments(parser)
        # self.getMarkDownArguments(parser)
        # parser.set_defaults(func=markdown)
        # # admin
        # parser = subparsers.add_parser('admin', formatter_class=argparse.ArgumentDefaultsHelpFormatter,
        #                                help='A collection of utility features')
        # self.getAdminArguments(parser)
        # parser.set_defaults(func=admin)

    def __call__(self):
        args, unknown_args = self.master_parser.parse_known_args()
        # calling the associated functions
        try:
            args.func(args, unknown_args)
        except Exception as e:
            if '--debug' in unknown_args:
                raise
            else:
                env.logger.error(e)
                sys.exit(1)

    def getCommonArguments(self, parser):
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
                        help='''generate table of contents''')
        parser.add_argument('-a', '--author',
                        action='store',
                        help='''author's name''')
        parser.add_argument('-t', '--title',
                        action='store',
                        help='''title of document''')
        parser.add_argument('-d', '--date',
                        action='store',
                        default = env.nice_time,
                        help='''date, leave empty for current date''')
        parser.add_argument('-l', '--lite',
                        action='store_true',
                        help='''mask commented-out text from output''')
        parser.add_argument('-r', '--long_ref',
                        action='store_true',
                        help='''additionally include DOI and HTTP links in reference paper''')
#        parser.add_argument('--no_reference',
#                        action='store_true',
#                        help='''do not include reference in the document''')

    def getDocArguments(self, parser):
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
                        help='''generate footnote instead of reference''')
        parser.add_argument('--font',
                        default = 'bch',
                        choices = ['bch', 'default', 'serif', 'tt', 'roman'],
                        help='''font type, default to "bch"''')
        parser.add_argument('--font_size',
                        type=int,
                        default = 10,
                        help='''font size, default to 10''')
        parser.add_argument('-f', '--vanilla',
                        action='store_true',
                        help='''force build document from scratch without using cached data''')

    def getSlidesArguments(self, parser):
        parser.add_argument('-i', '--institute',
                        action='store',
                        help='''institute of author''')
        parser.add_argument('--theme',
                        choices = ['heavy', 'compact', 'plain'],
                        default = 'compact',
                        help='''slides style theme''')
        parser.add_argument('--color',
                        choices = ['rice', 'uchicago'],
                        default = 'rice',
                        help='''color theme for non-plain slides''')
        parser.add_argument('--stoc',
                        action='store_true',
                        help='''generate table of contents for each section''')
        parser.add_argument('--thank',
                        action='store_true',
                        help='''generate last 'thank you' page''')
        parser.add_argument('--mode',
                        choices = ['presentation', 'notes', 'handout'],
                        default = 'presentation',
                        help='''output document mode (default set to 'presentation')''')
        parser.add_argument('-f', '--vanilla',
                        action='store_true',
                        help='''force build document from scratch without using cached data''')

    def getHtmlArguments(self, parser):
        parser.add_argument('--columns',
                        type = int,
                        choices = [1,2,3],
                        default = 1,
                        help='''number of columns in html page (1 ~ 3)''')
        parser.add_argument('-s', '--separate',
                        action='store_true',
                        help='''use separate files for css and js scripts''')
        parser.add_argument('--plain',
                        action='store_true',
                        help='''plain html code for text body (no style, no title / author, etc.)''')
        parser.add_argument('--figure_path',
                        metavar = 'PATH',
                        default = '',
                        help='''path to where figures are saved''')

    def getDokuwikiArguments(self, parser):
        parser.add_argument('--showall',
                        action='store_true',
                        help='''unfold source code / output fields in page by default''')
        parser.add_argument('--compact_toc',
                        action='store_true',
                        help='''generate compact table of contents (will override --toc)''')
        # group = parser.add_mutually_exclusive_group()
        parser.add_argument('--permission',
                        metavar='user',
                        type= str,
                        help='''authorized user name or group name of this page''')
        parser.add_argument('--disqus', action = 'store_true', help = 'Add "disqus" comment section to page')
        parser.add_argument('--figure_path',
                        metavar = 'PATH',
                        default = '',
                        help='''path to where figures are saved''')
