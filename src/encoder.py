#!/usr/bin/env python3
# -*- coding: utf-8 -*-
import os, re
from collections import OrderedDict
from .utils import wraptxt
from .style import DOC_PACKAGES, DOC_CONFIG, BM_MODE, BM_CONFIG, \
     BM_TITLE, BM_THANK, BM_THEME, HTML_STYLE, HTML_SYN

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
        self.sq = None
        self.dq = None
        self.bar = '\|'
        self.box_kw = []
        self.direct_url = False
        self.no_ref = False

    def GetURL(self, value, link_text = ''):
        return value

    def GetRef(self, value1, value2, value3):
        return ''

    def FmtListItem(self, value, level):
        return value

    def FmtListStart(self, value, level):
        return value

    def FmtListEnd(self, value, level):
        return value

    def GetTable(self, table, label = None):
        return ''

    def FmtBibStart(self, value):
        return value

    def FmtBibEnd(self, value):
        return value

    def FmtBibItem(self, k, v1, v2):
        return ''

    def FindBibKey(self, value):
        return []

    def GetCodes(self, text, k, label = None):
        return text

    def GetVerbatim(self, text, label = None):
        return text

    def GetBox(self, text, k, label = None):
        return text

    def GetCMD(self, value, index = None):
        return value

    def GetChapter(self, value, add_head = None, index = None):
        return value

    def GetSection(self, value, add_head = None, index = None):
        return value

    def GetHighlight(self, value):
        return value

    def GetSubsubsection(self, value, index = None):
        return value

    def GetSubsection(self, value, add_head = None, index = None):
        return value

    def GetLine(self, value):
        return '\n{}\n'.format(value)

    def RaiseSubsubsection(self, value):
        pass

    def GetSubsectionTail(self):
        return ''

    def GetDocumentTail(self):
        return ''

    def GetDocumentHead(self):
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
        super().__init__()
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
        self.dq = r"``\1''"
        self.sq = r"`\1'"
        self.bar = '\$\|\$'
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

    def GetURL(self, value, link_text = ''):
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

    def FmtListStart(self, value, level):
        return '\\begin{itemize}\n' + value

    def FmtListEnd(self, value, level):
        return value + '\n\\end{itemize}'

    def GetTable(self, table, label = None):
        table = [['\seqsplit{{{}}}'.format(iitem.replace(' ', '~'))
                  if len([x for x in iitem if x == ' ']) > 2 else iitem for iitem in item]
                  for item in table]
        ncols = list(set([len(x) for x in table]))
        nseqsplit = max([len([iitem for iitem in item if iitem.startswith('\\seqsplit')]) for item in table])
        if len(ncols) > 1:
            raise ValueError("Number of columns not consistent in table. Please replace empty columns with placeholder symbol, e.g. '-'.\n``{0} ...``".format('\t'.join(table[0])))
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

    def GetChapter(self, value, add_head, index = None):
        self.doctype = 'report'
        return '\\chapter{' + value + '}'

    def GetSection(self, value, add_head, index = None):
        return ('\\section*{' if self.no_num else '\\section{') + value + '}'

    def GetHighlight(self, value):
        # return '\\shabox{' + value + '}'
        return '\\colorbox{yellow}{\\begin{varwidth}{\\dimexpr\\linewidth-2\\fboxsep}{\\color{red}\\textbf{' + value + '}}\\end{varwidth}}'

    def GetSubsubsection(self, value, index = None):
        return ('\\subsubsection*{' if self.no_num else '\\subsubsection{') + value + '}'

    def GetSubsection(self, value, add_head, index = None):
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
        self.tablefont = table_font_size

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

    def GetChapter(self, value, add_head, index = None):
        prefix = ('\\end{frame}\n\n' if add_head else '') + '\\section{'
        return prefix + value + '}'

    def GetSection(self, value, add_head, index = None):
        prefix = ('\\end{frame}\n\n' if add_head else '') + '\\subsection{'
        return prefix + value + '}'

    def GetHighlight(self, value):
        return '\\colorbox{yellow}{\\textcolor{red}{\\textbf{' + value + '}}}'

    def GetSubsubsection(self, value, index = None):
        return '\\framesubtitle{' + value + '}'

    def GetSubsection(self, value, add_head, index = None):
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

