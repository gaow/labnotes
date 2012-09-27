import sys, argparse
import codecs
from .utils import getfname, pdflatex, indexhtml
from .logtranslator import LogToTex, LogToBeamer, LogToHtml

def doc(args):
    tex = LogToTex(args.title, args.author, args.toc, args.footnote, args.filename, no_num = args.no_section_number, no_ref = False)
    lite = 1 if args.lite else 0
    fname = getfname(args.filename, args.output)
    pdflatex(fname, tex.get(lite), vanilla=args.vanilla)
    return

def slides(args):
    tex = LogToBeamer(args.title, args.author, args.institute, args.toc, args.mode, args.theme, args.thank, args.filename)
    lite = 1 if args.lite else 0
    fname = getfname(args.filename, args.output)
    pdflatex(fname, tex.get(lite), vanilla=args.vanilla, beamer = True)
    return

def html(args):
    htm = LogToHtml(args.title, args.author, args.toc, args.filename)
    lite = 1 if args.lite else 0
    fname = getfname(args.filename, args.output, suffix='.html')
    body, css, js = htm.get(lite, args.separate)
    if body:
        with codecs.open(fname + '.html', 'w', encoding='UTF-8', errors='ignore') as f: f.writelines(body)
    if css:
        with open('main.css', 'w') as f: f.writelines(css)
    if js:
        with open('main.js', 'w') as f: f.writelines(js)
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
        self.master_parser = argparse.ArgumentParser(
        description = '''Compile formatted log notes into pdf file''',
        prog = 'gw_log',
        fromfile_prefix_chars = '@',
        epilog = '''gw_log, motivated by documenting the workflow for the ESP6900 data analysis.
        Contact: Gao Wang <gaow@bcm.edu>''')
        self.master_parser.add_argument('--version', action='version', version='%(prog)s 1.0alpha')
        subparsers = self.master_parser.add_subparsers()
        # latex
        parser = subparsers.add_parser('doc', help='Generate text document from log file(s)')
        self.getTexArguments(parser)
        self.getDocArguments(parser)
        parser.set_defaults(func=doc)
        # beamer
        parser = subparsers.add_parser('slides', help='Generate slides from log file(s)')
        self.getTexArguments(parser)
        self.getSlidesArguments(parser)
        parser.set_defaults(func=slides)
        # html
        parser = subparsers.add_parser('html', help='Generate HTML page from log file(s)')
        self.getTexArguments(parser)
        self.getHtmlArguments(parser)
        parser.set_defaults(func=html)
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
            sys.exit('Unexpected error occured while processing {}: {}'.format('-'.join(args.filename), e))

    def getTexArguments(self, parser):
        parser.add_argument('filename',
                        metavar = 'FN',
                        nargs = '+',
                        help='''name of the input log file(s)''')
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
        parser.add_argument('--toc',
                        action='store_true',
                        default = '',
                        help='''generate table of contents''')
        parser.add_argument('-o', '--output',
                        metavar='name',
                        type=str,
                        help='''name of output file''')

    def getDocArguments(self, parser):
        parser.add_argument('-f', '--footnote',
                        action='store_true',
                        default = '',
                        help='''generate footnote instead of reference''')
#        parser.add_argument('--no_reference',
#                        action='store_true',
#                        help='''do not include reference in the document''')
        parser.add_argument('--no_section_number',
                        action='store_true',
                        help='''generate un-numbered sections''')
        parser.add_argument('-v', '--vanilla',
                        action='store_true',
                        default = '',
                        help='''build document from scratch without using cached data''')

    def getSlidesArguments(self, parser):
        parser.add_argument('-i', '--institute',
                        action='store',
                        default = '',
                        help='''institute of author''')
        parser.add_argument('--theme',
                        type = str,
                        choices = ['heavy', 'compact', 'plain'],
                        default = 'compact',
                        help='''slides style theme''')
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
        parser.add_argument('-s', '--separate',
                        action='store_true',
                        help='''use separate files for css and js scripts''')

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