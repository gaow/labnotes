import os, sys, re
from time import strftime, localtime
from collections import OrderedDict
import codecs
from utils import wraptxt
from ltheme import MODE, CONFIG, TITLE, THANK, THEME, DOC_PACKAGES, DOC_CONFIG
from htheme import HTML_STYLE, JS_SCRIPT

SYNTAX = {'r':'r',
          'sh':'bash',
          'py':'python',
          'tex':'latex',
          'c':'c',
          'cpp':'cpp',
          'h':'c',
          'sqlite':'sql'
          }

# base class
class TexParser:
    def __init__(self, title, author, fname):
        self.title = ' '.join([x[0].upper() + (x[1:] if len(x) > 1 else '') for x in self.m_recode(title).split()])
        self.author = self.m_recode(author)
        self.fn = '-'.join(fname)
        self.mark = '#'
        self.text = []
        self.PARSER_RULE = {
                'list':'self.m_blockizeList',
                'table':'self.m_blockizeTable',
                'out':'self.m_blockizeOut',
                }
        for item in list(set(SYNTAX.values())):
            self.PARSER_RULE[item] = 'self.m_blockizeIn'
        for item in ['warning', 'tip', 'important', 'note']:
            self.PARSER_RULE[item] = 'self.m_blockizeAlert'
        self.comments = []
        self.keywords = ['list', 'table']
        self.bib = {}
        self.textbib = ''
        self.footnote = False
        self.tablefont = 'footnotesize'
        # dirty place holders ....
        self.blockph = 'ABLOCKBLOODYPLACEHOLDER'
        self.latexph = 'ALATEXBLOODYRAWPATTERNPLACEHOLDER'
        self.htmlph = 'AHTMLBLOODYRAWPATTERNPLACEHOLDER'
        self.pause = False
        self.fig_support = ['jpg','pdf','png']
        self.fig_tag = 'tex'

    def m_recode(self, line):
        # the use of ? is very important
        #>>> re.sub(r'@@(.*)@@', r'\\texttt{\1}', line)
        #'\\texttt{aa@@, @@aabb}'
        #>>> re.sub(r'@@(.*?)@@', r'\\texttt{\1}', line)
        #'\\texttt{aa}, \\texttt{aabb}'
        if not line:
            return ''
        line = line.strip()
        raw = []
        # support for raw latex syntax
        pattern = re.compile(r'@@@(.*?)@@@')
        for m in re.finditer(pattern, line):
            line = line.replace(m.group(0), self.latexph + str(len(raw)))
            raw.append(m.group(1))
        # latex keywords
        for item in [('\\', '!!\\backslash!!'),('$', '\$'),('!!\\backslash!!', '$\\backslash$'),
                ('{', '\{'),('}', '\}'),('%', '\%'), ('_', '\-\_'),('|', '$|$'),('&', '\&'),('<', '$<$'),
                ('>', '$>$'),('~', '$\sim$'), ('^', '\^{}'), ('#', '\#')]:
            line = line.replace(item[0], item[1])
        line = re.sub(r'"""(.*?)"""', r'\\textbf{\\textit{\1}}', line)
        line = re.sub(r'""(.*?)""', r'\\textbf{\1}', line)
        line = re.sub(r'"(.*?)"', r'\\textit{\1}', line)
        line = re.sub(r'@@(.*?)@@', r'\\texttt{\1}', line)
        # url
        pattern = re.compile('@(.*?)@')
        for m in re.finditer(pattern, line):
            line = line.replace(m.group(0), '\\url{%s}' % m.group(1).replace('\-\_', '\_').replace('$\sim$', '~'))
        # citation
        # [note|reference] defines the pattern for citation.
        # Will have to use [note$|$reference] here since '|' was previously replaced by $|$
        pattern = re.compile('\[(?P<a>.+?)\$\|\$(?P<b>.+?)\]')
        # re.compile('\[(.+?)\|(.+?)\]')
        for m in re.finditer(pattern, line):
            if not self.footnote:
                k = re.sub('\W', '', m.group('a'))
                if not k:
                    self.quit("Invalid citation keyword for reference item '{}'.".format(m.group('b')))
                if k in self.bib.keys():
                    if self.bib[k] != [m.group('a'), m.group('b')]:
                        k += str(len(self.bib.keys()))
                self.bib[k] = [m.group('a'), m.group('b')]
                #line = line.replace(m.group(0), '\\cite[%s]{%s}' % (m.group('a'), k))
                line = line.replace(m.group(0), '{\\color{MidnightBlue}%s}~\\cite{%s}' % (m.group('a'), k))
            else:
                line = line.replace(m.group(0), '{\\color{MidnightBlue}%s}~\\footnote{%s}' % (m.group('a'), '\\underline{' + m.group('a') + '} ' + m.group('b')))
        # recover raw latex syntax
        for i in range(len(raw)):
            line = line.replace(self.latexph + str(i), raw[i])
        return line

    def _bulkreplace(self, text, start, end, nestedtext):
        end += 1
        if (end - start) > len(nestedtext):
            for i in range(start, end):
                j = i - start
                if j < len(nestedtext):
                    text[i] = nestedtext[j]
                else:
                    text[i] = None
        else:
            self.quit('This is a bug in _bulkreplace() function. Please report it to Gao Wang.')
        return [x for x in text if x is not None]

    def m_parseBlocks(self, text):
        idx = 0
        while True:
            if idx >= len(text):
                break
            if text[idx].startswith(self.mark + '}') and '--' not in text[idx]:
                self.quit("Invalid use of '%s' without previous %s{, near %s" % \
                        (text[idx], self.mark, text[idx+1] if idx + 1 < len(text) else "end of document"))
            if text[idx].startswith(self.mark + '{') and '--' not in text[idx]:
                # define block
                bname = text[idx].split('{')[1].strip()
                if bname not in [x for x in self.keywords]:
                    self.quit("Invalid block definition '%s{ %s'" % (self.mark, bname))
                # find block end
                endidx = None
                text[idx] = ''
                base = 0
                for i in range(idx + 1, len(text)):
                    # nested block identified
                    if text[i].startswith(self.mark + '{'):
                        if '--' in text[i]:
                            self.quit('Invalid use of "%s{----" within block environment, near %') %\
                                (self.mark, self.text[i+1] if i + 1 < len(self.text) else "end of document")
                        base += 1
                    # block end identified
                    if text[i].startswith(self.mark + '}'):
                        if text[i].rstrip() == self.mark + '}':
                            if base == 0:
                                endidx = i
                                break
                            else:
                                base -= 1
                        else:
                            self.quit("Invalid %s '%s', near %s" % \
                                    ('nested use of' if '--' in text[i] else 'symbol', text[i], text[i+1] if idx + 1 < len(text) else "end of document"))
                if not endidx:
                    # end of block not found
                    self.quit("'%s{ %s' and '%s}' must pair properly, near %s" % \
                            (self.mark, bname, self.mark, text[idx+1] if idx + 1 < len(text) else "end of document"))
                if idx + 1 == endidx:
                    # trivial block
                    text.insert(endidx, '\n')
                    endidx += 1
                # block end found, take out this block as new text
                # and apply the recursion
                nestedtext = self.m_parseBlocks(text[idx+1:endidx])
                text = self._bulkreplace(text, idx, endidx, nestedtext)
                newend = idx + len(nestedtext) - 1
                # combine block values
                for i in range(idx + 1, newend + 1):
                    text[idx] += '\n' + text[i]
                del text[(idx + 1) : (newend + 1)]
                # parse the block
                text[idx] = 'BEGIN' + self.blockph + eval(self.PARSER_RULE[bname])(text[idx], bname) + 'END' + self.blockph
            #
            idx += 1
        return text

    def m_parseComments(self):
        for idx, item in enumerate(self.text):
            # define comment
            if self.text[idx].startswith(self.mark + '}') and '--' in self.text[idx]:
                self.quit("Invalid use of '%s}----' without previous '%s{----', near %s" % (self.mark, self.mark, self.text[idx+1] if idx + 1 < len(self.text) else "end of document") )
            if item.startswith(self.mark + '{') and '--' in item:
                endidx = None
                for i in range(idx+1, len(self.text)):
                    if self.text[i].startswith(self.mark + '{') and '--' in self.text[i]:
                        self.quit("Nested use of blocks is disallowed: '{0}', near {1}".format(self.text[i], self.text[i+1] if idx + 1 < len(self.text) else "end of document"))
                    if self.text[i].startswith(self.mark + '}') and '--' in self.text[i]:
                        endidx = i
                        break
                if not endidx:
                    self.quit('Comment blocks must appear in pairs, near {0}'.format(self.text[i+1] if idx + 1 < len(self.text) else "end of document"))
                self.comments.append([idx, endidx])
                self.text[idx] = ''
                self.text[endidx] = ''
        return

    def _holdblockplace(self, text, mode = 'remove', rule = {}):
        # there should be better way to make sure the existing block not to be modified but will use this solution for now
        mapping = {}
        if mode == 'hold':
            text = re.split('({}|{})'.format('BEGIN' + self.blockph, 'END' + self.blockph), text)
            idxes = [0]
            i = 1
            while i < len(text):
                if text[i] == 'BEGIN' + self.blockph:
                    # block identified
                    try:
                        flag = self.blockph not in text[i+1] and text[i+2] == 'END' + self.blockph
                        if not flag: raise ValueError("invalid block flag found")
                    except:
                        self.quit("This is a bug in _holdblockplace() function. Please report it to Gao Wang.")
                    # block checked
                    text[i] = self.blockph + str(i) + 'E'
                    mapping[text[i]] = text[i+1]
                    idxes.append(i)
                    # block skipped
                    i += 3
                else:
                    # no block identified
                    idxes.append(i)
                    i += 1
            text = ''.join([item for idx, item in enumerate(text) if idx in idxes])
        elif mode == 'release':
            mapping = rule
            for k, item in mapping.items():
                text = text.replace(k, item)
        elif mode == 'remove':
            text = re.sub(r'{0}|{1}'.format('BEGIN' + self.blockph, 'END' + self.blockph), '', text)
        return text, mapping

    def _holdfigureplace(self, text):
        pattern = re.compile('#\*(.*?)(\n|$)')
        for m in re.finditer(pattern, text):
            fig = 'BEGIN' + self.blockph + self._parseFigure(m.group(1), self.fig_support, self.fig_tag) + 'END' + self.blockph + '\n'
            text = text.replace(m.group(0), fig, 1)
        return text

    def _parseFigure(self, text, support = ['jpg','pdf','png'], tag = 'tex'):
        if text.startswith(self.mark + '*'):
            text = text[len(self.mark)+1:].strip()
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
            fname = os.path.split(fig)[-1]
            if not '.' in fname:
                self.quit("Cannot determine graphic file format for '{}'. Valid extensions are {}".format(fname, ' '.join(support)))
            if fname.split('.')[-1] not in support:
                self.quit("Input file format '{}' not supported. Valid extensions are {}".format(fname.split('.')[-1], ' '.join(support)))
            if not os.path.exists(fig):
                self.quit("Cannot find file %s" % fig)
            # syntax images
            if tag == 'tex':
                lines[idx] = '\\includegraphics[width=%s\\textwidth]{%s}\n' % (width, os.path.abspath(fig))
            else:
                lines[idx] = '<p><center><img src="{}" alt="{}" width="{}" /></center></p>'.format(fig, os.path.split(fig)[-1], int(width * 800))
        if tag == 'tex':
            if len(lines) > 1:
                w_minipage = int(1.0 / (1.0 * len(lines)) * 90) / 100.0
                lines = ['\\subfigure{' + x + '}\n' for x in lines]
                lines[0] = '\\begin{figure}[H]\n\\centering\n\\mbox{\n' + lines[0]
                lines[-1] += '\n}\n\\end{figure}\n'
            else:
                lines[0] = '\\begin{figure}[H]\n\\centering\n' + lines[0]
                lines[-1] += '\\end{figure}\n'
        return '\n'.join(lines)

    def _checknest(self, text, kw=None):
        pattern = re.compile('{}(.*?){}'.format('BEGIN' + self.blockph, 'END' + self.blockph), re.DOTALL)
        # re.match() will not work here
        # will not work without re.DOTALL
        for m in re.finditer(pattern, text):
            if m:
                e = m.group(1)
                if kw is None:
                    self.quit('Cannot nest this blocks here:\n{0}'.format(e[:max(200, len(e))]))
                else:
                    for k in kw:
                        if re.search(k, '%r' % e):
                            self.quit('Cannot nest this blocks here:\n{0}'.format(e[:max(200, len(e))]))
        return

    def _checkblockprefix(self, text):
        for item in text.split('\n'):
            if item.strip() and (not (item.startswith(self.blockph) or item.startswith(self.mark))):
                self.quit('Items must start with "{0}" in this block. Problematic text is: "{1}"'.format(self.mark, item))
        return

    def m_blockizeList(self, text, k):
        # handle 2nd level indentation first
        # in the mean time take care of recoding
        text = self._holdfigureplace(text)
        text, mapping = self._holdblockplace(text, mode = 'hold')
        self._checkblockprefix(text)
        text = text.split('\n')
        idx = 0
        while idx < len(text):
            if text[idx].startswith(self.blockph):
                idx += 1
                continue
            if text[idx].startswith(self.mark * 2):
                start = idx
                end = idx
                text[idx] = self.mark * 2 + self.m_recode(text[idx][2:])
                text[idx] = re.sub(r'^{0}'.format(self.mark * 2), '\\item ', text[idx])
                if idx + 1 < len(text):
                    for j in range(idx + 1, len(text) + 1):
                        try:
                            if not text[j].startswith(self.mark * 2):
                                break
                            else:
                                text[j] = self.mark * 2 + self.m_recode(text[j][2:])
                                text[j] = re.sub(r'^{0}'.format(self.mark * 2), '\\item ', text[j])
                                end = j
                        except IndexError:
                            pass
                #
                text[start] = '\\begin{itemize}\n' + text[start]
                text[end] = text[end] + '\n\\end{itemize}'
                idx = end + 1
            elif text[idx].startswith(self.mark):
                text[idx] = self.mark + self.m_recode(text[idx][1:])
                idx += 1
            else:
                text[idx] = self.m_recode(text[idx])
                idx += 1
        # handle 1st level indentation
        text = '\n'.join([x if x.startswith(self.blockph) else re.sub(r'^{0}'.format(self.mark), '\\item ', x) for x in text])
        text = self._holdblockplace(text, mode = 'release', rule = mapping)[0]
        text = '\\begin{itemize}\n%s\n\\end{itemize}\n' % text
        # this is for beamer \pause option
        if self.pause:
            text = text.replace('\\item -', '\\pause \\item ')
        return text

    def m_blockizeTable(self, text, k):
        self._checknest(text)
        table = [[self.m_recode(iitem) for iitem in item.split('\t')] for item in text.split('\n') if item]
        ncols = list(set([len(x) for x in table]))
        if len(ncols) > 1:
            self.quit("Number of columns not consistent for table. Please replace empty columns with placeholder symbol, e.g. '-'. {}".format(text))
        try:
            cols = 'c' * ncols[0]
            head = '\\begin{center}\n{\\%s\\begin{longtable}{%s}\n\\hline\n' % (self.tablefont, cols)
            body = '&'.join(table[0]) + '\\\\\n' + '\\hline\n' + '\\\\\n'.join(['&'.join(item) for item in table[1:]]) + '\\\\\n'
            tail = '\\hline\n\\end{longtable}}\n\\end{center}\n'
        except IndexError:
            return ''
        return head + body + tail

    def m_parseBib(self):
        if not self.bib:
            return
        self.textbib = '\\begin{thebibliography}{9}\n'
        bibkeys = []
        #unique, ordered reference list
        for line in self.text:
            bibkeys.extend([m.group(1) for m in re.finditer(re.compile('\\cite{(.*?)}'), line)])
        seen = set()
        for k in [x for x in bibkeys if x not in seen and not seen.add(x)]:
            self.textbib += '\\bibitem{%s}\n[%s]\\\\%s\n' % (k, self.bib[k][0], self.bib[k][1])
        self.textbib += '\\end{thebibliography}'

    def get(self, include_comment):
        return 'None'

    def quit(self, msg):
        sys.exit('\033[91mAn ERROR has occured while processing input text "{}":\033[0m\n\t '.format(self.fn) + msg)

