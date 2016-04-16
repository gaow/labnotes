#!/usr/bin/env python
# -*- coding: utf-8 -*-
import sys, shutil, os, re, argparse
import codecs
from .utils import env, regulate_output, pdflatex, indexhtml
from .encoder import LaTeX
from .parser import ParserCore

def doc(args, unknown_args):
    fname = regulate_output(args.filename, args.output)
    runner = ParserCore(args.filename, 'tex', long if args.long_ref else 'short', args.lite)
    worker = LaTeX(args.title, args.author, args.date, args.toc, args.footnote, args.font, args.font_size,
                   table_font_size = 'footnotesize', no_num = args.no_section_number,
                   no_page = args.no_page_number, no_ref = False, twocols = args.twocols,
                   landscape = args.landscape)
    pdflatex(fname, runner(worker), vanilla=args.vanilla)
    return

class Main:
    def __init__(self, version):
        self.master_parser = argparse.ArgumentParser(
        description = '''Compile formatted notes into various publishable formats''',
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
        # parser = subparsers.add_parser('slides', formatter_class=argparse.ArgumentDefaultsHelpFormatter,
        #                                help='Generate slides from notes file(s)')
        # self.getCommonArguments(parser)
        # self.getSlidesArguments(parser)
        # parser.set_defaults(func=slides)
        # # html
        # parser = subparsers.add_parser('html', formatter_class=argparse.ArgumentDefaultsHelpFormatter,
        #                                help='Generate HTML page from notes file(s)')
        # self.getCommonArguments(parser)
        # self.getHtmlArguments(parser)
        # parser.set_defaults(func=html)
        # # dokuwiki
        # parser = subparsers.add_parser('dokuwiki', formatter_class=argparse.ArgumentDefaultsHelpFormatter,
        #                                help='Generate dokuwiki text from notes file(s)')
        # self.getCommonArguments(parser)
        # self.getDokuwikiArguments(parser)
        # parser.set_defaults(func=dokuwiki)
        # # pmwiki
        # parser = subparsers.add_parser('pmwiki', formatter_class=argparse.ArgumentDefaultsHelpFormatter,
        #                                help='Generate pmwiki text from notes file(s)')
        # self.getCommonArguments(parser)
        # self.getPmwikiArguments(parser)
        # parser.set_defaults(func=pmwiki)
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
