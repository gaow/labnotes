import os
class btheme:
    def __init__(self, outdir):
        self.outdir = outdir
        self.beamercolorthemericeowl = '''
% The Rice Owl Beamer Color Theme ver. 0.00 (2008/10/10)
% Copyright 2008 by Daina Chiba (d.chiba@rice.edu)
%
% This file may be distributed and/or modified
%
% 1. under the LaTeX Project Public License and/or
% 2. under the GNU Public License.
%

\\ProvidesPackageRCS $Header: /cvsroot/latex-beamer/latex-beamer/themes/color/beamercolorthemericeowl.sty,v 0.1 2008/10/09 16:51:00 daina Exp $

\\mode<presentation>

\\definecolor{riceblue}{RGB}{0,36,106}
\\definecolor{ricegray}{RGB}{94,96,98}

\\setbeamercolor*{normal text}{fg=black,bg=white}
\\setbeamercolor*{alerted text}{fg=red}
\\setbeamercolor*{example text}{fg=black}
\\setbeamercolor*{structure}{fg=riceblue, bg=white}

\\setbeamerfont{alerted text}{series=\\bfseries}

\\setbeamercolor*{palette primary}{fg=white,bg=riceblue}
\\setbeamercolor*{palette secondary}{fg=white,bg=ricegray}
\\setbeamercolor*{palette tertiary}{fg=white,bg=riceblue}
\\setbeamercolor*{palette quaternary}{fg=white,bg=black}

\\setbeamercolor{titlelike}{fg=riceblue, bg=white}
\\setbeamercolor{frametitle}{fg=riceblue, bg=white}
\\setbeamercolor{frametitle right}{fg=riceblue, bg=white}

\\setbeamercolor{sidebar}{bg=ricegray}

\\setbeamercolor*{palette sidebar primary}{fg=black}
\\setbeamercolor*{palette sidebar secondary}{fg=black}
\\setbeamercolor*{palette sidebar tertiary}{fg=black}
\\setbeamercolor*{palette sidebar quaternary}{fg=black}

\\setbeamercolor*{item projected}{fg=white,bg=riceblue}

\\setbeamercolor{block title}{fg=white,bg=riceblue}
\\setbeamercolor{block title alerted}{use=alerted text,fg=white,bg=alerted text.fg!75!black}
\\setbeamercolor{block title example}{use=example text,fg=white,bg=example text.fg!75!black}
\\setbeamercolor{block body}{parent=normal text,use=block title,bg=block title.bg!15!bg}
\\setbeamercolor{block body alerted}{parent=normal text,use=block title alerted,bg=block title alerted.bg!15!bg}
\\setbeamercolor{block body example}{parent=normal text,use=block title example,bg=block title example.bg!15!bg}

\\setbeamercolor*{separation line}{}
\\setbeamercolor*{fine separation line}{}

\\mode
<all>
        '''
        self.beamerouterthemeinfolines = '''
% Copyright 2007 by Till Tantau
%
% This file may be distributed and/or modified
%
% 1. under the LaTeX Project Public License and/or
% 2. under the GNU Public License.
%
% See the file doc/licenses/LICENSE for more details.

\\ProvidesPackageRCS $Header: /cvsroot/latex-beamer/latex-beamer/themes/outer/beamerouterthemeinfolines.sty,v 1.9 2007/01/28 20:48:30 tantau Exp $


\\mode<presentation>

\\setbeamercolor*{author in head/foot}{parent=palette tertiary}
\\setbeamercolor*{title in head/foot}{parent=palette secondary}
\\setbeamercolor*{date in head/foot}{parent=palette primary}

\\setbeamercolor*{section in head/foot}{parent=palette tertiary}
\\setbeamercolor*{subsection in head/foot}{parent=palette secondary}

\\defbeamertemplate*{footline}{infolines theme}
{
  \\leavevmode%
  \\hbox{%
  \\begin{beamercolorbox}[wd=.333333\\paperwidth,ht=2.25ex,dp=1ex,center]{author in head/foot}%
    \\usebeamerfont{author in head/foot}\\insertshorttitle
  \\end{beamercolorbox}%
  \\begin{beamercolorbox}[wd=.333333\\paperwidth,ht=2.25ex,dp=1ex,center]{title in head/foot}%
    \\usebeamerfont{title in head/foot}\\insertshortauthor% <\\insertshortinstitute>
  \\end{beamercolorbox}%
  \\begin{beamercolorbox}[wd=.333333\\paperwidth,ht=2.25ex,dp=1ex,right]{date in head/foot}%
    \\usebeamerfont{date in head/foot}\\insertshortdate{}\\hspace*{2em}
    \\insertframenumber{} / \\inserttotalframenumber\\hspace*{2ex}
  \\end{beamercolorbox}}%
  \\vskip0pt%
}

\\defbeamertemplate*{headline}{infolines theme}
{
  \\leavevmode%
  \\hbox{%
  \\begin{beamercolorbox}[wd=.5\\paperwidth,ht=2.25ex,dp=1ex,right]{section in head/foot}%
    \\usebeamerfont{section in head/foot}\\insertsectionhead\\hspace*{2ex}
  \\end{beamercolorbox}%
  \\begin{beamercolorbox}[wd=.5\\paperwidth,ht=2.25ex,dp=1ex,left]{subsection in head/foot}%
    \\usebeamerfont{subsection in head/foot}\\hspace*{2ex}\\insertsubsectionhead
  \\end{beamercolorbox}}%
  \\vskip0pt%
}

\\setbeamersize{text margin left=1em,text margin right=1em}

\\mode
<all>
        '''
        self.beamerthemeBoadilla = '''
% Copyright 2004 by Manuel Carro <mcarro@fi.upm.es>
%
% This file may be distributed and/or modified
%
% 1. under the LaTeX Project Public License and/or
% 2. under the GNU Public License.
%
% See the file doc/licenses/LICENSE for more details.

\\ProvidesPackageRCS $Header: /cvsroot/latex-beamer/latex-beamer/themes/theme/beamerthemeBoadilla.sty,v 1.2 2007/01/28 20:48:30 tantau Exp $

\\mode<presentation>

\\newif\\ifbeamer@secheader
\\beamer@secheaderfalse

\\DeclareOptionBeamer{secheader}{\\beamer@secheadertrue}
\\ProcessOptionsBeamer

% Tills' opinion: should be done in an inner theme, not here.

\\usesubitemizeitemtemplate{%
    \\tiny\\raise1.5pt\\hbox{\\color{beamerstructure}$\\blacktriangleright$}%
}
\\usesubsubitemizeitemtemplate{%
    \\tiny\\raise1.5pt\\hbox{\\color{beamerstructure}$\\bigstar$}%
}

\\setbeamersize{text margin left=1em,text margin right=1em}

\\ifbeamer@secheader\\else\\setbeamertemplate{headline}[infolines]\\fi

\\mode
<all>
        '''

    def put(self):
        with open(os.path.join(self.outdir, 'beamercolorthemericeowl.sty'), 'w', encoding='UTF-8') as f:
            f.write(self.beamercolorthemericeowl)
        with open(os.path.join(self.outdir, 'beamerouterthemeinfolines.sty'), 'w', encoding='UTF-8') as f:
            f.write(self.beamerouterthemeinfolines)
        with open(os.path.join(self.outdir, 'beamerthemeBoadilla.sty'), 'w', encoding='UTF-8') as f:
            f.write(self.beamerthemeBoadilla)
        return

