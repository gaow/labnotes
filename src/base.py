#!/usr/bin/env python
# -*- coding: utf-8 -*-
import os, sys, re
from time import strftime, localtime
from collections import OrderedDict
import codecs
from .utils import wraptxt, multispace2tab, getPaper, gettxtfromfile, gettxtfromcmd
from .style import MODE, CONFIG, TITLE, THANK, THEME, DOC_PACKAGES, DOC_CONFIG, HTML_STYLE

FONT = {'bch':'bch',
        'default':'default',
        'serif':'\\sfdefault',
        'tt':'\\ttdefault',
        'roman':'ptm'
    }

SYNTAX = {'r':'R',
          'bash':'sh',
          'python':'py',
          'perl':'pl',
          'latex':'tex',
          'c':'c',
          'cpp':'cpp',
          'sql':'sqlite',
          'php':'php',
          'text':'txt',
          'raw':'txt',
          '$':'txt'
          }

COMMENT = {'r':'#',
          'bash':'#',
          'python':'#',
          'perl':'#',
          'latex':'%',
          'c':'//',
          'cpp':'//',
          'sql':'#',
          'php':'#',
          'text':''
          }

# base class
class TexParser:
    def __init__(self, title, author, fname, long_ref = True):
        self.title = title.replace('\\n', '\n')
        self.author = author.replace('\\n', '\n')
        self.fn = '-'.join(fname)
        self.mark = '#'
        self.text = []
        self.PARSER_RULE = {
                'list':'self.m_blockizeList',
                'table':'self.m_blockizeTable',
                'out':'self.m_blockizeOut'
                }
        for item in list(set(SYNTAX.keys())):
            self.PARSER_RULE[item] = 'self.m_blockizeIn'
        for item in ['warning', 'tip', 'important', 'note']:
            self.PARSER_RULE[item] = 'self.m_blockizeAlert'
        self.comments = []
        self.keywords = ['list', 'table']
        self.bib = {}
        self.textbib = ''
        self.footnote = False
        self.tablefont = 'footnotesize'
        # dirty place holders ....
        self.blockph = 'TIGERNOTEBLOCKUGLYPLACEHOLDER'
        self.rawph = 'TIGERNOTERAWPATTERNUGLYPLACEHOLDER'
        self.pause = False
        self.fig_support = ['jpg','pdf','png', 'eps']
        self.fig_tag = 'tex'
        self.long_ref = long_ref

    def capitalize(self, text):
        omit = ["a", "an", "the", "and", "but", "or", "nor", "as", "at", "by", "for", "in", "of", "on", "to", "but", "cum", "mid", "off", "per", "qua", "re", "up", "via", "to", "from", "into", "onto", "with", "within", "without"]
        text = text.split()
        if len(text) == 0:
            return ''
        # first word capitalized anyways
        out = text[0][0].upper() + (text[0][1:] if len(text[0]) > 1 else '')
        # omit keywords for the rest
        if len(text) > 1:
            out += ' ' + ' '.join([x[0].upper() + (x[1:] if len(x) > 1 else '') if x not in omit else x for x in text[1:]])
        return out

    def m_recode(self, line):
        # the use of ? is very important
        #>>> re.sub(r'@@(.*)@@', r'\\texttt{\1}', line)
        #'\\texttt{aa@@, @@aabb}'
        #>>> re.sub(r'@@(.*?)@@', r'\\texttt{\1}', line)
        #'\\texttt{aa}, \\texttt{aabb}'
        if not line:
            return ''
        line = line.strip()
        raw = []
        # support for raw latex syntax
        pattern = re.compile(r'{\$(.*?)\$}')
        for m in re.finditer(pattern, line):
            line = line.replace(m.group(0), "{0}{1}E".format(self.rawph, len(raw)))
            raw.append(m.group(1))
        # DOI online lookup
        pattern = re.compile('@DOI://(.*?)@')
        for m in re.finditer(pattern, line):
            line = line.replace(m.group(0), getPaper(m.group(1), self.long_ref))
        # latex keywords
        for item in [('\\', '!!\\backslash!!'),('$', '\$'),('!!\\backslash!!', '$\\backslash$'),
                ('{', '\{'),('}', '\}'),('%', '\%'), ('_', '\-\_'),('|', '$|$'),('&', '\&'),('<', '$<$'),
                ('>', '$>$'),('~', '$\sim$'), ('^', '\^{}'), ('#', '\#')]:
            line = line.replace(item[0], item[1])
        line = re.sub(r'"""(.*?)"""', r'\\textbf{\\textit{\1}}', line)
        line = re.sub(r'""(.*?)""', r'\\textbf{\1}', line)
        line = re.sub(r'"(.*?)"', r'\\textit{\1}', line)
        line = re.sub(r'@@(.*?)@@', r'\\texttt{\1}', line)
        # url
        pattern = re.compile('@(\S*?)@')
        for m in re.finditer(pattern, line):
            line = line.replace(m.group(0), '\\url{%s}' % m.group(1).replace('\-\_', '\_').replace('$\sim$', '~'))
        # citation
        # [note|reference] defines the pattern for citation.
        # Will have to use [note$|$reference] here since '|' was previously replaced by $|$
        pattern = re.compile('\[(\s*)(?P<a>.+?)(\s*)\$\|\$(\s*)(?P<b>.+?)(\s*)\]')
        # re.compile('\[(.+?)\|(.+?)\]')
        for m in re.finditer(pattern, line):
            if not self.footnote:
                k = re.sub('\W', '', m.group('a'))
                if not k:
                    self.quit("Invalid citation keyword for reference item '{0}'.".format(m.group('b')))
                if k in list(self.bib.keys()):
                    if self.bib[k] != [m.group('a'), m.group('b')]:
                        k += str(len(list(self.bib.keys())))
                self.bib[k] = [m.group('a'), m.group('b')]
                #line = line.replace(m.group(0), '\\cite[%s]{%s}' % (m.group('a'), k))
                line = line.replace(m.group(0), '{\\color{MidnightBlue}%s}~\\cite{%s}' % (m.group('a'), k))
            else:
                line = line.replace(m.group(0), '{\\color{MidnightBlue}%s}~\\footnote{%s}' % (m.group('a'), '\\underline{' + m.group('a') + '} ' + m.group('b')))
        # recover raw latex syntax
        for i in range(len(raw)):
            line = line.replace("{0}{1}E".format(self.rawph, i), raw[i])
        return line

    def _bulkreplace(self, text, start, end, nestedtext):
        end += 1
        if (end - start) > len(nestedtext):
            for i in range(start, end):
                j = i - start
                if j < len(nestedtext):
                    text[i] = nestedtext[j]
                else:
                    text[i] = None
        else:
            self.quit('This is a bug in _bulkreplace() function. Please report it to Gao Wang.')
        return [x for x in text if x is not None]

    def m_parseBlocks(self, text):
        idx = 0
        while True:
            if idx >= len(text):
                break
            if text[idx].startswith(self.mark + '{$') and '$}' in text[idx]:
                idx += 1
                continue
            if text[idx].startswith(self.mark + '}') and '--' not in text[idx]:
                self.quit("Invalid use of '%s' without previous %s{, near %s" % \
                        (text[idx], self.mark, text[idx+1] if idx + 1 < len(text) else "end of document"))
            if text[idx].startswith(self.mark + '{') and '--' not in text[idx]:
                # define block
                bname = text[idx].split('{')[1].strip()
                try:
                    # blabel only applicable to some input boxes
                    bname, blabel = bname.split(None, 1)
                except:
                    blabel = None
                if bname not in [x for x in self.keywords]:
                    self.quit("Invalid block definition '%s{ %s'" % (self.mark, bname))
                # find block end
                endidx = None
                text[idx] = ''
                base = 0
                for i in range(idx + 1, len(text)):
                    # nested block identified
                    if text[i].startswith(self.mark + '{'):
                        if '--' in text[i]:
                            self.quit('Invalid use of "%s{----" within block environment, near %s' % \
                                (self.mark, self.text[i+1] if i + 1 < len(self.text) else "end of document"))
                        base += 1
                    # block end identified
                    if text[i].startswith(self.mark + '}'):
                        if text[i].rstrip() == self.mark + '}':
                            if base == 0:
                                endidx = i
                                break
                            else:
                                base -= 1
                        else:
                            self.quit("Invalid %s '%s', near %s" % \
                                    ('nested use of' if '--' in text[i] else 'symbol', text[i], text[i+1] if idx + 1 < len(text) else "end of document"))
                if not endidx:
                    # end of block not found
                    self.quit("'%s{ %s' and '%s}' must pair properly, near %s" % \
                            (self.mark, bname, self.mark, text[idx+1] if idx + 1 < len(text) else "end of document"))
                if idx + 1 == endidx:
                    # trivial block
                    text.insert(endidx, '\n')
                    endidx += 1
                # block end found, take out this block as new text
                # and apply the recursion
                nestedtext = self.m_parseBlocks(text[idx+1:endidx])
                text = self._bulkreplace(text, idx, endidx, nestedtext)
                newend = idx + len(nestedtext) - 1
                # combine block values
                for i in range(idx + 1, newend + 1):
                    text[idx] += '\n' + text[i]
                del text[(idx + 1) : (newend + 1)]
                # parse the block
                text[idx] = 'BEGIN' + self.blockph + \
                    eval(self.PARSER_RULE[bname])(text[idx], bname, blabel) + \
                    'END' + self.blockph
            #
            idx += 1
        return text

    def m_parseComments(self):
        for idx, item in enumerate(self.text):
            # define comment
            if self.text[idx].startswith(self.mark + '}') and '--' in self.text[idx]:
                self.quit("Invalid use of '%s}----' without previous '%s{----', near %s" % (self.mark, self.mark, self.text[idx+1] if idx + 1 < len(self.text) else "end of document") )
            if item.startswith(self.mark + '{') and '--' in item:
                endidx = None
                for i in range(idx+1, len(self.text)):
                    if self.text[i].startswith(self.mark + '{') and '--' in self.text[i]:
                        self.quit("Nested use of blocks is disallowed: '{0}', near {1}".format(self.text[i], self.text[i+1] if idx + 1 < len(self.text) else "end of document"))
                    if self.text[i].startswith(self.mark + '}') and '--' in self.text[i]:
                        endidx = i
                        break
                if not endidx:
                    self.quit('Comment blocks must appear in pairs, near {0}'.format(self.text[i+1] if idx + 1 < len(self.text) else "end of document"))
                self.comments.append([idx, endidx])
                self.text[idx] = ''
                self.text[endidx] = ''
        return

    def _holdblockplace(self, text, mode = 'remove', rule = {}):
        # there should be better way to make sure the existing block not to be modified but will use this solution for now
        mapping = {}
        if mode == 'hold':
            text = re.split('({0}|{1})'.format('BEGIN' + self.blockph, 'END' + self.blockph), text)
            idxes = [0]
            i = 1
            while i < len(text):
                if text[i] == 'BEGIN' + self.blockph:
                    # block identified
                    try:
                        flag = self.blockph not in text[i+1] and text[i+2] == 'END' + self.blockph
                        if not flag: raise ValueError("invalid block flag found")
                    except:
                        self.quit("This is a bug in _holdblockplace() function. Please report it to Gao Wang.")
                    # block checked
                    text[i] = self.blockph + str(i) + 'E'
                    mapping[text[i]] = text[i+1]
                    idxes.append(i)
                    # block skipped
                    i += 3
                else:
                    # no block identified
                    idxes.append(i)
                    i += 1
            text = ''.join([item for idx, item in enumerate(text) if idx in idxes])
        elif mode == 'release':
            mapping = rule
            for k, item in list(mapping.items()):
                text = text.replace(k, item)
        elif mode == 'remove':
            text = re.sub(r'{0}|{1}'.format('BEGIN' + self.blockph, 'END' + self.blockph), '', text)
        return text, mapping

    def _holdfigureplace(self, text):
        pattern = re.compile('#\*(.*?)(\n|$)')
        for m in re.finditer(pattern, text):
            fig = 'BEGIN' + self.blockph + self.insertFigure(m.group(1), support = self.fig_support, tag = self.fig_tag) + 'END' + self.blockph + '\n'
            text = text.replace(m.group(0), fig, 1)
        return text

    def insertFigure(self, text, support = ['jpg','pdf','png'], tag = 'tex', remote_path = ''):
        if text.startswith(self.mark + '*'):
            text = text[len(self.mark)+1:].strip()
        else:
            text = text.strip()
        if not text:
            return ''
        lines = [x.strip() for x in text.split(';') if x.strip()]
        for idx, line in enumerate(lines):
            try:
                fig, width = line.split()
                width = float(width)
            except ValueError:
                fig = line.split()[0]
                width = 0.9
            if (not tag.endswith('wiki')) and width > 1:
                width = 0.9
            fname = os.path.split(fig)[-1]
            if not '.' in fname:
                self.quit("Cannot determine graphic file format for '{0}'. Valid extensions are {1}".format(fname, ' '.join(support)))
            extension = fname.split('.')[-1]
            if extension.lower() not in support:
                self.quit("Input file format '{0}' not supported. Valid extensions are {1}".format(extension, ' '.join(support)))
            if not os.path.exists(fig):
                self.quit("Cannot find file %s" % fig)
            # syntax images
            if tag == 'tex':
                lines[idx] = '\\includegraphics[width=%s\\textwidth]{%s}\n' % (width, os.path.abspath(fig))
            elif tag == 'html':
                if extension == 'pdf':
                    lines[idx] = '<a style="text-shadow: 1px 1px 1px #999;" href="{0}">{1}</a>\n'.format(os.path.join(remote_path, fname), 'Download Image "{0}"'.format(fname))
                else:
                    lines[idx] = '<p><center><img src="{0}" alt="{1}" width="{2}%" /></center></p>'.format(fig, fname, int(width * 100))
            elif tag.endswith("wiki"):
                if tag == 'dokuwiki':
                    # dokuwiki style 
                    if extension == 'pdf':
                        lines[idx] = "[[{0}|{1}]]\n".format(os.path.join(remote_path, fname), 'Download Image "{0}"'.format(fname))
                    else:
                        sep = ':' if not '://' in remote_path else '/'
                        lines[idx] = '{{%s%s%s?%s}}' % (remote_path, sep, fname, width) 
                if tag == 'pmwiki':
                    if extension == 'pdf':
                        lines[idx] = "[[{0}|{1}]]\n".format(os.path.join(remote_path, fname), 'Download Image "{0}"'.format(fname))
                    else:
                        lines[idx] = '%center% Attach:%s' % (fname)
            else:
                self.quit('Unknown tag for figure {0}'.format(tag))
        if tag == 'tex':
            if len(lines) > 1:
                w_minipage = int(1.0 / (1.0 * len(lines)) * 90) / 100.0
                lines = ['\\subfigure{' + x + '}\n' for x in lines]
                lines[0] = '\\begin{figure}[H]\n\\centering\n\\mbox{\n' + lines[0]
                lines[-1] += '\n}\n\\end{figure}\n'
            else:
                lines[0] = '\\begin{figure}[H]\n\\centering\n' + lines[0]
                lines[-1] += '\\end{figure}\n'
        return '\n'.join(lines)

    def _checknest(self, text, kw=None):
        pattern = re.compile('{0}(.*?){1}'.format('BEGIN' + self.blockph, 'END' + self.blockph), re.DOTALL)
        # re.match() will not work here
        # will not work without re.DOTALL
        for m in re.finditer(pattern, text):
            if m:
                e = m.group(1)
                if kw is None:
                    self.quit('Cannot nest this blocks here:\n{0}'.format(e[:max(200, len(e))]))
                else:
                    for k in kw:
                        if re.search(k, '%r' % e):
                            self.quit('Cannot nest this blocks here:\n{0}'.format(e[:max(200, len(e))]))
        return

    def _checkblockprefix(self, text):
        for item in text.split('\n'):
            if item.strip() and (not (item.startswith(self.blockph) or item.startswith(self.mark))):
                self.quit('Items must start with "{0}" in this block. Problematic text is: "{1}"'.format(self.mark, item))
        return

    def m_blockizeList(self, text, k, label = None):
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
                text[idx] = re.sub(r'^{0}'.format(self.mark * 2), '\\item ', text[idx])
                if idx + 1 < len(text):
                    for j in range(idx + 1, len(text) + 1):
                        try:
                            if not text[j].startswith(self.mark * 2):
                                break
                            else:
                                text[j] = self.mark * 2 + self.m_recode(text[j][2:])
                                text[j] = re.sub(r'^{0}'.format(self.mark * 2), '\\item ', text[j])
                                end = j
                        except IndexError:
                            pass
                #
                text[start] = '\\begin{itemize}\n' + text[start]
                text[end] = text[end] + '\n\\end{itemize}'
                idx = end + 1
            elif text[idx].startswith(self.mark):
                text[idx] = self.mark + self.m_recode(text[idx][1:])
                idx += 1
            else:
                text[idx] = self.m_recode(text[idx])
                idx += 1
        # handle 1st level indentation
        text = '\n'.join([x if x.startswith(self.blockph) else re.sub(r'^{0}'.format(self.mark), '\\item ', x) for x in text])
        text = self._holdblockplace(text, mode = 'release', rule = mapping)[0]
        text = '\\begin{itemize}\n%s\n\\end{itemize}\n' % text
        # this is for beamer \pause option
        if self.pause:
            text = text.replace('\\item -', '\\pause \\item ')
        return text

    def m_blockizeTable(self, text, k, label = None):
        self._checknest(text)
        table = [['\seqsplit{{{}}}'.format(self.m_recode(iitem).replace(' ', '~')) if len([x for x in iitem if x == ' ']) > 2 else self.m_recode(iitem) for iitem in multispace2tab(item).split('\t')] for item in text.split('\n') if item]
        ncols = list(set([len(x) for x in table]))
        nseqsplit = max([len([iitem for iitem in item if iitem.startswith('\\seqsplit')]) for item in table])
        if len(ncols) > 1:
            self.quit("Number of columns not consistent for table. Please replace empty columns with placeholder symbol, e.g. '-'. {0}".format(text))
        try:
            cols = ''.join(['c' if len([item[i] for item in table if item[i].startswith('\\seqsplit')]) == 0 else 'p{{{}pt}}'.format((480-(ncols[0]-nseqsplit)*10)/nseqsplit) for i in range(ncols[0])])
            head = '\\begin{center}\n{\\%s\\begin{longtable}{%s}\n\\hline\n' % (self.tablefont, cols)
            body = '&'.join(table[0]) + '\\\\\n' + '\\hline\n' + '\\\\\n'.join(['&'.join(item) for item in table[1:]]) + '\\\\\n'
            tail = '\\hline\n\\end{longtable}}\n\\end{center}\n'
        except IndexError:
            return ''
        return head + body + tail

    def m_parseBib(self):
        if not self.bib:
            return
        self.textbib = '\\begin{thebibliography}{9}\n'
        bibkeys = []
        #unique, ordered reference list
        for line in self.text:
            bibkeys.extend([m.group(1) for m in re.finditer(re.compile('\\cite{(.*?)}'), line)])
        seen = set()
        for k in [x for x in bibkeys if x not in seen and not seen.add(x)]:
            self.textbib += '\\bibitem{%s}\n[%s]\\\\%s\n' % (k, self.bib[k][0], self.bib[k][1])
        self.textbib += '\\end{thebibliography}'

    def get(self, include_comment):
        return 'None'

    def quit(self, msg):
        sys.exit('\033[91mAn ERROR has occured while processing input text "{0}":\033[0m\n\t '.format(self.fn) + msg)


