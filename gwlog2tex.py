import sys, re, os

def recodeKw(line):
    if not line:
        return ''
    for item in [('\\', '!!\\backslash!!'),('$', '\$'),('!!\\backslash!!', '$\\backslash$'),
            ('{', '\{'),('}', '\}'),('%', '\%'), ('_', '\_'),('&', '\&'),('<', '$<$'),
            ('>', '$>$'),('~', '\~{}'), ('^', '\^{}'), ('#', '\#')]:
        line = line.replace(item[0], item[1])
    return line

def wraptxt(line, sep, by):
    sline = ''
    i = 0
    for item in list(line):
        if item == '\n':
            i = 0
        if i % by  == 0 and i >= by:
            sline += item + sep + '\n'
        else:
            sline += item
        i += 1
    return sline

class LogToTex:
    def __init__(self, title, author, filename):
        self.title = ' '.join([x.capitalize() for x in recodeKw(title).lower().split()])
        self.author = recodeKw(author)
        self.text = []
        for fn in filename:
            try:
                self.text.extend(list(line for line in (l.rstrip() for l in open(fn).readlines()) if line))
            except IOError as e:
                sys.exit(e)
        self.blocks = {}
        self.syntax = ['latex', 'python', 'bash', 'r', 'c', 'cpp']
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
            if self.text[idx].startswith('#}') and '--' not in self.text[idx]:
                sys.exit("ERROR: invalid use of '%s' without previous #{" % (self.text[idx]))
            if self.text[idx].startswith('#{') and '--' not in self.text[idx]:
                # define block
                bname = self.text[idx].split('{')[1].strip()
                if bname not in self.syntax + ['out', 'list']:
                    sys.exit("ERROR: invalid block definition '#{ %s'" % (bname))
                endidx = None
                self.text[idx] = ''
                # find end of block
                for i in range(idx+1, len(self.text)):
                    # do not allow nested blocks
                    if self.text[i].startswith('#{'):
                        sys.exit("ERROR: nested use of blocks is disallowed: '{0}'".format(self.text[i]))
                    # find end of block
                    if self.text[i].startswith('#}'):
                        if self.text[i].rstrip() == '#}':
                            endidx = i
                            break
                        else:
                            sys.exit("ERROR: invalid %s '%s'" % ('nested use of' if '--' in self.text[i] else 'symbol', self.text[i]))
                if not endidx:
                    sys.exit("ERROR: '#{ %s' and '#}' must appear in pairs" % (bname))
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
            if item.startswith('#{') and '--' in item:
                endidx = None
                for i in range(idx+1, len(self.text)):
                    if self.text[i].startswith('#}') and '--' in self.text[i]:
                        endidx = i
                        break
                if not endidx:
                    sys.exit('ERROR: comment blocks must appear in pairs')
                self.blocks['err'].append([idx, endidx])
                self.text[idx] = ''
                self.text[endidx] = ''
        return

    def m_blockizeIn(self):
        for item in self.syntax:
            if len(self.blocks[item]) == 0:
                continue
            for i in self.blocks[item]:
                self.text[i] = '\\begin{minted}[samepage=false, fontfamily=tt,\nfontsize=\\scriptsize, xleftmargin=1pt,\nframe=lines, framerule=1pt, framesep=2mm,\nlabel=\\fbox{%s}]{%s}\n%s\n\\end{minted}' % (item.upper(), item, wraptxt(self.text[i], '\\', 130))
        return

    def m_blockizeOut(self):
        if len(self.blocks['out']) == 0:
            return
        for i in self.blocks['out']:
           self.text[i] = '\\begin{Verbatim}[samepage=false, fontfamily=tt,\nfontsize=\\footnotesize, formatcom=\\color{rblue},\nframe=lines, framerule=1pt, framesep=2mm,\nlabel=\\fbox{\\scriptsize OUTPUT}, labelposition=topline]\n%s\n\\end{Verbatim}' % wraptxt(self.text[i], '', 115)
        return

    def m_blockizeList(self):
        if len(self.blocks['list']) == 0:
            return
        for i in self.blocks['list']:
           self.text[i] = '\\begin{itemize}%s\n\\end{itemize}' % recodeKw(re.sub(r'^#|\n#', '\\item ', self.text[i])).replace('$\\backslash$item', '\n\\item')
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
            if not self.text[idx].startswith('#'):
                # regular cmd
                cmd = wraptxt(self.text[idx], '\n', 110).split('\n')
                self.text[idx] = ''.join(['\\mint[bgcolor=bg, fontsize=\\footnotesize]{text}!' + x + ('\\' if (i + 1) < len(cmd) else '') + '!' for i, x in enumerate(cmd) if x != ''])
                idx += 1
                continue
            if self.text[idx].startswith('###') and self.text[idx+1].startswith('#') and (not self.text[idx+1].startswith('##')) and self.text[idx+2].startswith('###'):
                # section
                self.text[idx] = ''
                self.text[idx + 1] = '\\section{' + ' '.join([x.capitalize() for x in recodeKw(self.text[idx + 1][1:]).lower().split()]) + '}'
                self.text[idx + 2] = ''
                idx += 3
                continue
            if self.text[idx].startswith('##'):
                # too many #'s
                sys.exit("You have so many urgly '#' symbols in a regular line. Please clear them up in this line: '{0}'".format(self.text[idx]))
            if self.text[idx].startswith('#!!'):
                # subsection, subsubsection ...
                self.text[idx] = '\\subsubsection*{' + recodeKw(self.text[idx][3:]) + '}'
                idx += 1
                continue
            if self.text[idx].startswith('#!'):
                # subsection, subsubsection ...
                self.text[idx] = '\\subsection{' + recodeKw(self.text[idx][2:]) + '}'
                idx += 1
                continue
            if self.text[idx].startswith('#*'):
                # date
                self.text[idx] = '\\shabox{' + self.text[idx][2:] + '}'
                idx += 1
                continue
            if self.text[idx].startswith('#'):
                # a plain line here
                self.text[idx] = '\n' + recodeKw(self.text[idx][1:]) + '\n'
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
        self.text = [x for x in self.text if len(x)>0]
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
\\usepackage[pdfstartview=FitH]{hyperref}
\\usepackage[dvipsnames]{xcolor}
\\usepackage{minted}
\\usepackage{upquote}
\\usepackage{titlesec}
\\renewcommand\\rmdefault{bch}
\\newcommand{\\ie}{\\textit{i.e.}}
\\newcommand\\me{\\mathrm{e}}
\\newcommand\\mlog{\\mathrm{log}}
\\linespread{1.1}
\\setlength{\\parskip}{8pt plus1pt minus2pt}
\\parindent 0ex
\\geometry{left=0.8in,right=0.8in,top=0.8in,bottom=0.8in}
\\titleformat{\\subsubsection}
{\\color{MidnightBlue}\\normalfont\\large\\bfseries}
{\\color{MidnightBlue}\\thesection}{1em}{}
\\definecolor{bg}{rgb}{0.95,0.95,0.95}
\\definecolor{rblue}{rgb}{0,.14,.41}
\\title{%s}
\\author{%s}
\\date{Last updated: \\today}
\\raggedbottom
\\begin{document}
%s\n%s
\\end{document}''' % (self.title, self.author, '\\maketitle' if self.title else '', '\n'.join(self.text))
