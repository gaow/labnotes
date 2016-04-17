#!/usr/bin/env python
# -*- coding: utf-8 -*-
import sys, shutil, os, re, argparse, codecs
from .utils import env, regulate_output, pdflatex, indexhtml
from .parser import ParserCore
from .encoder import LaTeX, Beamer, Html, Dokuwiki, Markdown
from .markdown_toclify import markdown_toclify
from .blog import BlogCFG, edit_blog, upload_blog
from .bookdown import prepare_bookdown

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
        raise ValueError('Cannot write output to ``{0}`` due to name conflict with input!'.format(fname + '.txt'))
    with codecs.open(fname + '.txt', 'w', encoding='UTF-8', errors='ignore') as f:
        f.writelines(runner(worker))
    return

def markdown(args, unknown_args):
    args.suffix = '.' + args.suffix
    runner = ParserCore(args.filename, 'markdown', 'long' if args.long_ref else 'short', args.lite,
                        figure_path = args.figure_path)
    # Currently none of these 3 input variables is used
    worker = Markdown(args.title, args.author, args.date)
    text = runner(worker).split('\n')
    fname = None
    if args.output:
        # check if output name is a directory name
        # then use the Github wiki style output:
        # the first line of file as filename
        if os.path.isdir(args.output):
            for idx, item in enumerate(text):
                if item:
                    fname = os.path.join(args.out, re.sub(r'#|:', '', item).strip().replace(' ', '-'))
                    text = text[(idx + 1):]
                    break
    if not fname:
        fname = regulate_output(args.filename, args.output, suffix=args.suffix)
    fname += args.suffix
    if args.filename == fname:
        raise ValueError('Cannot write output to ``{0}`` due to name conflict with input!'.format(fname))
    with codecs.open(fname, 'w', encoding='UTF-8', errors='ignore') as f:
        f.writelines('\n'.join(text))
    if args.toc:
        markdown_toclify(input_file = fname,
                         output_file = fname, github = True, back_to_top = True)
    return

def blog(args, unknown_args):
    config = BlogCFG(args.config, args.date)
    if args.make:
        upload_blog(config, args.user)
    else:
        edit_blog(config)
    return

def bind(args, unknown_args):
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
                         args.repo, args.pdf, args.output, unknown_args)

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
        # markdown
        parser = subparsers.add_parser('markdown', formatter_class=argparse.ArgumentDefaultsHelpFormatter,
                                       help='Generate markdown text from notes file(s)')
        self.getCommonArguments(parser)
        self.getMarkDownArguments(parser)
        parser.set_defaults(func=markdown)
        # markdown
        parser = subparsers.add_parser('blog', formatter_class=argparse.ArgumentDefaultsHelpFormatter,
                                       help='A simple HTML blog manager')
        self.getBlogArguments(parser)
        parser.set_defaults(func=blog)
        # bind
        parser = subparsers.add_parser('bind', formatter_class=argparse.ArgumentDefaultsHelpFormatter,
                                       help='Bind multiple documents')
        self.getBindArguments(parser)
        parser.set_defaults(func=bind)

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
                        metavar = 'filename',
                        nargs = '+',
                        help='''name of the input notes file(s)''')
        parser.add_argument('-a', '--author',
                        metavar='name',
                        help='''author's name''')
        parser.add_argument('-t', '--title',
                        metavar='text',
                        help='''title of document''')
        parser.add_argument('-d', '--date',
                        metavar='date',
                        default = env.nice_time,
                        help='''date, leave empty for current date''')
        parser.add_argument('-o', '--output',
                        metavar='name',
                        type=str,
                        help='''name of output file''')
        parser.add_argument('--toc',
                        action='store_true',
                        help='''generate table of contents''')
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
                        metavar = 'dir',
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
                        metavar = 'dir',
                        default = '',
                        help='''path to where figures are saved''')

    def getMarkDownArguments(self, parser):
        parser.add_argument('--suffix',
                        metavar='EXT',
                        default='md',
                        help='''output file suffix''')
        parser.add_argument('--figure_path',
                        metavar = 'dir',
                        default = '',
                        help='''path to where figures are saved''')

    def getBlogArguments(self, parser):
        parser.add_argument('-d', '--date', help='''Date to edit''')
        parser.add_argument('-c', dest = 'config', default = '~/.labnotes/blog.yml', help = 'blog configuration file')
        parser.add_argument('-u', '--user', help='''username to web host''')
        parser.add_argument('-m', '--make', action='store_true', help = 'generate and upload pages')

    def getBindArguments(self, parser):
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
                        nargs = '+',
                        help='''source notes to generate PDF file from''')