SLIDES = '''
\\documentclass[ignorenonframetext,mathserif,12pt]{beamer}
'''
HOUT = '''
\\documentclass[letterpaper,11pt]{extarticle}
\\usepackage[noamsthm]{beamerarticle}
'''
THEME = {'heavy': '\\usetheme[numbers]{Rice}\n\\usecolortheme{riceowl}\n',
        'compact': '\\usetheme{Boadilla}\n\\usecolortheme{riceowl}\n',
        'plain': '\\usetheme{Boadilla}\n\\usecolortheme{dove}\n'
        }
CONFIG = '''
%%%%%%%%%%%%%%%%%%
%%%% Packages
%%%%%%%%%%%%%%%%%%
\\usepackage{amsmath}
\\usepackage{amssymb}
\\usepackage{url}
\\usepackage{verbatim}
\\usepackage{mathpazo}
\\usepackage{mathptmx}
\\usepackage{latexsym}
\\usepackage{graphicx}
\\usepackage{color}
\\usepackage{hyperref}
\\usepackage{beamerthemesplit}
\\usepackage{pgf,pgfarrows,pgfnodes,pgfautomata,pgfheaps,pgfshade}
\\usepackage{marvosym}
\\usepackage{bm}         %% 数学粗体（命令 \\bm）
\\usepackage{upgreek}    %% 直立体希腊字母（主要使用 \\uppi）
\\urlstyle{tt}
\\usepackage{lastpage}
\\usepackage{verbatim}
\\usepackage{ulem}
\\usepackage{pdfpages}

%%%%%%%%%%%%%%%%%%
%%%% 自定义命令
%%%%%%%%%%%%%%%%%%

\\newcommand\\dif{\\mathrm{d}}     %% 无前导空格的微分算子 d （一般用于分式）
\\newcommand\\diff{\\,\\dif}        %% 有前导空格的微分算子 d （一般用于积分式）
\\newcommand\\me{\\mathrm{e}}      %% 自然对数的底 e
\\newcommand\\mi{\\mathrm{i}}      %% 虚数单位 i
\\newcommand{\\defeq}{\\xlongequal{\\text{def}}}    %% 定义为
\\newcommand*{\\set}[1]{\\left\\{ #1 \\right\\}}                  %% 列举式集合
\\newcommand*{\\Set}[2]{\\left\\{ \\, #1 \\colon #2 \\, \\right\\}}  %% 描述式集合（分号隔开）
\\newcommand*{\\abs}[1]{\\left\\lvert #1 \\right\\rvert}          %% 绝对值
\\newcommand*{\\p}[1]{\\Pr{\\left\\{ #1\\right\\}}}  %% Probability

\\newcommand{\\cc}[1]{\\textcolor{red}{#1}} %% New color
\\newcommand{\\ie}{\\textit{i.e.}} %% i.e.
\\newcommand{\\bb}[1]{\\textbf{\\textcolor{blue}{#1}}}
\\newcommand{\\m}{\\Male}

\\newcommand{\\ignore}[1]{}
\\newcommand{\\mynote}[1]{\\textit{#1}}

\\definecolor{rblue}{rgb}{0,.14,.41}
\\newcommand{\\rb}[1]{\\textcolor{rblue}{#1}}
\\newcommand{\\rd}[1]{\\textcolor{red}{#1}}
\\newcommand{\\myref}[1]{\\tiny \\textit{#1}}
\\newcommand{\\itm}[1]{\\begin{itemize} \\item #1 \\end{itemize}}
\\hypersetup{
	pdftitle={Beamer Present},
	pdfsubject={Beamer Present},
	pdfauthor={gw_log},
%%	pdfpagemode={FullScreen},
	pdfkeywords={acrobat, Beamer},
	colorlinks={true},
	linkcolor={purple},
%% Predefined colors: red, green, blue, cyan, magenta, yellow, black, darkgray, gray, lightgray, orange, violet, purple, and brown
}
%%\\newenvironment{script}[1]
%%{\\block{}{#1}\\footnotesize\\semiverbatim}
%%{\\endsemiverbatim\\endblock}
%%\\newenvironment{out}
%%{\\exampleblock{}\\tiny\\semiverbatim}
%%{\\endsemiverbatim\\endexampleblock}

%%%%%%%%%%%%%%%%%%
%% Slide -- Rice color theme
%%%%%%%%%%%%%%%%%%

%%\\usetheme[numbers]{Rice}
	%% [ricet]		show the \\Large "RICE" word mark at the top-right
	%% [ricetm]		show the \\large "RICE" word mark at the top-right
	%% [ricets]		show the \\small "RICE" word mark at the top-right
	%% [riceb]		show the "RICE" word mark at the bottom-left
	%% [compress]	show only the current section / subsection in the top navigation area.
	%%			recommended if you have more than three subsections in at least one section
	%% [minimal]	hide top navigation
	%% [numbers]	show page numbers at the bottom-right
	%% [noshadow]	remove shadow
	%% [nologo]	remove Rice logo from the title page
	%% [ricegray]	use ricegray instead of riceblue
	%% [bgricegray]	use ricegray as background color
	%% [bggray]	use light gray as background color
	%% [smoothb]	top navigation with balls
    %% Themes(v3.0):
    %%	- W/o navigation bar: default, boxes, Bergen, Madrid, Pittsburgh, Rochester
    %% - With a treelike navigation bar: Antibes, JuanLesPins, Montpellier
    %% - With a TOC sidebar: Berkeley, PaloAlto, Goettingen, Marburg, Hannover
    %% - With a mini frame navigation: Berlin, Ilmenau, Dresden, Darmstadt, Frankfurt, Singapore, Szeged
    %% - With section and subsection titles: Copenhagen, Luebeck, Malmoe, Warsaw

%%\\usecolortheme{riceowl}
%%\\usecolortheme{dolphin}
%%\\usecolortheme{seagull}

    %% Four basic color themes:
    %% - Default and special purpose themes: default, structure 
    %% - Complete color themes: albatross, beetle, crane, dove, fly, seagull
    %% - Inner color themes: lily, orchid
    %% - Outer color themes: whale, seahorse

%%%%%%%%%%%%%%%%%%
%% Slide -- A simple clear theme
%%%%%%%%%%%%%%%%%%

%%\\usetheme{Boadilla}
%%\\usecolortheme{riceowl}
%%\\useinnertheme[shadow]{rounded}
\\useinnertheme{rectangles}
\\useoutertheme{infolines}
\\setbeamertemplate{bibliography item}[text]

%%%%%%%%%%%%%%%%%%
%% Inner theme settings
%%%%%%%%%%%%%%%%%%

\\setbeamercovered{transparent}
\\setbeamertemplate{blocks}[rounded]%%[shadow=true] %% format blocks
%%\\setbeamertemplate{footline}[frame number]
%% ----------- It is possible to customize Beamer color as follows
%%\\setbeamercolor{frametitle}{fg=black,bg=blue!6}
%%\\setbeamercolor{alerted_text}{fg=red!65black} %% to change \\alert color.
%%\\colorlet{structure}{blue!30!black} %% to change \\structure color.
%%\\setbeamertemplate{background canvas}[vertical shading][bottom=white,top=blue!5] %% background color
%% ----------- Set color for Beamer box
\\setbeamercolor{greencolu}{fg=white,bg=green!50!black}
\\setbeamercolor{greencoll}{fg=black,bg=green!8}
\\setbeamercolor{bluecolu}{fg=white,bg=blue!50!black}
\\setbeamercolor{bluecoll}{fg=black,bg=blue!8}
\\setbeamercolor{redcolu}{fg=white,bg=red!50!black}
\\setbeamercolor{redcoll}{fg=black,bg=red!8}

%%\\usefoottemplate{\\vbox{%%
%%\\tinycolouredline{structure!25}%%
%%{\\color{white}\\textbf{\\insertshortauthor\\hfill%%
%%\\insertshortinstitute}}%%
%%\\tinycolouredline{structure}%%
%%{\\color{white}\\textbf{\\insertshorttitle}\\hfill}%%
%%}}

%%%%%%%%%%%%%%%%%%
%% Logo settings
%%%%%%%%%%%%%%%%%%

%%\\pgfdeclaremask{baylor}{figures/baylor}
%%\\pgfdeclareimage[mask=baylor,width=.2in]{baylor-logo}{figures/baylor}
%%\\logo{\\vbox{\\vskip .1cm  \\hskip 9.8cm \\hbox{\\pgfuseimage{baylor-logo}}}}
%%\\logo{\\pgfuseimage{baylor-logo}}

%%%%%%%%%%%%%%%%%%
%% Notes (article version) layout settings
%%%%%%%%%%%%%%%%%%

\\mode<article>
{
  \\usepackage{times}
  \\usepackage[hmargin=1in, vmargin=1in]{geometry}
  \\definecolor{linkcolour}{rgb}{0,0.2,0.6}
  \\hypersetup{colorlinks, breaklinks, urlcolor=purple, linkcolor=linkcolour}
  \\usepackage{fancyhdr}
  \\usepackage{fancyvrb}

  \\pagestyle{fancy} %% fancy page: with header and footer
  \\setlength\\headheight{14pt}
  \\lhead{\\texttt{\\title, \\author}}
  \\rhead{\\texttt{\\today}}
  \\cfoot{\\thepage}
  \\renewcommand{\\headrulewidth}{0pt}
  \\renewcommand{\\footrulewidth}{0pt}
}

\\setbeamertemplate{frame end}{
    \\marginpar{\\scriptsize\\hbox to .2in{\\sffamily \\hfill\\strut\\insertframenumber}\\hrule height .2pt}
}
\\setlength{\\marginparwidth}{.2in}
\\setlength{\\marginparsep}{.5in}

%%\\makeatletter
%%\\let\\origstartsection=\\@startsection
%%\\def\\@startsection#1#2#3#4#5#6{%%
%%  \\origstartsection{#1}{#2}{#3}{#4}{#5}{#6\\normalfont\\sffamily\\color{blue!50!black}\\selectfont}}
%%\\makeatother

\\mode
<all>
'''