class HtmlParser(TexParser):
    def __init__(self, title, author, filename, header=False, long_ref=True):
        TexParser.__init__(self, title, author, filename, long_ref)
        self.text = []
        for fn in filename:
            try:
                with codecs.open(fn, 'r', encoding='UTF-8', errors='ignore') as f:
                    #lines = [l.rstrip() for l in f.readlines() if l.rstrip()]
                    lines = [l.rstrip() for l in f.readlines()]
                self.text.extend(lines)
            except IOError as e:
                sys.exit(e)
        self.alertbox = ['warning', 'tip', 'important', 'note']
        self.keywords = list(set(SYNTAX.keys())) + self.alertbox + ['err', 'out', 'list', 'table']
        self.wrap_width = 90
        self.tablefont = 'small'
        self.fig_support = ['jpg', 'jpeg', 'tif','png', 'pdf']
        self.html_tag = False
        if header:
            # the header be title and author embedded
            if author:
                self.text.insert(0, '{1}{0}, {2}'.format(author, self.mark, strftime("%a %d %b %Y %H:%M:%S", localtime())))
            if title:
                self.text = [self.mark * 3, '{0}!{1}'.format(self.mark, title), self.mark * 3] + self.text

    def _parseUrlPrefix(self, text):
        prefix = re.search(r'^(.+?)://', text)
        if prefix:
            return prefix.group(0), text.replace(prefix.group(0), '')
        else:
            return 'http://', text

    def _parseUrl(self, line):
        pattern = re.compile('@(\S*?)@')
        for m in re.finditer(pattern, line):
            prefix, address = self._parseUrlPrefix(m.group(1))
            line = line.replace(m.group(0), '<a href="{0}{1}">{1}</a>'.format(prefix, address, address))      
        return line

    def _parsecmd(self, line, idx):
        return '<pre><code class = "nohighlight">{}</code></pre>\n'.\
          format(wraptxt(line, '\\', int(self.wrap_width)))
        
    def m_recode(self, line):
        if not line:
            return ''
        line = line.strip()
        raw = []
        # support for raw html syntax/symbols
        pattern = re.compile(r'{\$(.*?)\$}')
        for m in re.finditer(pattern, line):
            line = line.replace(m.group(0), "{0}{1}E".format(self.rawph, len(raw)))
            raw.append(m.group(1))
        # DOI online lookup
        pattern = re.compile('@DOI://(.*?)@')
        for m in re.finditer(pattern, line):
            line = line.replace(m.group(0), getPaper(m.group(1), self.long_ref))
        # html keywords
        # no need to convert most of them
        for item in [
               # ('\\', '&#92;'),('$', '&#36;'),
               # ('{', '&#123;'),('}', '&#125;'),
               # ('%', '&#37;'),('--', '&mdash;'),
               # ('-', '&ndash;'),('&', '&amp;'),
               # ('~', '&tilde;'),('^', '&circ;'),
               # ('``', '&ldquo;'),('`', '&lsquo;'),
               # ('#', '&#35;'),
                ('<', '&lt;'),('>', '&gt;'),
                ]:
            line = line.replace(item[0], item[1])
        line = re.sub(r'"""(.*?)"""', r'<strong><em>\1</em></strong>', line)
        line = re.sub(r'""(.*?)""', r'<strong>\1</strong>', line)
        line = re.sub(r'"(.*?)"', r'<em>\1</em>', line)
        # line = re.sub(r'@@(.*?)@@', r'<span style="font-family: monospace">\1</span>', line)
        line = re.sub(r'@@(.*?)@@', r'<kbd>\1</kbd>', line)
        # single/double quotes translated from latex syntax
        line = re.sub(r"``(.*?)''", r'"\1"', line)
        line = re.sub(r"`(.*?)'", r"'\1'", line)
        # footnote and hyperlink
        # [note|reference] defines the pattern for citation.
        pattern = re.compile('\[(\s*)(?P<a>.+?)(\s*)\|(\s*)(?P<b>.+?)(\s*)\]')
        # re.compile('\[(.+?)\|(.+?)\]')
        for m in re.finditer(pattern, line):
            # [text|@link@] defines the pattern for direct URL.
            if re.match(r'(\s*)@(\S*?)@(\s*)', m.group('b')):
                prefix, address = self._parseUrlPrefix(m.group('b').strip()[1:-1])
                line = line.replace(m.group(0), '<a style="text-shadow: 1px 1px 1px #999;" href="{0}{1}">{2}</a>'.format(prefix, address, m.group('a')))
            else:
                k = re.sub('\W', '', m.group('a'))
                if not k:
                    self.quit("Invalid citation keyword for reference item '{0}'.".format(m.group('b')))
                if k in list(self.bib.keys()):
                    if self.bib[k] != [m.group('a'), m.group('b')]:
                        k += str(len(list(self.bib.keys())))
                self.bib[k] = [m.group('a'), self._parseUrl(m.group('b'))]
                line = line.replace(m.group(0), '<a href="#footnote-{0}">{1}</a>'.format(k, m.group('a')))
        # standalone url
        line = self._parseUrl(line)
        # recover raw html syntax
        for i in range(len(raw)):
            line = line.replace("{0}{1}E".format(self.rawph, i), raw[i])
        return line.strip()

    def m_blockizeList(self, text, k, label = None):
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
        text = '<ul>\n%s\n</ul>\n' % text
        if self.html_tag:
            return '<HTML>\n' + text + '\n</HTML>\n'
        else:
            return text
        
    def m_blockizeTable(self, text, k, label = None):
        self._checknest(text)
        table = [[self.m_recode(iitem) for iitem in multispace2tab(item).split('\t')] for item in text.split('\n') if item]
        ncols = list(set([len(x) for x in table]))
        if len(ncols) > 1:
            self.quit("Number of columns not consistent for table. Please replace empty columns with placeholder symbol, e.g. '-'. {0}".format(text))
        start = '<td style="vertical-align: top;"><{0}>'.format(self.tablefont)
        end = '<br /></{0}></td>'.format(self.tablefont)
        head = '<center><table><tbody>'
        body = []
        line = ''
        try:
            for cell in table[0]:
                line += start + '<b>' + cell + '</b>' + end + '\n'
            body.append(line)
            for item in table[1:]:
                line = ''
                for cell in item:
                    line += start + cell + end + '\n'
                body.append(line)
        except IndexError:
            # emtpy table
            pass
        #
        for idx, item in enumerate(body):
            if idx % 2:
                body[idx] = '<tr>' + item + '</tr>'
            else:
                body[idx] = '<tr class="dark">' + item + '</tr>'
        tail = '</tbody></table></center>\n'
        text = head + '\n'.join(body) + tail
        if self.html_tag:
            return '<HTML>\n' + text + '\n</HTML>\n'
        else:
            return text

        
    def m_blockizeIn(self, text, k, label = None):
        if text.startswith("file:///"): text = gettxtfromfile(text) 
        if text.startswith("output:///"): text = gettxtfromcmd(text) 
        if k.lower() == 'raw' or k.lower() == '$': return text
        self._checknest(text)
        text = wraptxt(text, '', int(self.wrap_width), rmblank = True,
                       prefix = COMMENT[k.lower()])
        text = '<pre><code class = "{0}">{3}{3}\n{3}{3} LANGUAGE: {0}, ID: {2}\n{3}{3}\n{1}</code></pre>'.\
          format(k.lower(), text, label if label else k.lower(), COMMENT[k.lower()])
        if self.html_tag:
            return '<HTML>\n' + text + '\n</HTML>\n'
        else:
            return text

    def m_blockizeOut(self, text, k, label = None):
        if text.startswith("file:///"): text = gettxtfromfile(text) 
        if text.startswith("output:///"): text = gettxtfromcmd(text)
        self._checknest(text)
        nrow = len(text.split('\n'))
        text = '<center><textarea rows="%s", wrap="off">%s</textarea></center>' % (max(min(nrow, 30), 1), text)
        if self.html_tag:
            return '<HTML>\n' + text + '\n</HTML>\n'
        else:
            return text
        
    def m_blockizeAlert(self, text, k, label = None):
        self._checknest(text, kw = [r'id="wrapper"'])
        text = self._holdfigureplace(text)
        text, mapping = self._holdblockplace(text, mode = 'hold')
        self._checkblockprefix(text)
        text = '\n'.join([item if item.startswith(self.blockph) else self.m_recode(re.sub(r'^{0}'.format(self.mark), '', item)) for item in text.split('\n')])
        text = self._holdblockplace(text, mode = 'release', rule = mapping)[0]
        text = '<center><div id="wrapper"><div class="{0}"><div style="font-family:\'PT Sans\', comic sans ms;text-align:center;text-decoration:underline{3}; margin-bottom:3px">{1}</div>{2}</div></div></center>'.\
                        format(k.lower(), k.capitalize() if not label else self.m_recode(label), text, ';color:red' if k.lower() == 'warning' else '')
        if self.html_tag:
            return '<HTML>\n' + text + '\n</HTML>\n'
        else:
            return text
