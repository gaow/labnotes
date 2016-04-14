#!/usr/bin/env python
# -*- coding: utf-8 -*-
import sys, shutil, os, re, argparse
import codecs
from .utils import getfname, pdflatex, indexhtml
from .doc import Tex
from .slides import Beamer
from .html import Html
from .dokuwiki import Dokuwiki
from .pmwiki import Pmwiki
from .markdown import MarkDown
from .markdown_toclify import markdown_toclify
from .bookdown import prepare_bookdown
from . import VERSION

def doc(args, unknown_args):
    tex = Tex(args.title, args.author, args.date, args.toc, args.footnote, args.font, args.font_size,
                   args.filename, long_ref = args.long_ref, no_num = args.no_section_number,
                   no_page = args.no_page_number, no_ref = False, twocols = args.twocols,
                   landscape = args.landscape)
    lite = 1 if args.lite else 0
    fname = getfname(args.filename, args.output)
    pdflatex(fname, tex.get(lite), vanilla=args.vanilla)
    return

def slides(args, unknown_args):
    tex = Beamer(args.title, args.author, args.date, args.institute,
                      args.toc, args.stoc, args.mode, args.theme,
                      args.thank, args.filename, long_ref = args.long_ref)
    lite = 1 if args.lite else 0
    fname = getfname(args.filename, args.output)
    pdflatex(fname, tex.get(lite), vanilla = args.vanilla,
             beamer_institute = args.color)
    return

def html(args, unknown_args):
    htm = Html(args.title, args.author, args.toc,
               args.filename, args.columns,
               long_ref = args.long_ref, fig_path = args.figure_path)
    lite = 1 if args.lite else 0
    fname = getfname(args.filename, args.output, suffix='.html')
    body, css = htm.get(lite, args.separate, args.plain)
    if body:
        with codecs.open(fname + '.html', 'w', encoding='UTF-8', errors='ignore') as f: f.writelines(body)
    if css:
        with open('style.css', 'w') as f: f.writelines(css)
    # woff = os.path.join(os.path.dirname(sys.modules['libtigernotes'].__file__), 'PTSans.woff')
    # if os.path.exists(woff):
    #     shutil.copy2(woff, '.')
    # else:
    #     # cannot find font in current directory either
    #     if not os.path.isfile('PTSans.woff'):
    #         sys.stderr.write("WARNING: font file 'PTSans.woff' might be missing (http://www.google.com/webfonts/specimen/PT+Sans)\n")
    return

def dokuwiki(args, unknown_args):
    toc = 0
    if args.toc:
        toc = 2
    if args.compact_toc:
        toc = 1
    htm = Dokuwiki(args.title, args.author, args.filename, toc,
                   args.showall, args.prefix, long_ref = args.long_ref, version_info = args.stamps)
    lite = 1 if args.lite else 0
    fname = getfname(args.filename, args.output, suffix='.txt')
    if args.filename == fname + '.txt':
        raise ValueError('Cannot write output as "{0}": name conflict with source file. Please rename either of them')
    with codecs.open(fname + '.txt', 'w', encoding='UTF-8', errors='ignore') as f:
        if args.permission:
            user = re.sub(r'^\\', '', re.sub(r'^"|^\'|"$|\'$', '', args.permission))
            f.write('<ifauth !{0}>\nThis post is only visible to authorized members. Please login if you are one of them.\n</ifauth>\n<ifauth {0}>\n'.format(user))
        f.writelines(htm.get(lite))
        if args.disqus:
            f.write('\n\\\\\n\\\\\n\\\\\n~~DISQUS~~')
        if args.permission:
            f.write('\n</ifauth>')
    return

def pmwiki(args, unknown_args):
    htm = Pmwiki(args.title, args.author, args.filename, args.toc, args.prefix, long_ref = args.long_ref)
    lite = 1 if args.lite else 0
    fname = getfname(args.filename, args.output, suffix='.txt')
    if args.filename == fname + '.txt':
        raise ValueError('Cannot write output as "{0}": name conflict with source file. Please rename either of them')
    with codecs.open(fname + '.txt', 'w', encoding='UTF-8', errors='ignore') as f:
        f.writelines(htm.get(lite))
    return

def markdown(args, unknown_args):
    args.suffix = '.' + args.suffix
    toc = None
    htm = MarkDown(args.title, args.author, args.filename, toc, args.prefix, long_ref = args.long_ref)
    lite = 1 if args.lite else 0
    out = os.path.split(args.output) if args.output else None
    fname = None
    if out and out[-1] == '-':
        # Github wiki style output, will use first line (title section) of the document as title
        for idx, item in enumerate(htm.text):
            if not item:
                continue
            else:
                fname = os.path.join(os.path.join(*out[:-1]),
                                     item.replace('#', '').strip().replace(':', '').replace(' ', '-'))
                htm.text = htm.text[(idx + 1):]
                break
    else:
        fname = getfname(args.filename, args.output, suffix = args.suffix)
    if fname is None:
        return
    fname += args.suffix
    if args.filename == fname:
        raise ValueError('Cannot write output as "{0}": name conflict with source file. Please rename either of them')
    with codecs.open(fname, 'w', encoding='UTF-8', errors='ignore') as f:
        f.writelines(htm.get(lite))
    if args.toc:
        markdown_toclify(input_file = fname,
                         output_file = fname, github = True, back_to_top = True)
    return

def admin(args, unknown_args):
    if args.html:
        fname = 'index.html'
        if args.output:
            fname = getfname([], args.output, suffix='.html') + '.html'
        otext = indexhtml([x for x in args.html if x != fname])
        with codecs.open(fname, 'w', encoding='UTF-8', errors='ignore') as f:
            f.writelines(otext)
    if args.md:
        prepare_bookdown(args.md, args.title, args.author, args.date,
                         args.description, args.url, args.url_edit,
                         args.repo, args.pdf, args.output)
    return