class Html(BaseEncoder):
    def __init__(self, title, author, date, toc, num_columns,
                 table_font_size = 'small', separate_css = True,
                 text_only = False):
        super().__init__()
        self.swaps = [
               # ('\\', '&#92;'),('$', '&#36;'),
               # ('{', '&#123;'),('}', '&#125;'),
               # ('%', '&#37;'),('--', '&mdash;'),
               # ('-', '&ndash;'),('&', '&amp;'),
               # ('~', '&tilde;'),('^', '&circ;'),
               # ('``', '&ldquo;'),('`', '&lsquo;'),
               # ('#', '&#35;'),
                ('<', '&lt;'),('>', '&gt;')
            ]
        self.bl = r'<strong><em>\1</em></strong>'
        self.bd = r'<strong>\1</strong>'
        self.it = r'<em>\1</em>'
        self.tt = r'<kbd>\1</kbd>'
        self.dq = r'"\1"'
        self.sq = r"'\1'"
        self.box_kw = [r'id="wrapper"']
        self.direct_url = True
        self.no_ref = False
        # parameters
        self.toc = toc
        self.toc = toc
        if num_columns == 2:
            self.frame = 'two-col'
        elif num_columns == 3:
            self.frame = 'three-col'
        else:
            self.frame = 'frame'
        self.dtoc = OrderedDict()
        self.title = title
        self.author = author
        self.date = date
        self.wrap_width = 90
        self.tablefont = table_font_size
        self.separate_css = separate_css
        self.text_only = text_only

    def GetURL(self, value, link_text = ''):
        m = re.search(r'^(.+?)://', value)
        if m:
            prefix, address = m.group(0), value.replace(m.group(0), '')
        else:
            prefix = 'http://'
            address = value
        if link_text:
            return '<a style="text-shadow: 1px 1px 1px #999;" href="{0}{1}">{2}</a>'.\
              format(prefix, address, link_text)
        else:
            return '<a href="{0}{1}">{1}</a>'.format(prefix, address, address)

    def GetRef(self, value1, value2, value3):
        return '<a href="#footnote-{0}">{1}</a>'.format(value3, value1)

    def FmtListItem(self, value, level):
        return re.sub(r'^{0}'.format(M * level), '<li>', value) + '</li>'

    def FmtListStart(self, value, level):
        return ('<ol>\n' if level == 2 else '<ul>\n') + value

    def FmtListEnd(self, value, level):
        return value + ('\n</ol>' if level == 2 else '\n</ul>')

    def GetTable(self, table, label = None):
        ncols = list(set([len(x) for x in table]))
        if len(ncols) > 1:
            raise ValueError("Number of columns not consistent for table. Please replace empty columns with placeholder symbol, e.g. '-'.\n``{0} ...``".format('\t'.join(table[0])))
        start = '<td style="vertical-align: top;"><{0}>'.format(self.tablefont)
        end = '<br /></{0}></td>'.format(self.tablefont)
        head = '<center><table><tbody>'
        body = []
        line = ''
        try:
            for cell in table[0]:
                line += start + '<b>' + cell + '</b>' + end + '\n'
            body.append(line)
            for item in table[1:]:
                line = ''
                for cell in item:
                    line += start + cell + end + '\n'
                body.append(line)
        except IndexError:
            # emtpy table
            pass
        #
        for idx, item in enumerate(body):
            if idx % 2:
                body[idx] = '<tr>' + item + '</tr>'
            else:
                body[idx] = '<tr class="dark">' + item + '</tr>'
        tail = '</tbody></table></center>\n'
        text = head + '\n'.join(body) + tail
        return text

    def FmtBibStart(self, value):
        return '<hr style="border: 3px double #555;margin-top:2em;margin-bottom:1em;">\n' + value

    def FmtBibItem(self, k, v1, v2):
        return '<p id="footnote-{0}">[{1}]: {2}</p>\n'.format(k, v1, v2)

    def FindBibKey(self, value):
        return [m.group(1) for m in re.finditer(re.compile('"#footnote-(.*?)"'), value)]

    def GetCodes(self, text, k, label = None):
        text = wraptxt(text, '', int(self.wrap_width), rmblank = True,
                       prefix = COMMENT[k.lower()])
        text = '<pre><code class = "{0}">{3}{3}\n{3}{3} LANGUAGE: {0}, ID: {2}\n{3}{3}\n{1}</code></pre>'.\
          format(k.lower(), text, label if label else k.lower(), COMMENT[k.lower()])
        return text

    def GetVerbatim(self, text, label = None):
        nrow = len(text.split('\n'))
        text = '<center><textarea rows="%s", wrap="off">%s</textarea></center>' % \
          (max(min(nrow, 30), 1), text)
        return text

    def GetBox(self, text, k, label = None):
        text = '<center><div id="wrapper"><div class="{0}"><div style="font-family:\'PT Sans\', comic sans ms;text-align:center;text-decoration:underline{3}; margin-bottom:3px">{1}</div>{2}</div></div></center>'.\
                        format(k.lower(), k.capitalize() if not label else label, text,
                               ';color:red' if k.lower() == 'warning' else '')
        return text

    def GetCMD(self, value, index = None):
        line = '\n'.join(value)
        return '<pre><code class = "nohighlight">{}</code></pre>\n'.\
          format(wraptxt(line, '\\', int(self.wrap_width)))

    def GetChapter(self, value, add_head = None, index = None):
        self.dtoc['chapter_{0}'.format(index)] = value
        return '''
        <h1 class="superheading" id="chapter_{0}">{1}</h1><hr size="5" noshade>
        '''.format(index, value)

    def GetSection(self, value, add_head = None, index = None):
        self.dtoc['section_{0}'.format(index)] = value
        return '''
        <h2 class="heading" id="section_{0}">{1}</h2>
        '''.format(index, value)

    def GetHighlight(self, value):
        return '<span style="color:red;background:yellow;font-weight:bold">' + value + '</span>'

    def GetSubsubsection(self, value, index = None):
        return '''
        <h3 class="subsubheading">&#9642; {0}</h3>
        '''.format(value)

    def GetSubsection(self, value, add_head = None, index = None):
        self.dtoc['subsection_{0}'.format(index)] = value
        return '''
        <h3 class="subheading" id="subsection_{0}">{1}</h3>
        '''.format(index, value)

    def GetLine(self, value):
        return '\n<p>{}</p>\n'.format(value)

    # def GetDocumentHead(self):
    #     res = ''
    #     if title:
    #         res = '\n'.join([M * 3, '{0}!{1}'.format(M, self.title), M * 3])
    #     if author:
    #         res += '\n' + '{1}{0}, {2}'.format(self.author, M, env.precise_time)
    #     return res

    def Write(self, value):
        def format_title(title, author, date):
            return '''
            <div class="top">
            {0}{1}
            </div>
            '''.format('<h1 class="title">{0}</h1>'.format(title)
                       if title else '', '<div class="author" >Edited by {0}, on {1}</div>'.\
                       format(author, date if date else env.precise_time) if author else '')

        def _csize(v, k):
            if k.startswith('chapter'):
                return '<big>{0}</big>'.format(v)
            elif k.startswith('section'):
                return '{0}'.format(v)
            else:
                return '<small>{0}</small>'.format(v)

        def _isize(k):
            if k.startswith('chapter'):
                return 'text-decoration:underline'
            elif k.startswith('section'):
                return 'padding-left:2em'
            else:
                return 'padding-left:4em'

        def format_toc(dtoc):
            if not dtoc:
                return ''
            head = '<b>Contents:</b><ul id="toc">\n'
            tail = '\n</ul>'
            body = '\n'.join(['<li><span style="{0}">{1}</span><a href="#{2}">{3}</a></li>'.\
                              format(_isize(k), _csize(v,k),k,'&clubs;') \
                              for k, v in list(dtoc.items())])
            return '<div class="frame">' + head + body + tail + '</div>'

        if self.text_only:
            # Export pure text for use with other templates
            return '\n'.join(value), '', ''
        otext = '<!DOCTYPE html><html><head><title>{0}</title>\n'.\
          format((self.title + ' | ' + self.author) if self.title or self.author else '')
        if self.separate_css:
            otext += '<link href="style.css" rel="stylesheet" type="text/css">'
        else:
            otext += '<style type="text/css">\n{0}</style>'.format(HTML_STYLE)
        # syntax highlight and mathjax support
        otext += HTML_SYN
        otext += '</head><body><a name="top"></a>%s%s<div class="%s"><div class="content">%s</div></div></body></html>' % (format_title(self.title, self.author, self.date),
                       (format_toc(self.dtoc) if self.toc else ''),
                       self.frame, '\n'.join(value))
        return otext, HTML_STYLE if self.separate_css else ''

