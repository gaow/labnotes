import sys, re, os

def recodeKw(line):
    if not line:
        return ''
    line = line.strip()
    for item in [('\\', '!!\\backslash!!'),('$', '\$'),('!!\\backslash!!', '$\\backslash$'),
            ('{', '\{'),('}', '\}'),('%', '\%'), ('_', '\_'),('&', '\&'),('<', '$<$'),
            ('>', '$>$'),('~', '$\sim$'), ('^', '\^{}'), ('#', '\#')]:
        line = line.replace(item[0], item[1])
    line = re.sub(r'"""(.*?)"""', r'\\textbf{\\textit{\1}}', line)
    line = re.sub(r'""(.*?)""', r'\\textbf{\1}', line)
    line = re.sub(r'"(.*?)"', r'\\textit{\1}', line)
    line = re.sub(r'@@(.*?)@@', r'\\texttt{\1}', line)
    line = re.sub(r'@(.*?)@', r'\\url{\1}', line)
    return line

def wraptxt(line, sep, by):
    # will also remove blank lines, if any
    sline = ''
    i = 0
    for item in list(line):
        if item == '\n' and i == 0:
            # unnecessary wrap
            continue
        if item == '\n':
            # natural wrap
            sline += item
            i = 0
            continue
        j = 1
        if item == '\t':
            # assume 1 tab = 8 white spaces
            j = 9
        for k in range(j):
            if i == by:
                # time to wrap
                sline += item + sep + '\n'
                i = 0
                break
            else:
                i += 1
        if not i == 0:
            sline += item
    return sline

SYNTAX = {'r':'r',
          'sh':'bash',
          'py':'python',
          'tex':'latex',
          'c':'c',
          'cpp':'cpp',
          'h':'c',
          'sqlite':'sql'
          }

class LogToTex:
    def __init__(self, title, author, notoc, filename):
        self.title = ' '.join([x[0].upper() + (x[1:] if len(x) > 1 else '') for x in recodeKw(title).split()])
        self.author = recodeKw(author)
        self.notoc = notoc
        self.text = []
        self.ftype = []
        self.mark = '#'
        if sum([x.split('.')[-1].lower() in ['c','cpp','h'] for x in filename]) == len(filename):
            self.mark = '//'
        for fn in filename:
            try:
                self.ftype.append(fn.split('.')[-1].lower())
                lines = [l.rstrip() for l in open(fn).readlines() if l.rstrip()]
                if fn.split('.')[-1].lower() in ['r','sh','py','c','cpp','h']:
                    sys.stderr.write("WARNING: Treating input as {0} source code. Please use a different filename extension if this is not your intension.".format(SYNTAX[fn.split('.')[-1].lower()]))
                    if lines[0].startswith('#!/') and fn.split('.')[-1].lower() in lines[0].lower():
                        del lines[0]
                    lines.insert(0,self.mark*3)
                    lines.insert(0,self.mark + fn.upper())
                    lines.insert(0,self.mark*3)
                self.text.extend(lines)
            except IOError as e:
                sys.exit(e)
        self.blocks = {}
        self.syntax = list(set(SYNTAX.values()))
        for item in self.syntax + ['err', 'out', 'list']:
            self.blocks[item] = []
#        for idx, item in enumerate(self.text):
#            print idx, item
        self.m_parseBlocks()
