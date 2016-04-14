#!/usr/bin/env python
# -*- coding: utf-8 -*-
import codecs, os
from . import BOOKDOWN_CFG as cfg, BOOKDOWN_OUT as out, \
     BOOKDOWN_TEX as tex, BOOKDOWN_STYLE as style, \
     BOOKDOWN_TOC as toc, BOOKDOWN_IDX as idx
from .utils import env, dict2str
from pysos.sos_script import SoS_Script

def get_sos(files, pdf):
    bookdown_section = '''
[1]
# Build bookdown in HTML
check_R_library('rstudio/bookdown')
check_R_library('rstudio/DT')
check_command('pandoc')
quiet = 'T'
formats = ['bookdown::gitbook']
input: %s
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
  cmd = sprintf("bookdown::render_book(c(${input!r,}), '%%s', quiet = %%s, preview = T)", fmt, quiet)
  res = bookdown:::Rscript(c('-e', shQuote(cmd)))
  if (res != 0) stop('Failed to compile the book to ', fmt)
  if (travis && fmt == 'bookdown::epub_book')
    bookdown::calibre('bookdown.epub', 'mobi')
}
''' % (repr(files))
    if pdf:
        pdf_section = '''
[2]
input: '%s'
output: '%s/_main.pdf'
run:
    tigernotes doc ${input} -o ${output} %s
''' % (pdf[0], pdf[1], pdf[2])
    else:
        pdf_section = ''
    return(bookdown_section + pdf_section)

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
    out['bookdown::gitbook']['css'] = os.path.join(env.tmp_dir, 'style.css')
    out['bookdown::html_chapters']['css'] = [os.path.join(env.tmp_dir, 'style.css'),
                                             os.path.join(env.tmp_dir, 'toc.css')]
    out['bookdown::epub_book']['stylesheet'] = os.path.join(env.tmp_dir, 'style.css')
    out['bookdown::pdf_book']['includes']['in_header'] = os.path.join(env.tmp_dir, 'preamble.tex')
    if output:
        cfg['output_dir'] = output
    out['bookdown::gitbook']['config']['toc']['before'] = '{}'.format(
        out['bookdown::gitbook']['config']['toc']['before'].replace('VALUE', idx['title']))
    out['bookdown::gitbook']['config']['toc']['after'] = '{}'.format(
        out['bookdown::gitbook']['config']['toc']['after'].replace('VALUE',
                                                                   '{} {}'.format(env.year, idx['author'])))
    cfg['rmd_files']['html'] = list(files)
    cfg['rmd_files']['latex'] = list(files)
    if pdf:
        pdf = (pdf, cfg['output_dir'], '{} {} {} --toc --long_ref --font_size 12'.\
               format('-a {}'.format(author) if author else '',
                      '-t {}'.format(title) if title else '',
                      '-d {}'.format(date) if date else ''))
    #
    with open('_output.yml', 'w') as f:
        f.write(dict2str(out))
    with open('_bookdown.yml', 'w') as f:
        f.write(dict2str(cfg))
    tmp_fn = files[0]
    with open(tmp_fn) as f:
        tmp = f.read()
    os.remove(tmp_fn)
    files[0] = 'index.rmd'
    with open(files[0], 'w') as f:
        f.write('---\n{}\n---\n{}'.format(dict2str(idx), tmp))
    SoS_Script(get_sos(files, pdf)).workflow().run()
    with open(tmp_fn, 'w') as f:
        f.write(tmp)
    os.remove('_output.yml')
    os.remove('_bookdown.yml')
    os.remove('index.rmd')
