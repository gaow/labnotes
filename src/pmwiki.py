#!/usr/bin/env python
# -*- coding: utf-8 -*-
from .base import *
def mathjaxphp_convert(item):
    item = re.sub(r'\$(.*?)\$', r'{$\1$}', item)
    item = re.sub(r'\\\((.*?)\\\)', r'{$\1$}', item)
    item = re.sub(r'\\\[(.*?)\\\]', r'{$$\1$$}', item)
    return item
    
class Pmwiki(HtmlParser):
    def __init__(self, title, author, fname, toc, img_path):
        HtmlParser.__init__(self, title, author, fname, header=True)
        self.toc = toc
        self.fig_tag = "Pmwiki"
        if img_path is None:
            self.img_path = ''
        else:
            self.img_path = img_path
        self.hasfn = False
        self.text = self.m_parseBlocks(self.text)
        self.m_parseComments()
        self.m_parseText()

    def _parseUrl(self, line):
        pattern = re.compile('@(.*?)@')
        for m in re.finditer(pattern, line):
            line = line.replace(m.group(0), '[[' + m.group(1) + ']]')
        return line
        
    def m_recode_pmwiki(self, line):
        # the use of ? is very important
        #>>> re.sub(r'@@(.*)@@', r'\\texttt{\1}', line)
        #'\\texttt{aa@@, @@aabb}'
        #>>> re.sub(r'@@(.*?)@@', r'\\texttt{\1}', line)
        #'\\texttt{aa}, \\texttt{aabb}'
        if not line:
            return ''
        line = line.rstrip()
        raw = []
        # support for raw latex syntax
        pattern = re.compile(r'{\$(.*?)\$}')
        for m in re.finditer(pattern, line):
            line = line.replace(m.group(0), "{0}{1}E".format(self.rawph, len(raw)))
            raw.append(m.group(1))
        # DOI online lookup
        pattern = re.compile('@DOI://(.*?)@')
        for m in re.finditer(pattern, line):
            line = line.replace(m.group(0), getPaper(m.group(1)))
        line = re.sub(r'"""(.*?)"""', r"''''\1''''", line)
        line = re.sub(r'""(.*?)""', r"'''\1'''", line)
        line = re.sub(r'"(.*?)"', r"''\1''", line)
        line = re.sub(r'@@(.*?)@@', r"MONOSPACEPLACEHOLDERSTART\1MONOSPACEPLACEHOLDEREND", line)
        # single/double quotes translated from latex syntax
        line = re.sub(r"``(.*?)''", r'"\1"', line)
        line = re.sub(r"`(.*?)'", r"'\1'", line)
        # footnote and link
        pattern = re.compile('\[(\s*)(?P<a>.+?)(\s*)\|(\s*)(?P<b>.+?)(\s*)\]')
        for m in re.finditer(pattern, line):
            if re.match(r'(\s*)@(.*?)@(\s*)', m.group('b')):
                # is a link (internal or external). Have to flip this into [link|link name]
                line = line.replace(m.group(0), '[[{1}|{0}]]'.\
                                        format(m.group('a'),
                                               re.sub(r'^(\s*)@|@(\s*)$', '', m.group('b'))))
            else:
                # is footnote
                self.hasfn = True
                line = line.replace(m.group(0), m.group('a') + '[^{0}^]'.format(self._parseUrl(m.group('b'))))
        # url
        line = self._parseUrl(line)
        # recover monospace
        line = re.sub(r'MONOSPACEPLACEHOLDERSTART(.*?)MONOSPACEPLACEHOLDEREND', r'@@\1@@', line)
        # recover raw latex syntax
        for i in range(len(raw)):
            #  {$$ ... $$} and {$...$} for MathJax.php for pmwiki, have to replace to that
            item = mathjaxphp_convert(raw[i])
            line = line.replace("{0}{1}E".format(self.rawph, i), item)
        return line

    def m_blockizeList(self, text, k, label = None):
        text = self._holdfigureplace(text)
        text, mapping = self._holdblockplace(text, mode = 'hold')
        self._checkblockprefix(text)
        text = text.split('\n')
        text = '\n'.join([x if x.startswith(self.blockph) else self.m_recode_pmwiki(re.sub(r'^{0}'.format(self.mark), '*\t', re.sub(r'^{0}'.format(self.mark*2), '**\t', x))) for x in text]) + '\n'
        text = self._holdblockplace(text, mode = 'release', rule = mapping)[0]
        return text

    def m_blockizeTable(self, text, k, label = None):
        self._checknest(text)
        table = [[self.m_recode(iitem) for iitem in multispace2tab(item).split('\t')] for item in text.split('\n') if item]
        ncols = list(set([len(x) for x in table]))
        if len(ncols) > 1:
            self.quit("Number of columns not consistent for table. Please replace empty columns with placeholder symbol, e.g. '-'. {0}".format(text))
        body = '|| border=1 align=center width=80%\n' + '||! ' + ' ||! '.join(table[0]) + ' ||\n' + '\n'.join(['|| ' + ' || '.join(item) + ' ||' for item in table[1:]]) + '\n' 
        return body

    def _parsecmd(self, text, serial, numbered = False):
        head = '>>cmd<<\n[@\n'
        lines = '\n'.join(text)
        tail = '\n@]\n>><<\n'
        return head + lines + tail
        
    def m_blockizeIn(self, text, k, label = None, sxh3 = False):
        if text.startswith("file:///"): text = gettxtfromfile(text) 
        if k.lower() == 'raw': return text
        self._checknest(text)
        text = '(:codestart {0}:)\n{1}\n(:codeend:)\n'.format(k.lower(), wraptxt(text, '', 1000, rmblank = True))
        return text
    
    def m_blockizeOut(self, text, k, label = None):
        if text.startswith("file:///"): text = gettxtfromfile(text) 
        self._checknest(text)
        text = '>>frame<<\n[@\n{0}\n@]\n>><<\n'.format(text)
        return text
        
    def m_blockizeAlert(self, text, k, label = None):
        self._checknest(text, kw = [r'>>tip|>>warning|>>important|>>note'])
        text = self._holdfigureplace(text)
        text, mapping = self._holdblockplace(text, mode = 'hold')
        self._checkblockprefix(text)
        text = '\n'.join([item if item.startswith(self.blockph) else self.m_recode_pmwiki(re.sub(r'^{0}'.format(self.mark), '', item)).lstrip() for item in text.split('\n')])
        text = self._holdblockplace(text, mode = 'release', rule = mapping)[0]
        text = '>>{0}<<\n{1}\n>><<\n'.format(k.lower(), text)
        return text

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
                # chapter as title in pmwiki
                chapter = self.capitalize(self.m_recode_pmwiki(self.text[idx + 1][len(self.mark)+1:]))
                self.text[idx] = ''
                self.text[idx + 1] = '(:title ' + chapter + ' :)' + '\n(:toc:)\n'
                self.text[idx + 2] = ''
                idx += 3
                continue
            if self.text[idx].startswith(self.mark * 3) and self.text[idx+1].startswith(self.mark) and (not self.text[idx+1].startswith(self.mark * 2)) and self.text[idx+2].startswith(self.mark * 3):
                # section
                section = self.capitalize(self.m_recode_pmwiki(self.text[idx + 1][len(self.mark):]))
                self.text[idx] = ''
                self.text[idx + 1] = '!!' + section
                self.text[idx + 2] = ''
                idx += 3
                continue
            if self.text[idx].startswith(self.mark * 2):
                # too many #'s
                self.quit("You have so many urgly '{0}' symbols in a regular line. Please clear them up in this line: '{1}'".format(self.mark, self.text[idx]))
            if self.text[idx].startswith(self.mark + '!!!'):
                # box
                # FIXME
                self.text[idx] = self.m_recode_pmwiki(self.text[idx][len(self.mark)+3:])
                idx += 1
                continue
            if self.text[idx].startswith(self.mark + '!!'):
                # subsection, subsubsection ...
                self.text[idx] = '!!!!' + self.m_recode_pmwiki(self.text[idx][len(self.mark)+2:])
                idx += 1
                continue
            if self.text[idx].startswith(self.mark + '!'):
                # subsection, subsubsection ...
                subsection = self.m_recode_pmwiki(self.text[idx][len(self.mark)+1:])
                self.text[idx] = '!!!' + subsection
                idx += 1
                continue
            if self.text[idx].startswith(self.mark + '*'):
                # fig: figure.png 0.9
                self.text[idx] = self.insertFigure(self.text[idx], support = self.fig_support, tag = self.fig_tag, remote_path = self.img_path)
                idx += 1
                continue
            if self.text[idx].startswith(self.mark):
                # a plain line here
                self.text[idx] = self.m_recode_pmwiki(self.text[idx][len(self.mark):]) + '\n'
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
        # do not use strip at all, for pmwiki
        self.text = [x.lstrip() for x in self.text if x.lstrip()]
        otext = '\n'.join(self.text)
        if self.hasfn:
            otext += '\n[^#^]\n'
        if not self.toc:
            otext = otext.replace('(:toc:)', '')
        return otext