# derived classes
class LogToTex(TexParser):
    def __init__(self, title, author, toc, footnote, filename, no_num = False, no_ref = False):
        TexParser.__init__(self, title, author, filename)
        if sum([x.split('.')[-1].lower() in ['c','cpp','h'] for x in filename]) == len(filename):
            self.mark = '//'
        self.ftype = []
        self.text = []
        for fn in filename:
            try:
                self.ftype.append(fn.split('.')[-1].lower())
                with codecs.open(fn, 'r', encoding='UTF-8', errors='ignore') as f:
                    lines = [l.rstrip() for l in f.readlines() if l.rstrip()]
                if fn.split('.')[-1].lower() in ['r','sh','py','c','cpp','h']:
                    sys.stderr.write("WARNING: Treating input as {0} source code. Please use a different filename extension if this is not your intension.\n".format(SYNTAX[fn.split('.')[-1].lower()]))
                    if lines[0].startswith('#!/') and fn.split('.')[-1].lower() in lines[0].lower():
                        del lines[0]
#                    lines.insert(0,self.mark*3)
#                    lines.insert(0,self.mark + fn.upper())
#                    lines.insert(0,self.mark*3)
                self.text.extend(lines)
            except IOError as e:
                sys.exit(e)
        self.toc = toc
        self.doctype = 'article'
        self.footnote = footnote
        self.no_num = no_num
        self.bclogo = {'warning':'\\bcattention', 'tip':'\\bclampe', 'important':'\\bctakecare', 'note':'\\bccrayon'}
        self.keywords = list(set(SYNTAX.values())) + self.bclogo.keys() + ['out', 'list', 'table']
        self.text = self.m_parseBlocks(self.text)
        self.m_parseComments()
        self.m_parseText()
        if not no_ref:
            self.m_parseBib()
            self.text.append(self.textbib)

    def m_blockizeIn(self, text, k):
        self._checknest(text)
        return '\\begin{minted}[samepage=false, fontfamily=tt,\nfontsize=\\scriptsize, xleftmargin=1pt,\nframe=lines, framerule=1pt, framesep=2mm,\nlabel=\\fbox{%s}]{%s}\n%s\n\\end{minted}\n' % (k.upper(), k, wraptxt(text, '\\' if k == 'bash' else '', 131))

    def m_blockizeOut(self, text, k):
        self._checknest(text)
        return '\\begin{Verbatim}[samepage=false, fontfamily=tt,\nfontsize=\\footnotesize, formatcom=\\color{rgray},\nframe=lines, framerule=1pt, framesep=2mm,\nlabel=\\fbox{\\scriptsize OUTPUT}, labelposition=topline]\n%s\n\\end{Verbatim}\n' % wraptxt(text, '', 116)

    def m_blockizeAlert(self, text, k):
        self._checknest(text, kw = [r'\\\\begin{bclogo}', r'\\\\end{bclogo}'])
        text = self._holdfigureplace(text)
        text, mapping = self._holdblockplace(text, mode = 'hold')
        self._checkblockprefix(text)
        text = '\n'.join([item if item.startswith(self.blockph) else self.m_recode(re.sub(r'^{0}'.format(self.mark), '', item)) for item in text.split('\n')])
        text = self._holdblockplace(text, mode = 'release', rule = mapping)[0]
        return '\\begin{bclogo}[logo=%s, couleurBarre=MidnightBlue, noborder=true, couleur=white]{~%s}%s\n\\end{bclogo}\n' % (self.bclogo[k], k.capitalize(), text)

    def m_parseText(self):
        skip = []
        for idx, item in enumerate(self.text):
            if self.blockph in item:
                self.text[idx] = self._holdblockplace(item, mode = 'remove')[0]
                skip.append(idx)
        idx = 0
        while idx < len(self.text):
            if idx in skip or self.text[idx] == '':
                # no need to process
                idx += 1
                continue
            if list(set(self.ftype)) == ['txt'] and not self.text[idx].startswith(self.mark):
                self.text[idx] = self.mark + self.text[idx]
            if not self.text[idx].startswith(self.mark):
                # regular cmd text, or with syntax
                if idx + 1 < len(self.text):
                    for i in range(idx + 1, len(self.text) + 1):
                        try:
                            if self.text[i].startswith(self.mark) or i in skip or self.text[i] == '':
                                break
                        except IndexError:
                            pass
                else:
                    i = idx + 1
                lan = list(set(self.ftype))
                sep = '\\'
                cnt = 114
                sminted = '\\mint[bgcolor=bg, fontsize=\\footnotesize]{text}?'
                lminted = '\\begin{minted}[bgcolor=bg, fontsize=\\footnotesize]{text}\n'
                #
                if (len(lan) == 1 and lan[0] in ['r','sh','py']) or self.mark == '//':
                    if lan[0] == 'h': lan[0] = 'cpp'
                    sep = '' if not lan[0] == 'sh' else '\\'
                    cnt = 131
                    sminted = '\\mint[fontfamily=tt,\nfontsize=\\scriptsize, xleftmargin=1pt,\nframe=lines, framerule=0.5pt, framesep=2mm]{%s}?' % (SYNTAX[lan[0]])
                    lminted =  '\\begin{minted}[samepage=false, fontfamily=tt,\nfontsize=\\scriptsize, xleftmargin=1pt,\nframe=lines, framerule=0.5pt, framesep=2mm]{%s}\n' % (SYNTAX[lan[0]])
                #
                cmd = '\n'.join([wraptxt(x, sep, cnt) for x in self.text[idx:i]])
                cmd = cmd.split('\n')
                if len(cmd) == 1:
                    self.text[idx] = sminted + cmd[0] + '?'
                else:
                    self.text[idx] = lminted + '\n'.join(cmd) + '\n\\end{minted}'
                    for j in range(idx + 1, i):
                        self.text[j] = ''
                idx = i
                continue
            if self.text[idx].startswith(self.mark * 3) and self.text[idx+1].startswith(self.mark + '!') and self.text[idx+2].startswith(self.mark * 3):
                # chapter
                self.doctype = 'report'
                self.text[idx] = ''
                self.text[idx + 1] = '\\chapter{' + ' '.join([x[0].upper() + (x[1:] if len(x) > 1 else '') for x in self.m_recode(self.text[idx + 1][len(self.mark)+1:]).split()]) + '}'
                self.text[idx + 2] = ''
                idx += 3
                continue
            if self.text[idx].startswith(self.mark * 3) and self.text[idx+1].startswith(self.mark) and (not self.text[idx+1].startswith(self.mark * 2)) and self.text[idx+2].startswith(self.mark * 3):
                # section
                self.text[idx] = ''
                self.text[idx + 1] = ('\\section*{' if self.no_num else '\\section{') + \
                        ' '.join([x[0].upper() + (x[1:] if len(x) > 1 else '') for x in self.m_recode(self.text[idx + 1][len(self.mark):]).split()]) + '}'
                self.text[idx + 2] = ''
                idx += 3
                continue
            if self.text[idx].startswith(self.mark * 2):
                # too many #'s
                self.quit("You have so many urgly '{0}' symbols in a regular line. Please clear them up in this line: '{1}'".format(self.mark, self.text[idx]))
            if self.text[idx].startswith(self.mark + '!!!'):
                # box
                #self.text[idx] = '\\shabox{' + self.m_recode(self.text[idx][len(self.mark)+3:]) + '}'
                self.text[idx] = '\\colorbox{yellow}{\\begin{varwidth}{\\dimexpr\\linewidth-2\\fboxsep}{\\color{red}\\textbf{' + self.m_recode(self.text[idx][len(self.mark)+3:]) + '}}\\end{varwidth}}\n'
                idx += 1
                continue
            if self.text[idx].startswith(self.mark + '!!'):
                # subsection, subsubsection ...
                self.text[idx] = '\\subsubsection{' + self.m_recode(self.text[idx][len(self.mark)+2:]) + '}'
                idx += 1
                continue
            if self.text[idx].startswith(self.mark + '!'):
                # subsection, subsubsection ...
                self.text[idx] = ('\\subsection*{' if self.no_num else '\\subsection{') + self.m_recode(self.text[idx][len(self.mark)+1:]) + '}'
                idx += 1
                continue
            if self.text[idx].startswith(self.mark + '*'):
                # fig: figure.pdf 0.9
                self.text[idx] = self._parseFigure(self.text[idx], self.fig_support, self.fig_tag)
                idx += 1
                continue
            if self.text[idx].startswith(self.mark):
                # a plain line here
                self.text[idx] = '\n' + self.m_recode(self.text[idx][len(self.mark):]) + '\n'
                idx += 1
                continue
        return

    def get(self, include_comment):
        if include_comment and len(self.comments) > 0:
            for idx in range(len(self.text)):
                for item in self.comments:
                    if idx in range(item[0], item[1]):
                        self.text[idx] = ''
                        break
        self.text = filter(None, self.text)
        return ('\\documentclass[oneside, 10pt]{%s}' % self.doctype + DOC_PACKAGES) + \
                ('\\usepackage[Lenny]{fncychap}' if self.doctype == 'report' else '') + \
                ('\\renewcommand\\%s{References}' % 'bibname' if self.doctype == 'report' else 'refname') + \
                DOC_CONFIG + '\\title{%s}\n' % self.title + '\\author{%s}\n' % self.author + \
                '\\date{Last updated: \\today}\n\\raggedbottom\n\\begin{document}\n' + \
                '%s\n%s\n\\bigskip\n%s' % ('\\maketitle' if self.title or self.author else '', '\\tableofcontents' if self.toc else '', '\n'.join(self.text)) + \
                '\n\\end{document}'


