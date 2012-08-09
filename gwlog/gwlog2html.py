import sys, re, os
import codecs
from utils import wraptxt, TexParser

HTML_STYLE = '''
<link rel="stylesheet" type="text/css">
<style type="text/css">
body
{
        margin:40px 0;
        padding:0;
	font-family: 'Lucida Grande', 'Lucida Sans', 'Lucida Sans Unicode', Tahoma, sans-serif;
        font-size: 9pt;
        text-align:justify;
        line-height: 150%;
}

table {border-spacing: 2px;}
td, th
{
	border: 0;
	padding: 10px;
	text-align: left;
}
td
{
	vertical-align:top;
}
th
{
	background-color:#eee;
}
td.flag
{
	font-family:monospace;
}
tr.dark
{
	background-color:#f9f9f9;
}

ul
{
	list-style-type: lower-greek;
	font-family: 'Lucida Grande';
}

a,
a:link,
a:visited,
a:active
{
	color: #3366CC;
	border-bottom: 1px dotted #3366CC;
	text-decoration:none;
}
a:hover
{
	border-bottom: none;
	color: #000030;
}

.normal
{
	font-family: Helvetica, Arial, sans-serif;
	font-size: 10pt;
}

.minorhead
{
	color: #666;
	font-family: monospace;
	line-height: 30px;
}

.gray
{
	color:#666;
	font-weight: bold;
	font-family:monospace;
	background: #eee;
	padding: 2px 6px 2px 6px;
	white-space: nowrap;
}

.frame
{
	margin: 0px auto 50px auto;
	width: 800px;
}

.content
{
	padding: 0 20px;
}

.title
{
	font-variant: small-caps;
	margin:0;
	padding:0;
	font-family: Georgia, Times, serif;
	font-size:20pt;
	color:rgb(220, 20, 60);
}

.superheading
{
	margin-top: 40px;
	font-size: 16pt;
	color: #666;
}

.heading
{
	margin-top: 30px;
	font-size: 14pt;
	color:rgb(220, 20, 60);
}

.subheading
{
	margin-top: 20px;
	font-size: 12pt;
	color:#304860;
}

.subsubheading
{
	margin-top: 15px;
	font-size: 12pt;
	font-weight:normal;
	color: #666;
}

.download
{
	font-weight: normal;
	font-family: Georgia;
	background: #eee;
	padding:20px 20px;
	color: #666;
	text-align:center;
	font-style: italic;
}
.download:hover
{
	background:#fafafa;
}
.download a
{
	text-transform: uppercase;
	font-weight: bold;
	font-size: 12pt;
	text-shadow: 1px 1px 1px #999;
	border: none;
	font-style: normal;
}

#clear { clear:both; }

#form
{
	background-color: #f9f9f9;
	padding: 5px 20px 20px 20px;
}

#form .set
{
	float: left;
	margin-right: 20px;
}

#form .field
{
	border: 1px solid #ccc;
	padding: 1px;
	margin-top: 5px;
	width: 150px;
}

#form .text_input
{
	width: 146px;
}

#form #zoosbmt
{
	margin-top: 5px;
}
</style>
'''

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
        self.keywords = ['err', 'list', 'table', 'out']
        for item in self.keywords:
            self.blocks[item] = []
        self.m_parseBlocks()
        self.m_blockizeAll()
        self.m_parseText()

    def m_blockizeAll(self):
#FIXME
#        self.m_blockizeIn()
        self.m_blockizeOut()
        self.m_blockizeList()
        self.m_blockizeTable(fsize='small')
#FIXME
#        self.m_blockizeAlert()

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
        line = re.sub(r'@@(.*?)@@', r'<span style="font-family: monospace">\1</span>', line)
        # url
        pattern = re.compile('@(.*?)@')
        for m in re.finditer(pattern, line):
            line = line.replace(m.group(0), '<a href="{0}">{0}</a>'.format(m.group(1).replace('&tilde;', '~')))
        # citation
        # [note|reference] defines the pattern for citation.
        pattern = re.compile('\[(?P<a>.+?)\|(?P<b>.+?)\]')
        # re.compile('\[(.+?)\|(.+?)\]')
        for m in re.finditer(pattern, line):
            line = line.replace(m.group(0), '<a style="text-shadow: 1px 1px 1px #999;" href="%s">%s</a>' % (m.group('b'), m.group('a')))
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
            head = '<table><tbody>'
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
            tail = '</tbody></table>\n'
            self.text[i] = head + '\n'.join(body) + tail
        return

    def m_blockizeOut(self):
        if len(self.blocks['out']) == 0:
            return
        for i in self.blocks['out']:
            self.text[i] = '<br /><textarea rows="20" cols="120">{}</textarea><br />'.format(self.text[i])
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
            if not self.text[idx].startswith(self.mark):
