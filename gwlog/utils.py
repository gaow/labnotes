import os, sys, re
from subprocess import PIPE, Popen
import tempfile
from minted import minted
from ltheme import btheme
from htheme import HTML_INDEX
from collections import OrderedDict
import codecs

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
            sys.stderr.write('''
                    * * *
                    * Oops! One of the following problems occurred:
                    * 1. Missing required software / packages dependencies
                    *   -> Install the dependencies documented in README
                    * 2. LaTeX gives a warning message
                    *   -> Did you get the pdf file? If so, ignore the warning
                    *   -> Run the problem again to see if it goes away
                    * 3. Invalid raw LaTeX syntax
                    *   -> Make sure text in between @@@ ... @@@ symbols is legal
                    * 4. Cache files messed up
                    *   -> Try to run the program with '--vanilla' option
                    * 5. Other issues
                    *   -> Tips above do not get rid of the problem
                    *   -> Report file "{0}-ERROR.txt" to Gao Wang
                    * * *\n\n'''.format(fname))
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
    d = OrderedDict()
    try:
        nbars = 0
        for fn in fnames:
            if fn == ',':
                # write a bar
                d[',{}'.format(nbars)] = '<hr style="margin-top:1em;margin-bottom:.5em;">'
                nbars += 1
                continue
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
    #otext = '\n'.join(['<li><span>{0}{1}</span>{4}<a href="{2}">{3}</a></li>'.format(v[0].replace('_', ' '), '&nbsp;&nbsp;<em><small>by {}</small></em>'.format(v[1]) if v[1] else '', k, '[view]', '<a href="{}">{}</a>'.format(k.replace('.html', '.pdf'), '&nbsp;&nbsp;[download]') if os.path.exists(k.replace('.html', '.pdf')) else '') for k, v in d.items()])
    otext = ''
    for k, v in d.items():
        if not k.startswith(','):
            otext += '<li><span>{0}{1}</span>{4}<a href="{2}">{3}</a></li>'.format(re.sub(r'(\s*)-(\s*)', ' - ', v[0].replace('_', ' ')), '&nbsp;&nbsp;<em><sub>Last edited: {}</sub></em>'.format(v[1]) if v[1] else '', k, '[view]', '<a href="{}">{}</a>'.format(k.replace('.html', '.pdf'), '&nbsp;&nbsp;[download]') if os.path.exists(k.replace('.html', '.pdf')) else '') + '\n'
        else:
            otext += v + '\n'
    return HTML_INDEX['head'] + otext + HTML_INDEX['tail']