class LogToBeamer(TexParser):
    def __init__(self, title, author, institute, toc, mode, theme, thank, filename):
        TexParser.__init__(self, title, author, filename)
        self.text = []
        for fn in filename:
            try:
                with codecs.open(fn, 'r', encoding='UTF-8', errors='ignore') as f:
                    #lines = [l.rstrip() for l in f.readlines() if l.rstrip()]
                    lines = [l.rstrip() for l in f.readlines()]
                self.text.extend(lines)
            except IOError as e:
                sys.exit(e)
        self.institute = institute
        self.toc = toc
        self.mode = mode
        self.theme = theme
        self.wrap_adjust = 1
        if self.mode == 'notes':
            self.wrap_adjust = 1.38
        else:
            if self.theme == 'heavy':
                self.wrap_adjust = 0.92
        self.thank = thank
        self.alertbox = ['warning', 'tip', 'important', 'note']
        self.keywords = list(set(SYNTAX.values())) + self.alertbox + ['err', 'out', 'list', 'table']
        self.pause = True
        self.tablefont = 'tiny'
        self.text = self.m_parseBlocks(self.text)
        self.m_parseComments()
        self.m_parseText()
        self.m_parseBib()
        if self.thank:
            self.text.append(THANK)
        if self.textbib:
            self.text.append('\\appendix\n\\begin{frame}[allowframebreaks]\n\\tiny\n' + \
                self.textbib + '\n\\end{frame}')

    def m_blockizeIn(self, text, k):
        self._checknest(text)
        return '\\begin{exampleblock}{\\texttt{%s}}\\scriptsize\n\\begin{Verbatim}\n%s\n\\end{Verbatim}\n\\end{exampleblock}\n' % \
                        (k.capitalize(), wraptxt(text, '', int(78 * self.wrap_adjust), rmblank = False))

    def m_blockizeOut(self, text, k):
        self._checknest(text)
        return '\\begin{exampleblock}{}\\tiny\n\\begin{Verbatim}\n%s\n\\end{Verbatim}\n\\end{exampleblock}\n' % \
                    wraptxt(text, '', int(105 * self.wrap_adjust), rmblank = False)

    def m_blockizeAlert(self, text, k):
        self._checknest(text, kw = [r'\\\\begin{(.*?)block}', r'\\\\end{(.*?)block}'])
        text = self._holdfigureplace(text)
        text, mapping = self._holdblockplace(text, mode = 'hold')
        self._checkblockprefix(text)
        text = '\n'.join([item if item.startswith(self.blockph) else self.m_recode(re.sub(r'^{0}'.format(self.mark), '', item)) for item in text.split('\n')])
        text = self._holdblockplace(text, mode = 'release', rule = mapping)[0]
        return '\\begin{{{0}block}}{{{1}}}\n{2}\n\\end{{{0}block}}\n'.\
                        format('alert' if k in ['important', 'warning'] else '', k.capitalize(), text)

    def m_parseText(self):
        skip = []
        for idx, item in enumerate(self.text):
            if self.blockph in item:
                self.text[idx] = self._holdblockplace(item, mode = 'remove')[0]
                skip.append(idx)
        idx = 0
        framestart = 0
        frameend = 0
        while idx < len(self.text):
            if idx in skip or self.text[idx] == '':
                # no need to process
                idx += 1
                continue
            if not self.text[idx].startswith(self.mark):
                # regular cmd text, or with syntax
                if idx + 1 < len(self.text):
                    for i in range(idx + 1, len(self.text) + 1):
                        try:
                            if self.text[i].startswith(self.mark) or i in skip or self.text[i] == '':
                                break
                        except IndexError:
                            pass
                else:
                    i = idx + 1
                sep = ''
                cnt = int(62 * self.wrap_adjust)
                sminted = '\\Verb?'
                lminted = '\\begin{Verbatim}[fontsize=\\footnotesize]\n'
                #
                cmd = '\n'.join([wraptxt(x, sep, cnt) for x in self.text[idx:i]])
                cmd = cmd.split('\n')
                if len(cmd) == 1:
                    self.text[idx] = sminted + cmd[0] + '?'
                else:
                    self.text[idx] = lminted + '\n'.join(cmd) + '\n\\end{Verbatim}'
                    for j in range(idx + 1, i):
                        self.text[j] = ''
                idx = i
                continue
            if self.text[idx].startswith(self.mark * 3) and self.text[idx+1].startswith(self.mark + '!') and self.text[idx+2].startswith(self.mark * 3):
                # section
                prefix = '\\section{'
                if framestart > frameend:
                    prefix = '\\end{frame}\n\n' + prefix
                    frameend += 1
                self.text[idx] = ''
                self.text[idx + 1] = prefix + ' '.join([x[0].upper() + (x[1:] if len(x) > 1 else '') for x in self.m_recode(self.text[idx + 1][len(self.mark)+1:]).split()]) + '}'
                self.text[idx + 2] = ''
                idx += 3
                continue
            if self.text[idx].startswith(self.mark * 3) and self.text[idx+1].startswith(self.mark) and (not self.text[idx+1].startswith(self.mark * 2)) and self.text[idx+2].startswith(self.mark * 3):
                # sub-section
                prefix = '\\subsection{'
                if framestart > frameend:
                    prefix = '\\end{frame}\n\n' + prefix
                    frameend += 1
                self.text[idx] = ''
                self.text[idx + 1] = prefix + ' '.join([x[0].upper() + (x[1:] if len(x) > 1 else '') for x in self.m_recode(self.text[idx + 1][len(self.mark):]).split()]) + '}'
                self.text[idx + 2] = ''
                idx += 3
                continue
            if self.text[idx].startswith(self.mark * 2):
                # too many #'s
                self.quit("You have so many urgly '{0}' symbols in a regular line. Please clear them up in this line: '{1}'".format(self.mark, self.text[idx]))
            if self.text[idx].startswith(self.mark + '!!!'):
                # box
                self.text[idx] = '\\colorbox{yellow}{\\textcolor{red}{\\textbf{' + self.m_recode(self.text[idx][len(self.mark)+3:]) + '}}}'
                idx += 1
                continue
            if self.text[idx].startswith(self.mark + '!!'):
                # framesubtitle ...
                hastitle = False
                try:
                    hastitle = 'frametitle' in self.text[idx-1]
                except Exception as e:
                    pass
                if not hastitle:
                    self.quit("'{0}!!' has to be preceded by a line starting with '{0}!', near '{1}'".format(self.mark, self.text[idx]))
                self.text[idx] = '\\framesubtitle{' + self.m_recode(self.text[idx][len(self.mark)+2:]) + '}'
                idx += 1
                continue
            if self.text[idx].startswith(self.mark + '!'):
                # frame
                prefix = '\\begin{frame}[fragile, shrink]\n\\frametitle{'
                if framestart > frameend:
                    prefix = '\\end{frame}\n\n' + prefix
                    frameend += 1
                framestart += 1
                self.text[idx] = prefix + self.m_recode(self.text[idx][len(self.mark)+1:]) + '}'
                idx += 1
                continue
            if self.text[idx].startswith(self.mark + '*'):
                # fig: figure.pdf 0.9
                self.text[idx] = self._parseFigure(self.text[idx], self.fig_support, self.fig_tag)
                idx += 1
                continue
            if self.text[idx].startswith(self.mark):
                # a plain line here
                self.text[idx] = '\n' + self.m_recode(self.text[idx][len(self.mark):]) + '\n'
                idx += 1
                continue
        if framestart > frameend:
            self.text.append('\\end{frame}\n')
        self.m_checkEmptySlides(self.text)
        return

    def m_stitle(self, length):
        stitle = self.title
        # length ok
        if len(stitle.replace('\\text', '')) < length:
            return stitle
        # have to chop
        if '\\' in self.title:
            stitle = self.title[:self.title.index('\\')]
        return stitle[:min(length, len(stitle))] + '...'

    def m_checkEmptySlides(self, ltext):
        text = ''.join(ltext)
        pattern = re.compile(r'\\\\begin{frame}\[fragile, shrink\](.*?)\\\\end{frame}')
        for m in re.finditer(pattern, '%r' % text):
            frame = m.group(1)
            frametitle = re.search(r'\\\\frametitle{(.*?)}', frame).group(1).encode().decode('unicode_escape')
            frame = re.sub(r'\\\\frametitle{(.*?)}', '', frame)
            frame = re.sub(r'\\\\framesubtitle{(.*?)}', '', frame)
            if len(re.sub(r'\s', '', frame.encode().decode('unicode_escape'))) == 0:
                self.quit("Empty slides not allowed, near '{}'".format(frametitle))
        return

    def get(self, include_comment):
        titlepage = '\\frame{\\titlepage}\n' if not self.mode == 'notes' else '\\maketitle\n'
        tocpage = '\\begin{frame}[allowframebreaks]\n\\frametitle{Outline}\n\\tableofcontents[hideallsubsections]\n\\end{frame}\n' if not self.mode == 'notes' else '\\tableofcontents\n'
        sectiontoc = '\\AtBeginSection[]\n{\n\\begin{frame}<beamer>\n\\frametitle{$\clubsuit$}\n\\tableofcontents[currentsection, currentsubsection, sectionstyle=show/hide, subsectionstyle=show/show/hide]\n\\end{frame}\n}\n'
        if include_comment and len(self.comments) > 0:
            for idx in range(len(self.text)):
                for item in self.comments:
                    if idx in range(item[0], item[1]):
                        self.text[idx] = ''
                        break
        self.text = filter(None, self.text)
        otext = '{}'.format(MODE[self.mode]) + \
                CONFIG + '{}'.format(THEME[self.theme.lower()]) + TITLE
        if self.title or self.author:
            otext += '\n\\title[%s]{%s}\n%% \\subtitle\n\\author{%s}\n' % \
                (self.m_stitle(30), self.title, self.author)
        if self.institute:
            otext += '\\institute[%s]{%s}\n' % (self.institute, self.institute)
        otext += '\\date{\\today}\n%s\\begin{document}\n%s\n%s' % (
                sectiontoc if self.toc else '',
                titlepage if self.title or self.author else '',
                tocpage if self.toc else ''
                )
        otext += '\n'.join(self.text) + '\n\\end{document}'
        return otext


