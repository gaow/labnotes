#!/usr/bin/env python
# -*- coding: utf-8 -*-
VERSION = "0.0.1"
FULL_VERSION = "0.0.1-rev336"
BOOKDOWN_CFG = {'chapter_name': '', 'repo': '', 'output_dir': '_book', 'rmd_files': {'latex': [], 'html': []}, 'clean': []}
BOOKDOWN_OUT = {'bookdown::epub_book': {'stylesheet': 'style.css'}, 'bookdown::gitbook': {'config': {'toc': {'collapse': 'subsection', 'after': '<center> VALUE </center>', 'scroll_highlight': True, 'before': '<li><a href="./"> VALUE </a></li>'}, 'search': True, 'fontsettings': {'theme': 'white', 'family': 'sans', 'size': 2}, 'sharing': {'google': False, 'all': ['facebook', 'google', 'twitter', 'weibo', 'instapaper'], 'vk': False, 'weibo': False, 'instapper': False, 'facebook': True, 'twitter': True}, 'download': ['pdf'], 'edit': {'text': 'Edit', 'link': ''}, 'toolbar': {'position': 'fixed'}}, 'split_by': 'section', 'css': 'style.css'}, 'bookdown::html_chapters': {'css': ['style.css', 'toc.css']}, 'bookdown::pdf_book': {'latex_engine': 'xelatex', 'includes': {'in_header': 'preamble.tex'}, 'keep_tex': True, 'citation_package': 'natbib'}}
BOOKDOWN_IDX = {'description': 'Labnotes bookdown template', 'site': 'bookdown::bookdown_site', 'knit': 'bookdown::render_book', 'biblio-style': 'apalike', 'url': 'https://bookdown.org/', 'documentclass': 'book', 'link-citations': True, 'github-repo': '', 'title': 'Lab Notes', 'bibliography': ['~/.tigernotes/reference.bib'], 'date': '`r Sys.Date()`', 'author': '&copy; J. Doe'}
BOOKDOWN_TEX = r"""
\usepackage{booktabs}
\usepackage{longtable}
\usepackage{framed,color}
\definecolor{shadecolor}{RGB}{248,248,248}

\ifxetex
  \usepackage{letltxmacro}
  \setlength{\XeTeXLinkMargin}{1pt}
  \LetLtxMacro\SavedIncludeGraphics\includegraphics
  \def\includegraphics#1#{% #1 catches optional stuff (star/opt. arg.)
    \IncludeGraphicsAux{#1}%
  }%
  \newcommand*{\IncludeGraphicsAux}[2]{%
    \XeTeXLinkBox{%
      \SavedIncludeGraphics#1{#2}%
    }%
  }%
\fi

\newenvironment{rmdblock}[1]
  {\begin{shaded*}
  \begin{itemize}
  \renewcommand{\labelitemi}{
    \raisebox{-.7\height}[0pt][0pt]{
      {\setkeys{Gin}{width=3em,keepaspectratio}\includegraphics{images/#1}}
    }
  }
  \item
  }
  {
  \end{itemize}
  \end{shaded*}
  }
\newenvironment{rmdnote}
  {\begin{rmdblock}{note}}
  {\end{rmdblock}}
\newenvironment{rmdcaution}
  {\begin{rmdblock}{caution}}
  {\end{rmdblock}}
\newenvironment{rmdimportant}
  {\begin{rmdblock}{important}}
  {\end{rmdblock}}
\newenvironment{rmdtip}
  {\begin{rmdblock}{tip}}
  {\end{rmdblock}}
\newenvironment{rmdwarning}
  {\begin{rmdblock}{warning}}
  {\end{rmdblock}}

"""
BOOKDOWN_STYLE = r"""
.rmdcaution, .rmdimportant, .rmdnote, .rmdtip, .rmdwarning {
  padding: 1em 1em 1em 4em;
  margin-bottom: 10px;
  background: #f5f5f5 5px center/3em no-repeat;
} 
.rmdcaution {
  background-image: url("../images/caution.png");
}
.rmdimportant {
  background-image: url("../images/important.png");
}
.rmdnote {
  background-image: url("../images/note.png");
}
.rmdtip {
  background-image: url("../images/tip.png");
}
.rmdwarning {
  background-image: url("../images/warning.png");
}
.kable_wrapper {
  border-spacing: 20px 0;
  border-collapse: separate;
  border: none;
  margin: auto;
}
.kable_wrapper > tbody > tr > td {
  vertical-align: top;
}
p.caption {
  color: #777;
  margin-top: 10px;
}
p code {
  white-space: inherit;
}
pre {
  word-break: normal;
  word-wrap: normal;
}
pre code {
  white-space: inherit;
}

"""
BOOKDOWN_TOC = r"""
#TOC ul,
#TOC li,
#TOC span,
#TOC a {
  margin: 0;
  padding: 0;
  position: relative;
}
#TOC {
  line-height: 1;
  border-radius: 5px 5px 0 0;
  background: #141414;
  background: linear-gradient(to bottom, #333333 0%, #141414 100%);
  border-bottom: 2px solid #0fa1e0;
  width: auto;
}
#TOC:after,
#TOC ul:after {
  content: '';
  display: block;
  clear: both;
}
#TOC a {
  background: #141414;
  background: linear-gradient(to bottom, #333333 0%, #141414 100%);
  color: #ffffff;
  display: block;
  padding: 19px 20px;
  text-decoration: none;
  text-shadow: none;
}
#TOC ul {
  list-style: none;
}
#TOC > ul > li {
  display: inline-block;
  float: left;
  margin: 0;
}
#TOC > ul > li > a {
  color: #ffffff;
}
#TOC > ul > li:hover:after {
  content: '';
  display: block;
  width: 0;
  height: 0;
  position: absolute;
  left: 50%;
  bottom: 0;
  border-left: 10px solid transparent;
  border-right: 10px solid transparent;
  border-bottom: 10px solid #0fa1e0;
  margin-left: -10px;
}
#TOC > ul > li:first-child > a {
  border-radius: 5px 0 0 0;
}
#TOC.align-right > ul > li:first-child > a,
#TOC.align-center > ul > li:first-child > a {
  border-radius: 0;
}
#TOC.align-right > ul > li:last-child > a {
  border-radius: 0 5px 0 0;
}
#TOC > ul > li.active > a,
#TOC > ul > li:hover > a {
  color: #ffffff;
  box-shadow: inset 0 0 3px #000000;
  background: #070707;
  background: linear-gradient(to bottom, #262626 0%, #070707 100%);
}
#TOC .has-sub {
  z-index: 1;
}
#TOC .has-sub:hover > ul {
  display: block;
}
#TOC .has-sub ul {
  display: none;
  position: absolute;
  width: 200px;
  top: 100%;
  left: 0;
}
#TOC .has-sub ul li a {
  background: #0fa1e0;
  border-bottom: 1px dotted #31b7f1;
  filter: none;
  display: block;
  line-height: 120%;
  padding: 10px;
  color: #ffffff;
}
#TOC .has-sub ul li:hover a {
  background: #0c7fb0;
}
#TOC ul ul li:hover > a {
  color: #ffffff;
}
#TOC .has-sub .has-sub:hover > ul {
  display: block;
}
#TOC .has-sub .has-sub ul {
  display: none;
  position: absolute;
  left: 100%;
  top: 0;
}
#TOC .has-sub .has-sub ul li a {
  background: #0c7fb0;
  border-bottom: 1px dotted #31b7f1;
}
#TOC .has-sub .has-sub ul li a:hover {
  background: #0a6d98;
}
#TOC ul ul li.last > a,
#TOC ul ul li:last-child > a,
#TOC ul ul ul li.last > a,
#TOC ul ul ul li:last-child > a,
#TOC .has-sub ul li:last-child > a,
#TOC .has-sub ul li.last > a {
  border-bottom: 0;
}

"""