class LogOpts:
    def __init__(self):
        self.master_parser = argparse.ArgumentParser(
        description = '''Compile formatted notes into various publishable formats''',
        prog = 'tigernotes',
        fromfile_prefix_chars = '@',
        epilog = '''Copyright 2012 Gao Wang <gaow@uchicago.edu> GNU General Public License''')
        self.master_parser.add_argument('--version', action='version', version='%(prog)s {0}'.format(VERSION))
        subparsers = self.master_parser.add_subparsers(dest = 'command-name')
        subparsers.required = True
        # latex
        parser = subparsers.add_parser('doc', formatter_class=argparse.ArgumentDefaultsHelpFormatter,
                                       help='Generate text document from notes file(s)')
        self.getTexArguments(parser)
        self.getDocArguments(parser)
        parser.set_defaults(func=doc)
        # beamer
        parser = subparsers.add_parser('slides', formatter_class=argparse.ArgumentDefaultsHelpFormatter,
                                       help='Generate slides from notes file(s)')
        self.getTexArguments(parser)
        self.getSlidesArguments(parser)
        parser.set_defaults(func=slides)
        # html
        parser = subparsers.add_parser('html', formatter_class=argparse.ArgumentDefaultsHelpFormatter,
                                       help='Generate HTML page from notes file(s)')
        self.getTexArguments(parser)
        self.getHtmlArguments(parser)
        parser.set_defaults(func=html)
        # dokuwiki
        parser = subparsers.add_parser('dokuwiki', formatter_class=argparse.ArgumentDefaultsHelpFormatter,
                                       help='Generate dokuwiki text from notes file(s)')
        self.getTexArguments(parser)
        self.getDokuwikiArguments(parser)
        parser.set_defaults(func=dokuwiki)
        # pmwiki
        parser = subparsers.add_parser('pmwiki', formatter_class=argparse.ArgumentDefaultsHelpFormatter,
                                       help='Generate pmwiki text from notes file(s)')
        self.getTexArguments(parser)
        self.getPmwikiArguments(parser)
        parser.set_defaults(func=pmwiki)
        # markdown
        parser = subparsers.add_parser('markdown', formatter_class=argparse.ArgumentDefaultsHelpFormatter,
                                       help='Generate markdown text from notes file(s)')
        self.getTexArguments(parser)
        self.getMarkDownArguments(parser)
        parser.set_defaults(func=markdown)
        # admin
        parser = subparsers.add_parser('admin', formatter_class=argparse.ArgumentDefaultsHelpFormatter,
                                       help='A collection of utility features')
        self.getAdminArguments(parser)
        parser.set_defaults(func=admin)

    def run(self):
        args, unknown_args = self.master_parser.parse_known_args()
        # calling the associated functions
        # args.func(args)
        try:
            args.func(args, unknown_args)
        except Exception as e:
            raise
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
                        help='''remote relative path for image, usually is the namespace a wiki page belongs to''')

    def getMarkDownArguments(self, parser):
        parser.add_argument('--prefix',
                        metavar='PATH',
                        type=str,
                        help='''remote relative path for image''')
        parser.add_argument('--suffix',
                        metavar='EXT',
                        type=str,
                        default='md',
                        help='''output file suffix''')

    def getDokuwikiArguments(self, parser):
        self.getPmwikiArguments(parser)
        parser.add_argument('--showall',
                        action='store_true',
                        default = '',
                        help='''unfold source code / output fields in page by default''')
        parser.add_argument('--compact_toc',
                        action='store_true',
                        default = '',
                        help='''generate compact table of contents (will override --toc)''')
        parser.add_argument('--stamps', nargs = "*", choices = ['time', 'git-version'],
                            help = '''Additional version information to be appended to wiki page''')
        # group = parser.add_mutually_exclusive_group()
        group = parser
        group.add_argument('--permission',
                        metavar='user',
                        type=str,
                        help='''authorized user name or group name of this page''')
        group.add_argument('--disqus', action = 'store_true', help = 'Add "disqus" comment section to page')

    def getAdminArguments(self, parser):
        group = parser.add_argument_group('Index HTML')
        parser.add_argument('-o', '--output',
                        metavar='name',
                        type=str,
                        help='''name of output file prefix''')
        group.add_argument('--html',
                        metavar = 'FN',
                        nargs = '+',
                        help='''name of the input file(s)''')
        group = parser.add_argument_group('Prepare bookdown')
        group.add_argument('--md',
                        metavar = 'FN',
                        nargs = '+',
                        help='''name of the input file(s)''')
        group.add_argument('-a', '--author',
                        action='store',
                        default = '',
                        help='''author's name''')
        group.add_argument('-t', '--title',
                        action='store',
                        default = '',
                        help='''title of document''')
        group.add_argument('-d', '--date',
                        action='store',
                        default = '',
                        help='''date, leave empty for current date''')
        group.add_argument('--description',
                        action='store',
                        default = '',
                        help='''description, a message string or a file name''')
        group.add_argument('--url',
                        action='store',
                        default = '',
                        help='''URL of the website to publish''')
        group.add_argument('--url-edit', dest = 'url_edit',
                        action='store',
                        default = '',
                        help='''URL of the source to edit''')
        group.add_argument('--repo',
                        action='store',
                        default = '',
                        help='''github repo, if available''')
        group.add_argument('--pdf',
                        action='store',
                        help='''source notes to generate PDF file from''')