class LogToHtml(TexParser):
    def __init__(self, title, author, toc, filename):
        TexParser.__init__(self, title, author, filename)
        self.text = []
        for fn in filename:
            try:
                with codecs.open(fn, 'r', encoding='UTF-8', errors='ignore') as f:
                    #lines = [l.rstrip() for l in f.readlines() if l.rstrip()]
                    lines = [l.rstrip() for l in f.readlines()]
                self.text.extend(lines)
            except IOError as e:
                sys.exit(e)
        self.toc = toc
        self.dtoc = OrderedDict()
        self.alertbox = ['warning', 'tip', 'important', 'note']
        self.keywords = list(set(SYNTAX.values())) + self.alertbox + ['err', 'out', 'list', 'table']
        self.wrap_width = 90
        self.tablefont = 'small'
        self.anchor_id = 0
        self.fig_support = ['jpg','tif','png']
        self.fig_tag = 'html'
        self.text = self.m_parseBlocks(self.text)
        self.m_parseComments()
        self.m_parseText()
        self.m_parseBib()
        self.text.append(self.textbib)

    def _parseUrlPrefix(self, text):
        prefix = re.search(r'^(.+?)://', text)
        if prefix:
            return prefix.group(0), text.replace(prefix.group(0), '')
        else:
            return '', text

    def m_recode(self, line):
        if not line:
            return ''
        line = line.strip()
        raw = []
        # support for raw html syntax/symbols
        pattern = re.compile(r'@@@(.*?)@@@')
        for m in re.finditer(pattern, line):
            line = line.replace(m.group(0), self.htmlph + str(len(raw)))
            raw.append(m.group(1))
        # html keywords
        # no need to convert most of them
        for item in [
#                ('\\', '&#92;'),('$', '&#36;'),
#                ('{', '&#123;'),('}', '&#125;'),
#                ('%', '&#37;'),('--', '&mdash;'),
#                ('-', '&ndash;'),('&', '&amp;'),
#                ('~', '&tilde;'),('^', '&circ;'),
#                ('``', '&ldquo;'),('`', '&lsquo;'),
#                ('#', '&#35;'),
                ('<', '&lt;'),('>', '&gt;'),
                ]:
            line = line.replace(item[0], item[1])
        line = re.sub(r'"""(.*?)"""', r'<strong><em>\1</em></strong>', line)
        line = re.sub(r'""(.*?)""', r'<strong>\1</strong>', line)
        line = re.sub(r'"(.*?)"', r'<em>\1</em>', line)
