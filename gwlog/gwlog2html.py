import sys, re, os
import codecs
from collections import OrderedDict
from utils import wraptxt, TexParser, SYNTAX
from htheme import HTML_STYLE, JS_SCRIPT

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
        for item in self.keywords:
            self.blocks[item] = []
        self.wrap_width = 120
        self.m_parseBlocks()
        self.m_blockizeAll()
        self.m_parseText()
        self.m_parseBib()
        self.text.append(self.textbib)

    def m_blockizeAll(self):
        self.m_blockizeIn()
        self.m_blockizeOut()
        self.m_blockizeList()
        self.m_blockizeTable(fsize='small')
        self.m_blockizeAlert()

    def m_recode(self, line):
        if not line:
            return ''
        line = line.strip()
        raw = []
        ph = 'HTMLRAWPATTERNPLACEHOLDER'
        # support for raw html syntax/symbols
        pattern = re.compile(r'@@@(.*?)@@@')
        for m in re.finditer(pattern, line):
            line = line.replace(m.group(0), ph + str(len(raw)))
            raw.append(m.group(1))
        # html keywords
        # no need to convert any
#        for item in [
#                ('\\', '&#92;'),('$', '&#36;'),
#                ('{', '&#123;'),('}', '&#125;'),
#                ('%', '&#37;'),('--', '&mdash;'),
#                ('-', '&ndash;'),('&', '&amp;'),
#                ('<', '&lt;'),('>', '&gt;'),
#                ('~', '&tilde;'),('^', '&circ;'),
#                ('``', '&ldquo;'),('`', '&lsquo;'),
#                ('#', '&#35;')
#                ]:
#            line = line.replace(item[0], item[1])
        line = re.sub(r'"""(.*?)"""', r'<strong><em>\1</em></strong>', line)
        line = re.sub(r'""(.*?)""', r'<strong>\1</strong>', line)
        line = re.sub(r'"(.*?)"', r'<em>\1</em>', line)
