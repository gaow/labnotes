#!/usr/bin/env python
# -*- coding: utf-8 -*-
import codecs, os
from . import BOOKDOWN_CFG as cfg, BOOKDOWN_OUT as out, \
     BOOKDOWN_TEX as tex, BOOKDOWN_STYLE as style, \
     BOOKDOWN_TOC as toc
from .utils import env, dict2str
from pysos.sos_script import SoS_Script

def get_sos(files, pdf):
    formats = ['bookdown::gitbook']
    if pdf:
        formats.append('bookdown::pdf_book')
    return '''
[1]
# Build bookdown in HTML
check_R_library('rstudio/bookdown')
check_R_library('rstudio/DT')
check_command('pandoc')
quiet = 'T'
formats = %s
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
''' % (repr(formats), repr(files))

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
        out['title'] = title
    if author:
        out['author'] = author
    if date:
        out['date'] = date
    if description:
        if os.path.isfile(description):
            out['description'] = open(description).read()
        else:
            out['description'] = description
    if url:
        out['url'] = url
    else:
        del out['url']
    if repo:
        out['github-repo'] = repo
        cfg['repo'] = repo
    else:
        del out['github-repo']
        del cfg['repo']
    out['bookdown::gitbook']['css'] = os.path.join(env.tmp_dir, 'style.css')
    out['bookdown::html_chapters']['css'] = [os.path.join(env.tmp_dir, 'style.css'),
                                             os.path.join(env.tmp_dir, 'toc.css')]
    out['bookdown::epub_book']['stylesheet'] = os.path.join(env.tmp_dir, 'style.css')
    out['bookdown::pdf_book']['includes']['in_header'] = os.path.join(env.tmp_dir, 'preamble.tex')
    if output:
        cfg['output_dir'] = output
    out['bookdown::gitbook']['config']['toc']['before'] = '{}'.format(
        out['bookdown::gitbook']['config']['toc']['before'].replace('VALUE', out['title']))
    out['bookdown::gitbook']['config']['toc']['after'] = '{}'.format(
        out['bookdown::gitbook']['config']['toc']['after'].replace('VALUE', out['author']))
    cfg['rmd_files']['html'] = list(files)
    cfg['rmd_files']['latex'] = list(files)
    #
    with open('_output.yml', 'w') as f:
        f.write(dict2str(out))
    with open('_bookdown.yml', 'w') as f:
        f.write(dict2str(cfg))
    SoS_Script(get_sos(files, pdf)).workflow().run()
    os.remove('_output.yml')
    os.remove('_bookdown.yml')
