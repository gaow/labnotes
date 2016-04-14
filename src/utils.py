#!/usr/bin/env python
# -*- coding: utf-8 -*-
import os, sys, re, datetime
import glob, shutil, shlex
import yaml
from io import StringIO
from subprocess import PIPE, Popen
import tempfile
from .minted import minted
from .style import btheme, HTML_INDEX
from .doi import PaperList
from collections import OrderedDict
import codecs
import stat

class Environment:
    def __init__(self):
        self.get_tmpdir()
        self.raw_time = datetime.datetime.now()
        self.year = self.raw_time.strftime("%Y")
        self.month = self.raw_time.strftime("%m")
        self.date = self.raw_time.strftime("%d")
        self.month_name = self.raw_time.strftime("%B")
        self.time = self.year + self.month + self.date

    def get_tmpdir(self):
        self.tmp_dir = None
        pattern = re.compile(r'tigernotes_cache_*(.*)')
        for fn in os.listdir(tempfile.gettempdir()):
            if pattern.match(fn):
                self.tmp_dir = os.path.join(tempfile.gettempdir(), fn)
                break
        if self.tmp_dir is None:
            self.reset_tmpdir()

    def reset_tmpdir(self):
        if self.tmp_dir:
            shutil.rmtree(self.tmp_dir)
            sys.stderr.write('INFO: cache folder {0} is removed\n'.format(self.tmp_dir))
            self.tmp_dir = tempfile.mkdtemp(prefix='tigernotes_cache_')
        else:
            self.tmp_dir = tempfile.mkdtemp(prefix='tigernotes_cache_')
        if (not os.access(self.tmp_dir, os.R_OK)) or \
          (not os.access(self.tmp_dir, os.W_OK)) or \
          (os.stat(self.tmp_dir).st_mode & stat.S_ISVTX == 512):
                home_dir = os.getenv("HOME")
                self.tmp_dir = os.path.join(home_dir, '.tigernotes/cache')
                if not os.path.exists(self.tmp_dir):
                        os.makedirs(self.tmp_dir)

env = Environment()

def getfname(innames, outname, suffix='.pdf'):
    if not outname:
        fname = '-'.join([os.path.splitext(name)[0] for name in innames])
    else:
        fname = outname
    if fname.endswith(suffix):
        fname = fname.replace(suffix, '')
    directories = os.path.split(fname)[:-1]
    for directory in directories:
        if directory is not '':
            if not os.path.exists(directory):
                os.makedirs(directory)
    return fname

def wraptxt(line, sep, by, rmblank = True, prefix = ''):
    # will also remove blank lines, if any
    if by <= 0:
        return line
    # comment flag
    comment = False
    sline = ''
    i = 0
    for item in list(line):
        if item == prefix and (re.search(r'\n(\s*)$', sline) or sline == ''):
            # time to comment
            comment = True
        if item == '\n' and i == 0:
            if rmblank:
                # unnecessary wrap
                continue
        if item == '\n':
            # natural wrap
            sline += item
            comment = False
            i = 0
            continue
        j = 1
        if item == '\t':
            # assume 1 tab = 8 white spaces
            j = 9
        for k in range(j):
            if i == by:
                # time to wrap
                sline += item + sep + '\n' + (prefix + ' ' if comment else '')
                i = 0
                break
            else:
                i += 1
        if not i == 0:
            sline += item
    return sline

def multispace2tab(line):
    p = re.compile(r' \s+|\t\s+')
    return p.sub('\t', line)

def readfromfile(fname, start = None, end = None):
    try:

        with codecs.open(os.path.expanduser(fname), 'r', encoding='UTF-8', errors='ignore') as f:
            text = [x.rstrip() for x in f.readlines()]
        if start is not None and end is None:
            end = len(text)
        if start is not None and end is not None and start >= 1 and end <= len(text):
            return '\n'.join(text[start-1:end])
        else:
            return '\n'.join(text)
    except Exception as e:
        sys.exit('Cannot load {0}: {1}'.format(fname, e))

def gettxtfromfile(text):
    flist = text.split('\n')
    for idx, item in enumerate(flist):
        if item.startswith('file:///'):
            item = item[8:].split()
            if len(item) == 2:
                item.append(None)
            if len(item) == 3:
                try:
                    item[1] = int(item[1])
                    item[2] = int(item[2]) if item[2] is not None else None
                except:
                    sys.exit("Invalid input argument '{0} {1}' for '{2}'".format(item[1], item[2], item[0]))
                flist[idx] = readfromfile(item[0], item[1], item[2])
            else:
                flist[idx] = readfromfile(item[0])
    return '\n'.join(flist)

def gettxtfromcmd(text):
    flist = text.split('\n')
    for idx, item in enumerate(flist):
        if item.startswith('output:///'):
            flist[idx] = Popen(shlex.split(item[10:]), stdout=PIPE).communicate()[0].decode('utf-8')
    return '\n'.join(flist)