#        line = re.sub(r'@@(.*?)@@', r'<span style="font-family: monospace">\1</span>', line)
        line = re.sub(r'@@(.*?)@@', r'<code>\1</code>', line)
        # hyperlink
        # [text|@link@] defines the pattern for citation.
        pattern = re.compile('\[(?P<a>.+?)\|@(?P<b>.+?)@\]')
        for m in re.finditer(pattern, line):
            line = line.replace(m.group(0), '<a style="text-shadow: 1px 1px 1px #999;" href="http://{0}">{1}</a>'.format(m.group('b').replace('http://', '', 1), m.group('a')))
        # url
        pattern = re.compile('@(.*?)@')
        for m in re.finditer(pattern, line):
            line = line.replace(m.group(0), '<a href="http://{0}">{0}</a>'.format(m.group(1).replace('http://', '', 1)))
        # footnote
        # [note|reference] defines the pattern for citation.
        pattern = re.compile('\[(?P<a>.+?)\|(?P<b>.+?)\]')
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
        # recover raw html syntax
        for i in range(len(raw)):
            line = line.replace(ph + str(i), raw[i])
        return line


    def m_blockizeList(self):
        if len(self.blocks['list']) == 0:
            return
        for i in self.blocks['list']:
            if i >= len(self.text):
                self.quit('BUG: block specification does not match text')
            if not self.text[i].startswith(self.mark):
                self.quit('Items must start with "{0}" in list block. Problematic text is: \n {1}'.format(self.mark, self.text[i]))
            # handle 2nd level indentation first
            # in the mean time take care of recoding
            text = self.text[i].split('\n')
            idx = 0
            while idx < len(text):
                if text[idx].startswith(self.mark * 2):
                    start = idx
                    end = idx
                    text[idx] = self.mark * 2 + self.m_recode(text[idx][2:])
                    text[idx] = re.sub(r'^{0}'.format(self.mark * 2), '<li> ', text[idx]) + '</li>'
                    if idx + 1 < len(text):
                        for j in range(idx + 1, len(text) + 1):
                            try:
                                if not text[j].startswith(self.mark * 2):
                                    break
                                else:
                                    text[j] = self.mark * 2 + self.m_recode(text[j][2:])
                                    text[j] = re.sub(r'^{0}'.format(self.mark * 2), '<li> ', text[j]) + '</li>'
                                    end = j
                            except IndexError:
                                pass
                    #
                    text[start] = '<ul>\n' + text[start]
                    text[end] = text[end] + '\n</ul>'
                    idx = end + 1
                elif text[idx].startswith(self.mark):
                    text[idx] = self.mark + self.m_recode(text[idx][1:])
                    idx += 1
                else:
                    text[idx] = self.m_recode(text[idx])
                    idx += 1
            # handle 1st level indentation
            self.text[i] = '\n'.join(text)
            self.text[i] = '<ol>\n%s\n</ol>\n' % re.sub(r'^{0}|\n{0}'.format(self.mark), '\n<li> ', self.text[i] + '</li>')
        return


    def m_blockizeTable(self, fsize = 'small'):
        if len(self.blocks['table']) == 0:
            return
        for i in self.blocks['table']:
            table = [[self.m_recode(iitem) for iitem in item.split('\t')] for item in self.text[i].split('\n')]
            ncols = list(set([len(x) for x in table]))
            if len(ncols) > 1:
                self.quit("Number of columns not consistent for table. Please replace empty columns with placeholder symbol, e.g. '-'. {}".format(self.text[i]))
            start = '<td style="vertical-align: top;"><{}>'.format(fsize)
            end = '<br /></{}></td>'.format(fsize)
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
            self.text[i] = head + '\n'.join(body) + tail
        return


    def _parsecmd(self, text, serial):
        head = '<div><div id="highlighter_{}" class="syntaxhighlighter bash"><table border="0" cellpadding="0" cellspacing="0"><tbody><tr><td class="gutter">'.format(serial)
        numbers = ''.join(['<div class="line number{0} index{1} alt{2}">{0}</div>'.format(j+1, j, 2 - j % 2) for j in range(len(text))]) + '</td><td class="code"><div class="container">'
        lines = ''.join(['<div class="line number{0} index{1} alt{2}"><code class="bash plain">{3}</code></div>'.format(j+1, j, 2 - j % 2, line) for j, line in enumerate(text)])
        tail = '</div></td></tr></tbody></table></div></div>'
        return head + numbers + lines + tail

    def m_blockizeIn(self):
        for item in list(set(SYNTAX.values())):
            if len(self.blocks[item]) == 0:
                continue
            for i in self.blocks[item]:
                self.text[i] = '<div style="color:rgb(220, 20, 60);font-weight:bold;text-align:right;padding-right:2em;"><span class="textborder">' + \
                        item.capitalize() + '</span></div>' + \
                        self._parsecmd(wraptxt(self.text[i], '', int(self.wrap_width), rmblank = True).split('\n'), i)
        return

    def m_blockizeOut(self):
        if len(self.blocks['out']) == 0:
            return
        for i in self.blocks['out']:
            self.text[i] = '<br /><textarea rows="20" cols="105">{}</textarea><br />'.format(self.text[i])
        return

    def m_blockizeAlert(self):
        for k in self.alertbox:
            if len(self.blocks[k]) == 0:
                continue
            for i in self.blocks[k]:
                if not self.text[i].startswith(self.mark):
                    self.quit('Items must start with "{0}" in blocks. Problematic text is: \n {1}'.format(self.mark, self.text[i]))
                self.text[i] = '<center><div id="wrapper"><div class="{0}"><strong>{1}:</strong><br />{2}</div></div></center>'.\
                        format(k.lower(), k.capitalize(), self.m_recode(re.sub(r'^{0}|\n{0}'.format(self.mark), '', self.text[i])))
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
                cmd = '\n'.join([wraptxt(x, '', int(self.wrap_width)) for x in self.text[idx:i]])
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
                try:
                    fig, width = self.text[idx][len(self.mark)+1:].split()
                    width = float(width)
                except ValueError:
                    fig = self.text[idx][len(self.mark)+1:].split()[0]
                    width = 0.9
                if not '.' in fig:
                    self.quit("Cannot determine graphic file format for '%s'. Valid extensions are 'tif', 'png' and 'jpg'" % fig)
                if fig.split('.')[1] not in ['jpg','tif','png']:
                    self.quit("Input file format '%s' not supported. Valid extensions are 'tif', 'png' and 'jpg'" % fig.split('.')[1])
                if not os.path.exists(fig):
                    self.quit("Cannot find file %s" % fig)
                self.text[idx] = '<p><center><img src="{}" alt="{}" width="{}" /></center></p>'.format(os.path.abspath(fig), os.path.split(fig)[-1], int(width * 800))
                idx += 1
                continue
            if self.text[idx].startswith(self.mark):
                # a plain line here
                self.text[idx] = '\n' + self.m_recode(self.text[idx][len(self.mark):]) + '\n'
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

    def get(self, include_comment):
        if include_comment and len(self.blocks['err']) > 0:
            for idx in range(len(self.text)):
                for item in self.blocks['err']:
                    if idx in range(item[0], item[1]):
                        self.text[idx] = ''
                        break
        self.text = [x.strip() for x in self.text if x and x.strip()]
        self.text = [x if x.startswith('<h') else x + '<br />' for x in self.text]
        return '''
<!DOCTYPE html>
<html><head><title>{} | {}</title>
{}{}
</head><body><a name="top"></a>
<div class="frame">
{}
<div class="content">
{}
</div></div></body></html>
        '''.format(self.title, self.author, HTML_STYLE, JS_SCRIPT, self.m_title(self.title, self.author), (self.m_toc(self.dtoc) if self.toc else '') + '\n'.join(self.text))

    def m_title(self, title, author):
        return '''
        <div class="top">
        {}{}
        </div>
        '''.format('<h1 class="title">{}</h1>'.format(title) if title else '', '<center><h3 class="subsubheading"><em>Edited by: {}</em></h3></center>'.format(author) if author else '')

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
        <h3 class="subsubheading"><em>{}</em></h3>
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
