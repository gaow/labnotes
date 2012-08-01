import sys, re, os
import codecs
from utils import wraptxt, TexParser
from gwlog2tex import SYNTAX
from btheme import MODE, CONFIG, TITLE, THANK, THEME

class LogToBeamer(TexParser):
    def __init__(self, title, author, institute, toc, mode, theme, thank, filename):
        TexParser.__init__(self, title, author)
        self.text = []
        self.textbib = None
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
        for item in self.keywords:
            self.blocks[item] = []
        self.m_parseBlocks()
        self.m_blockizeAll()
        self.m_parseText()
        self.m_parseBib()
        if self.thank:
            self.text.append(THANK)
        if self.textbib:
            self.text.append('\\appendix\n\\begin{frame}[allowframebreaks]\n\\tiny\n' + \
                self.textbib + '\n\\end{frame}')

    def m_blockizeIn(self):
        for item in list(set(SYNTAX.values())):
            if len(self.blocks[item]) == 0:
                continue
            for i in self.blocks[item]:
                self.text[i] = '\\begin{exampleblock}{\\texttt{%s}}\\scriptsize\n\\begin{Verbatim}\n%s\n\\end{Verbatim}\n\\end{exampleblock}\n' % \
                        (item.capitalize(), wraptxt(self.text[i], '', int(78 * self.wrap_adjust), rmblank = False))
        return

    def m_blockizeOut(self):
        if len(self.blocks['out']) == 0:
            return
        for i in self.blocks['out']:
            self.text[i] = '\\begin{exampleblock}{}\\tiny\n\\begin{Verbatim}\n%s\n\\end{Verbatim}\n\\end{exampleblock}\n' % \
                    wraptxt(self.text[i], '', int(105 * self.wrap_adjust), rmblank = False)
        return

    def m_blockizeAlert(self):
        for k in self.alertbox:
            if len(self.blocks[k]) == 0:
                continue
            for i in self.blocks[k]:
                if not self.text[i].startswith(self.mark):
                    sys.exit('ERROR: items must start with "{0}" in blocks. Problematic text is: \n {1}'.format(self.mark, self.text[i]))
                self.text[i] = '\\begin{{{0}block}}{{{1}}}\n{2}\n\\end{{{0}block}}\n'.\
                        format('alert' if k in ['important', 'warning'] else '', k.capitalize(), self.m_recode(re.sub(r'^{0}|\n{0}'.format(self.mark), '', self.text[i])))
        return

    def m_blockizeAll(self):
        self.m_blockizeIn()
        self.m_blockizeOut()
        self.m_blockizeList(pause=True)
        self.m_blockizeTable(fsize='tiny')
        self.m_blockizeAlert()

    def m_parseText(self):
        skip = []
        for item in self.blocks.keys():
            for i in self.blocks[item]:
                try:
                    skip.extend(i)
                except:
                    skip.append(i)
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
                sys.exit("You have so many urgly '{0}' symbols in a regular line. Please clear them up in this line: '{1}'".format(self.mark, self.text[idx]))
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
                    sys.exit("'{0}!!' has to be preceded by a line starting with '{0}!', near '{1}'".format(self.mark, self.text[idx]))
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
                self.text[idx] = '\\centering\\includegraphics[width=%s\\textwidth]{%s}\n' % (width, os.path.abspath(fig))
                idx += 1
                continue
            if self.text[idx].startswith(self.mark):
                # a plain line here
                self.text[idx] = '\n' + self.m_recode(self.text[idx][len(self.mark):]) + '\n'
                idx += 1
                continue
        if framestart > frameend:
            self.text.append('\\end{frame}\n')
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

    def get(self, include_comment):
        titlepage = '\\frame{\\titlepage}\n' if not self.mode == 'notes' else '\\maketitle\n'
        tocpage = '\\begin{frame}[allowframebreaks]\n\\frametitle{Outline}\n\\tableofcontents[hideallsubsections]\n\\end{frame}\n' if not self.mode == 'notes' else '\\tableofcontents\n'
        sectiontoc = '\\AtBeginSection[]\n{\n\\begin{frame}<beamer>\n\\frametitle{$\clubsuit$}\n\\tableofcontents[currentsection, currentsubsection, sectionstyle=show/hide, subsectionstyle=show/show/hide]\n\\end{frame}\n}\n'
        if include_comment and len(self.blocks['err']) > 0:
            for idx in range(len(self.text)):
                for item in self.blocks['err']:
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
