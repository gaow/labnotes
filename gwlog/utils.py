import os, sys, re
from subprocess import PIPE, Popen
import tempfile
from minted import minted
from btheme import btheme
from htheme import HTML_INDEX
from collections import OrderedDict
import codecs

SYNTAX = {'r':'r',
          'sh':'bash',
          'py':'python',
          'tex':'latex',
          'c':'c',
          'cpp':'cpp',
          'h':'c',
          'sqlite':'sql'
          }

# functions
def getfname(innames, outname, suffix='.pdf'):
	if not outname:
		fname = '-'.join([os.path.splitext(name)[0] for name in innames])
	else:
		fname = outname
	if fname.endswith(suffix):
		fname = fname.replace(suffix, '')
	return os.path.split(fname)[-1]

def wraptxt(line, sep, by, rmblank = True):
    # will also remove blank lines, if any
    sline = ''
    i = 0
    for item in list(line):
        if item == '\n' and i == 0:
            if rmblank:
                # unnecessary wrap
                continue
        if item == '\n':
            # natural wrap
            sline += item
            i = 0
            continue
        j = 1
        if item == '\t':
            # assume 1 tab = 8 white spaces
            j = 9
        for k in range(j):
            if i == by:
                # time to wrap
                sline += item + sep + '\n'
                i = 0
                break
            else:
                i += 1
        if not i == 0:
            sline += item
    return sline

import stat
def pdflatex(fname, text, vanilla=False, beamer = False):
	# setup temp dir
	tmp_dir = None
	pattern = re.compile(r'gw_log_cache_*(.*)')
	for fn in os.listdir(tempfile.gettempdir()):
		if pattern.match(fn):
			tmp_dir = os.path.join(tempfile.gettempdir(), fn)
			break
	if tmp_dir and vanilla:
		os.system('rm -rf {0}'.format(tmp_dir))
		sys.stderr.write('INFO: cache folder {0} is removed\n'.format(tmp_dir))
		tmp_dir = tempfile.mkdtemp(prefix='gw_log_cache_')
	if not tmp_dir:
		tmp_dir = tempfile.mkdtemp(prefix='gw_log_cache_')
	if (not os.access(tmp_dir, os.R_OK)) or (not os.access(tmp_dir, os.W_OK)) or (os.stat(tmp_dir).st_mode & stat.S_ISVTX == 512):
			home_dir = os.getenv("HOME")
			tmp_dir = os.path.join(home_dir, 'gw_log_cache')
			if not os.path.exists(tmp_dir): os.makedirs(tmp_dir)
	dest_dir = os.getcwd()
	os.chdir(tmp_dir)
	# write tex file
	with open(fname + '.tex', 'w', encoding='utf-8') as f:
		f.writelines(text)
	# write sty file
	if not beamer:
		m = minted(tmp_dir)
		m.put()
	else:
		m = btheme(tmp_dir)
		m.put()
	# compile
	sys.stderr.write('Building {0} "{1}" ...\n'.format('document' if not beamer else 'slides', fname + '.pdf'))
	for visit in [1,2]:
		# too bad we cannot pipe tex to pdflatex with the output behavior under ctrl ... have to write the disk
		tc = Popen(["pdflatex", "-shell-escape", "-halt-on-error", "-file-line-error", fname + '.tex'],
			stdin = PIPE, stdout = PIPE, stderr = PIPE)
		out, error = tc.communicate()
		if (tc.returncode) or error.decode(sys.getdefaultencoding()) or (not os.path.exists(fname + '.pdf')):
			with open(os.path.join(dest_dir, '{0}-ERROR.txt'.format(fname)), 'w', encoding='utf-8') as f:
				f.writelines(out.decode(sys.getdefaultencoding()) + error.decode(sys.getdefaultencoding()))
			os.system('rm -f {0}.out {0}.toc {0}.aux {0}.log {0}.nav {0}.snm {0}.vrb'.format(fname))
			#sys.stderr.write('DEBUG:\n\t$ cd {0}\n\t$ pdflatex -shell-escape -halt-on-error -file-line-error {1}\n'.format(tmp_dir, fname + '.tex'))
			sys.stderr.write('Oops!... non-empty error message or non-zero return code captured. Please run the program again.\n'\
					'\033[91mNOTE: If you have used raw LaTeX syntax @@@ ... @@@ please make sure the syntax are valid ' \
					'(the program will crash on invalid raw LaTeX code).\nNOTE: You can also try to run with --vanilla option to remove '\
					'potentially problematic cached files.\n\033[0mIf this message presists after all your trouble-shooting, '\
					'please find file "{0}-ERROR.txt" and report it to Gao Wang.\n'.format(fname))
			sys.exit(1)
		if visit == 1:
			sys.stderr.write('Still working ...\n')
			os.system('rm -f *.pdf')
		else:
			os.system('mv -f {0} {1}'.format(fname + '.pdf', dest_dir))
			os.system('rm -f {0}.out {0}.toc {0}.aux {0}.log {0}.nav {0}.snm {0}.vrb'.format(fname))
			os.system('rm -f {0}'.format(os.path.join(dest_dir, '{0}-ERROR.txt'.format(fname))))
	sys.stderr.write('Done!\n')
	return

