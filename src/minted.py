#!/usr/bin/env python
# -*- coding: utf-8 -*-
import os, codecs
class minted:
    def __init__(self, outdir):
        self.outdir = outdir
        # two modifications to original minted.sty
        # 1) Add "-f" to "rm" command, to accommodate for my version of rm
        # 2) use "./pygmentize" instead of system "pygmentize"
        self.sty = r'''%%
%% This is file `minted.sty',
%% generated with the docstrip utility.
%%
%% The original source files were:
%%
%% minted.dtx  (with options: `package')
%% Copyright 2010--2011 Konrad Rudolph
%% 
%% This work may be distributed and/or modified under the
%% conditions of the LaTeX Project Public License, either version 1.3
%% of this license or (at your option) any later version.
%% The latest version of this license is in
%%   http://www.latex-project.org/lppl.txt
%% and version 1.3 or later is part of all distributions of LaTeX
%% version 2005/12/01 or later.
%% 
%% Additionally, the project may be distributed under the terms of the new BSD
%% license.
%% 
%% This work has the LPPL maintenance status `maintained'.
%% 
%% The Current Maintainer of this work is Konrad Rudolph.
%% 
%% This work consists of the files minted.dtx and minted.ins
%% and the derived file minted.sty.
\NeedsTeXFormat{LaTeX2e}
\ProvidesPackage{minted}[2011/09/17 v1.7 Yet another Pygments shim for LaTeX]
\RequirePackage{keyval}
\RequirePackage{fancyvrb}
\RequirePackage{xcolor}
\RequirePackage{float}
\RequirePackage{ifthen}
\RequirePackage{calc}
\RequirePackage{ifplatform}
\DeclareOption{chapter}{\def\minted@float@within{chapter}}
\DeclareOption{section}{\def\minted@float@within{section}}
\ProcessOptions\relax
\ifwindows
  \providecommand\DeleteFile[1]{\immediate\write18{del #1}}
\else
  \providecommand\DeleteFile[1]{\immediate\write18{rm -f #1}}
\fi
\newboolean{AppExists}
\newcommand\TestAppExists[1]{
  \ifwindows
    \DeleteFile{\jobname.aex}
    \immediate\write18{for \string^\@percentchar i in (#1.exe #1.bat #1.cmd)
      do set >\jobname.aex <nul: /p x=\string^\@percentchar \string~$PATH:i>>\jobname.aex} %$
    \newread\@appexistsfile
    \immediate\openin\@appexistsfile\jobname.aex
    \expandafter\def\expandafter\@tmp@cr\expandafter{\the\endlinechar}
    \endlinechar=-1\relax
    \readline\@appexistsfile to \@apppathifexists
    \endlinechar=\@tmp@cr
    \ifthenelse{\equal{\@apppathifexists}{}}
     {\AppExistsfalse}
     {\AppExiststrue}
    \immediate\closein\@appexistsfile
    \DeleteFile{\jobname.aex}
\immediate\typeout{file deleted}
  \else
    \immediate\write18{which #1 && touch \jobname.aex}
    \IfFileExists{\jobname.aex}
     {\AppExiststrue
      \DeleteFile{\jobname.aex}}
     {\AppExistsfalse}
  \fi}
\newcommand\minted@resetoptions{}
\newcommand\minted@defopt[1]{
  \expandafter\def\expandafter\minted@resetoptions\expandafter{%
    \minted@resetoptions
    \@namedef{minted@opt@#1}{}}}
\newcommand\minted@opt[1]{
  \expandafter\detokenize%
    \expandafter\expandafter\expandafter{\csname minted@opt@#1\endcsname}}
\newcommand\minted@define@opt[3][]{
  \minted@defopt{#2}
  \ifthenelse{\equal{#1}{}}{
    \define@key{minted@opt}{#2}{\@namedef{minted@opt@#2}{#3}}}
   {\define@key{minted@opt}{#2}[#1]{\@namedef{minted@opt@#2}{#3}}}}
\newcommand\minted@define@switch[3][]{
  \minted@defopt{#2}
  \define@booleankey{minted@opt}{#2}
   {\@namedef{minted@opt@#2}{#3}}
   {\@namedef{minted@opt@#2}{#1}}}
\minted@defopt{extra}
\newcommand\minted@define@extra[1]{
  \define@key{minted@opt}{#1}{
    \expandafter\def\expandafter\minted@opt@extra\expandafter{%
      \minted@opt@extra,#1=##1}}}
\newcommand\minted@define@extra@switch[1]{
  \define@booleankey{minted@opt}{#1}
   {\expandafter\def\expandafter\minted@opt@extra\expandafter{%
      \minted@opt@extra,#1}}
   {\expandafter\def\expandafter\minted@opt@extra\expandafter{%
      \minted@opt@extra,#1=false}}}
\minted@define@switch{texcl}{-P texcomments}
\minted@define@switch{mathescape}{-P mathescape}
\minted@define@switch{linenos}{-P linenos}
\minted@define@switch{startinline}{-P startinline}
\minted@define@switch[-P funcnamehighlighting=False]%
  {funcnamehighlighting}{-P funcnamehighlighting}
\minted@define@opt{gobble}{-F gobble:n=#1}
\minted@define@opt{bgcolor}{#1}
\minted@define@extra{frame}
\minted@define@extra{framesep}
\minted@define@extra{framerule}
\minted@define@extra{rulecolor}
\minted@define@extra{numbersep}
\minted@define@extra{firstnumber}
\minted@define@extra{stepnumber}
\minted@define@extra{firstline}
\minted@define@extra{lastline}
\minted@define@extra{baselinestretch}
\minted@define@extra{xleftmargin}
\minted@define@extra{xrightmargin}
\minted@define@extra{fillcolor}
\minted@define@extra{tabsize}
\minted@define@extra{fontfamily}
\minted@define@extra{fontsize}
\minted@define@extra{fontshape}
\minted@define@extra{fontseries}
\minted@define@extra{formatcom}
\minted@define@extra{label}
\minted@define@extra@switch{numberblanklines}
\minted@define@extra@switch{showspaces}
\minted@define@extra@switch{resetmargins}
\minted@define@extra@switch{samepage}
\minted@define@extra@switch{showtabs}
\minted@define@extra@switch{obeytabs}
\newsavebox{\minted@bgbox}
\newenvironment{minted@colorbg}[1]{
  \def\minted@bgcol{#1}
  \noindent
  \begin{lrbox}{\minted@bgbox}
  \begin{minipage}{\linewidth-2\fboxsep}}
 {\end{minipage}
  \end{lrbox}%
  \colorbox{\minted@bgcol}{\usebox{\minted@bgbox}}}
\newwrite\minted@code
\newcommand\minted@savecode[1]{
  \immediate\openout\minted@code\jobname.pyg
  \immediate\write\minted@code{#1}
  \immediate\closeout\minted@code}
\newcommand\minted@pygmentize[2][\jobname.pyg]{
  \def\minted@cmd{./pygmentize -l #2 -f latex -F tokenmerge
    \minted@opt{gobble} \minted@opt{texcl} \minted@opt{mathescape}
    \minted@opt{startinline} \minted@opt{funcnamehighlighting}
    \minted@opt{linenos} -P "verboptions=\minted@opt{extra}"
    -o \jobname.out.pyg #1}
  \immediate\write18{\minted@cmd}
  % For debugging, uncomment:
  %\immediate\typeout{\minted@cmd}
  \ifthenelse{\equal{\minted@opt@bgcolor}{}}
   {}
   {\begin{minted@colorbg}{\minted@opt@bgcolor}}
  \input{\jobname.out.pyg}
  \ifthenelse{\equal{\minted@opt@bgcolor}{}}
   {}
   {\end{minted@colorbg}}
  \DeleteFile{\jobname.out.pyg}}
\newcommand\minted@usedefaultstyle{\usemintedstyle{default}}
\newcommand\usemintedstyle[1]{
  \renewcommand\minted@usedefaultstyle{}
  \immediate\write18{pygmentize -S #1 -f latex > \jobname.pyg}
  \input{\jobname.pyg}}
\newcommand\mint[3][]{
  \DefineShortVerb{#3}
  \minted@resetoptions
  \setkeys{minted@opt}{#1}
  \SaveVerb[aftersave={
    \UndefineShortVerb{#3}
    \minted@savecode{\FV@SV@minted@verb}
    \minted@pygmentize{#2}
    \DeleteFile{\jobname.pyg}}]{minted@verb}#3}
\newcommand\minted@proglang[1]{}
\newenvironment{minted}[2][]
 {\VerbatimEnvironment
  \renewcommand{\minted@proglang}[1]{#2}
  \minted@resetoptions
  \setkeys{minted@opt}{#1}
  \begin{VerbatimOut}[codes={\catcode`\^^I=12}]{\jobname.pyg}}%
 {\end{VerbatimOut}
  \minted@pygmentize{\minted@proglang{}}
  \DeleteFile{\jobname.pyg}}
\newcommand\inputminted[3][]{
  \minted@resetoptions
  \setkeys{minted@opt}{#1}
  \minted@pygmentize[#3]{#2}}
\newcommand\newminted[3][]{
  \ifthenelse{\equal{#1}{}}
   {\def\minted@envname{#2code}}
   {\def\minted@envname{#1}}
  \newenvironment{\minted@envname}
   {\VerbatimEnvironment\begin{minted}[#3]{#2}}
   {\end{minted}}
  \newenvironment{\minted@envname *}[1]
   {\VerbatimEnvironment\begin{minted}[#3,##1]{#2}}
   {\end{minted}}}
\newcommand\newmint[3][]{
  \ifthenelse{\equal{#1}{}}
   {\def\minted@shortname{#2}}
   {\def\minted@shortname{#1}}
  \expandafter\newcommand\csname\minted@shortname\endcsname[2][]{
    \mint[#3,##1]{#2}##2}}
\newcommand\newmintedfile[3][]{
  \ifthenelse{\equal{#1}{}}
   {\def\minted@shortname{#2file}}
   {\def\minted@shortname{#1}}
  \expandafter\newcommand\csname\minted@shortname\endcsname[2][]{
    \inputminted[#3,##1]{#2}{##2}}}
\@ifundefined{minted@float@within}
 {\newfloat{listing}{h}{lol}}
 {\newfloat{listing}{h}{lol}[\minted@float@within]}
\newcommand\listingscaption{Listing}
\floatname{listing}{\listingscaption}
\newcommand\listoflistingscaption{List of listings}
\providecommand\listoflistings{\listof{listing}{\listoflistingscaption}}
\AtBeginDocument{
  \minted@usedefaultstyle}
\AtEndOfPackage{
  \ifnum\pdf@shellescape=1\relax\else
    \PackageError{minted}
     {You must invoke LaTeX with the
      -shell-escape flag}
     {Pass the -shell-escape flag to LaTeX. Refer to the minted.sty
      documentation for more information.}\fi
  \TestAppExists{pygmentize}
  \ifAppExists\else
    \PackageError{minted}
     {You must have `pygmentize' installed
      to use this package}
     {Refer to the installation instructions in the minted
      documentation for more information.}
  \fi}
\endinput
%%
%% End of file `minted.sty'.
'''
        self.pygmentize = r'''#!/bin/bash
# An ugly hack to speed up pdflatex using the minted package place this file
# with the name 'pygmentize' somewhere on your path before the 'real'
# pygmentize, such that this file gets executed and can act as a wrapper around
# the 'real' pygmentize.  This script computes a hash-value (md5sum) of the
# input file from minted and caches the output of pygmentize.  The cached files
# are stored in a .minted/ directory next to the TeX doc.

real_pygmentize=`which pygmentize`
if [ -z $real_pygmentize ]; then
    rm -rf pygments
    hg clone http://bitbucket.org/birkenfeld/pygments-main pygments
    real_pygmentize="pygments/pygmentize"
fi

# find the output file used by minted
take_outfile=0
for arg in $@
do
  if [ $take_outfile -eq 1 ]
  then
    outfile=$arg
    take_outfile=0
  fi
  if [ $arg = -o ]
  then
    take_outfile=1
  fi
done

# the last parameter is the input file
infile=${@: -1}

# Create the .minted/ directory, if it doesn't exist.
minted_cache=".minted_cache"
if [[ ! -d ${minted_cache} ]]; then
    mkdir ${minted_cache}
fi

# compute the hash value of the input
hash="${minted_cache}/$( md5sum ${infile} | cut -d' ' -f1 )"
if [[ -f ${hash} ]]; then
  # we have cached output from pygmentize
  cp ${hash} ${outfile}
else
  # call 'real' pygmentize and cache the result
  $real_pygmentize "$@"
  cp ${outfile} ${hash}
fi
'''
    def put(self):
        with codecs.open(os.path.join(self.outdir, 'minted.sty'), 'w', encoding='UTF-8') as f:
            f.write(self.sty)
        with codecs.open(os.path.join(self.outdir, 'pygmentize'), 'w', encoding='UTF-8') as f:
            f.write(self.pygmentize)
        os.chmod(os.path.join(self.outdir, 'pygmentize'), 0755)
        return os.path.join(self.outdir, 'pygmentize')