#FIXME
#                # regular cmd text, or with syntax
#                if idx + 1 < len(self.text):
#                    for i in range(idx + 1, len(self.text) + 1):
#                        try:
#                            if self.text[i].startswith(self.mark) or i in skip or self.text[i] == '':
#                                break
#                        except IndexError:
#                            pass
#                else:
#                    i = idx + 1
#                lan = list(set(self.ftype))
#                sep = '\\'
#                cnt = 114
#                sminted = '\\mint[bgcolor=bg, fontsize=\\footnotesize]{text}?'
#                lminted = '\\begin{minted}[bgcolor=bg, fontsize=\\footnotesize]{text}\n'
#                #
#                if (len(lan) == 1 and lan[0] in ['r','sh','py']) or self.mark == '//':
#                    if lan[0] == 'h': lan[0] = 'cpp'
#                    sep = '' if not lan[0] == 'sh' else '\\'
#                    cnt = 131
#                    sminted = '\\mint[fontfamily=tt,\nfontsize=\\scriptsize, xleftmargin=1pt,\nframe=lines, framerule=0.5pt, framesep=2mm]{%s}?' % (SYNTAX[lan[0]])
#                    lminted =  '\\begin{minted}[samepage=false, fontfamily=tt,\nfontsize=\\scriptsize, xleftmargin=1pt,\nframe=lines, framerule=0.5pt, framesep=2mm]{%s}\n' % (SYNTAX[lan[0]])
#                #
#                cmd = '\n'.join([wraptxt(x, sep, cnt) for x in self.text[idx:i]])
#                cmd = cmd.split('\n')
#                if len(cmd) == 1:
#                    self.text[idx] = sminted + cmd[0] + '?'
#                else:
#                    self.text[idx] = lminted + '\n'.join(cmd) + '\n\\end{minted}'
#                    for j in range(idx + 1, i):
#                        self.text[j] = ''
#                idx = i
#FIXME
#FIXME
                idx += 1
                continue
            if self.text[idx].startswith(self.mark * 3) and self.text[idx+1].startswith(self.mark + '!') and self.text[idx+2].startswith(self.mark * 3):
                # chapter
                self.text[idx] = ''
                self.text[idx + 1] = self.m_chapter(
                        ' '.join([x[0].upper() + (x[1:] if len(x) > 1 else '') for x in self.m_recode(self.text[idx + 1][len(self.mark)+1:]).split()])
                        )
                self.text[idx + 2] = ''
                idx += 3
                continue
            if self.text[idx].startswith(self.mark * 3) and self.text[idx+1].startswith(self.mark) and (not self.text[idx+1].startswith(self.mark * 2)) and self.text[idx+2].startswith(self.mark * 3):
                # section
                self.text[idx] = ''
                self.text[idx + 1] = self.m_section(
                        ' '.join([x[0].upper() + (x[1:] if len(x) > 1 else '') for x in self.m_recode(self.text[idx + 1][len(self.mark):]).split()])
                        )
                self.text[idx + 2] = ''
                idx += 3
                continue
            if self.text[idx].startswith(self.mark * 2):
                # too many #'s
                self.quit("You have so many urgly '{0}' symbols in a regular line. Please clear them up in this line: '{1}'".format(self.mark, self.text[idx]))
            if self.text[idx].startswith(self.mark + '!!!'):
#FIXME
#                # box
#                self.text[idx] = '\\shabox{' + self.m_recode(self.text[idx][len(self.mark)+3:]) + '}'
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
                self.text[idx] = self.m_ssection(
                        self.m_recode(self.text[idx][len(self.mark)+1:])
                        )
                idx += 1
                continue
            if self.text[idx].startswith(self.mark + '*'):
#FIXME
#                # fig: figure.pdf 0.9
#                try:
#                    fig, width = self.text[idx][len(self.mark)+1:].split()
#                except ValueError:
#                    fig = self.text[idx][len(self.mark)+1:].split()[0]
#                    width = 0.9
#                if not '.' in fig:
#                    self.quit("Cannot determine graphic file format for '%s'. Valid extensions are 'pdf', 'png' and 'jpg'" % fig)
#                if fig.split('.')[1] not in ['jpg','pdf','png']:
#                    self.quit("Input file format '%s' not supported. Valid extensions are 'pdf', 'png' and 'jpg'" % fig.split('.')[1])
#                if not os.path.exists(fig):
#                    self.quit("Cannot find file %s" % fig)
#                self.text[idx] = '\\begin{center}\\includegraphics[width=%s\\textwidth]{%s}\\end{center}' % (width, os.path.abspath(fig))
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
        self.text = [x.strip() for x in self.text if x and x.strip()]
        self.text = [x if x.startswith('<h') else x + '<br />' for x in self.text]
        return '''
<!DOCTYPE html>
<html><head><title>{} | {}</title>
{}
</head><body><a name="top"></a>
<div class="frame">
{}
<div class="content">
{}
</div></div></body></html>
        '''.format(self.title, self.author, HTML_STYLE, self.m_title(self.title, self.author), '\n'.join(self.text))

    def m_title(self, title, author):
        return '''
        <div class="top">
        <h1 class="title">{}</h1>
        <h3 class="subsubheading"><em>{}</em></h3>
        </div>
        '''.format(title, author)

    def m_chapter(self, text):
        return '''
        <h1 class="superheading">{}</h1>
        '''.format(text)

    def m_section(self, text):
        return '''
        <h2 class="heading">{}</h2>
        '''.format(text)

    def m_ssection(self, text):
        return '''
        <h3 class="subheading">{}</h3>
        '''.format(text)

    def m_sssection(self, text):
        return '''
        <h3 class="subsubheading"><em>{}</em></h3>
        '''.format(text)
