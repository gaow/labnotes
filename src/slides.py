from .base import *
from .style import MODE, CONFIG, TITLE, THANK, THEME
import codecs
class Beamer(TexParser):
    def __init__(self, title, author, institute, toc, stoc, mode, theme, thank, filename):
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
        self.institute = institute.replace('\\n', '\n')
        self.toc = toc
        # section toc
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

    def m_blockizeIn(self, text, k, label = None):
        self._checknest(text)
        return '\\begin{exampleblock}{\\texttt{%s}}\\scriptsize\n\\begin{Verbatim}\n%s\n\\end{Verbatim}\n\\end{exampleblock}\n' % \
                        (k.capitalize() if not label else self.m_recode(label), wraptxt(text, '', int(78 * self.wrap_adjust), rmblank = False, prefix = COMMENT[k.lower()]))

    def m_blockizeOut(self, text, k, label = None):
        self._checknest(text)
        return '\\begin{exampleblock}{0}\\tiny\n\\begin{Verbatim}\n%s\n\\end{Verbatim}\n\\end{exampleblock}\n' % \
                    wraptxt(text, '', int(105 * self.wrap_adjust), rmblank = False)

    def m_blockizeAlert(self, text, k, label = None):
        self._checknest(text, kw = [r'\\\\begin{(.*?)block}', r'\\\\end{(.*?)block}'])
        text = self._holdfigureplace(text)
        text, mapping = self._holdblockplace(text, mode = 'hold')
        self._checkblockprefix(text)
        text = '\n'.join([item if item.startswith(self.blockph) else self.m_recode(re.sub(r'^{0}'.format(self.mark), '', item)) for item in text.split('\n')])
        text = self._holdblockplace(text, mode = 'release', rule = mapping)[0]
        fmt = ''
        if k == 'important':
            fmt = 'example'
        if k == 'warning':
            fmt = 'alert'
        return '\\begin{{{0}block}}{{{1}}}\n{2}\n\\end{{{0}block}}\n'.\
                        format(fmt, k.capitalize() if not label else self.m_recode(label), text)

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
                self.text[idx + 1] = prefix + self.capitalize(self.m_recode(self.text[idx + 1][len(self.mark)+1:])) + '}'
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
                self.text[idx + 1] = prefix + self.capitalize(self.m_recode(self.text[idx + 1][len(self.mark):])) + '}'
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
                prefix = '\\begin{frame}[fragile, shrink]\n'
                title = self.m_recode(self.text[idx][len(self.mark)+1:])
                # skip acknowledge slide section ID
                if title.lower() == 'acknowledgment':
                    prefix = '\\section*{Acknowledgment}\n' + prefix
                if framestart > frameend:
                    prefix = '\\end{frame}\n\n' + prefix
                    frameend += 1
                framestart += 1
                self.text[idx] = prefix + ('' if title == '.' else  '\\frametitle{' + title + '}')
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
        return stitle[:min(length, len(stitle))] + ' ...'

    def m_checkEmptySlides(self, ltext):
        text = ''.join(ltext)
        pattern = re.compile(r'\\\\begin{frame}\[fragile, shrink\](.*?)\\\\end{frame}')
        for m in re.finditer(pattern, '%r' % text):
            frame = m.group(1)
            try:
                frametitle = re.search(r'\\\\frametitle{(.*?)}', frame).group(1).encode().decode('unicode_escape')
            except:
                frametitle = '#!.'
            frame = re.sub(r'\\\\frametitle{(.*?)}', '', frame)
            frame = re.sub(r'\\\\framesubtitle{(.*?)}', '', frame)
            if len(re.sub(r'\s', '', frame.encode().decode('unicode_escape'))) == 0:
                self.quit("Empty slides not allowed, near '{0}'".format(frametitle))
        return

    def get(self, include_comment):
        titlepage = '\\frame{\\titlepage}\n' if not self.mode == 'notes' else '\\maketitle\n'
        tocpage = '\\begin{frame}[allowframebreaks]\n\\frametitle{Outline}\n\\tableofcontents%s\n\\end{frame}\n' % ('[hideallsubsections]' if self.stoc else '') if not self.mode == 'notes' else '\\tableofcontents\n'
        sectiontoc = '\\AtBeginSection[]\n{\n\\begin{frame}<beamer>\n\\tableofcontents[currentsection, currentsubsection, sectionstyle=show/hide, subsectionstyle=show/show/hide]\n\\end{frame}\n}\n' if self.stoc else ''
        if include_comment and len(self.comments) > 0:
            for idx in range(len(self.text)):
                for item in self.comments:
                    if idx in range(item[0], item[1]):
                        self.text[idx] = ''
                        break
        self.text = filter(None, self.text)
        otext = '{0}'.format(MODE[self.mode]) + \
                CONFIG + '{0}'.format(THEME[self.theme.lower()]) + TITLE
        if self.title or self.author:
            otext += '\n\\title[%s]{%s}\n%% \\subtitle\n\\author[%s]{%s}\n' % \
                (self.m_stitle(35), self.title, re.sub(r'\\inst{(.*?)}', '', self.author).strip().split(r'\and')[0].strip(), self.author)
        if self.institute:
            otext += '\\institute[%s]{%s}\n' % (re.sub(r'\\inst{(.*?)}', '', self.institute).strip().split(r'\and')[0].strip(), self.institute)
        otext += '\\date{\\today}\n%s\\begin{document}\n%s\n%s' % (
                sectiontoc if self.toc else '',
                titlepage if self.title or self.author else '',
                tocpage if self.toc else ''
                )
        otext += '\n'.join(self.text) + '\n\\end{document}'
        return otext
