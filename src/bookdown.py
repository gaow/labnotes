#!/usr/bin/env python
# -*- coding: utf-8 -*-
import codecs, os, shutil
from . import BOOKDOWN_CFG as cfg, BOOKDOWN_OUT as out, \
     BOOKDOWN_TEX as tex, BOOKDOWN_STYLE as style, \
     BOOKDOWN_TOC as toc, BOOKDOWN_IDX as idx
from .utils import env, dict2str, cd
from pysos.sos_script import SoS_Script

def get_sos(files, pdf, check_deps, workdir):
    bookdown_header = '''
[1]
# Build bookdown in HTML
'''
    if check_deps:
        check_section = '''
check_R_library('rstudio/bookdown')
check_R_library('rstudio/DT')
check_command('pandoc')
'''
    else:
        check_section = ''
    bookdown_section = '''
quiet = 'T'
formats = ['bookdown::gitbook']
input: %s
R: workdir = %s
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
    tigernotes doc ${input!q} -o ${output!q} %s
''' % (repr(pdf[0]), repr(os.path.join(workdir, pdf[1], '_main.pdf')), pdf[2])
    else:
        pdf_section = ''
    return(bookdown_header + check_section + bookdown_section + pdf_section)

def prepare_bookdown(files, title, author, date, description, url, url_edit, repo, pdf, output):
    # write resources
    with codecs.open(os.path.join(env.tmp_dir, 'style.css'), 'w', encoding='UTF-8') as f:
            f.write(style)
    with codecs.open(os.path.join(env.tmp_dir, 'toc.css'), 'w', encoding='UTF-8') as f:
            f.write(toc)
    with codecs.open(os.path.join(env.tmp_dir, 'preamble.tex'), 'w', encoding='UTF-8') as f:
            f.write(tex)
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
    out['bookdown::gitbook']['css'] = os.path.join(env.tmp_dir, 'style.css')
    out['bookdown::html_chapters']['css'] = [os.path.join(env.tmp_dir, 'style.css'),
                                             os.path.join(env.tmp_dir, 'toc.css')]
    out['bookdown::epub_book']['stylesheet'] = os.path.join(env.tmp_dir, 'style.css')
    out['bookdown::pdf_book']['includes']['in_header'] = os.path.join(env.tmp_dir, 'preamble.tex')
    workdir = os.getcwd()
    if output:
        os.makedirs(output, exist_ok = True)
        cfg['output_dir'] = os.path.basename(output)
        workdir = os.path.dirname(output)
    else:
        os.mkdirs(cfg['output_dir'], exist_ok = True)
    out['bookdown::gitbook']['config']['toc']['before'] = '{}'.format(
        out['bookdown::gitbook']['config']['toc']['before'].replace('VALUE', idx['title']))
    out['bookdown::gitbook']['config']['toc']['after'] = '{}'.format(
        out['bookdown::gitbook']['config']['toc']['after'].replace('VALUE',
                                                                   '{} {}'.format(env.year, idx['author'])))
    if pdf:
        pdf = (pdf, cfg['output_dir'], '{} {} {} --toc --long_ref --font_size 12'.\
               format('-a {}'.format(repr(author)) if author else '',
                      '-t {}'.format(repr(title)) if title else '',
                      '-d {}'.format(repr(date)) if date else ''))
    #
    if os.path.exists(os.path.join(env.tmp_dir, env.time) + '.deps'):
        check_deps = False
    else:
        check_deps = True
    # Move files around to resolve path problem for bookdown
    filenames = ['index.rmd' if idx == 0 else '{}_{}'.format(str(idx).zfill(4), os.path.basename(x))
                 for idx, x in enumerate(files)]
    for x, y in zip(files[1:], filenames[1:]):
        shutil.copy(x, os.path.join(workdir, y))
    with open(files[0]) as f:
        tmp = f.read()
    for f in files:
        os.rename(f, os.path.join(env.tmp_dir, os.path.basename(f)))
    with cd(workdir):
        with open(filenames[0], 'w') as f:
            f.write('---\n{}\n---\n{}'.format(dict2str(idx), tmp))
        cfg['rmd_files']['html'] = list(filenames)
        cfg['rmd_files']['latex'] = list(filenames)
        with open('_output.yml', 'w') as f:
            f.write(dict2str(out))
        with open('_bookdown.yml', 'w') as f:
            f.write(dict2str(cfg))
    error_msg = None
    try:
        SoS_Script(get_sos(filenames, pdf, check_deps, workdir)).workflow().run()
    except Exception as e:
        error_msg = e
    for f in files:
        os.rename(os.path.join(env.tmp_dir, os.path.basename(f)), f)
    with cd(workdir):
        os.remove('_output.yml')
        os.remove('_bookdown.yml')
        for f in filenames:
            os.remove(f)
    if error_msg is None:
        os.system('touch %s' % os.path.join(env.tmp_dir, env.time) + '.deps')
    else:
        raise RuntimeError(e)
