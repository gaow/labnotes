from .style import DOC_PACKAGES, DOC_CONFIG
from .base import *
class Tex(TexParser):
    def __init__(self, title, author, toc, footnote, filename, no_num = False, no_page = False, no_ref = False):
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
        self.no_page = no_page
        self.bclogo = {'warning':'\\bcattention', 'tip':'\\bclampe', 'important':'\\bctakecare', 'note':'\\bccrayon'}
        self.keywords = list(set(SYNTAX.values())) + self.bclogo.keys() + ['out', 'list', 'table']
        self.text = self.m_parseBlocks(self.text)
        self.m_parseComments()
        self.m_parseText()
        if not no_ref:
            self.m_parseBib()
            self.text.append(self.textbib)

    def m_blockizeIn(self, text, k, label = None):
        self._checknest(text)
        return '\\begin{minted}[samepage=false, fontfamily=tt,\nfontsize=\\scriptsize, xleftmargin=1pt,\nframe=lines, framerule=1pt, framesep=2mm,\nlabel=\\fbox{%s}]{%s}\n%s\n\\end{minted}\n' % (k.upper() if not label else self.m_recode(label), k, wraptxt(text, '\\' if k == 'bash' else '', 131))

    def m_blockizeOut(self, text, k, label = None):
        self._checknest(text)
        return '\\begin{Verbatim}[samepage=false, fontfamily=tt,\nfontsize=\\footnotesize, formatcom=\\color{rgray},\nframe=lines, framerule=1pt, framesep=2mm,\nlabel=\\fbox{\\scriptsize %s}, labelposition=topline]\n%s\n\\end{Verbatim}\n' % ('OUTPUT' if not label else self.m_recode(label), wraptxt(text, '', 116))

    def m_blockizeAlert(self, text, k, label = None):
        self._checknest(text, kw = [r'\\\\begin{bclogo}', r'\\\\end{bclogo}'])
        text = self._holdfigureplace(text)
        text, mapping = self._holdblockplace(text, mode = 'hold')
        self._checkblockprefix(text)
        text = '\n'.join([item if item.startswith(self.blockph) else self.m_recode(re.sub(r'^{0}'.format(self.mark), '', item)) for item in text.split('\n')])
        text = self._holdblockplace(text, mode = 'release', rule = mapping)[0]
        return '\\begin{bclogo}[logo=%s, couleurBarre=MidnightBlue, noborder=true, couleur=white]{~%s}%s\n\\end{bclogo}\n' % (self.bclogo[k], k.capitalize() if not label else self.m_recode(label), text)

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
                self.text[idx + 1] = '\\chapter{' + self.capitalize(self.m_recode(self.text[idx + 1][len(self.mark)+1:])) + '}'
                self.text[idx + 2] = ''
                idx += 3
                continue
            if self.text[idx].startswith(self.mark * 3) and self.text[idx+1].startswith(self.mark) and (not self.text[idx+1].startswith(self.mark * 2)) and self.text[idx+2].startswith(self.mark * 3):
                # section
                self.text[idx] = ''
                self.text[idx + 1] = ('\\section*{' if self.no_num else '\\section{') + \
                        self.capitalize(self.m_recode(self.text[idx + 1][len(self.mark):])) + '}'
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
                self.text[idx] = self.insertFigure(self.text[idx], support = self.fig_support, tag = self.fig_tag)
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
        return '\\documentclass[oneside, 10pt]{%s}' % self.doctype + DOC_PACKAGES + \
                ('\\usepackage[Lenny]{fncychap}' if self.doctype == 'report' else '') + \
                '\\renewcommand\\%s{References}' % ('bibname' if self.doctype == 'report' else 'refname') + \
                DOC_CONFIG + ('\\pagestyle{empty}\n' if self.no_page else '') + \
                '\\title{%s}\n' % self.title + '\\author{%s}\n' % self.author + \
                '\\date{Last updated: \\today}\n\\raggedbottom\n\\begin{document}\n' + \
                '%s\n%s\n\\bigskip\n%s' % ('\\maketitle' if self.title or self.author else '', '\\tableofcontents' if self.toc else '', '\n'.join(self.text)) + \
                '\n\\end{document}'