#        print(self.blocks)
#        for idx, item in enumerate(self.text):
#            print idx, item
#        print(self.text)
        self.m_blockizeIn()
        self.m_blockizeOut()
        self.m_blockizeList()
        self.m_parseText()
        #print('\n'.join(self.text))
        #sys.exit(0)

    def m_parseBlocks(self):
        idx = 0
        while True:
            if idx >= len(self.text):
                break
            if self.text[idx].startswith(self.mark + '}') and '--' not in self.text[idx]:
                sys.exit("ERROR: invalid use of '%s' without previous %s{, near %s" % (self.text[idx], self.mark, self.text[idx+1] if idx + 1 < len(self.text) else "end of document"))
            if self.text[idx].startswith(self.mark + '{') and '--' not in self.text[idx]:
                # define block
                bname = self.text[idx].split('{')[1].strip()
                if bname not in self.syntax + ['out', 'list']:
                    sys.exit("ERROR: invalid block definition '%s{ %s'" % (self.mark, bname))
                endidx = None
                self.text[idx] = ''
                # find end of block
                for i in range(idx+1, len(self.text)):
                    # do not allow nested blocks
                    if self.text[i].startswith(self.mark + '{'):
                        sys.exit("ERROR: nested use of blocks is disallowed: '{0}', near {1}".format(self.text[i], self.text[i+1] if idx + 1 < len(self.text) else "end of document"))
                    # find end of block
                    if self.text[i].startswith(self.mark + '}'):
                        if self.text[i].rstrip() == self.mark + '}':
                            endidx = i
                            break
                        else:
                            sys.exit("ERROR: invalid %s '%s', near %s" % ('nested use of' if '--' in self.text[i] else 'symbol', self.text[i], self.text[i+1] if idx + 1 < len(self.text) else "end of document"))
                if not endidx:
                    sys.exit("ERROR: '%s{ %s' and '%s}' must appear in pairs, near %s" % (self.mark, bname, self.mark, self.text[idx+1] if idx + 1 < len(self.text) else "end of document"))
                # combine block values
                for i in range(idx + 1, endidx):
                    self.text[idx] += self.text[i] + ('\n' if not i + 1 == endidx else '')
                del self.text[(idx + 1) : (endidx + 1)]
                    # keep block index
                self.blocks[bname].append(idx)
            idx += 1
            continue
        #
        for idx, item in enumerate(self.text):
            # define err block
            if self.text[idx].startswith(self.mark + '}') and '--' in self.text[idx]:
                sys.exit("ERROR: invalid use of '%s}----' without previous '%s{----', near %s" % (self.mark, self.mark, self.text[idx+1] if idx + 1 < len(self.text) else "end of document") )
            if item.startswith(self.mark + '{') and '--' in item:
                endidx = None
                for i in range(idx+1, len(self.text)):
                    if self.text[i].startswith(self.mark + '{') and '--' in self.text[i]:
                        sys.exit("ERROR: nested use of blocks is disallowed: '{0}', near {1}".format(self.text[i], self.text[i+1] if idx + 1 < len(self.text) else "end of document"))
                    if self.text[i].startswith(self.mark + '}') and '--' in self.text[i]:
                        endidx = i
                        break
                if not endidx:
                    sys.exit('ERROR: comment blocks must appear in pairs, near {0}'.format(self.text[i+1] if idx + 1 < len(self.text) else "end of document"))
                self.blocks['err'].append([idx, endidx])
                self.text[idx] = ''
                self.text[endidx] = ''
        return

    def m_blockizeIn(self):
        for item in self.syntax:
            if len(self.blocks[item]) == 0:
                continue
            for i in self.blocks[item]:
                self.text[i] = '\\begin{minted}[samepage=false, fontfamily=tt,\nfontsize=\\scriptsize, xleftmargin=1pt,\nframe=lines, framerule=1pt, framesep=2mm,\nlabel=\\fbox{%s}]{%s}\n%s\n\\end{minted}' % (item.upper(), item, wraptxt(self.text[i], '\\' if item == 'bash' else '', 131))
        return

    def m_blockizeOut(self):
        if len(self.blocks['out']) == 0:
            return
        for i in self.blocks['out']:
            self.text[i] = '\\begin{Verbatim}[samepage=false, fontfamily=tt,\nfontsize=\\footnotesize, formatcom=\\color{rblue},\nframe=lines, framerule=1pt, framesep=2mm,\nlabel=\\fbox{\\scriptsize OUTPUT}, labelposition=topline]\n%s\n\\end{Verbatim}' % wraptxt(self.text[i], '', 116)
        return

    def m_blockizeList(self):
        if len(self.blocks['list']) == 0:
            return
        for i in self.blocks['list']:
            if not self.text[i].startswith(self.mark):
                sys.exit('ERROR: items must start with "{0}" in list block. Problematic text is: \n {1}'.format(self.mark, self.text[i]))
            self.text[i] = '\\begin{itemize}%s\n\\end{itemize}' % recodeKw(re.sub(r'^{0}|\n{0}'.format(self.mark), '\\item ', self.text[i])).replace('$\\backslash$item', '\n\\item')
        return

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
                sminted = '\\mint[bgcolor=bg, fontsize=\\footnotesize]{text}!'
                lminted = '\\begin{minted}[bgcolor=bg, fontsize=\\footnotesize]{text}\n'
                #
                if (len(lan) == 1 and lan[0] in ['r','sh','py']) or self.mark == '//':
                    if lan[0] == 'h': lan[0] = 'cpp'
                    sep = '' if not lan[0] == 'sh' else '\\'
                    cnt = 131
                    sminted = '\\mint[fontfamily=tt,\nfontsize=\\scriptsize, xleftmargin=1pt,\nframe=lines, framerule=0.5pt, framesep=2mm]{%s}!' % (SYNTAX[lan[0]])
                    lminted =  '\\begin{minted}[samepage=false, fontfamily=tt,\nfontsize=\\scriptsize, xleftmargin=1pt,\nframe=lines, framerule=0.5pt, framesep=2mm]{%s}\n' % (SYNTAX[lan[0]])
                #
                cmd = '\n'.join([wraptxt(x, sep, cnt) for x in self.text[idx:i]])
                cmd = cmd.split('\n')
                if len(cmd) == 1:
                    self.text[idx] = sminted + cmd[0] + '!'
                else:
                    self.text[idx] = lminted + '\n'.join(cmd) + '\n\\end{minted}'
                    for j in range(idx + 1, i):
                        self.text[j] = ''
                idx = i
                continue
            if self.text[idx].startswith(self.mark * 3) and self.text[idx+1].startswith(self.mark) and (not self.text[idx+1].startswith(self.mark * 2)) and self.text[idx+2].startswith(self.mark * 3):
                # section
                self.text[idx] = ''
                self.text[idx + 1] = '\\section{' + ' '.join([x[0].upper() + (x[1:] if len(x) > 1 else '') for x in recodeKw(self.text[idx + 1][len(self.mark):]).split()]) + '}'
                self.text[idx + 2] = ''
                idx += 3
                continue
            if self.text[idx].startswith(self.mark * 2):
                # too many #'s
                sys.exit("You have so many urgly '{0}' symbols in a regular line. Please clear them up in this line: '{1}'".format(self.mark, self.text[idx]))
            if self.text[idx].startswith(self.mark + '!!!'):
                # box
                self.text[idx] = '\\shabox{' + recodeKw(self.text[idx][len(self.mark)+3:]) + '}'
                idx += 1
                continue
            if self.text[idx].startswith(self.mark + '!!'):
                # subsection, subsubsection ...
                self.text[idx] = '\\subsubsection*{' + recodeKw(self.text[idx][len(self.mark)+2:]) + '}'
                idx += 1
                continue
            if self.text[idx].startswith(self.mark + '!'):
                # subsection, subsubsection ...
                self.text[idx] = '\\subsection{' + recodeKw(self.text[idx][len(self.mark)+1:]) + '}'
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
                self.text[idx] = '\\begin{center}\\includegraphics[width=%s\\textwidth]{%s}\\end{center}' % (width, fig)
                idx += 1
                continue
            if self.text[idx].startswith(self.mark):
                # a plain line here
                self.text[idx] = '\n' + recodeKw(self.text[idx][len(self.mark):]) + '\n'
                idx += 1
                continue
        return

    def get(self, code):
        if code and len(self.blocks['err']) > 0:
            for idx in range(len(self.text)):
                for item in self.blocks['err']:
                    if idx in range(item[0], item[1]):
                        self.text[idx] = ''
                        break
        self.text = filter(None, self.text)
        return '''\\documentclass[oneside, 10pt]{article}
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
\\renewcommand\\rmdefault{bch}
\\newcommand{\\ie}{\\textit{i.e.}}
\\newcommand\\me{\\mathrm{e}}
\\newcommand\\mlog{\\mathrm{log}}
\\linespread{1.1}
\\setlength{\\parskip}{8pt plus 1pt minus 1pt}
\\parindent 0ex
\\geometry{left=0.8in,right=0.8in,top=0.8in,bottom=0.8in}
\\titleformat{\\subsubsection}
{\\color{MidnightBlue}\\normalfont\\large\\bfseries}
{\\color{MidnightBlue}\\thesection}{1em}{}
\\definecolor{bg}{rgb}{0.95,0.95,0.95}
\\definecolor{rblue}{rgb}{0,.14,.41}
\\definecolor{linkcolour}{rgb}{0,0.2,0.6}
\\hypersetup{colorlinks, breaklinks,urlcolor=linkcolour, linkcolor=linkcolour}
\\title{%s}
\\author{%s}
\\date{Last updated: \\today}
\\raggedbottom
\\begin{document}
%s\n%s\n\\bigskip\n%s
\\end{document}''' % (self.title, self.author, '\\maketitle' if self.title else '', '' if self.notoc else '\\tableofcontents', '\n'.join(self.text))