class Dokuwiki(BaseEncoder):
    def __init__(self, title, author, date, toc, show_all, permission, disqus):
        super().__init__()
        self.swaps = [('--', '%%--%%', r'@@(.*?)@@'),
                      ('__', '%%__%%', r'@@(.*?)@@')]
        self.bl = r"**//\1//**"
        self.bd = r'**\1**'
        self.it = r'//\1//'
        self.tt = r"''\1''"
        self.sq = r"'\1'"
        self.dq = r'"\1"'
        self.box_kw = [r'box 80']
        self.direct_url = True
        self.no_ref = True
        # parameters
        self.title = title
        self.author = author
        self.date = date
        self.toc = toc
        self.show_all = show_all
        self.wrap_width = -1
        self.sxh3 = False
        self.box_colors = {'warning': 'red', 'important': 'orange', 'tip': 'blue', 'note': 'green'}
        self.permission = permission
        self.disqus = disqus

    def GetURL(self, value, link_text = ''):
        if link_text:
            return '[[{}|{}]]'.format(value, link_text)
        else:
            return value

    def GetRef(self, value1, value2, value3):
        return value1 + '(({0}))'.format(value2)

    def FmtListItem(self, value, level):
        return re.sub(r'^{0}'.format(M * level), '\t' * level + '* ', value)

    def GetTable(self, table, label = None):
        ncols = list(set([len(x) for x in table]))
        if len(ncols) > 1:
            raise ValueError("Number of columns not consistent for table. Please replace empty columns with placeholder symbol, e.g. '-'.\n``{0} ...``".format('\t'.join(table[0])))
        body = '<WRAP center 105%>\n' + '^  ' + '  ^  '.join(table[0]) + '  ^\n' + '\n'.join(['|  ' + '  |  '.join(item) + '  |' for item in table[1:]]) + '\n</WRAP>\n'
        return body

    def GetCodes(self, text, k, label = None):
        # no wrap, totally rely on dokuwiki
        # text = wraptxt(text, '', 1000, rmblank = True)
        # require sxh3 plugin
        if self.sxh3:
            text = '<sxh {0}{1};gutter: false;>\n\n'.format(
                k.lower() if k.lower() not in ['s', 'r'] else 'plain',
                ';title: {0}'.format(label) if label else ''
                ) +  text + '\n\n</sxh>'
        # non-sxh3 version
        else:
            text = '<code {0} {1}>\n'.format(
                k.lower() if k.lower() not in ['s', 'r'] else 'rsplus',
                '{0}{1}'.format('_'.join(re.sub(r'[^a-zA-Z0-9]',' ', os.path.splitext(label)[0]).split())
                                if label else 'download-source',
                                ('.' + SYNTAX[k.lower()]) if k.lower() != 'text'
                                else (os.path.splitext(label)[1] if label else '.txt'))
                ) +  text + '\n</code>'
        if self.show_all:
            text = '<hidden initialState="visible" -noprint>\n{0}\n</hidden>\\\\'.format(text)
        else:
            text = '<hidden -noprint>\n{0}\n</hidden>\\\\'.format(text)
        return text

    def GetVerbatim(self, text, label = None):
        text = '\n'.join(['  ' + x for x in text.split('\n')])
        if self.show_all:
            text = '<hidden initialState="visible" -noprint>\n{0}\n</hidden>\\\\'.format(text)
        else:
            text = '<hidden -noprint>\n{0}\n</hidden>\\\\'.format(text)
        return text

    def GetBox(self, text, k, label = None):
        text = '<box 80% round {0}|**__{1}__**>\n{2}\n</box>'.\
          format(self.box_colors[k.lower()] if k.lower() in self.box_colors else 'black',
                 k.lower().capitalize() if not label else label, text)
        return text

    def GetCMD(self, value, index = None):
        cmd = '\n'.join([wraptxt(x, '\\', int(self.wrap_width)) for x in value])
        head = '<code bash>\n'
        tail = '\n</code>\\\\'
        return head + cmd + tail

    def GetChapter(self, value, add_head = None, index = None):
        return '===== ' + value + ' ====='

    def GetSection(self, value, add_head = None, index = None):
        return '==== ' + value + ' ===='

    def GetHighlight(self, value):
        return '<wrap em hi>\n' + value + '\n</wrap>\n'

    def GetSubsubsection(self, value, index = None):
        return '== ' + value + ' =='

    def GetSubsection(self, value, add_head = None, index = None):
        return '=== ' + value + ' ==='

    def Write(self, value):
        otext = '\n'.join(value)
        # mathjax support
        # otext = '<HTML><script type="text/javascript" src="http://cdn.mathjax.org/mathjax/latest/MathJax.js?config=TeX-AMS-MML_HTMLorMML"></script><link href="style.css" rel="stylesheet" type="text/css"><script LANGUAGE="JavaScript" src="style.js"></script></HTML>\n' + otext
        if self.toc == 0:
            otext = '~~NOTOC~~\n' + otext
        if self.toc == 2:
            otext = otext.split('\n')
            insert_point = [idx for idx, item in enumerate(otext)
                            if item.startswith('=====') and item.endswith("=====")]
            if len(insert_point) != 1:
                otext = '{{INLINETOC}}\n\\\\\n' + '\n'.join(otext)
            else:
                otext.insert(insert_point[0] + 1,  '{{INLINETOC}}\n\\\\')
                otext = '\n'.join(otext)
        if self.permission:
            user = re.sub(r'^\\', '', re.sub(r'^"|^\'|"$|\'$', '', self.permission))
            otext = '<ifauth !{0}>\nThis post is only visible to authorized members. Please login if you are one of them.\n</ifauth>\n<ifauth {0}>\n' + otext
        if self.disqus:
            otext += '\n\\\\\n\\\\\n\\\\\n~~DISQUS~~'
        if self.permission:
            otext += '\n</ifauth>'
        return otext

