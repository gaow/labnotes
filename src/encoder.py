#!/usr/bin/env python3
# -*- coding: utf-8 -*-
import os, re
from .utils import wraptxt
from .style import DOC_PACKAGES, DOC_CONFIG, BM_MODE, BM_CONFIG, \
     BM_TITLE, BM_THANK, BM_THEME

M = '#' # Lines of regular labnotes text start with hashtag
FONT = {'bch':'bch',
        'default':'default',
        'serif':'\\sfdefault',
        'tt':'\\ttdefault',
        'roman':'ptm'
        }
COMMENT = {'r':'#',
          'bash':'#',
          'python':'#',
          'perl':'#',
          'latex':'%',
          'c':'//',
          'cpp':'//',
          'sql':'#',
          'php':'#',
          'text':''
          }
SYNTAX = {'r':'R',
          'bash':'sh',
          'python':'py',
          'perl':'pl',
          'latex':'tex',
          'c':'c',
          'cpp':'cpp',
          'sql':'sqlite',
          'php':'php',
          'text':'txt',
          'raw':'txt',
          '$':'txt'
          }

class BaseEncoder:
    def __init__(self):
        self.swaps = []
        self.bl = None
        self.bd = None
        self.it = None
        self.tt = None
        self.box_kw = []

    def GetURL(self, value):
        return ''

    def GetRef(self, value1, value2, value3):
        return ''

    def FmtListItem(self, value, level):
        return ''

    def FmtListStart(self, value):
        return ''

    def FmtListEnd(self, value):
        return ''

    def GetTable(self, table, label = None):
        return ''

    def FmtBibStart(self, value):
        return ''

    def FmtBibEnd(self, value):
        return ''

    def FmtBibItem(self, k, v1, v2):
        return ''

    def FindBibKey(self, value):
        return []

    def GetCodes(self, text, k, label = None):
        return ''

    def GetVerbatim(self, text, label = None):
        return ''

    def GetBox(self, text, k, label = None):
        return ''

    def GetCMD(self, value, index = None):
        return ''

    def GetChapter(self, value, add_head = None):
        return ''

    def GetSection(self, value, add_head = None):
        return ''

    def GetHighlight(self, value):
        return ''

    def GetSubsubsection(self, value):
        return ''

    def GetSubsection(self, value, add_head = None):
        return ''

    def RaiseSubsubsection(self, value):
        pass

    def GetSubsectionTail(self):
        return ''

    def GetDocumentTail(self):
        return ''

    def Write(self, value):
        return ''

class FigureInserter:
    def __init__(self, text, support, tag, remote_path = ''):
        if text.startswith(M + '*'):
            text = text[len(M)+1:].strip()
        else:
            text = text.strip()
        if not text:
            return ''
        lines = [x.strip() for x in text.split(';') if x.strip()]
        for idx, line in enumerate(lines):
            try:
                fig, width = line.split()
                width = float(width)
            except ValueError:
                fig = line.split()[0]
                width = 0.9
            # if (not tag.endswith('wiki')) and width > 1:
            #     width = 0.9
            fname = os.path.basename(fig)
            if not '.' in fname:
                raise ValueError("Cannot determine file format for ``{0}``. Valid extensions are ``{1}``".\
                          format(fname, ' '.join(support)))
            extension = fname.split('.')[-1]
            if extension.lower() not in support:
                raise ValueError("Input file format ``{0}`` not supported. Valid extensions are ``{1}``".\
                          format(extension, ' '.join(support)))
            if not os.path.exists(fig):
                raise ValueError("Cannot find file ``%s``" % fig)
            if not remote_path:
                fig = os.path.abspath(fig)
            else:
                fig = os.path.join(remote_path, fname)
            # syntax images
            if tag == 'tex':
                lines[idx] = '\\includegraphics[width=%s\\textwidth]{%s}\n' % (width, fig)
            elif tag == 'html':
                if extension == 'pdf':
                    lines[idx] = '<a style="text-shadow: 1px 1px 1px #999;" href="{0}">{1}</a>\n'.\
                      format(fig, 'Download Image "{0}"'.format(fname))
                else:
                    lines[idx] = '<p><center><img src="{0}" alt="{1}" width="{2}%" /></center></p>'.\
                      format(fig, fname, int(width * 100))
            elif tag.endswith("wiki"):
                if tag == 'dokuwiki':
                    # dokuwiki style
                    if extension == 'pdf':
                        lines[idx] = "[[{0}|{1}]]\n".format(fig, 'Download Image "{0}"'.format(fname))
                    else:
                        sep = ':' if not '://' in remote_path else '/'
                        lines[idx] = '{{%s%s%s?%s}}' % (remote_path, sep, fname, width)
                if tag == 'pmwiki':
                    if extension == 'pdf':
                        lines[idx] = "[[{0}|{1}]]\n".format(fig, 'Download Image "{0}"'.format(fname))
                    else:
                        lines[idx] = '%center% Attach:%s' % (fname)
            elif tag == 'markdown':
                    lines[idx] = '![]({})'.format(fig)
            else:
                raise ValueError('Unknown tag ``{0}`` for figures!'.format(tag))
        if tag == 'tex':
            if len(lines) > 1:
                w_minipage = int(1.0 / (1.0 * len(lines)) * 90) / 100.0
                lines = ['\\subfigure{' + x + '}\n' for x in lines]
                lines[0] = '\\begin{figure}[H]\n\\centering\n\\mbox{\n' + lines[0]
                lines[-1] += '\n}\n\\end{figure}\n'
            else:
                lines[0] = '\\begin{figure}[H]\n\\centering\n' + lines[0]
                lines[-1] += '\\end{figure}\n'
        self.data = '\n'.join(lines)

    def Insert(self):
        return self.data

