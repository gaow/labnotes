#!/usr/bin/env python
# -*- coding: utf-8 -*-
from .style import DOC_PACKAGES, DOC_CONFIG
from .base import *
import codecs
class Tex(TexParser):
    def __init__(self, title, author, date, toc, footnote, font, font_size,
                 filename, no_num = False, no_page = False, no_ref = False, twocols = False):
        TexParser.__init__(self, title, author, filename)
        self.text = []
        for fn in filename:
            try:
                with codecs.open(fn, 'r', encoding='UTF-8', errors='ignore') as f:
                    lines = [l.rstrip() for l in f.readlines() if l.rstrip() and f.readlines()]
                    # in case I need to parse source code
                    if len(lines) > 0 and lines[0].startswith('#!/') \
                      and fn.split('.')[-1].lower() in lines[0].lower():
                        del lines[0]
                self.text.extend(lines)
            except IOError as e:
                raise
        self.date = date
        self.toc = toc
        self.doctype = 'article'
        self.footnote = footnote
        self.font_size = font_size
        self.font = font
        self.no_num = no_num
        self.no_page = no_page
        self.twocols = twocols
        self.bclogo = {'warning':'\\bcattention', 'tip':'\\bclampe',
                       'important':'\\bctakecare', 'note':'\\bccrayon'}
        self.keywords = list(set(SYNTAX.keys())) + self.bclogo.keys() + ['out', 'list', 'table']
        self.text = self.m_parseBlocks(self.text)
        self.m_parseComments()
        self.m_parseText()
        if not no_ref:
            self.m_parseBib()
            self.text.append(self.textbib)

    def m_blockizeIn(self, text, k, label = None):
        if text.startswith("file:///"): text = gettxtfromfile(text) 
        if k.lower() == 'raw' or k.lower() == '$': return text
        self._checknest(text)
        return '\\begin{minted}[samepage=false, fontfamily=tt,\nfontsize=\\scriptsize, xleftmargin=1pt,\nframe=lines, framerule=1pt, framesep=2mm,\nlabel=\\fbox{%s}]{%s}\n%s\n\\end{minted}\n' % (k.upper() if not label else self.m_recode(label), k, wraptxt(text, '\\' if k == 'bash' else '', 131, rmblank = False, prefix = COMMENT[k.lower()]))

    def m_blockizeOut(self, text, k, label = None):
        if text.startswith("file:///"): text = gettxtfromfile(text) 
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
                # regular cmd text
                if idx + 1 < len(self.text):
                    for i in range(idx + 1, len(self.text) + 1):
                        try:
                            if self.text[i].startswith(self.mark) or i in skip or self.text[i] == '':
                                break
                        except IndexError:
                            pass
                else:
                    i = idx + 1
                sep = '\\'
                cnt = 114
                sminted = '\\mint[bgcolor=bg, fontsize=\\footnotesize]{text}?'
                lminted = '\\begin{minted}[bgcolor=bg, fontsize=\\footnotesize]{text}\n'
                cmd = '\n'.join([wraptxt(x, sep, cnt) for x in self.text[idx:i]])
                cmd = cmd.split('\n')
                if len(cmd) == 1 and "?" not in cmd[0] and "`" not in cmd[0]:
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
                self.text[idx] = ('\\subsubsection*{' if self.no_num else '\\subsubsection{')+ self.m_recode(self.text[idx][len(self.mark)+2:]) + '}'
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
        return '\\documentclass[oneside%s]{%s}' % (',twocolumn' if self.twocols else '', self.doctype) + DOC_PACKAGES + \
                ('\\usepackage[Lenny]{fncychap}\n' if self.doctype == 'report' else '') + \
                ('\\usepackage{mathptmx}\n' if self.font == 'roman' else '') + \
                '\\renewcommand\\%s{References}\n' % ('bibname' if self.doctype == 'report' else 'refname') + \
                (('\\renewcommand\\rmdefault{%s}\n' % FONT[self.font]) if (self.font != 'default' and self.font != 'roman') else '') + \
                DOC_CONFIG + ('\\pagestyle{empty}\n' if self.no_page else '') + \
                (('\\setlength{\\columnsep}{%s}\\setlength{\\columnseprule}{%s}\n' % ('2em','0pt')) if self.twocols else '') + \
                '\\title{%s}\n' % self.title + '\\author{%s}\n' % self.author + \
                '\\date{%s}\n\\raggedbottom\n\\begin{document}\n' % (self.date if self.date else 'Last updated: \\today') + \
                '\\fontsize{%s}{%s}\\selectfont\n' % (self.font_size, int(self.font_size * 1.2)) + \
                '%s\n%s\n\\bigskip\n%s\n\\end{document}' % ('\\maketitle' if self.title or self.author else '',
                                                            '\\tableofcontents' if self.toc else '', '\n'.join(self.text)) 