def pdflatex(fname, text, vanilla=False, beamer_institute = None):
    def empty(directory, name):
        for item in ['out','toc','aux','log','nav','snm','vrb']:
            item = os.path.join(directory, '{0}.{1}'.format(name, item))
            if os.path.exists(item): os.remove(item)
    # setup temp dir
    dest_dir = os.path.dirname(os.path.abspath(os.path.expanduser(fname)))
    fname = os.path.split(fname)[-1]
    cwd = os.getcwd()
    os.chdir(env.tmp_dir)
    # write tex file
    with codecs.open(fname + '.tex', 'w', encoding='utf-8') as f:
        f.writelines(text)
    # write sty file
    if beamer_institute is None:
        m = minted(env.tmp_dir)
        m.put()
    else:
        m = btheme(env.tmp_dir)
        m.put(beamer_institute)
    # compile
    sys.stderr.write('Building {0} "{1}" ...\n'.format('document' if beamer_institute is None else 'slides', fname + '.pdf'))
    cmd = ["pdflatex", "-shell-escape", "-halt-on-error", "-file-line-error", fname + '.tex']
    for visit in [1,2]:
        # too bad we cannot pipe tex to pdflatex with the output behavior under ctrl ... have to write the disk
        tc = Popen(cmd, stdin = PIPE, stdout = PIPE, stderr = PIPE)
        out, error = tc.communicate()
        if visit == 2 and ((tc.returncode or error) and (not os.path.exists(fname + '.pdf'))):
            with codecs.open(os.path.join(cwd, '{0}-ERROR.txt'.format(fname)), 'w', encoding='utf-8') as f:
                try:
                    f.writelines(out.decode(sys.getdefaultencoding()) + error.decode(sys.getdefaultencoding()))
                except:
                    f.writelines("Error running: " + " ".join(cmd) + '\n')
            empty(env.tmp_dir, fname)
            sys.stderr.write('''
                    * * *
                    * Oops! One of the following problems occurred:
                    * 1. Missing required software / packages dependencies
                    *   -> Install the required dependencies
                    * 2. Invalid raw LaTeX syntax
                    *   -> Make sure text between {{$ ... $}} syntax is legal
                    * 3. Cache files messed up
                    *   -> Try to run the program with '--vanilla' option
                    * 4. Internal bugs
                    *   -> Report file "{0}-ERROR.txt" to Gao Wang
                    * * *\n\n'''.format(fname))
            sys.exit(1)
        if visit == 1:
            sys.stderr.write('Still working ...\n')
        else:
            shutil.move(os.path.join(env.tmp_dir, (fname + '.pdf')),
                        os.path.join(dest_dir, fname + '.pdf'))
            empty(env.tmp_dir, fname)
            ferr = os.path.join(cwd, '{0}-ERROR.txt'.format(fname))
            if os.path.exists(ferr): os.remove(ferr)
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
    for k, v in list(d.items()):
        if not k.startswith(','):
            otext += '<li><span>{0}{1}</span>{4}<a href="{2}">{3}</a></li>'.format(re.sub(r'(\s*)-(\s*)', ' - ', v[0].replace('_', ' ')), '&nbsp;&nbsp;<em><sub>Last edited: {}</sub></em>'.format(v[1]) if v[1] else '', k, '[view]', '<a href="{}">{}</a>'.format(k.replace('.html', '.pdf'), '&nbsp;&nbsp;[download]') if os.path.exists(k.replace('.html', '.pdf')) else '') + '\n'
        else:
            otext += v + '\n'
    return HTML_INDEX['head'] + otext + HTML_INDEX['tail']

def getPaper(doi, longref):
    doi = doi.rstrip('/')
    datadir = os.path.expanduser('~/.tigernotes')
    if not os.path.isdir(datadir):
        os.makedirs(datadir)
    database = os.path.join(datadir, 'references')
    finder = PaperList(database)
    sys.stderr.write('Searching for {0} ...\r'.format(doi))
    sys.stderr.flush()
    # update database
    status = finder.addPaper(doi)
    sys.stderr.write('{0}: {1} {3}, {2} in database\n'.format(doi,
		status[0].upper(), status[1].upper(), 'online'))
    finder.dump()
    # format citation
    info = finder.extract(doi)
    for k, value in list(info.items()):
        if len(info[k]) == 0:
            return doi
    if longref:
        info = '{0} ({2}). ""{1}"". "{3}". doi:@@{4}@@ | @{5}@'.\
          format(info['authors'],
               info['title'], info['date'],
               info['journal'], info['DOI'],
               info['link'])
    else:
        info = '{0} ({2}). ""{1}"". "{3}"'.\
          format(info['authors'],
               info['title'], info['date'],
               info['journal'])
    if sys.version_info[0] == 2:
        return info.decode("ascii", "ignore").encode('utf-8')
    else:
        return info

class cd:
    """Context manager for changing the current working directory"""
    def __init__(self, newPath):
        self.newPath = newPath

    def __enter__(self):
        self.savedPath = os.getcwd()
        os.chdir(self.newPath)

    def __exit__(self, etype, value, traceback):
        os.chdir(self.savedPath)

def dict2str(value, replace = []):
    out = StringIO()
    yaml.dump(value, out, default_flow_style=False)
    res = out.getvalue()
    out.close()
    for item in replace:
        res = res.replace(item[0], item[1])
    return res
