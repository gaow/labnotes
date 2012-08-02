import os, sys, re
from subprocess import PIPE, Popen
import tempfile
from minted import minted
from btheme import btheme

# functions
def getfname(innames, outname):
	if not outname:
		fname = '-'.join([os.path.splitext(name)[0] for name in innames])
	else:
		fname = outname
	if fname.endswith('.pdf'):
		fname = fname.replace('.pdf', '')
	return fname

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
			sys.stderr.write('WARNING: Non-empty error message or non-zero return code captured. Please run the program again.\n')
			sys.exit('If this message presists please find file "{0}-ERROR.txt" and report it to Gao Wang.\n'.format(fname))
		if visit == 1:
			sys.stderr.write('Still working ...\n')
			os.system('rm -f *.pdf')
		else:
			os.system('mv -f {0} {1}'.format(fname + '.pdf', dest_dir))
			os.system('rm -f {0}.out {0}.toc {0}.aux {0}.log {0}.nav {0}.snm {0}.vrb'.format(fname))
			os.system('rm -f {0}'.format(os.path.join(dest_dir, '{0}-ERROR.txt'.format(fname))))
	sys.stderr.write('Done!\n')
	return


# classes
class TexParser:
    def __init__(self, title, author):
        self.title = ' '.join([x[0].upper() + (x[1:] if len(x) > 1 else '') for x in self.m_recode(title).split()])
        self.author = self.m_recode(author)
        self.mark = '#'
        self.text = []
        self.blocks = {}
        self.keywords = ['err', 'list', 'table']
        for item in self.keywords:
            self.blocks[item] = []
        self.bib = {}
        self.footnote = False

    def m_recode(self, line):
        # the use of ? is very important
        #>>> re.sub(r'@@(.*)@@', r'\\texttt{\1}', line)
        #'\\texttt{aa@@, @@aabb}'
        #>>> re.sub(r'@@(.*?)@@', r'\\texttt{\1}', line)
        #'\\texttt{aa}, \\texttt{aabb}'
        if not line:
            return ''
        line = line.strip()
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
        pattern = re.compile('\[(?P<a>.+?)\|(?P<b>.+?)\]')
        # re.compile('\[(.+?)\|(.+?)\]')
        for m in re.finditer(pattern, line):
            if not self.footnote:
                k = re.sub('\W', '', m.group('a'))
                if not k:
                    sys.exit("Invalid citation keyword for reference item '{}'.".format(m.group('b')))
                if k in self.bib.keys():
                    if self.bib[k] != [m.group('a'), m.group('b')]:
                        k += str(len(self.bib.keys()))
                self.bib[k] = [m.group('a'), m.group('b')]
                #line = line.replace(m.group(0), '\\cite[%s]{%s}' % (m.group('a'), k))
                line = line.replace(m.group(0), '{\\color{MidnightBlue}%s}~\\cite{%s}' % (m.group('a'), k))
            else:
                line = line.replace(m.group(0), '{\\color{MidnightBlue}%s}~\\footnote{%s}' % (m.group('a'), '\\underline{' + m.group('a') + '} ' + m.group('b')))
        return line

    def m_parseBlocks(self):
        idx = 0
        while True:
            if idx >= len(self.text):
                break
            if self.text[idx].startswith(self.mark + '}') and '--' not in self.text[idx]:
                sys.exit("ERROR: invalid use of '%s' without previous %s{, near %s" % (self.text[idx], self.mark, self.text[idx+1] if idx + 1 < len(self.text) else "end of document"))
            if self.text[idx].startswith(self.mark + '{') and '--' not in self.text[idx]:
                # define block
                bname = self.text[idx].split('{')[1].strip()
                if bname not in [x for x in self.keywords if x != 'err']:
                    sys.exit("ERROR: invalid block definition '%s{ %s'" % (self.mark, bname))
                endidx = None
                self.text[idx] = ''
                # find end of block
                for i in range(idx+1, len(self.text)):
                    # do not allow nested blocks
                    if self.text[i].startswith(self.mark + '{'):
                        sys.exit("ERROR: nested use of blocks is disallowed: '{0}', near {1}".format(self.text[i], self.text[i+1] if idx + 1 < len(self.text) else "end of document"))
                    # find end of block
                    if self.text[i].startswith(self.mark + '}'):
                        if self.text[i].rstrip() == self.mark + '}':
                            endidx = i
                            break
                        else:
                            sys.exit("ERROR: invalid %s '%s', near %s" % ('nested use of' if '--' in self.text[i] else 'symbol', self.text[i], self.text[i+1] if idx + 1 < len(self.text) else "end of document"))
                if not endidx:
                    sys.exit("ERROR: '%s{ %s' and '%s}' must appear in pairs, near %s" % (self.mark, bname, self.mark, self.text[idx+1] if idx + 1 < len(self.text) else "end of document"))
                # combine block values
                for i in range(idx + 1, endidx):
                    self.text[idx] += self.text[i] + ('\n' if not i + 1 == endidx else '')
                del self.text[(idx + 1) : (endidx + 1)]
                # keep block index
                self.blocks[bname].append(idx)
            idx += 1
            continue
        #
        for idx, item in enumerate(self.text):
            # define err block
            if self.text[idx].startswith(self.mark + '}') and '--' in self.text[idx]:
                sys.exit("ERROR: invalid use of '%s}----' without previous '%s{----', near %s" % (self.mark, self.mark, self.text[idx+1] if idx + 1 < len(self.text) else "end of document") )
            if item.startswith(self.mark + '{') and '--' in item:
                endidx = None
                for i in range(idx+1, len(self.text)):
                    if self.text[i].startswith(self.mark + '{') and '--' in self.text[i]:
                        sys.exit("ERROR: nested use of blocks is disallowed: '{0}', near {1}".format(self.text[i], self.text[i+1] if idx + 1 < len(self.text) else "end of document"))
                    if self.text[i].startswith(self.mark + '}') and '--' in self.text[i]:
                        endidx = i
                        break
                if not endidx:
                    sys.exit('ERROR: comment blocks must appear in pairs, near {0}'.format(self.text[i+1] if idx + 1 < len(self.text) else "end of document"))
                self.blocks['err'].append([idx, endidx])
                self.text[idx] = ''
                self.text[endidx] = ''
        return

    def m_blockizeList(self, pause = False):
        if len(self.blocks['list']) == 0:
            return
        for i in self.blocks['list']:
            if i >= len(self.text):
                sys.exit('BUG: block specification does not match text')
            if not self.text[i].startswith(self.mark):
                sys.exit('ERROR: items must start with "{0}" in list block. Problematic text is: \n {1}'.format(self.mark, self.text[i]))
            # handle 2nd level indentation first
            # in the mean time take care of recoding
            text = self.text[i].split('\n')
            idx = 0
            while idx < len(text):
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
            self.text[i] = '\n'.join(text)
            self.text[i] = '\\begin{itemize}%s\n\\end{itemize}\n' % re.sub(r'^{0}|\n{0}'.format(self.mark), '\n\\item ', self.text[i])
            # this is for beamer \pause option
            if pause:
                self.text[i] = self.text[i].replace('\\item -', '\\pause \\item ')
        return

    def m_blockizeTable(self, fsize = 'footnotesize'):
        if len(self.blocks['table']) == 0:
            return
        for i in self.blocks['table']:
            table = [[self.m_recode(iitem) for iitem in item.split('\t')] for item in self.text[i].split('\n')]
            ncols = list(set([len(x) for x in table]))
            if len(ncols) > 1:
                sys.exit("ERROR: number of columns not consistent for table. Please replace empty columns with placeholder symbol, e.g. '-'. {}".format(self.text[i]))
            cols = 'c' * ncols[0]
            head = '\\begin{center}\n{\\%s\\begin{longtable}{%s}\n\\hline\n' % (fsize, cols)
            body = '&'.join(table[0]) + '\\\\\n' + '\\hline\n' + '\\\\\n'.join(['&'.join(item) for item in table[1:]]) + '\\\\\n'
            tail = '\\hline\n\\end{longtable}}\n\\end{center}\n'
            self.text[i] = head + body + tail
        return

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
