import sys, re, os
import codecs
from utils import wraptxt, TexParser

SYNTAX = {'r':'r',
          'sh':'bash',
          'py':'python',
          'tex':'latex',
          'c':'c',
          'cpp':'cpp',
          'h':'c',
          'sqlite':'sql'
          }

class LogToTex(TexParser):
    def __init__(self, title, author, toc, footnote, filename):
        TexParser.__init__(self, title, author)
        if sum([x.split('.')[-1].lower() in ['c','cpp','h'] for x in filename]) == len(filename):
            self.mark = '//'
        self.ftype = []
        self.text = []
        self.textbib = None
        for fn in filename:
            try:
                self.ftype.append(fn.split('.')[-1].lower())
                with codecs.open(fn, 'r', encoding='UTF-8', errors='ignore') as f:
                    lines = [l.rstrip() for l in f.readlines() if l.rstrip()]
                if fn.split('.')[-1].lower() in ['r','sh','py','c','cpp','h']:
                    sys.stderr.write("WARNING: Treating input as {0} source code. Please use a different filename extension if this is not your intension.\n".format(SYNTAX[fn.split('.')[-1].lower()]))
                    if lines[0].startswith('#!/') and fn.split('.')[-1].lower() in lines[0].lower():
                        del lines[0]
                    lines.insert(0,self.mark*3)
                    lines.insert(0,self.mark + fn.upper())
                    lines.insert(0,self.mark*3)
                self.text.extend(lines)
            except IOError as e:
                sys.exit(e)
        self.toc = toc
        self.doctype = 'article'
        self.footnote = footnote
        self.bclogo = {'warning':'\\bcattention', 'tip':'\\bclampe', 'important':'\\bctakecare', 'note':'\\bccrayon'}
        self.keywords = list(set(SYNTAX.values())) + self.bclogo.keys() + ['err', 'out', 'list']
        for item in self.keywords:
            self.blocks[item] = []
        self.m_parseBlocks()
        self.m_blockizeAll()
        self.m_parseText()
        self.m_parseBib()
        self.text.append(self.textbib)

    def m_blockizeIn(self):
        for item in list(set(SYNTAX.values())):
            if len(self.blocks[item]) == 0:
                continue
            for i in self.blocks[item]:
                self.text[i] = '\\begin{minted}[samepage=false, fontfamily=tt,\nfontsize=\\scriptsize, xleftmargin=1pt,\nframe=lines, framerule=1pt, framesep=2mm,\nlabel=\\fbox{%s}]{%s}\n%s\n\\end{minted}\n' % (item.upper(), item, wraptxt(self.text[i], '\\' if item == 'bash' else '', 131))
        return

    def m_blockizeOut(self):
        if len(self.blocks['out']) == 0:
            return
        for i in self.blocks['out']:
            self.text[i] = '\\begin{Verbatim}[samepage=false, fontfamily=tt,\nfontsize=\\footnotesize, formatcom=\\color{rgray},\nframe=lines, framerule=1pt, framesep=2mm,\nlabel=\\fbox{\\scriptsize OUTPUT}, labelposition=topline]\n%s\n\\end{Verbatim}\n' % wraptxt(self.text[i], '', 116)
        return

    def m_blockizeBclogo(self):
        for k in self.bclogo.keys():
            if len(self.blocks[k]) == 0:
                continue
            for i in self.blocks[k]:
                if not self.text[i].startswith(self.mark):
                    sys.exit('ERROR: items must start with "{0}" in logo-ed blocks. Problematic text is: \n {1}'.format(self.mark, self.text[i]))
                self.text[i] = '\\begin{bclogo}[logo=%s, couleurBarre=MidnightBlue, noborder=true, couleur=white]{~%s}%s\n\\end{bclogo}\n' % (self.bclogo[k], k.capitalize(), self.m_recode(re.sub(r'^{0}|\n{0}'.format(self.mark), '', self.text[i])))
        return

    def m_blockizeAll(self):
        self.m_blockizeIn()
        self.m_blockizeOut()
        self.m_blockizeList()
        self.m_blockizeBclogo()

    def m_parseText(self):
        skip = []
        for item in self.blocks.keys():
            for i in self.blocks[item]:
                try:
                    skip.extend(i)
                except:
                    skip.append(i)
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
                self.text[idx + 1] = '\\section{' + ' '.join([x[0].upper() + (x[1:] if len(x) > 1 else '') for x in self.m_recode(self.text[idx + 1][len(self.mark):]).split()]) + '}'
                self.text[idx + 2] = ''
                idx += 3
                continue
            if self.text[idx].startswith(self.mark * 2):
                # too many #'s
                sys.exit("You have so many urgly '{0}' symbols in a regular line. Please clear them up in this line: '{1}'".format(self.mark, self.text[idx]))
            if self.text[idx].startswith(self.mark + '!!!'):
                # box
                self.text[idx] = '\\shabox{' + self.m_recode(self.text[idx][len(self.mark)+3:]) + '}'
                idx += 1
                continue
            if self.text[idx].startswith(self.mark + '!!'):
                # subsection, subsubsection ...
                self.text[idx] = '\\subsubsection*{' + self.m_recode(self.text[idx][len(self.mark)+2:]) + '}'
                idx += 1
                continue
            if self.text[idx].startswith(self.mark + '!'):
                # subsection, subsubsection ...
                self.text[idx] = '\\subsection{' + self.m_recode(self.text[idx][len(self.mark)+1:]) + '}'
                idx += 1
                continue
            if self.text[idx].startswith(self.mark + '*'):
                # fig: figure.pdf 0.9
                try:
                    fig, width = self.text[idx][len(self.mark)+1:].split()
                except ValueError:
                    fig = self.text[idx][len(self.mark)+1:].split()[0]
                    width = 0.9
                if not '.' in fig:
                    sys.exit("ERROR: Cannot determine graphic file format for '%s'. Valid extensions are 'pdf', 'png' and 'jpg'" % fig)
                if fig.split('.')[1] not in ['jpg','pdf','png']:
                    sys.exit("ERROR: Input file format '%s' not supported. Valid extensions are 'pdf', 'png' and 'jpg'" % fig.split('.')[1])
                if not os.path.exists(fig):
                    sys.exit("ERROR: Cannot find file %s" % fig)
                self.text[idx] = '\\begin{center}\\includegraphics[width=%s\\textwidth]{%s}\\end{center}' % (width, os.path.abspath(fig))
                idx += 1
                continue
            if self.text[idx].startswith(self.mark):
                # a plain line here
                self.text[idx] = '\n' + self.m_recode(self.text[idx][len(self.mark):]) + '\n'
                idx += 1
                continue
        return

    def get(self, include_comment):
        if include_comment and len(self.blocks['err']) > 0:
            for idx in range(len(self.text)):
                for item in self.blocks['err']:
                    if idx in range(item[0], item[1]):
                        self.text[idx] = ''
                        break
        self.text = filter(None, self.text)
        return '''\\documentclass[oneside, 10pt]{%s}
\\usepackage{geometry}
\\usepackage{fullpage}
\\usepackage{amsmath}
\\usepackage{booktabs}
\\usepackage{amssymb}
\\usepackage{amsthm}
\\usepackage{bm}
\\usepackage{fancyhdr}
\\usepackage{fancyvrb}
\\usepackage{shadow}
\\usepackage[pdftex]{graphicx}
\\usepackage[bookmarksnumbered=true,pdfstartview=FitH]{hyperref}
\\usepackage[dvipsnames]{xcolor}
\\usepackage{minted}
\\usepackage{upquote}
\\usepackage{titlesec}
%s
\\renewcommand\\rmdefault{bch}
\\newcommand{\\ie}{\\textit{i.e.}}
\\newcommand\\me{\\mathrm{e}}
\\newcommand\\mlog{\\mathrm{log}}
\\linespread{1.1}
\\setlength{\\parskip}{8pt plus 1pt minus 1pt}
\\parindent 0ex
\\geometry{left=0.8in,right=0.8in,top=0.8in,bottom=0.8in}
\\renewcommand\\%s{References}
\\renewcommand{\\labelitemii}{$\\triangleright$}
\\makeatletter
\\renewcommand\\@biblabel[1]{#1.}
\\renewcommand\\@cite[1]{\\textsuperscript{#1}}
\\makeatother
\\definecolor{bg}{rgb}{0.95,0.95,0.95}
\\definecolor{rblue}{rgb}{0,.14,.41}
\\definecolor{rgray}{RGB}{94,96,98}
\\definecolor{wwwcolor}{rgb}{0,0.2,0.6}
\\titleformat{\\subsubsection}
{\\color{rblue}\\normalfont\\large\\bfseries}
{\\color{rblue}\\thesection}{1em}{}
\\hypersetup{colorlinks, breaklinks, urlcolor=wwwcolor, linkcolor=wwwcolor, citecolor=MidnightBlue}
\\usepackage[tikz]{bclogo}
\\title{%s}
\\author{%s}
\\date{Last updated: \\today}
\\raggedbottom
\\begin{document}
%s\n%s\n\\bigskip\n%s
\\end{document}''' % (self.doctype, '\\usepackage[Lenny]{fncychap}' if self.doctype == 'report' else '', 'bibname' if self.doctype == 'report' else 'refname', self.title, self.author, '\\maketitle' if self.title or self.author else '', '\\tableofcontents' if self.toc else '', '\n'.join(self.text))
