import os, sys, re
from subprocess import PIPE, Popen
import tempfile
from minted import minted

def getfname(innames, outname):
	if not outname:
		fname = '-'.join([os.path.splitext(name)[0] for name in innames])
	else:
		fname = outname
	if fname.endswith('.pdf'):
		fname = fname.replace('.pdf', '')
	return fname

def wraptxt(line, sep, by):
    # will also remove blank lines, if any
    sline = ''
    i = 0
    for item in list(line):
        if item == '\n' and i == 0:
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


def pdflatex(fname, text, vanilla=False):
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
	m = minted(tmp_dir)
	m.put()
	sys.stderr.write('Building document "{0}" ...\n'.format(fname + '.pdf'))
	for iter in [1,2]:
		# too bad we cannot pipe tex to pdflatex with the output behavior under ctrl ... have to write the disk
		tc = Popen(["pdflatex", "-shell-escape", "-halt-on-error", "-file-line-error", fname + '.tex'],
			stdin = PIPE, stdout = PIPE, stderr = PIPE)
		out, error = tc.communicate()
		if (tc.returncode) or error.decode(sys.getdefaultencoding()) or (not os.path.exists(fname + '.pdf')):
			with open(os.path.join(dest_dir, '{0}-ERROR.txt'.format(fname)), 'w', encoding='utf-8') as f:
				f.writelines(out.decode(sys.getdefaultencoding()) + error.decode(sys.getdefaultencoding()))
			os.system('rm -f *.out *.toc *.aux *.log')
			#sys.stderr.write('DEBUG:\n\t$ cd {0}\n\t$ pdflatex -shell-escape -halt-on-error -file-line-error {1}\n'.format(tmp_dir, fname + '.tex'))
			sys.stderr.write('WARNING: Non-empty error message or non-zero return code captured. Please run the program again.\n')
			sys.exit('If this message presists please find file "{0}-ERROR.txt" and report it to Gao Wang.\n'.format(fname))
		if iter == 1:
			sys.stderr.write('Still working ...\n')
			os.system('rm -f *.pdf')
		else:
			os.system('mv -f {0} {1}'.format(fname + '.pdf', dest_dir))
			os.system('rm -f *.out *.toc *.aux *.log')
			os.system('rm -f {0}'.format(os.path.join(dest_dir, '{0}-ERROR.txt'.format(fname))))
	sys.stderr.write('Done!\n')
	return