def uniq(seq):
    seen = set()
    seen_add = seen.add
    return [x for x in seq if x not in seen and not seen_add(x)]

def indexhtml(fnames):
    fnames = uniq(fnames)
    d = OrderedDict()
    try:
        for fn in fnames:
            with codecs.open(fn, 'r', encoding='UTF-8', errors='ignore') as f:
                flag = True
                while flag:
                    line = f.readline()
                    if not line:
                        break
                    m = re.search(r'<!DOCTYPE html><html><head><title>(.+?)\|(.+?)</title>', line)
                    if m:
                        if m.group(1).strip():
                            d[fn] = (m.group(1).strip(), m.group(2).strip())
                            flag = False
            if flag:
                sys.stderr.write('WARNING: Cannot find valid title for "{}". Please make sure the html files are generated with "--title" option\n'.format(fn))
        if len(d) == 0:
            sys.exit('WARNING: No output generated')
    except Exception as e:
        sys.exit("ERROR processing input html: {}".format(e))
    #
    otext = '\n'.join(['<li><span>{0}{1}</span>{4}<a href="{2}">{3}</a></li>'.format(v[0].replace('_', ' '), '&nbsp;&nbsp;<em><small>by {}</small></em>'.format(v[1]) if v[1] else '', k, '[view]', '<a href="{}">{}</a>'.format(k.replace('.html', '.pdf'), '&nbsp;&nbsp;[download]') if os.path.exists(k.replace('.html', '.pdf')) else '') for k, v in d.items()])
    return HTML_INDEX['head'] + otext + HTML_INDEX['tail']

