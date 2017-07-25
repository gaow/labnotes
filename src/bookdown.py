#!/usr/bin/env python3
# -*- coding: utf-8 -*-
import codecs, os, shutil, re
from . import BOOKDOWN_CFG as cfg, BOOKDOWN_OUT as out, \
     BOOKDOWN_TEX as tex, BOOKDOWN_STYLE as style, \
     BOOKDOWN_TOC as toc, BOOKDOWN_IDX as idx
from .utils import env, dict2str, cd
from sos.sos_script import SoS_Script
from sos.target import executable
from sos.R.target import R_library

def get_sos(files, pdf, workdir):
    bookdown_section = '''
[1]
# Build bookdown in HTML
quiet = 'T'
formats = ['bookdown::gitbook']
input: %s
task: workdir = %s
R:
###
# Code below are copied from
# https://github.com/rstudio/bookdown/blob/master/inst/examples/_render.R
###
quiet = ${quiet}
formats = c(${formats!r,})
travis = !is.na(Sys.getenv('CI', NA))

# provide default formats if necessary
if (length(formats) == 0) formats = c(
  'bookdown::pdf_book', 'bookdown::gitbook'
)
# render the book to all formats unless they are specified via command-line args
for (fmt in formats) {
  cmd = sprintf("bookdown::render_book(c(${input!r,}), '%%s', preview = T, quiet = %%s)", fmt, quiet)
  res = bookdown:::Rscript(c('-e', shQuote(cmd)))
  if (res != 0) stop('Failed to compile the book to ', fmt)
  if (travis && fmt == 'bookdown::epub_book')
    bookdown::calibre('bookdown.epub', 'mobi')
}
''' % (repr([os.path.join(workdir, f) for f in files]), repr(workdir))
    if pdf:
        pdf_section = '''
[2]
input: %s
output: %s
run:
    labnotes doc ${input!q} -o ${output!q} %s
''' % (repr(pdf[0]), repr(os.path.join(workdir, pdf[1], '_main.pdf')), pdf[2])
    else:
        pdf_section = ''
    return(bookdown_section + pdf_section)

def prepare_bookdown(files, title, author, date, description, no_section_number,
                     split_by, url, url_edit, repo, pdf, output, pdf_args):

    if not os.path.exists(os.path.join(env.tmp_dir, env.time) + '.deps'):
        R_library('rstudio/bookdown')
        R_library('rstudio/DT')
        executable('pandoc')
        os.system('touch %s' % os.path.join(env.tmp_dir, env.time) + '.deps')
    #
    if title:
        idx['title'] = title
    if author:
        idx['author'] = author
    if date:
        idx['date'] = date
    if description:
        if os.path.isfile(description):
            idx['description'] = open(description).read()
        else:
            idx['description'] = description
    if url:
        idx['url'] = url
    else:
        del idx['url']
    if repo:
        idx['github-repo'] = repo
        cfg['repo'] = repo
    else:
        del idx['github-repo']
        del cfg['repo']
    idx['author'] = '&copy; ' + idx['author']
    out['bookdown::gitbook']['css'] =  'style.css'
    out['bookdown::html_chapters']['css'] = ['style.css', 'toc.css']
    out['bookdown::epub_book']['stylesheet'] = 'style.css'
    if pdf:
        out['bookdown::pdf_book']['includes']['in_header'] = os.path.join(env.tmp_dir, 'preamble.tex')
    else:
        del out['bookdown::pdf_book']
    workdir = os.getcwd()
    if output:
        output = os.path.abspath(os.path.expanduser(output))
        os.makedirs(output, exist_ok = True)
        cfg['output_dir'] = os.path.basename(output)
        workdir = os.path.dirname(output)
    else:
        os.makedirs(cfg['output_dir'], exist_ok = True)
    out['bookdown::gitbook']['config']['toc']['before'] = '{}'.format(
        out['bookdown::gitbook']['config']['toc']['before'].replace('VALUE', idx['title']))
    out['bookdown::gitbook']['config']['toc']['after'] = '{}'.format(
        out['bookdown::gitbook']['config']['toc']['after'].replace('VALUE',
                                                                   '{} {}'.format(env.year, idx['author'])))
    if split_by:
        out['bookdown::gitbook']['split_by'] = split_by
    if no_section_number:
        out['bookdown::gitbook']['number_sections'] = 0
    if pdf:
        pdf = (pdf, cfg['output_dir'], '{} {} {} --toc --long_ref --font_size 12 {}'.\
               format('-a {}'.format(repr(author)) if author else '',
                      '-t {}'.format(repr(title)) if title else '',
                      '-d {}'.format(repr(date)) if date else '',
                      ' '.join(pdf_args)))
    # Move files around to resolve path problem for bookdown
    filenames = ['index.rmd' if idx == 0 else '{}_{}'.format(str(idx).zfill(4), os.path.basename(x))
                 for idx, x in enumerate(files)]
    filenames = [x if x.endswith('.rmd') else os.path.splitext(x)[0] + '.rmd' for x in filenames]
    for x, y in zip(files[1:], filenames[1:]):
        shutil.copy(x, os.path.join(workdir, y))
    with open(files[0]) as f:
        tmp = f.readlines()
        if len(tmp) == 0:
            tmp.append(' ')
        if not (tmp[0].startswith('# ')):
            name = os.path.splitext(os.path.basename(files[0]))[0].lstrip('0123456789.- ')
            tmp = ['# ' + re.sub(r'\-|_', ' ', name) + '\n'] \
                    + tmp
        tmp = ''.join(tmp)
    for i, fn in enumerate(files):
        if i == 0:
            continue
        with cd(workdir):
            with open(filenames[i]) as f:
                lines = f.readlines()
            if len(lines) == 0:
                lines.append(' ')
            if not (lines[0].startswith('# ')):
                name = os.path.splitext(os.path.basename(fn))[0].lstrip('0123456789.- ')
                lines = ['# ' + re.sub(r'\-|_', ' ', name) + '\n'] \
                        + lines
                with open(filenames[i], 'w') as f:
                    f.write(''.join(lines))
    # write resources
    with codecs.open(os.path.join(workdir, cfg['output_dir'], 'style.css'), 'w', encoding='UTF-8') as f:
            f.write(style)
    with codecs.open(os.path.join(workdir, cfg['output_dir'], 'toc.css'), 'w', encoding='UTF-8') as f:
            f.write(toc)
    with codecs.open(os.path.join(env.tmp_dir, 'preamble.tex'), 'w', encoding='UTF-8') as f:
            f.write(tex)
    error_msg = None
    try:
        with cd(workdir):
            with open(filenames[0], 'w') as f:
                f.write('---\n{}\n---\n{}'.format(dict2str(idx), tmp))
            cfg['rmd_files']['html'] = list(filenames)
            cfg['rmd_files']['latex'] = list(filenames)
            with open('_output.yml', 'w') as f:
                f.write(dict2str(out))
            with open('_bookdown.yml', 'w') as f:
                f.write(dict2str(cfg))
            sos_file = os.path.join(env.tmp_dir, 'bookdown.sos')
            with open(sos_file, 'w') as f:
                f.write(get_sos(filenames, pdf, workdir))
            os.system('sos run {}'.format(sos_file))
    except Exception as e:
        error_msg = e
    os.remove(sos_file)
    try:
        with cd(workdir):
            os.remove('_output.yml')
            os.remove('_bookdown.yml')
            for f in filenames:
                os.remove(f)
    except:
        pass
    if error_msg is not None:
        raise RuntimeError(error_msg)
