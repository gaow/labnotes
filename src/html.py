#!/usr/bin/env python
# -*- coding: utf-8 -*-
from .style import HTML_STYLE, HTML_SYN
from .base import *
from collections import OrderedDict

class Html(HtmlParser):
    def __init__(self, title, author, toc, filename, columns, long_ref = True, fig_path = ''):
        HtmlParser.__init__(self, title, author, filename, long_ref)
        self.toc = toc
        if columns == 2:
            self.frame = 'two-col'
        elif columns == 3:
            self.frame = 'three-col'
        else:
            self.frame = 'frame'
        self.dtoc = OrderedDict()
        self.fig_tag = 'html'
        self.fig_path = fig_path
        self.text = self.m_parseBlocks(self.text)
        self.m_parseComments()
        self.m_parseText()
        self.m_parseBib()
        self.text.append(self.textbib)

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
                cmd = '\n'.join(self.text[idx:i])
                self.text[idx] = self._parsecmd(cmd, idx)
                if len(self.text[idx:i]) > 1:
                    for j in range(idx + 1, i):
                        self.text[j] = ''
                idx = i
                continue
            if self.text[idx].startswith(self.mark * 3) and self.text[idx+1].startswith(self.mark + '!') and self.text[idx+2].startswith(self.mark * 3):
                # chapter
                chapter = self.capitalize(self.m_recode(self.text[idx + 1][len(self.mark)+1:]))
                cnt_chapter += 1
                self.dtoc['chapter_{0}'.format(cnt_chapter)] = chapter
                self.text[idx] = ''
                self.text[idx + 1] = self.m_chapter(chapter, cnt_chapter)
                self.text[idx + 2] = ''
                idx += 3
                continue
            if self.text[idx].startswith(self.mark * 3) and self.text[idx+1].startswith(self.mark) and (not self.text[idx+1].startswith(self.mark * 2)) and self.text[idx+2].startswith(self.mark * 3):
                # section
                section = self.capitalize(self.m_recode(self.text[idx + 1][len(self.mark):]))
                cnt_section += 1
                self.dtoc['section_{0}'.format(cnt_section)] = section
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
                self.dtoc['subsection_{0}'.format(cnt_subsection)] = subsection
                self.text[idx] = self.m_ssection(subsection, cnt_subsection)
                idx += 1
                continue
            if self.text[idx].startswith(self.mark + '*'):
                # fig: figure.png 0.9
                self.text[idx] = self.insertFigure(self.text[idx], support = self.fig_support,
                                                   tag = self.fig_tag, remote_path = self.fig_path)
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
            self.textbib += '<p id="footnote-{0}">[{1}]: {2}</p>\n'.format(k, self.bib[k][0], self.bib[k][1])

    def get(self, include_comment, separate, text_only = False):
        if include_comment and len(self.comments) > 0:
            for idx in range(len(self.text)):
                for item in self.comments:
                    if idx in range(item[0], item[1]):
                        self.text[idx] = ''
                        break
        self.text = [x.strip() for x in self.text if x and x.strip()]
        if text_only:
            return '\n'.join(self.text), '', ''
        otext = '<!DOCTYPE html><html><head><title>{0}</title>\n'.format((self.title + ' | ' + self.author) if self.title or self.author else '')
        if separate:
            otext += '<link href="style.css" rel="stylesheet" type="text/css">'
        else:
            otext += '<style type="text/css">\n{0}</style>'.format(HTML_STYLE)
        # syntax highlight and mathjax support
        otext += HTML_SYN
        otext += '</head><body><a name="top"></a>%s%s<div class="%s"><div class="content">%s</div></div></body></html>' % (self.m_title(self.title, self.author),
                       (self.m_toc(self.dtoc) if self.toc else ''),
                       self.frame, 
                       '\n'.join(self.text))
        return otext, HTML_STYLE if separate else ''

    def m_title(self, title, author):
        return '''
        <div class="top">
        {0}{1}
        </div>
        '''.format('<h1 class="title">{0}</h1>'.format(title) if title else '', '<div class="author" >Edited by {0}, on {1}</div>'.format(author, strftime("%a %d %b %Y %H:%M:%S", localtime())) if author else '')

    def m_chapter(self, text, i):
        return '''
        <h1 class="superheading" id="chapter_{0}">{1}</h1><hr size="5" noshade>
        '''.format(i, text)

    def m_section(self, text, i):
        return '''
        <h2 class="heading" id="section_{0}">{1}</h2>
        '''.format(i, text)

    def m_ssection(self, text, i):
        return '''
        <h3 class="subheading" id="subsection_{0}">{1}</h3>
        '''.format(i, text)

    def m_sssection(self, text):
        return '''
        <h3 class="subsubheading">&#9642; {0}</h3>
        '''.format(text)

    def _csize(self, v, k):
        if k.startswith('chapter'):
            return '<big>{0}</big>'.format(v)
        elif k.startswith('section'):
            return '{0}'.format(v)
        else:
            return '<small>{0}</small>'.format(v)

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
        body = '\n'.join(['<li><span style="{0}">{1}</span><a href="#{2}">{3}</a></li>'.format(self._isize(k), self._csize(v,k),k,'&clubs;') for k, v in list(dtoc.items())])
        return '<div class="frame">' + head + body + tail + '</div>'