# classes
class TexParser:
    def __init__(self, title, author, fname):
        self.title = ' '.join([x[0].upper() + (x[1:] if len(x) > 1 else '') for x in self.m_recode(title).split()])
        self.author = self.m_recode(author)
        self.fn = '-'.join(fname)
        self.mark = '#'
        self.text = []
        self.PARSER_RULE = {
                'list':'self.m_blockizeList',
                'table':'self.m_blockizeTable',
                'out':'self.m_blockizeOut',
                }
        for item in list(set(SYNTAX.values())):
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
        self.blockph = 'ABLOCKBLOODYPLACEHOLDER'
        self.latexph = 'ALATEXBLOODYRAWPATTERNPLACEHOLDER'
        self.htmlph = 'AHTMLBLOODYRAWPATTERNPLACEHOLDER'
        self.pause = False
        self.fig_support = ['jpg','pdf','png']
        self.fig_tag = 'tex'

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
        pattern = re.compile(r'@@@(.*?)@@@')
        for m in re.finditer(pattern, line):
            line = line.replace(m.group(0), self.latexph + str(len(raw)))
            raw.append(m.group(1))
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
        pattern = re.compile('@(.*?)@')
        for m in re.finditer(pattern, line):
            line = line.replace(m.group(0), '\\url{%s}' % m.group(1).replace('\-\_', '\_').replace('$\sim$', '~'))
        # citation
        # [note|reference] defines the pattern for citation.
        # Will have to use [note$|$reference] here since '|' was previously replaced by $|$
        pattern = re.compile('\[(?P<a>.+?)\$\|\$(?P<b>.+?)\]')
        # re.compile('\[(.+?)\|(.+?)\]')
        for m in re.finditer(pattern, line):
            if not self.footnote:
                k = re.sub('\W', '', m.group('a'))
                if not k:
                    self.quit("Invalid citation keyword for reference item '{}'.".format(m.group('b')))
                if k in self.bib.keys():
                    if self.bib[k] != [m.group('a'), m.group('b')]:
                        k += str(len(self.bib.keys()))
                self.bib[k] = [m.group('a'), m.group('b')]
                #line = line.replace(m.group(0), '\\cite[%s]{%s}' % (m.group('a'), k))
                line = line.replace(m.group(0), '{\\color{MidnightBlue}%s}~\\cite{%s}' % (m.group('a'), k))
            else:
                line = line.replace(m.group(0), '{\\color{MidnightBlue}%s}~\\footnote{%s}' % (m.group('a'), '\\underline{' + m.group('a') + '} ' + m.group('b')))
        # recover raw latex syntax
        for i in range(len(raw)):
            line = line.replace(self.latexph + str(i), raw[i])
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
            if text[idx].startswith(self.mark + '}') and '--' not in text[idx]:
                self.quit("Invalid use of '%s' without previous %s{, near %s" % \
                        (text[idx], self.mark, text[idx+1] if idx + 1 < len(text) else "end of document"))
            if text[idx].startswith(self.mark + '{') and '--' not in text[idx]:
                # define block
                bname = text[idx].split('{')[1].strip()
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
                            self.quit('Invalid use of "%s{----" within block environment, near %') %\
                                (self.mark, self.text[i+1] if i + 1 < len(self.text) else "end of document")
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
                text[idx] = 'BEGIN' + self.blockph + eval(self.PARSER_RULE[bname])(text[idx], bname) + 'END' + self.blockph
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
            text = re.split('({}|{})'.format('BEGIN' + self.blockph, 'END' + self.blockph), text)
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
            for k, item in mapping.items():
                text = text.replace(k, item)
        elif mode == 'remove':
            text = re.sub(r'{0}|{1}'.format('BEGIN' + self.blockph, 'END' + self.blockph), '', text)
        return text, mapping

    def _holdfigureplace(self, text):
        pattern = re.compile('#\*(.*?)(\n|$)')
        for m in re.finditer(pattern, text):
            fig = 'BEGIN' + self.blockph + self._parseFigure(m.group(1), self.fig_support, self.fig_tag) + 'END' + self.blockph + '\n'
            text = text.replace(m.group(0), fig, 1)
        return text

    def _parseFigure(self, line, support = ['jpg','pdf','png'], tag = 'tex'):
        if line.startswith(self.mark + '*'):
            line = line[len(self.mark)+1:].strip()
        else:
            line = line.strip()
        try:
            fig, width = line.strip().split()
            width = float(width)
        except ValueError:
            fig = line.strip().split()[0]
            width = 0.9
        if not '.' in fig:
            self.quit("Cannot determine graphic file format for '{}'. Valid extensions are {}".format(fig, ' '.join(support)))
        if fig.split('.')[1] not in support:
            self.quit("Input file format '{}' not supported. Valid extensions are {}".format(fig.split('.')[1], ' '.join(support)))
        if not os.path.exists(fig):
            self.quit("Cannot find file %s" % fig)
        if tag == 'tex':
            line = '\\begin{center}\\includegraphics[width=%s\\textwidth]{%s}\\end{center}' % (width, os.path.abspath(fig))
        else:
            line = '<p><center><img src="{}" alt="{}" width="{}" /></center></p>'.format(fig, os.path.split(fig)[-1], int(width * 800))
        return line

    def _checknest(self, text, kw=None):
        pattern = re.compile('{}(.*?){}'.format('BEGIN' + self.blockph, 'END' + self.blockph), re.DOTALL)
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

    def m_blockizeTable(self, text, k):
        self._checknest(text)
        table = [[self.m_recode(iitem) for iitem in item.split('\t')] for item in text.split('\n')]
        ncols = list(set([len(x) for x in table]))
        if len(ncols) > 1:
            self.quit("Number of columns not consistent for table. Please replace empty columns with placeholder symbol, e.g. '-'. {}".format(text))
        cols = 'c' * ncols[0]
        head = '\\begin{center}\n{\\%s\\begin{longtable}{%s}\n\\hline\n' % (self.tablefont, cols)
        body = '&'.join(table[0]) + '\\\\\n' + '\\hline\n' + '\\\\\n'.join(['&'.join(item) for item in table[1:]]) + '\\\\\n'
        tail = '\\hline\n\\end{longtable}}\n\\end{center}\n'
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
        sys.exit('\033[91mAn ERROR has occured while processing input text "{}":\033[0m\n\t '.format(self.fn) + msg)