class LaTeX(BaseEncoder):
    def __init__(self, title, author, date, toc, is_footnote, font,
                 font_size, table_font_size = 'footnotesize', no_num = False, no_page = False,
                 no_ref = False, twocols = False, landscape = False, pause = False):
        # configurations
        self.swaps = [('\\', '!!\\backslash!!'),('$', '\$'),
                      ('!!\\backslash!!', '$\\backslash$'),
                      ('{', '\{'),('}', '\}'),('%', '\%'), ('_', '\-\_'),
                      ('|', '$|$'),('&', '\&'),('<', '$<$'),
                      ('>', '$>$'),('~', '$\sim$'),
                      ('^', '\^{}'), ('#', '\#')]
        self.bl = r'\\textbf{\\textit{\1}}'
        self.bd = r'\\textbf{\1}'
        self.it = r'\\textit{\1}'
        self.tt = r'\\texttt{\1}'
        self.box_kw = [r'\\\\begin{bclogo}', r'\\\\end{bclogo}']
        # parameters
        self.title = title
        self.author = author
        self.date = date
        self.is_footnote = is_footnote
        self.pause = pause
        self.bclogo = {'warning':'\\bcattention', 'tip':'\\bclampe',
                       'important':'\\bctakecare', 'note':'\\bccrayon'}
        self.doctype = 'article'
        self.toc = toc
        self.footnote = is_footnote
        self.font_size = font_size
        self.font = font
        self.tablefont = table_font_size
        self.no_num = no_num
        self.no_page = no_page
        if self.footnote:
            self.no_ref = True
        else:
            self.no_ref = no_ref
        self.twocols = twocols
        self.landscape = landscape

    def GetURL(self, value):
        return '\\url{%s}' % value.replace('\-\_', '\_').replace('$\sim$', '~')

    def GetRef(self, value1, value2, value3):
        if self.is_footnote:
            return '{\\color{MidnightBlue}%s}~\\footnote{%s}' \
              % (value1, '\\underline{' + value1 + '} ' + value2)
        else:
            return '{\\color{MidnightBlue}%s}~\\cite{%s}' % (value1, value3)

    def FmtListItem(self, value, level):
        value = re.sub(r'^{0}'.format(M * level), '\\item ', value)
        if self.pause:
            value = value.replace('\\item -', '\\pause \\item ')
        return value

    def FmtListStart(self, value):
        return '\\begin{itemize}\n' + value

    def FmtListEnd(self, value):
        return value + '\n\\end{itemize}'

    def GetTable(self, table, label = None):
        table = [['\seqsplit{{{}}}'.format(iitem.replace(' ', '~'))
                  if len([x for x in iitem if x == ' ']) > 2 else iitem for iitem in item]
                  for item in table]
        ncols = list(set([len(x) for x in table]))
        nseqsplit = max([len([iitem for iitem in item if iitem.startswith('\\seqsplit')]) for item in table])
        if len(ncols) > 1:
            raise ValueError("Number of columns not consistent for table. Please replace empty columns with placeholder symbol, e.g. '-'.\n ``{0}``".format(text))
        try:
            cols = ''.join(['c' if len([item[i] for item in table if item[i].startswith('\\seqsplit')]) == 0 else 'p{{{}pt}}'.format((480-(ncols[0]-nseqsplit)*10)/nseqsplit) for i in range(ncols[0])])
            head = '\\begin{center}\n{\\%s\\begin{longtable}{%s}\n\\hline\n' % (self.tablefont, cols)
            body = '&'.join(table[0]) + '\\\\\n' + '\\hline\n' + '\\\\\n'.join(['&'.join(item) for item in table[1:]]) + '\\\\\n'
            tail = '\\hline\n\\end{longtable}}\n\\end{center}\n'
        except IndexError:
            return ''
        return head + body + tail

    def FmtBibStart(self, value):
        return '\\begin{thebibliography}{9}\n' + value

    def FmtBibEnd(self, value):
        return value + '\\end{thebibliography}'

    def FmtBibItem(self, k, v1, v2):
        return '\\bibitem{%s}\n[%s]\\\\%s\n' % (k, v1, v2)

    def FindBibKey(self, value):
        return [m.group(1) for m in re.finditer(re.compile('\\cite{(.*?)}'), value)]

    def GetCodes(self, text, k, label = None):
        return '\\begin{minted}[samepage=false, fontfamily=tt,\nfontsize=\\scriptsize, xleftmargin=1pt,\nframe=lines, framerule=1pt, framesep=2mm,\nlabel=\\fbox{%s}]{%s}\n%s\n\\end{minted}\n' % (k.upper() if not label else label, k, wraptxt(text, '\\' if k == 'bash' else '', 131, rmblank = False, prefix = COMMENT[k.lower()]))

    def GetVerbatim(self, text, label = None):
        return '\\begin{Verbatim}[samepage=false, fontfamily=tt,\nfontsize=\\footnotesize, formatcom=\\color{rgray},\nframe=lines, framerule=1pt, framesep=2mm,\nlabel=\\fbox{\\scriptsize %s}, labelposition=topline]\n%s\n\\end{Verbatim}\n' % ('OUTPUT' if not label else label, wraptxt(text, '', 116))

    def GetBox(self, text, k, label = None):
        return '\\begin{bclogo}[logo=%s, couleurBarre=MidnightBlue, noborder=true, couleur=white]{~%s}%s\n\\end{bclogo}\n' % (self.bclogo[k], k.capitalize() if not label else label, text)

    def GetCMD(self, value, index = None):
        def condense(cmd):
            tmp = [x.strip() for x in cmd.split('\n')]
            cmd = []
            for idx, item in enumerate(tmp):
                if item.endswith('\\') and tmp[min(idx+1, len(tmp)-1)] == '':
                    item = item[:-1]
                if item != '':
                    cmd.append(item)
            return cmd
        #
        sep = '\\'
        cnt = 114
        sminted = '\\mint[bgcolor=bg, fontsize=\\footnotesize]{text}?'
        lminted = '\\begin{minted}[bgcolor=bg, fontsize=\\footnotesize]{text}\n'
        cmd = '\n'.join([wraptxt(x, sep, cnt) for x in value])
        cmd = condense(cmd)
        if len(cmd) == 1 and "?" not in cmd[0] and "`" not in cmd[0]:
            cmd = sminted + cmd[0] + '?'
        else:
            cmd = lminted + '\n'.join(cmd) + '\n\\end{minted}'
        return cmd

    def GetChapter(self, value, add_head):
        self.doctype = 'report'
        return '\\chapter{' + value + '}'

    def GetSection(self, value, add_head):
        return ('\\section*{' if self.no_num else '\\section{') + value + '}'

    def GetHighlight(self, value):
        # return '\\shabox{' + value + '}'
        return '\\colorbox{yellow}{\\begin{varwidth}{\\dimexpr\\linewidth-2\\fboxsep}{\\color{red}\\textbf{' + value + '}}\\end{varwidth}}'

    def GetSubsubsection(self, value):
        return ('\\subsubsection*{' if self.no_num else '\\subsubsection{') + value + '}'

    def GetSubsection(self, value, add_head):
        return ('\\subsection*{' if self.no_num else '\\subsection{') + value + '}'

    def Write(self, value):
        return '\\documentclass[oneside%s%s]{%s}' % (',twocolumn' if self.twocols else '',
                                                     ',landscape' if self.landscape else '', self.doctype) + \
                                                     DOC_PACKAGES + \
                ('\\usepackage[Lenny]{fncychap}\n' if self.doctype == 'report' else '') + \
                ('\\usepackage{mathptmx}\n' if self.font == 'roman' else '') + \
                '\\renewcommand\\%s{References}\n' % ('bibname' if self.doctype == 'report' else 'refname') + \
                (('\\renewcommand\\rmdefault{%s}\n' % FONT[self.font]) if (self.font != 'default' and self.font != 'roman') else '') + \
                DOC_CONFIG + ('\\pagestyle{empty}\n' if self.no_page else '') + \
                (('\\setlength{\\columnsep}{%s}\\setlength{\\columnseprule}{%s}\n' % ('2em','0pt')) if self.twocols else '') + \
                '\\title{%s}\n' % self.title + '\\author{%s}\n' % self.author + \
                '\\date{%s}\n\\raggedbottom\n\\begin{document}\n' % self.date + \
                '\\fontsize{%s}{%s}\\selectfont\n' % (self.font_size, int(self.font_size * 1.2)) + \
                '%s\n%s\n\\bigskip\n%s\n\\end{document}' % ('\\maketitle' if self.title or self.author else '',
                                                            '\\tableofcontents' if self.toc else '', '\n'.join(value))