TITLE = '''
%%%%%%%%%%%%%%%%%%
%%%% Title Page
%%%%%%%%%%%%%%%%%%

%%\\title[Example slides using \\LaTeX ``Beamer'']{Example Presentation Created with the Beamer Package}
%% \\subtitle
%%\\author{Wang, Gao}
%%\\institute[Baylor Coll. Med.]{
%%	Department of Molecular and Human Genetics
%%	\\and
%%	Baylor College of Medicine
%%}
%%\\date[]{\\today}
%%\\date{December 27, 2009}

%%\\author[Webster,Gunzburger]{%%
%%  Clayton~Webster\\inst{1}
%%	\\and
%%  Max Gunzburger\\inst{2}}
%%\\institute[Florida State University]{
%%  \\inst{1}
%%  Department of Mathematics and School for Computational Science\\\\
%%  Florida State University
%%  \\and
%%  \\inst{2}
%%  School for Computational Science\\\\
%%  Florida State University}

%%\\institute[BCM]{\\includegraphics[width=.8cm]{figures/baylor.pdf} \\\\ {\\color{blue} Baylor College of Medicine}}
'''
THANK = '''
\\section*{Acknowledgement}
\\frame{
    \\begin{center}
    {\\Huge \\color{purple} \\textbf{Thank you!}} \\\\ \\bigskip
    {\\Large Questions? Criticisms?} \\\\  \\vfill
    \\end{center}
}
'''