class Markdown(BaseEncoder):
    def __init__(self, title, author, date):
        super().__init__()
        self.swaps = [(r'(\b|^)__', r'\\__', r'(\b|^)__(.*?)__(\b|$)'),
                      (r'(\b|^|@@)__', r'\\__', r'(\b|^)@@__(.*?)__@@($|\b)')]
        self.bl = r"**_\1_**" 
        self.bd = r'**\1**'
        self.it = r'*\1*'
        self.tt = r'`\1`' 
        self.sq = r"'\1'"
        self.dq = r'"\1"'
        self.direct_url = True
        # parameters
        self.title = title
        self.author = author
        self.date = date
        self.wrap_width = -1

    def GetURL(self, value, link_text = ''):
        if link_text:
            return '[{}]({})'.format(link_text, value)
        else:
            return value

    def GetRef(self, value1, value2, value3):
        return '<a name="#footnote-{0}">{1}</a>'.format(value3, value1)

    def FmtBibItem(self, k, v1, v2):
        return '[{1}](#footnote-{0}): {2}\n'.format(k, v1, v2)

    def FindBibKey(self, value):
        return [m.group(1) for m in re.finditer(re.compile('"#footnote-(.*?)"'), value)]

    def FmtListItem(self, value, level):
        return re.sub(r'^{0}'.format(M * level), ('\t' * (level - 1)) + '* ', value)

    def GetTable(self, table, label = None):
        ncols = list(set([len(x) for x in table]))
        if len(ncols) > 1:
            raise ValueError("Number of columns not consistent for table. Please replace empty columns with placeholder symbol, e.g. '-'.\n``{0} ...``".format('\t'.join(table[0])))
        hline = '|' + '|'.join([':{}:'.format('-' * (len(x) + 2)) for x in table[0]]) + '  |\n'
        body = '|  ' + '  |  '.join(table[0]) + '  |\n' + hline + '\n'.join(['|  ' + '  |  '.join(item) + '  |' for item in table[1:]]) + '\n'
        return body

    def GetCodes(self, text, k, label = None):
        text = '\n'.join(['  ' + x for x in text.split('\n')])
        text = '```{1}\n{0}\n```\n'.format(text, k.lower() if k.lower() != "text" else '')
        return text

    def GetVerbatim(self, text, label = None):
        k = label if label is not None else ''
        return self.GetCodes(text, k, label = None)

    def GetBox(self, text, k, label = None):
        return '**_{0}_**\n\n{1}\n'.format(label if label else k.lower().capitalize(), text)

    def GetCMD(self, value, index = None):
        cmd = '\n'.join([wraptxt(x, '\\', int(self.wrap_width)) for x in value])
        head = '```\n'
        tail = '\n```\n'
        return head + cmd + tail

    def GetChapter(self, value, add_head = None, index = None):
        return '# ' + value

    def GetSection(self, value, add_head = None, index = None):
        return '## ' + value

    def GetHighlight(self, value):
        return '**_' + value + '_**\n'

    def GetSubsubsection(self, value, index = None):
        return '#### ' + value

    def GetSubsection(self, value, add_head = None, index = None):
        return '### ' + value

    def Write(self, value):
        otext = '\n'.join(value)
        return otext