class Beamer(LaTeX):
    def __init__(self, title, author, date, institute, toc, stoc, is_footnote, table_font_size = 'tiny',
                 mode = 'presentation', theme = 'compact', thank = False):
        super().__init__(title, author, date, toc, is_footnote, None, None, table_font_size,
                       False, False, False, False, False, True)
        # configurations
        self.box_kw = [r'\\\\begin{(.*?)block}', r'\\\\end{(.*?)block}']
        # parameters
        self.institute = institute.replace('\\n', '\n') if institute else None
        self.stoc = stoc
        self.mode = mode
        self.theme = theme
        self.wrap_adjust = 1
        if self.mode == 'notes':
            self.wrap_adjust = 1.38
        else:
            if self.theme == 'heavy':
                self.wrap_adjust = 0.92
        self.thank = thank

    def FmtBibStart(self, value):
        return '\\appendix\n\\begin{frame}[allowframebreaks]\n\\tiny\n' + \
          '\\begin{thebibliography}{9}\n' + value

    def FmtBibEnd(self, value):
        return value + '\\end{thebibliography}' + '\n\\end{frame}'

    def GetCodes(self, text, k, label = None):
        return '\\begin{exampleblock}{\\texttt{%s}}\\scriptsize\n\\begin{Verbatim}\n%s\n\\end{Verbatim}\n\\end{exampleblock}\n' % (k.capitalize() if not label else label, wraptxt(text, '', int(78 * self.wrap_adjust), rmblank = False, prefix = COMMENT[k.lower()]))

    def GetVerbatim(self, text, label = None):
        return '\\begin{exampleblock}{%s}\\tiny\n\\begin{Verbatim}\n%s\n\\end{Verbatim}\n\\end{exampleblock}\n' % (label if label else "-", wraptxt(text, '', int(105 * self.wrap_adjust), rmblank = False))

    def GetBox(self, text, k, label = None):
        fmt = ''
        if k == 'important':
            fmt = 'example'
        if k == 'warning':
            fmt = 'alert'
        return '\\begin{{{0}block}}{{{1}}}\n{2}\n\\end{{{0}block}}\n'.\
                        format(fmt, k.capitalize() if not label else label, text)

    def GetCMD(self, value, index = None):
        sep = ''
        cnt = int(62 * self.wrap_adjust)
        sminted = '\\Verb?'
        lminted = '\\begin{Verbatim}[fontsize=\\footnotesize]\n'
        #
        cmd = '\n'.join([wraptxt(x, sep, cnt) for x in value])
        cmd = cmd.split('\n')
        if len(cmd) == 1:
            cmd = sminted + cmd[0] + '?'
        else:
            cmd = lminted + '\n'.join(cmd) + '\n\\end{Verbatim}'
        return cmd

    def GetChapter(self, value, add_head):
        prefix = ('\\end{frame}\n\n' if add_head else '') + '\\section{'
        return prefix + value + '}'

    def GetSection(self, value, add_head):
        prefix = ('\\end{frame}\n\n' if add_head else '') + '\\subsection{'
        return prefix + value + '}'

    def GetHighlight(self, value):
        return '\\colorbox{yellow}{\\textcolor{red}{\\textbf{' + value + '}}}'

    def GetSubsubsection(self, value):
        return '\\framesubtitle{' + value + '}'

    def GetSubsection(self, value, add_head):
        prefix = '\\begin{frame}[fragile, shrink]\n'
        if value.lower() == 'acknowledgment':
            prefix = '\\section*{Acknowledgment}\n' + prefix
        if add_head:
            prefix = '\\end{frame}\n\n' + prefix
        return prefix + ('' if value == '.' else  '\\frametitle{' + value + '}')

    def RaiseSubsubsetcion(self, value):
        if not 'frametitle' in value:
            raise ValueError("``{0}!!`` has follow a line starting with ``{0}!``, near ``{1}``".\
                      format(M, value))

    def GetSubsectionTail(self):
        return '\\end{frame}\n'

    def GetDocumentTail(self):
        return BM_THANK if self.thank else ''

    def Write(self, value):
        def raise_empty_slides(ltext):
            text = ''.join(ltext)
            pattern = re.compile(r'\\\\begin{frame}\[fragile, shrink\](.*?)\\\\end{frame}')
            for m in re.finditer(pattern, '%r' % text):
                frame = m.group(1)
                try:
                    frametitle = re.search(r'\\\\frametitle{(.*?)}', frame).group(1).encode().\
                      decode('unicode_escape')
                except:
                    frametitle = '#!.'
                frame = re.sub(r'\\\\frametitle{(.*?)}', '', frame)
                frame = re.sub(r'\\\\framesubtitle{(.*?)}', '', frame)
                if len(re.sub(r'\s', '', frame.encode().decode('unicode_escape'))) == 0:
                    raise ValueError("Empty slides not allowed, near ``{0}``".format(frametitle))
            return

        def short_title(length):
            stitle = self.title
            # length ok
            if len(stitle.replace('\\text', '')) < length:
                return stitle
            # have to chop
            if '\\' in self.title:
                stitle = self.title[:self.title.index('\\')]
            return stitle[:min(length, len(stitle))] + ' ...'

        raise_empty_slides(value)
        titlepage = '\\frame{\\titlepage}\n' if not self.mode == 'notes' else '\\maketitle\n'
        tocpage = '\\begin{frame}[allowframebreaks]\n\\frametitle{Outline}\n\\tableofcontents%s\n\\end{frame}\n' % ('[hideallsubsections]' if self.stoc else '') if not self.mode == 'notes' else '\\tableofcontents\n'
        sectiontoc = '\\AtBeginSection[]\n{\n\\begin{frame}<beamer>\n\\tableofcontents[currentsection, currentsubsection, sectionstyle=show/hide, subsectionstyle=show/show/hide]\n\\end{frame}\n}\n' if self.stoc else ''
        otext = '{0}'.format(BM_MODE[self.mode]) + \
                BM_CONFIG + '{0}'.format(BM_THEME[self.theme.lower()]) + BM_TITLE
        if self.title or self.author:
            otext += '\n\\title[%s]{%s}\n%% \\subtitle\n\\author[%s]{%s}\n' % \
                (short_title(35), self.title, re.sub(r'\\inst{(.*?)}', '', self.author).strip().split(r'\and')[0].strip(), self.author)
        if self.institute:
            otext += '\\institute[%s]{%s}\n' % (re.sub(r'\\inst{(.*?)}', '', self.institute).strip().split(r'\and')[0].strip(), self.institute)
        otext += '\\date{%s}\n%s\\begin{document}\n%s\n%s' % (
                self.date,
                sectiontoc if self.toc else '',
                titlepage if self.title or self.author else '',
                tocpage if self.toc else ''
                )
        otext += '\n'.join(value) + '\n\\end{document}'
        return otext
