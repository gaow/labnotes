import sys, re, os
import codecs
from collections import OrderedDict
from utils import wraptxt, TexParser, SYNTAX
from htheme import HTML_STYLE, JS_SCRIPT
from time import strftime, localtime

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
        table = [[self.m_recode(iitem) for iitem in item.split('\t')] for item in text.split('\n')]
        ncols = list(set([len(x) for x in table]))
        if len(ncols) > 1:
            self.quit("Number of columns not consistent for table. Please replace empty columns with placeholder symbol, e.g. '-'. {}".format(text))
        start = '<td style="vertical-align: top;"><{}>'.format(self.tablefont)
        end = '<br /></{}></td>'.format(self.tablefont)
        head = '<center><table><tbody>'
        body = []
        line = ''
        for cell in table[0]:
            line += start + '<b>' + cell + '</b>' + end + '\n'
        body.append(line)
        for item in table[1:]:
            line = ''
            for cell in item:
                line += start + cell + end + '\n'
            body.append(line)
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