#        line = re.sub(r'@@(.*?)@@', r'<span style="font-family: monospace">\1</span>', line)
        line = re.sub(r'@@(.*?)@@', r'<kbd>\1</kbd>', line)
        # hyperlink
        # [text|@link@] defines the pattern for citation.
        pattern = re.compile('\[(\s*)(?P<a>.+?)(\s*)\|(\s*)@(?P<b>.+?)@(\s*)\]')
        for m in re.finditer(pattern, line):
            prefix, address = self._parseUrlPrefix(m.group('b'))
            line = line.replace(m.group(0), '<a style="text-shadow: 1px 1px 1px #999;" href="{0}{1}">{2}</a>'.format(prefix, address, m.group('a')))
        # url
        pattern = re.compile('@(.*?)@')
        for m in re.finditer(pattern, line):
            prefix, address = self._parseUrlPrefix(m.group(1))
            line = line.replace(m.group(0), '<a href="{0}{1}">{1}</a>'.format(prefix, address, address))
        # footnote
        # [note|reference] defines the pattern for citation.
        pattern = re.compile('\[(\s*)(?P<a>.+?)(\s*)\|(\s*)(?P<b>.+?)(\s*)\]')
        # re.compile('\[(.+?)\|(.+?)\]')
        for m in re.finditer(pattern, line):
            k = re.sub('\W', '', m.group('a'))
            if not k:
                self.quit("Invalid citation keyword for reference item '{}'.".format(m.group('b')))
            if k in self.bib.keys():
                if self.bib[k] != [m.group('a'), m.group('b')]:
                    k += str(len(self.bib.keys()))
            self.bib[k] = [m.group('a'), m.group('b')]
            line = line.replace(m.group(0), '<a href="#footnote-{}">{}</a>'.format(k, m.group('a')))
        # more kw
        line = line.replace("''", '"')
        line = line.replace("``", '"')
        line = line.replace("`", "'")
        # recover raw html syntax
        for i in range(len(raw)):
            line = line.replace(self.htmlph + str(i), raw[i])
        return line.strip()

    def m_blockizeList(self, text, k):
        # handle 2nd level indentation first
        # in the mean time take care of recoding
        text = self._holdfigureplace(text)
        text, mapping = self._holdblockplace(text, mode = 'hold')
        self._checkblockprefix(text)
        text = text.split('\n')
        idx = 0
        while idx < len(text):
            if text[idx].startswith(self.blockph):
                idx += 1
                continue
            if text[idx].startswith(self.mark * 2):
                start = idx
                end = idx
                text[idx] = self.mark * 2 + self.m_recode(text[idx][2:])
                text[idx] = re.sub(r'^{0}'.format(self.mark * 2), '<li>', text[idx]) + '</li>'
                if idx + 1 < len(text):
                    for j in range(idx + 1, len(text) + 1):
                        try:
                            if not text[j].startswith(self.mark * 2):
                                break
                            else:
                                text[j] = self.mark * 2 + self.m_recode(text[j][2:])
                                text[j] = re.sub(r'^{0}'.format(self.mark * 2), '<li>', text[j]) + '</li>'
                                end = j
                        except IndexError:
                            pass
                #
                text[start] = '<ol>\n' + text[start]
                text[end] = text[end] + '\n</ol>'
                idx = end + 1
            elif text[idx].startswith(self.mark):
                text[idx] = self.mark + self.m_recode(text[idx][1:])
                idx += 1
            else:
                text[idx] = self.m_recode(text[idx])
                idx += 1
        # handle 1st level indentation
        text = '\n'.join([x if x.startswith(self.blockph) else  re.sub(r'^{0}'.format(self.mark), '<li>', x + '</li>') for x in text])
        text = self._holdblockplace(text, mode = 'release', rule = mapping)[0]
        return '<ul>\n%s\n</ul>\n' % text

    def m_blockizeTable(self, text, k):
        self._checknest(text)
        table = [[self.m_recode(iitem) for iitem in item.split('\t')] for item in text.split('\n') if item]
        ncols = list(set([len(x) for x in table]))
        if len(ncols) > 1:
            self.quit("Number of columns not consistent for table. Please replace empty columns with placeholder symbol, e.g. '-'. {}".format(text))
        start = '<td style="vertical-align: top;"><{}>'.format(self.tablefont)
        end = '<br /></{}></td>'.format(self.tablefont)
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
        return head + '\n'.join(body) + tail

    def _parsecmd(self, text, serial, numbered = False):
        head = '<div><div id="highlighter_{}" class="syntaxhighlighter bash"><table border="0" cellpadding="0" cellspacing="0"><tbody><tr><td class="gutter">'.format(serial)
        numbers = ''.join(['<div class="line number{0} index{1} alt{2}">{0}</div>'.format(j+1 if numbered else ' ', j, 2 - j % 2) for j in range(len(text))]) + '</td><td class="code"><div class="container">'
        lines = ''.join(['<div class="line number{0} index{1} alt{2}"><code class="bash plain">{3}</code></div>'.format(j+1, j, 2 - j % 2, line) for j, line in enumerate(text)])
        tail = '</div></td></tr></tbody></table></div></div>'
        return head + numbers + lines + tail

    def m_blockizeIn(self, text, k):
        self._checknest(text)
        self.anchor_id += 1
        return '<div style="color:rgb(220, 20, 60);font-weight:bold;text-align:right;padding-right:2em;"><span class="textborder">' + \
                        k.capitalize() + '</span></div>' + \
                        self._parsecmd(wraptxt(text, '', int(self.wrap_width), rmblank = True).split('\n'), str(self.anchor_id), numbered = True)

    def m_blockizeOut(self, text, k):
        self._checknest(text)
        nrow = len(text.split('\n'))
        return '<center><textarea rows="{}", wrap="off">{}</textarea></center>'.format(max(min(nrow, 30), 1), text)

    def m_blockizeAlert(self, text, k):
        self._checknest(text, kw = [r'id="wrapper"'])
        text = self._holdfigureplace(text)
        text, mapping = self._holdblockplace(text, mode = 'hold')
        self._checkblockprefix(text)
        text = '\n'.join([item if item.startswith(self.blockph) else self.m_recode(re.sub(r'^{0}'.format(self.mark), '', item)) for item in text.split('\n')])
        text = self._holdblockplace(text, mode = 'release', rule = mapping)[0]
        return '<center><div id="wrapper"><div class="{0}"><div style="font-family:comic sans ms;text-align:center;text-decoration:underline{3}; margin-bottom:3px">{1}</div>{2}</div></div></center>'.\
                        format(k.lower(), k.capitalize(), text, ';color:red' if k.lower() == 'warning' else '')

    def m_parseText(self):
        skip = []
        for idx, item in enumerate(self.text):
            if self.blockph in item:
                self.text[idx] = self._holdblockplace(item, mode = 'remove')[0]
                skip.append(idx)
        idx = 0
        cnt_chapter = cnt_section = cnt_subsection = 0
        while idx < len(self.text):
            if idx in skip or self.text[idx] == '':
                # no need to process
                idx += 1
                continue
            if not self.text[idx].startswith(self.mark):
                # regular cmd text, or with syntax
                if idx + 1 < len(self.text):
                    for i in range(idx + 1, len(self.text) + 1):
                        try:
                            if self.text[i].startswith(self.mark) or i in skip or self.text[i] == '':
                                break
                        except IndexError:
                            pass
                else:
                    i = idx + 1
                #
                cmd = '\n'.join([wraptxt(x, '\\', int(self.wrap_width)) for x in self.text[idx:i]])
                cmd = cmd.split('\n')
                if len(cmd) == 1:
                    self.text[idx] = self._parsecmd(cmd, idx)
                else:
                    self.text[idx] = self._parsecmd(cmd, idx)
                    for j in range(idx + 1, i):
                        self.text[j] = ''
                idx = i
                continue
            if self.text[idx].startswith(self.mark * 3) and self.text[idx+1].startswith(self.mark + '!') and self.text[idx+2].startswith(self.mark * 3):
                # chapter
                chapter = ' '.join([x[0].upper() + (x[1:] if len(x) > 1 else '') for x in self.m_recode(self.text[idx + 1][len(self.mark)+1:]).split()])
                cnt_chapter += 1
                self.dtoc['chapter_{}'.format(cnt_chapter)] = chapter
                self.text[idx] = ''
                self.text[idx + 1] = self.m_chapter(chapter, cnt_chapter)
                self.text[idx + 2] = ''
                idx += 3
                continue
            if self.text[idx].startswith(self.mark * 3) and self.text[idx+1].startswith(self.mark) and (not self.text[idx+1].startswith(self.mark * 2)) and self.text[idx+2].startswith(self.mark * 3):
                # section
                section = ' '.join([x[0].upper() + (x[1:] if len(x) > 1 else '') for x in self.m_recode(self.text[idx + 1][len(self.mark):]).split()])
                cnt_section += 1
                self.dtoc['section_{}'.format(cnt_section)] = section
                self.text[idx] = ''
                self.text[idx + 1] = self.m_section(section, cnt_section)
                self.text[idx + 2] = ''
                idx += 3
                continue
            if self.text[idx].startswith(self.mark * 2):
                # too many #'s
                self.quit("You have so many urgly '{0}' symbols in a regular line. Please clear them up in this line: '{1}'".format(self.mark, self.text[idx]))
            if self.text[idx].startswith(self.mark + '!!!'):
                # box
                self.text[idx] = '<span style="color:red;background:yellow;font-weight:bold">' + self.m_recode(self.text[idx][len(self.mark)+3:]) + '</span>'
                idx += 1
                continue
            if self.text[idx].startswith(self.mark + '!!'):
                # subsection, subsubsection ...
                self.text[idx] = self.m_sssection(
                        self.m_recode(self.text[idx][len(self.mark)+2:])
                        )
                idx += 1
                continue
            if self.text[idx].startswith(self.mark + '!'):
                # subsection, subsubsection ...
                subsection = self.m_recode(self.text[idx][len(self.mark)+1:])
                cnt_subsection += 1
                self.dtoc['subsection_{}'.format(cnt_subsection)] = subsection
                self.text[idx] = self.m_ssection(subsection, cnt_subsection)
                idx += 1
                continue
            if self.text[idx].startswith(self.mark + '*'):
                # fig: figure.png 0.9
                self.text[idx] = self._parseFigure(self.text[idx], self.fig_support, self.fig_tag)
                idx += 1
                continue
            if self.text[idx].startswith(self.mark):
                # a plain line here
                self.text[idx] = '\n<p>' + self.m_recode(self.text[idx][len(self.mark):]) + '</p>\n'
                idx += 1
                continue
        return

    def m_parseBib(self):
        if not self.bib:
            return
        bibkeys = []
        self.textbib = '<hr style="border: 3px double #555;margin-top:2em;margin-bottom:1em;">'
        #unique, ordered reference list
        for line in self.text:
            bibkeys.extend([m.group(1) for m in re.finditer(re.compile('"#footnote-(.*?)"'), line)])
        seen = set()
        for k in [x for x in bibkeys if x not in seen and not seen.add(x)]:
            self.textbib += '<p id="footnote-{}">[{}]: {}</p>\n'.format(k, self.bib[k][0], self.bib[k][1])

    def get(self, include_comment, separate):
        if include_comment and len(self.comments) > 0:
            for idx in range(len(self.text)):
                for item in self.comments:
                    if idx in range(item[0], item[1]):
                        self.text[idx] = ''
                        break
        self.text = [x.strip() for x in self.text if x and x.strip()]
        otext = '<!DOCTYPE html><html><head><title>{}</title>\n'.format((self.title + ' | ' + self.author) if self.title or self.author else '')
        if separate:
            otext += '<link href="main.css" rel="stylesheet" type="text/css"><script LANGUAGE="JavaScript" src="main.js"></script>'
        else:
            otext += '<style type="text/css">\n{}</style><script LANGUAGE="JavaScript">\n{}\n</script>'.format(HTML_STYLE, JS_SCRIPT)
        otext += '</head><body><a name="top"></a><div class="frame">{}<div class="content">{}</div></div></body></html>'.\
                format(self.m_title(self.title, self.author), (self.m_toc(self.dtoc) if self.toc else '') + '\n'.join(self.text))
        return otext, HTML_STYLE if separate else '', JS_SCRIPT if separate else ''

    def m_title(self, title, author):
        return '''
        <div class="top">
        {}{}
        </div>
        '''.format('<h1 class="title">{}</h1>'.format(title) if title else '', '<center><span style="color:#304860;font-family:comic sans ms;font-size:small">Edited by {}, on {}</span></center>'.format(author, strftime("%a %d %b %Y %H:%M:%S", localtime())) if author else '')

    def m_chapter(self, text, i):
        return '''
        <h1 class="superheading" id="chapter_{}">{}</h1><hr size="5" noshade>
        '''.format(i, text)

    def m_section(self, text, i):
        return '''
        <h2 class="heading" id="section_{}">{}</h2>
        '''.format(i, text)

    def m_ssection(self, text, i):
        return '''
        <h3 class="subheading" id="subsection_{}">{}</h3>
        '''.format(i, text)

    def m_sssection(self, text):
        return '''
        <h3 class="subsubheading">&#9642; {}</h3>
        '''.format(text)

    def _csize(self, v, k):
        if k.startswith('chapter'):
            return '<big>{}</big>'.format(v)
        elif k.startswith('section'):
            return '{}'.format(v)
        else:
            return '<small>{}</small>'.format(v)

    def _isize(self, k):
        if k.startswith('chapter'):
            return 'text-decoration:underline'
        elif k.startswith('section'):
            return 'padding-left:2em'
        else:
            return 'padding-left:4em'

    def m_toc(self, dtoc):
        if not dtoc:
            return ''
        head = '<b>Contents:</b><ul id="toc">\n'
        tail = '\n</ul>'
        body = '\n'.join(['<li><span style="{}">{}</span><a href="#{}">{}</a></li>'.format(self._isize(k), self._csize(v,k),k,'&clubs;') for k, v in dtoc.items()])
        return head + body + tail
