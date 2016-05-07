#!/usr/bin/env python3
# -*- coding: utf-8 -*-
import os, re, hashlib, codecs
from .utils import env, getPaper, multispace2tab, \
     gettxtfromfile, gettxtfromcmd
from .encoder import FigureInserter, M, SYNTAX

BLOCKS = ['list', 'table', 'out', 'warning', 'tip',
          'important', 'note'] + list(SYNTAX.keys())
FIGTYPES = ['jpg', 'png', 'jpeg', 'pdf']

class Element:
    def __init__(self, start, end):
        self.start = start
        self.end = end

class Table(Element):
    def __init__(self, start, end, name):
        Element.__init__(start, end)
        self.name = name

class Code(Element):
    def __init__(self, start, end, name, description):
        Element.__init__(start, end)
        self.name = name
        self.description = description

class Figure(Element):
    pass

class Raw(Element):
    def __init__(self, start, end, decoration):
        Element.__init__(start, end)
        self.decoration = decoration

class ParserCore:
    '''Main parser framework'''
    def __init__(self, filename, file_format, reference_format, purge_comment,
                 fig_path_adj = ''):
        self.format = file_format
        self.reference_format = reference_format
        self.PH = 'LAB{}NOTES'.format(hashlib.md5(env.precise_time.encode()).hexdigest()[:10])
        # Additional information for different elements in text.
        # Data for each element will be an Element object
        self.code = []
        self.raw = []
        self.table = []
        self.figure = []
        #
        self.dirnames = []
        self.text = []
        self.bib = {}
        for fn in filename:
            self.dirnames.append(os.path.dirname(fn))
            with codecs.open(fn, 'r', encoding='UTF-8', errors='ignore') as f:
                lines = [l.rstrip() for l in f.readlines()]
                # in case I need to parse source code
                if len(lines) > 0 and lines[0].startswith('#!/') \
                  and fn.split('.')[-1].lower() in lines[0].lower():
                    del lines[0]
            self.text.extend(lines)
        self.purge_comment = purge_comment
        self.fig_path_adj = fig_path_adj

    def __call__(self, worker):
        env.logger.info("Evaluating input document ...")
        self.PurgeComment()
        self.text = self.ParseBlock(self.text, worker)
        self.ParseText(worker)
        if not worker.no_ref:
            self.ParseBib(worker)
        return worker.Write(self.text)

    def PurgeComment(self):
        comments = []
        for idx, item in enumerate(self.text):
            # define comment
            if self.text[idx].startswith(M + '}') and '--' in self.text[idx]:
                raise ValueError("Invalid use of ``%s}----`` without previous ``%s{----``, near ``%s``" \
                          % (M, M, self.text[idx+1] if idx + 1 < len(self.text) else "end of document") )
            if item.startswith(M + '{') and '--' in item:
                endidx = None
                for i in range(idx+1, len(self.text)):
                    if self.text[i].startswith(M + '{') and '--' in self.text[i]:
                        raise ValueError("Nested comments not allowed: ``{0}``, near ``{1}``".\
                                         format(self.text[i],
                                                self.text[i+1] if idx + 1 < len(self.text)
                                                else "end of document"))
                    if self.text[i].startswith(M + '}') and '--' in self.text[i]:
                        endidx = i
                        break
                if not endidx:
                    raise ValueError('Comment blocks must appear in pairs, near ``{0}``'.\
                                     format(self.text[i+1] if idx + 1 < len(self.text)
                                            else "end of document"))
                comments.append([idx, endidx])
                self.text[idx] = ''
                self.text[endidx] = ''
        if self.purge_comment:
            for idx in range(len(self.text)):
                for item in comments:
                    if idx in range(item[0], item[1]):
                        self.text[idx] = ''
                        break

    def ParseBlock(self, text, worker):
        idx = 0
        while True:
            if idx >= len(text):
                break
            if text[idx].startswith(M + '{$') and '$}' in text[idx]:
                idx += 1
                continue
            if text[idx].startswith(M + '}') and '--' not in text[idx]:
                raise ValueError("Invalid use of ``%s`` without previous ``%s{``, near ``%s``" % \
                        (text[idx], M, text[idx+1]
                         if idx + 1 < len(text) else "end of document"))
            if text[idx].startswith(M + '{') and '--' not in text[idx]:
                # define block
                name = text[idx].split('{')[1].strip()
                try:
                    # label only applicable to some input boxes
                    name, label = name.split(None, 1)
                except:
                    label = None
                if name not in [x for x in BLOCKS]:
                    raise ValueError("Invalid block definition ``%s{ %s``" % (M, name))
                # find block end
                endidx = None
                text[idx] = ''
                base = 0
                for i in range(idx + 1, len(text)):
                    # nested block identified
                    if text[i].startswith(M + '{'):
                        if '--' in text[i]:
                            raise ValueError('Invalid use of ``%s{----`` inside block, near ``%s``' % \
                                (M, self.text[i+1] if i + 1 < len(self.text)
                                 else "end of document"))
                        base += 1
                    # block end identified
                    if text[i].startswith(M + '}'):
                        if text[i].rstrip() == M + '}':
                            if base == 0:
                                endidx = i
                                break
                            else:
                                base -= 1
                        else:
                            raise ValueError("Invalid %s ``%s``, near ``%s``" % \
                                    ('nested use of' if '--' in text[i] else 'symbol',
                                     text[i], text[i+1] if idx + 1 < len(text)
                                    else "end of document"))
                if not endidx:
                    # end of block not found
                    raise ValueError("``%s{ %s`` and ``%s}`` must pair properly, near ``%s``" % \
                            (M, name, M, text[idx+1] if idx + 1 < len(text)
                             else "end of document"))
                if idx + 1 == endidx:
                    # trivial block
                    text.insert(endidx, '\n')
                    endidx += 1
                # block end found, take out this block as new text
                # and apply the recursion
                nestedtext = self.ParseBlock(text[idx+1:endidx], worker)
                text = self.__ReplaceNested(text, idx, endidx, nestedtext)
                newend = idx + len(nestedtext) - 1
                # combine block values
                for i in range(idx + 1, newend + 1):
                    text[idx] += '\n' + text[i]
                del text[(idx + 1) : (newend + 1)]
                # parse the block
                text[idx] = 'BEGIN' + self.PH + \
                    self.PrepareBlock(text[idx], worker, name, label) + \
                    'END' + self.PH
            #
            idx += 1
        return text

    def ParseText(self, worker):
        skip = []
        for idx, item in enumerate(self.text):
            if self.PH in item:
                self.text[idx] = self.__ReserveBlock(item, mode = 'remove')[0]
                skip.append(idx)
        head = worker.GetDocumentHead()
        if head:
            self.text.insert(0, head)
        idx = 0
        # Keep track of section positions to add some section spec info
        # such as version, date, potentially
        start_subsection = end_subsection = count_chapter = count_section = count_subsection = 0
        while idx < len(self.text):
            if idx in skip or self.text[idx] == '':
                # no need to process
                idx += 1
                continue
            if not self.text[idx].startswith(M):
                # regular cmd text
                if idx + 1 < len(self.text):
                    for i in range(idx + 1, len(self.text) + 1):
                        try:
                            if self.text[i].startswith(M) or i in skip or self.text[i] == '':
                                break
                        except IndexError:
                            pass
                else:
                    i = idx + 1
                self.text[idx] = worker.GetCMD(self.text[idx:i], index = idx)
                for j in range(idx + 1, i):
                    self.text[j] = ''
                idx = i
                continue
            if self.text[idx].startswith(M * 3) and self.text[idx+1].startswith(M + '!') \
              and self.text[idx+2].startswith(M * 3):
                # chapter
                count_chapter += 1
                previous_ended = False
                if start_subsection > end_subsection:
                    previous_ended  = True
                    end_subsection += 1
                self.text[idx] = ''
                self.text[idx + 1] = worker.GetChapter(
                    self.Capitalize(self.Recode(self.text[idx + 1][len(M)+1:], worker)).strip(),
                    add_head = previous_ended, index = count_chapter)
                self.text[idx + 2] = ''
                idx += 3
                continue
            if self.text[idx].startswith(M * 3) and self.text[idx+1].startswith(M) \
              and (not self.text[idx+1].startswith(M * 2)) and self.text[idx+2].startswith(M * 3):
                # section
                count_section += 1
                previous_ended = False
                if start_subsection > end_subsection:
                    previous_ended  = True
                    end_subsection += 1
                self.text[idx] = ''
                self.text[idx + 1] = worker.GetSection(
                    self.Capitalize(self.Recode(self.text[idx + 1][len(M):], worker)).strip(),
                    add_head = previous_ended, index = count_section)
                self.text[idx + 2] = ''
                idx += 3
                continue
            if self.text[idx].startswith(M * 2):
                # too many ugly #'s
                env.logger.warning("If you are sure of two ``{0}{0}`` at the beginning of this line please enter a space between them to get rid of this warning:\n\t``{1}``".format(M, self.text[idx]))
            if self.text[idx].startswith(M + '!!!'):
                # highlight
                self.text[idx] = worker.GetHighlight(self.Recode(self.text[idx][len(M)+3:], worker).strip())
                idx += 1
                continue
            if self.text[idx].startswith(M + '!!'):
                if idx > 0:
                    # for beamer
                    worker.RaiseSubsubsection(self.text[idx - 1])
                # subsubsection
                self.text[idx] = worker.GetSubsubsection(self.Recode(self.text[idx][len(M)+2:], worker).strip())
                idx += 1
                continue
            if self.text[idx].startswith(M + '!'):
                # subsection
                count_subsection += 1
                previous_ended = False
                if start_subsection > end_subsection:
                    previous_ended  = True
                    end_subsection += 1
                start_subsection += 1
                self.text[idx] = worker.GetSubsection(self.Recode(self.text[idx][len(M)+1:], worker).strip(),
                                                      add_head = previous_ended, index = count_subsection)
                idx += 1
                continue
            if self.text[idx].startswith(M + '*'):
                # fig: figure.pdf 0.9
                self.text[idx] = FigureInserter(self.text[idx], support = FIGTYPES,
                                                tag = self.format, path_adj = self.fig_path_adj).Insert()
                idx += 1
                continue
            if self.text[idx].startswith(M):
                # a plain line here
                self.text[idx] = worker.GetLine(self.Recode(self.text[idx][len(M):], worker).strip())
                idx += 1
                continue
        if start_subsection > end_subsection:
            self.text.append(worker.GetSubsectionTail())
        self.text.append(worker.GetDocumentTail())
        return

    def ParseBib(self, worker):
        if not self.bib:
            return
        bibkeys = []
        textbib = ''
        #unique, ordered reference list
        for line in self.text:
            bibkeys.extend(worker.FindBibKey(line))
        seen = set()
        for k in [x for x in bibkeys if x not in seen and not seen.add(x)]:
            textbib += worker.FmtBibItem(k, self.bib[k][0], self.bib[k][1])
        textbib = worker.FmtBibStart(textbib)
        textbib = worker.FmtBibEnd(textbib)
        self.text.append(textbib)

    def Recode(self, line, worker):
        # the use of ? is very important
        #>>> re.sub(r'@@(.*)@@', r'\\texttt{\1}', line)
        #'\\texttt{aa@@, @@aabb}'
        #>>> re.sub(r'@@(.*?)@@', r'\\texttt{\1}', line)
        #'\\texttt{aa}, \\texttt{aabb}'
        if not line:
            return ''
        line = line.strip()
        raw = []
        # support for raw syntax
        pattern = re.compile(r'{\$(.*?)\$}')
        for m in re.finditer(pattern, line):
            line = line.replace(m.group(0), "{0}N{1}".format(self.PH, len(raw)))
            raw.append(m.group(1))
        # DOI online lookup
        pattern = re.compile('@DOI://(.*?)@')
        for m in re.finditer(pattern, line):
            line = line.replace(m.group(0), getPaper(m.group(1), self.reference_format))
        # in-line replacement of keywords
        for item in worker.swaps:
            if len(item) == 2:
                # plain swap
                line = line.replace(item[0], item[1])
            elif len(item) == 3:
                # conditional swap
                pattern = re.compile(item[2])
                for m in re.finditer(pattern, line):
                    line = line.replace(m.group(0), re.sub(item[0], item[1], m.group(0)))
        line = re.sub(r'"""(.*?)"""', worker.bl, line)
        line = re.sub(r'""(.*?)""', worker.bd, line)
        line = re.sub(r'"(.*?)"', worker.it, line)
        line = re.sub(r"``(.*?)''", worker.dq, line)
        line = re.sub(r"`(.*?)'", worker.sq, line)
        line = re.sub(r'@@(.*?)@@', worker.tt, line)
        # citation
        # [note|reference] defines the pattern for citation.
        # Will have to use [note$|$reference] here since '|' was previously replaced by $|$
        pattern = re.compile('\[(\s*)(?P<a>.+?)(\s*)%s(\s*)(?P<b>.+?)(\s*)\]' % worker.bar)
        # re.compile('\[(.+?)\|(.+?)\]')
        for m in re.finditer(pattern, line):
            # [text|@link@] defines the pattern for direct URL, in non pdf documents
            mm = re.match(r'(\s*)@(\S*?)@(\s*)', m.group('b'))
            if mm:
                content = worker.GetURL(mm.group(2), link_text = m.group('a'))
                if worker.direct_url:
                    # Directly embed URL, do not record reference
                    line = line.replace(m.group(0), content)
                    continue
            else:
                content = m.group('b')
            k = re.sub('\W', '', m.group('a'))
            if not k:
                raise ValueError("Invalid citation keyword for reference item ``{0}``.".\
                                 format(m.group('a')))
            if k in list(self.bib.keys()):
                if self.bib[k] != [m.group('a'), content]:
                    k += str(len(list(self.bib.keys())))
            self.bib[k] = [m.group('a'), content]
            line = line.replace(m.group(0), worker.GetRef(m.group('a'), content, k))
        # standalone url
        pattern = re.compile('@(\S*?)@')
        for m in re.finditer(pattern, line):
            line = line.replace(m.group(0), worker.GetURL(m.group(1)))
        # recover raw latex syntax
        for i in range(len(raw)):
            line = line.replace("{0}N{1}".format(self.PH, i), raw[i])
        return line

    def Capitalize(self, line):
        omit = ["a", "an", "the", "and", "but", "or", "nor", "as", "at", "by", "for", "in", "of", "on", "to", "but", "cum", "mid", "off", "per", "qua", "re", "up", "via", "to", "from", "into", "onto", "with", "within", "without"]
        line = line.split()
        if len(line) == 0:
            return ''
        # first word capitalized anyways
        out = line[0][0].upper() + (line[0][1:] if len(line[0]) > 1 else '')
        # omit keywords for the rest
        if len(line) > 1:
            out += ' ' + ' '.join([x[0].upper() + (x[1:] if len(x) > 1 else '') if x not in omit else x
                                   for x in line[1:]])
        return out

    def PrepareBlock(self, text, worker, name, label):
        if name == 'list':
            return self.PrepareList(text, worker, label)
        elif name == 'out':
            return self.PrepareVerbatim(text, worker, label)
        elif name == 'table':
            return self.PrepareTable(text, worker, label)
        elif name in ['warning', 'tip', 'important', 'note']:
            return self.PrepareBox(text, worker, name, label)
        else:
            return self.PrepareCodes(text, worker, name, label)

    def PrepareList(self, text, worker, label = None):
        # handle 2nd level indentation first
        # in the mean time take care of recoding
        text = self.__ReserveFigure(text)
        text, reserved = self.__ReserveBlock(text, mode = 'hold')
        self.__RaiseBlockMark(text)
        text = text.split('\n')
        idx = 0
        while idx < len(text):
            if text[idx].startswith(self.PH):
                idx += 1
                continue
            if text[idx].startswith(M * 2):
                start = idx
                end = idx
                text[idx] = M * 2 + self.Recode(text[idx][2:], worker)
                text[idx] = worker.FmtListItem(text[idx], 2)
                if idx + 1 < len(text):
                    for j in range(idx + 1, len(text) + 1):
                        try:
                            if not text[j].startswith(M * 2):
                                break
                            else:
                                text[j] = worker.FmtListItem(M * 2 + self.Recode(text[j][2:], worker), 2)
                                end = j
                        except IndexError:
                            pass
                #
                text[start] = worker.FmtListStart(text[start], 2)
                text[end] = worker.FmtListEnd(text[end], 2)
                idx = end + 1
            elif text[idx].startswith(M):
                text[idx] = M + self.Recode(text[idx][1:], worker)
                idx += 1
            else:
                text[idx] = self.Recode(text[idx], worker)
                idx += 1
        # handle 1st level indentation
        text = '\n'.join([x if x.startswith(self.PH) else worker.FmtListItem(x, 1) for x in text])
        text = self.__ReserveBlock(text, mode = 'release', cache = reserved)[0]
        text = worker.FmtListStart(text, 1)
        text = worker.FmtListEnd(text, 1)
        return text

    def PrepareTable(self, text, worker, label = None):
        self.__RaiseNested(text)
        table = [[self.Recode(iitem, worker) for iitem in multispace2tab(item).split('\t')] \
                 for item in text.split('\n') if item]
        return worker.GetTable(table, self.Recode(label, worker))

    def PrepareCodes(self, text, worker, k, label = None):
        text = text.split('\n')
        for idx, item in enumerate(text):
            if item.startswith("file:///"): text[idx] = gettxtfromfile(item, self.dirnames)
            elif item.startswith("output:///"): text[idx] = gettxtfromcmd(item, self.dirnames)
            else: continue
        text = '\n'.join(text)
        if k.lower() == 'raw' or k.lower() == '$': return text
        self.__RaiseNested(text)
        return worker.GetCodes(text, k, self.Recode(label, worker))

    def PrepareVerbatim(self, text, worker, label = None):
        text = text.split('\n')
        for idx, item in enumerate(text):
            if item.startswith("file:///"): text[idx] = gettxtfromfile(item, self.dirnames)
            elif item.startswith("output:///"): text[idx] = gettxtfromcmd(item, self.dirnames)
            else: continue
        text = '\n'.join(text)
        self.__RaiseNested(text)
        return worker.GetVerbatim(text, self.Recode(label, worker))

    def PrepareBox(self, text, worker, k, label = None):
        self.__RaiseNested(text, kw = worker.box_kw)
        text = self.__ReserveFigure(text)
        text, reserved = self.__ReserveBlock(text, mode = 'hold')
        self.__RaiseBlockMark(text)
        text = '\n'.join([item if item.startswith(self.PH) else self.Recode(re.sub(r'^{0}'.format(M), '', item), worker) for item in text.split('\n')])
        text = self.__ReserveBlock(text, mode = 'release', cache = reserved)[0]
        return worker.GetBox(text, k, self.Recode(label, worker))

    def __ReplaceNested(self, text, start,
                        end, nestedtext):
        end += 1
        if (end - start) > len(nestedtext):
            for i in range(start, end):
                j = i - start
                if j < len(nestedtext):
                    text[i] = nestedtext[j]
                else:
                    text[i] = None
        else:
            raise ValueError('Nested block size exceeds expected limit!')
        return [x for x in text if x is not None]

    def __ReserveBlock(self, text, mode = 'remove', cache = {}):
        # there should be better way to make sure the existing block not to be modified
        # but will use this solution for now
        reserved = {}
        if mode == 'hold':
            text = re.split('({0}|{1})'.format('BEGIN' + self.PH, 'END' + self.PH), text)
            idxes = [0]
            i = 1
            while i < len(text):
                if text[i] == 'BEGIN' + self.PH:
                    # block identified
                    flag = self.PH not in text[i+1] and text[i+2] == ('END' + self.PH)
                    if not flag:
                        raise ValueError("Invalid block found!")
                    # block checked
                    text[i] = self.PH + str(i) + 'E'
                    reserved[text[i]] = text[i+1]
                    idxes.append(i)
                    # block skipped
                    i += 3
                else:
                    # no block identified
                    idxes.append(i)
                    i += 1
            text = ''.join([item for idx, item in enumerate(text) if idx in idxes])
        elif mode == 'release':
            reserved = cache
            for k, item in list(reserved.items()):
                text = text.replace(k, item)
        elif mode == 'remove':
            text = re.sub(r'{0}|{1}'.format('BEGIN' + self.PH, 'END' + self.PH), '', text)
        return text, reserved

    def __ReserveFigure(self, text):
        pattern = re.compile('#\*(.*?)(\n|$)')
        for m in re.finditer(pattern, text):
            fig = 'BEGIN' + self.PH + FigureInserter(m.group(1), support = FIGTYPES,
                                             tag = self.format, path_adj = self.fig_path_adj).Insert() \
                                             + 'END' + self.PH + '\n'
            text = text.replace(m.group(0), fig, 1)
        return text

    def __RaiseNested(self, text, kw = None):
        pattern = re.compile('{0}(.*?){1}'.format('BEGIN' + self.PH, 'END' + self.PH), re.DOTALL)
        # re.match() will not work here
        # will not work without re.DOTALL
        for m in re.finditer(pattern, text):
            if m:
                e = m.group(1)
                if kw is None:
                    raise ValueError('Nested style not allowed:\n``{0}``'.format(e[:max(200, len(e))]))
                else:
                    for k in kw:
                        if re.search(k, '%r' % e):
                            raise ValueError('Nested style not allowed:\n``{0}``'.\
                                             format(e[:max(200, len(e))]))
        return

    def __RaiseBlockMark(self, text):
        for item in text.split('\n'):
            if item.strip() and (not (item.startswith(self.PH) or item.startswith(M))):
                raise ValueError('Items must start with ``{0}`` in this block. Problematic text: ``{1}``'.\
                          format(M, item))
        return
