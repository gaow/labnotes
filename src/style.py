#!/usr/bin/env python
# -*- coding: utf-8 -*-
import os, codecs
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
%\\setbeamercolor*{example text}{fg=ricegray}
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
        self.beamerouterthemerice = '''
% Outer Theme for Rice Beamer Style ver. 0.01 (2008/10/10)
% Copyright 2003      by Till Tantau   <tantau@users.sourceforge.net>
%       and 2008 by Daina Chiba <d.chiba@rice.edu>
%
% This program can be redistributed and/or modified under the terms
% of the GNU Public License, version 2.

\\ProvidesPackage{beamerouterthemerice}[2008/10/10]

\\mode<presentation>

%=========================================================%
% Logo
%=========================================================%
%\\pgfdeclareimage[height=2em,interpolate=true]{ricelogotext}{rice/rice-logo}

%\\ifbeamer@nologo
% \\titlegraphic{\\pgfuseimage{ricelogotext}}
%\\fi

%=========================================================%
% Colors and Shades
%=========================================================%

\\setbeamercolor{section in head/foot}{parent=palette primary}
\\setbeamercolor{subsection in head/foot}{parent=palette secondary}

\\setbeamercolor{author in head/foot}{parent=section in head/foot}
\\setbeamercolor{title in head/foot}{parent=subsection in head/foot}
\\setbeamercolor{date in head/foot}{parent=palette tertiary}

\\setbeamercolor{frametitle}{parent=subsection in head/foot}
\\setbeamercolor{frametitle right}{parent=section in head/foot}

\\usesectionheadtemplate
  {\\hfill\\insertsectionhead}
  {\\hfill\\color{fg!50!bg}\\insertsectionhead}

\\pgfdeclarehorizontalshading[frametitle.bg,frametitle right.bg]{beamer@frametitleshade}{\\paperheight}{%
  color(0pt)=(frametitle.bg);
  color(\\paperwidth)=(frametitle right.bg)}

\\AtBeginDocument{
  \\pgfdeclareverticalshading{beamer@topshade}{\\paperwidth}{%
    color(0pt)=(bg);
    color(4pt)=(black!50!bg)}
}




%=========================================================%
% Header
%=========================================================%

\\ifbeamer@compress
  \\defbeamertemplate*{headline}{rice theme}
  {%
    \\leavevmode%
    \\begin{beamercolorbox}[wd=.5\\paperwidth,ht=2.5ex,dp=1.125ex,right]{section in head/foot}%
      \\usebeamerfont{section in head/foot}\\insertsectionhead\\hspace*{2ex}
    \\end{beamercolorbox}%
    \\begin{beamercolorbox}[wd=.5\\paperwidth,ht=2.5ex,dp=1.125ex,left]{subsection in head/foot}%
      \\usebeamerfont{subsection in head/foot}\\hspace*{2ex}\\insertsubsectionhead
    \\end{beamercolorbox}%
  }

\\else

  \\ifbeamer@minimal
    \\defbeamertemplate*{headline}{rice theme}{}

  \\else
    \\defbeamertemplate*{headline}{rice theme}
    {%
      \\leavevmode%
      \\@tempdimb=2.4375ex%
      \\ifnum\\beamer@subsectionmax<\\beamer@sectionmax%
        \\multiply\\@tempdimb by\\beamer@sectionmax%
      \\else%
        \\multiply\\@tempdimb by\\beamer@subsectionmax%
      \\fi%
      \\ifdim\\@tempdimb>0pt%
        \\advance\\@tempdimb by 1.125ex%
        \\begin{beamercolorbox}[wd=.5\\paperwidth,ht=\\@tempdimb]{section in head/foot}%
          \\vbox to\\@tempdimb{\\vfil\\insertsectionnavigation{.5\\paperwidth}\\vfil}%
        \\end{beamercolorbox}%
        \\begin{beamercolorbox}[wd=.5\\paperwidth,ht=\\@tempdimb]{subsection in head/foot}%
          \\vbox to\\@tempdimb{\\vfil\\insertsubsectionnavigation{.5\\paperwidth}\\vfil}%
        \\end{beamercolorbox}%
      \\fi%
    }

  \\fi

\\fi

\\ifbeamer@shadow
  \\addtobeamertemplate{headline}
  {}
  {%
    \\vskip-0.2pt
    \\pgfuseshading{beamer@topshade}
    \\vskip-2pt
  }
\\fi


%=========================================================%
% Footer
%=========================================================%

\\ifbeamer@smoothb
	\\useoutertheme[subsection=false]{smoothbars}
\\else

\\ifbeamer@numbers
\\defbeamertemplate*{footline}{rice theme}
{%
  \\leavevmode%
  \\hbox{\\begin{beamercolorbox}[wd=.5\\paperwidth,ht=2.5ex,dp=1.125ex,leftskip=.3cm,rightskip=.3cm]{author in head/foot}%
   \\ifbeamer@riceb {\\footnotesize \\trjnfamily RICE} \\fi \\hfill 
    \\usebeamerfont{author in head/foot} \\hfill\\insertshortauthor
  \\end{beamercolorbox}%
  \\begin{beamercolorbox}[wd=.5\\paperwidth,ht=2.5ex,dp=1.125ex,leftskip=.3cm,rightskip=.3cm plus1fil]{title in head/foot}%
    \\usebeamerfont{title in head/foot}\\insertshorttitle \\hfill \\insertframenumber{}
  \\end{beamercolorbox}}%
  \\vskip0pt%
}

\\else

\\defbeamertemplate*{footline}{rice theme}
{%
  \\leavevmode%
%  \\hbox{\\begin{beamercolorbox}[wd=.5\\paperwidth,ht=2.5ex,dp=1.125ex,leftskip=.3cm plus1fill,rightskip=.3cm]{author in head/foot}%
  \\hbox{\\begin{beamercolorbox}[wd=.5\\paperwidth,ht=2.5ex,dp=1.125ex,leftskip=.3cm,rightskip=.3cm]{author in head/foot}   \\ifbeamer@riceb {\\footnotesize \\trjnfamily RICE} \\fi \\hfill 
    \\usebeamerfont{author in head/foot}\\insertshortauthor
  \\end{beamercolorbox}%
  \\begin{beamercolorbox}[wd=.5\\paperwidth,ht=2.5ex,dp=1.125ex,leftskip=.3cm,rightskip=.3cm plus1fil]{title in head/foot}%
    \\usebeamerfont{title in head/foot}\\insertshorttitle
  \\end{beamercolorbox}}%
  \\vskip0pt%
}
\\fi
\\fi

%=========================================================%
% Frame Title
%=========================================================%

\\defbeamertemplate*{frametitle}{rice theme}
{%
  \\nointerlineskip%
  \\ifbeamer@shadow
    \\vskip-2pt%
  \\fi
  \\hbox{\\leavevmode
    \\advance\\beamer@leftmargin by -12bp%
    \\advance\\beamer@rightmargin by -12bp%
    \\beamer@tempdim=\\textwidth%
    \\advance\\beamer@tempdim by \\beamer@leftmargin%
    \\advance\\beamer@tempdim by \\beamer@rightmargin%
    \\hskip-\\Gm@lmargin\\hbox{%
      \\setbox\\beamer@tempbox=\\hbox{\\begin{minipage}[b]{\\paperwidth}%
          \\vbox{}\\vskip-.75ex%
          \\leftskip0.3cm%
          \\rightskip0.3cm plus1fil\\leavevmode
            \\insertframetitle
            \\ifbeamer@ricet \\hfill {\\Large \\trjnfamily RICE}
            \\else \\ifbeamer@ricetm \\hfill {\\large \\trjnfamily RICE}
            \\else \\ifbeamer@ricets \\hfill {\\small \\trjnfamily RICE} \\fi \\fi
            \\fi%
          \\ifx\\insertframesubtitle\\@empty%
            \\strut\\par%
          \\else
            \\par{\\usebeamerfont*{framesubtitle}{\\usebeamercolor[fg]{framesubtitle}\\insertframesubtitle}\\strut\\par}%
          \\fi%
          \\nointerlineskip
          \\vbox{}%
          \\end{minipage}}%
      \\beamer@tempdim=\\ht\\beamer@tempbox%
      \\advance\\beamer@tempdim by 2pt%
      \\begin{pgfpicture}{0pt}{0pt}{\\paperwidth}{\\beamer@tempdim}
        \\usebeamercolor{frametitle right}
        \\pgfpathrectangle{\\pgfpointorigin}{\\pgfpoint{\\paperwidth}{\\beamer@tempdim}}
        \\pgfusepath{clip}
        \\pgftext[left,base]{\\pgfuseshading{beamer@frametitleshade}}
      \\end{pgfpicture}
      \\hskip-\\paperwidth%
      \\box\\beamer@tempbox%
    }%
    \\hskip-\\Gm@rmargin%
  }%
  \\nointerlineskip
  \\ifbeamer@shadow
    \\vskip-0.2pt
    \\hbox to\\textwidth{\\hskip-\\Gm@lmargin\\pgfuseshading{beamer@topshade}\\hskip-\\Gm@rmargin}
    \\vskip-2pt
  \\fi
}

%=========================================================%
% Compressed title page
%=========================================================%

\\newcommand{\\compressedtitle}{%
  {
  \\setbeamertemplate{headline}
  {
    \\leavevmode%
    \\begin{beamercolorbox}[wd=.5\\paperwidth,ht=2.5ex,dp=1.125ex,right]{section in head/foot}%
    \\end{beamercolorbox}%
    \\begin{beamercolorbox}[wd=.5\\paperwidth,ht=2.5ex,dp=1.125ex,left]{subsection in head/foot}%
    \\end{beamercolorbox}%
    \\ifbeamer@shadow
      \\vskip-0.2pt
      \\pgfuseshading{beamer@topshade}
      \\vskip-2pt
    \\fi
  }
  \\beamer@calculateheadfoot

  \\begin{frame}
  \\titlepage
  \\end{frame}
  }

  \\setbeamertemplate{headline}[rice theme]
  \\ifbeamer@shadow
    \\addtobeamertemplate{headline}
    {}
    {%
      \\vskip-0.2pt
      \\pgfuseshading{beamer@topshade}
      \\vskip-2pt
    }
  \\fi
  \\beamer@calculateheadfoot
}

\\mode
<all>
        '''
        self.beamerouterthemerice2 = '''
% Outer Theme for Rice Beamer Style ver. 0.01 (2008/10/10)
% Copyright 2003      by Till Tantau   <tantau@users.sourceforge.net>
%       and 2008 by Daina Chiba <d.chiba@rice.edu>
%
% This program can be redistributed and/or modified under the terms
% of the GNU Public License, version 2.

\\ProvidesPackage{beamerouterthemerice2}[2008/11/22]

\\newif\\ifbeamer@sb@subsection

\\DeclareOptionBeamer{subsection}[true]{\\csname beamer@sb@subsection#1\\endcsname}
\\ExecuteOptionsBeamer{subsection=true}
\\ProcessOptionsBeamer

\\mode<presentation>

%=========================================================%
% Logo
%=========================================================%
%\\pgfdeclareimage[height=2em,interpolate=true]{ricelogotext}{rice/rice-logo}

%\\ifbeamer@nologo
% \\titlegraphic{\\pgfuseimage{ricelogotext}}
%\\fi

\\setbeamercolor{frametitle}{parent=palette primary}
\\setbeamercolor{subsection in head/foot}{parent=palette secondary}
\\setbeamercolor{section in head/foot}{parent=palette quaternary}


\\beamer@compresstrue

\\AtBeginDocument{
  {
    \\usebeamerfont*{headline}
    \\colorlet{global.bg}{bg}
    \\usebeamercolor{subsection in head/foot}
    \\usebeamercolor{section in head/foot}
    \\usebeamercolor{frametitle}

    \\ifbeamer@sb@subsection
      \\pgfdeclareverticalshading{beamer@barshade}{\\the\\paperwidth}{%
         color(0ex)=(global.bg);%
         color(1ex)=(subsection in head/foot.bg);%
         color(3.25ex)=(subsection in head/foot.bg);%
         color(4.25ex)=(section in head/foot.bg);%
         color(9.75ex)=(section in head/foot.bg)%
       }
       \\pgfdeclareverticalshading{beamer@aboveframetitle}{\\the\\paperwidth}{%
         color(0ex)=(frametitle.bg);%
         color(1ex)=(frametitle.bg);%
         color(2ex)=(subsection in head/foot.bg)
       }
    \\else
      \\pgfdeclareverticalshading{beamer@barshade}{\\the\\paperwidth}{%
         color(0ex)=(global.bg);%
         color(1ex)=(section in head/foot.bg);%
         color(7ex)=(section in head/foot.bg)%
       }
     \\pgfdeclareverticalshading{beamer@aboveframetitle}{\\the\\paperwidth}{%
         color(0ex)=(frametitle.bg);%
         color(1ex)=(frametitle.bg);%
         color(2ex)=(section in head/foot.bg)
       }
    \\fi

    \\pgfdeclareverticalshading{beamer@belowframetitle}{\\the\\paperwidth}{%
      color(0ex)=(global.bg);%
      color(1ex)=(frametitle.bg)
    }
  }
}

                                % Head
\\defbeamertemplate*{headline}{smoothbars theme}
{%
  \\pgfuseshading{beamer@barshade}%
  \\ifbeamer@sb@subsection%
    \\vskip-9.75ex%
  \\else%
    \\vskip-7ex%
  \\fi%
  \\begin{beamercolorbox}[ignorebg,ht=2.25ex,dp=3.75ex]{section in head/foot}
    \\insertnavigation{\\paperwidth}
  \\end{beamercolorbox}%
  \\ifbeamer@sb@subsection%
    \\begin{beamercolorbox}[ignorebg,ht=2.125ex,dp=1.125ex,%
      leftskip=.3cm,rightskip=.3cm plus1fil]{subsection in head/foot}
      \\usebeamerfont{subsection in head/foot}\\insertsubsectionhead
    \\end{beamercolorbox}%
  \\fi%
}%


\\defbeamertemplate*{frametitle}{smoothbars theme}
{%
  \\nointerlineskip%
  \\usebeamerfont{headline}%
  \\begin{beamercolorbox}[wd=\\paperwidth,ht=1.5ex,dp=0ex,vmode]{empty}
    \\pgfuseshading{beamer@aboveframetitle}%
  \\end{beamercolorbox}%
  \\vskip-.5ex%
  \\nointerlineskip%
  \\begin{beamercolorbox}[wd=\\paperwidth,leftskip=.3cm,rightskip=.3cm plus1fil,vmode]{frametitle}
    \\usebeamerfont*{frametitle}\\insertframetitle
                \\ifbeamer@ricet \\hfill {\\Large \\trjnfamily RICE}
            \\else \\ifbeamer@ricetm \\hfill {\\large \\trjnfamily RICE}
            \\else \\ifbeamer@ricets \\hfill {\\small \\trjnfamily RICE} \\fi \\fi
            \\fi%
      \\ifx\\insertframesubtitle\\@empty%
        \\strut\\par%
      \\else
        \\par{\\usebeamerfont*{framesubtitle}{\\usebeamercolor[fg]{framesubtitle}\\insertframesubtitle}\\strut\\par}%
      \\fi%%
    \\usebeamerfont{headline}%
    \\vskip.5ex
  \\end{beamercolorbox}%
  \\nointerlineskip
  \\begin{beamercolorbox}[wd=\\paperwidth,ht=.5ex,dp=0ex]{empty}
    \\pgfuseshading{beamer@belowframetitle}%
  \\end{beamercolorbox}%
}
\\mode
<all>
        '''
        self.beamerthemeRice = '''
\\ProvidesPackage{beamerthemeRice}[2008/10/10]
\\def\\beamerRice@version{0.01}

% Copyright 2003      by Till Tantau  <tantau@users.sourceforge.net>
%       and 2008 by Daina Chiba <d.chiba@rice.edu>
%
% This program can be redistributed and/or modified under the terms
% of the GNU Public License, version 2.


\\mode<presentation>

\\newif\\ifbeamer@minimal
\\newif\\ifbeamer@nonav
\\newif\\ifbeamer@bggray
\\newif\\ifbeamer@bgricegray
\\newif\\ifbeamer@ricegray
\\newif\\ifbeamer@numbers
\\newif\\ifbeamer@shadow
\\newif\\ifbeamer@ricet
\\newif\\ifbeamer@ricetm
\\newif\\ifbeamer@ricets
\\newif\\ifbeamer@riceb
\\newif\\ifbeamer@nologo
\\newif\\ifbeamer@smoothb

\\beamer@minimalfalse
\\beamer@nonavfalse
\\beamer@bggrayfalse
\\beamer@bgricegrayfalse
\\beamer@ricegrayfalse
\\beamer@numbersfalse
\\beamer@shadowtrue
\\beamer@ricetfalse
\\beamer@ricetmfalse
\\beamer@ricetsfalse
\\beamer@ricebfalse
\\beamer@nologotrue
\\beamer@smoothbfalse

\\DeclareOptionBeamer{compress}{\\beamer@compresstrue}
\\DeclareOptionBeamer{minimal}{\\beamer@minimaltrue}
\\DeclareOptionBeamer{nonav}{\\beamer@nonavtrue}
\\DeclareOptionBeamer{bggray}{\\beamer@bggraytrue}
\\DeclareOptionBeamer{bgricegray}{\\beamer@bgricegraytrue}
\\DeclareOptionBeamer{ricegray}{\\beamer@ricegraytrue}
\\DeclareOptionBeamer{numbers}{\\beamer@numberstrue}
\\DeclareOptionBeamer{noshadow}{\\beamer@shadowfalse}
\\DeclareOptionBeamer{ricet}{\\beamer@ricettrue}
\\DeclareOptionBeamer{ricetm}{\\beamer@ricetmtrue}
\\DeclareOptionBeamer{ricets}{\\beamer@ricetstrue}
\\DeclareOptionBeamer{riceb}{\\beamer@ricebtrue}
\\DeclareOptionBeamer{nologo}{\\beamer@nologofalse}
\\DeclareOptionBeamer{smoothb}{\\beamer@smoothbtrue}

\\ProcessOptionsBeamer

\\usecolortheme{riceowl}

%\\ifbeamer@shadow
%  \\useinnertheme[shadow=true]{round}
%\\else
  \\useinnertheme{rectangles}
%\\fi

\\ifbeamer@bgricegray
  \\setbeamercolor{normal text}{fg=white,bg=ricegray}
  \\setbeamercolor{alerted text}{fg=yellow}
  \\setbeamercolor{block body}{parent=normal text,use=block title,bg=block title.bg!15!bg}
\\fi

\\ifbeamer@ricegray
  \\setbeamercolor{block title}{fg=white,bg=ricegray}
  \\setbeamercolor*{palette primary}{fg=white,bg=riceblue}
\\setbeamercolor*{palette secondary}{fg=white,bg=black}
  \\setbeamercolor*{palette tertiary}{fg=white,bg=ricegray!110}
\\setbeamercolor*{palette quaternary}{fg=white,bg=riceblue}
  \\setbeamercolor{titlelike}{fg=white, bg=ricegray}
  \\setbeamercolor{frametitle}{fg=white, bg=ricegray}
  \\setbeamercolor{frametitle right}{fg=white, bg=ricegray}
  \\setbeamercolor{sidebar}{bg=riceblue}
\\fi

\\ifbeamer@nonav
  \\setbeamertemplate{navigation symbols}{}  % Removes navigation symbols.
\\fi

\\ifbeamer@smoothb
    \\useoutertheme[subsection=false]{rice2}
  \\else
    \\useoutertheme{rice}
\\fi

\\setbeamerfont{block title}{size={}}

\\mode
<all>
        '''

    def put(self):
        with codecs.open(os.path.join(self.outdir, 'beamercolorthemericeowl.sty'), 'w', encoding='UTF-8') as f:
            f.write(self.beamercolorthemericeowl)
        with codecs.open(os.path.join(self.outdir, 'beamerouterthemeinfolines.sty'), 'w', encoding='UTF-8') as f:
            f.write(self.beamerouterthemeinfolines)
        with codecs.open(os.path.join(self.outdir, 'beamerthemeBoadilla.sty'), 'w', encoding='UTF-8') as f:
            f.write(self.beamerthemeBoadilla)
        with codecs.open(os.path.join(self.outdir, 'beamerouterthemerice.sty'), 'w', encoding='UTF-8') as f:
            f.write(self.beamerouterthemerice)
        with codecs.open(os.path.join(self.outdir, 'beamerouterthemerice2.sty'), 'w', encoding='UTF-8') as f:
            f.write(self.beamerouterthemerice2)
        with codecs.open(os.path.join(self.outdir, 'beamerthemeRice.sty'), 'w', encoding='UTF-8') as f:
            f.write(self.beamerthemeRice)
        return

MODE = {'presentation':'\\documentclass[ignorenonframetext,mathserif,12pt,dvipsnames]{beamer}\n\\mode<presentation>\n\\setbeamertemplate{blocks}[rounded][shadow=true]\n',
        'notes':'\\documentclass[letterpaper,10pt,dvipsnames]{extarticle}\n\\usepackage[noamsthm]{beamerarticle}\n\\mode<article>\n',
        'handout':'\\documentclass[ignorenonframetext,mathserif,handout,12pt,dvipsnames]{beamer}\n\\mode<handout>\n\\setbeamertemplate{blocks}[rounded][shadow=true]\n'
        }
THEME = {'heavy': '\\usetheme[numbers]{Rice}\n\\usecolortheme{riceowl}\n',
        'compact': '\\usetheme{Boadilla}\n\\usecolortheme{riceowl}\n\\useinnertheme{rectangles}\n\\useoutertheme{infolines}\n',
        'plain': '\\usetheme{Boadilla}\n\\usecolortheme{dove}\n\\useinnertheme{rectangles}\n\\useoutertheme{infolines}\n'
        }
CONFIG = '''
%%%%%%%%%%%%%%%%%%
%%%% Packages
%%%%%%%%%%%%%%%%%%
\\usepackage{amsmath}
\\usepackage{amssymb}
\\usepackage{url}
%% \\usepackage{mathpazo}
%% \\usepackage{mathptmx}
\\usepackage{latexsym}
\\usepackage{fancyvrb}
\\usepackage{graphicx}
\\usepackage{color}
\\usepackage{beamerthemesplit}
\\usepackage{pgf,pgfarrows,pgfnodes,pgfautomata,pgfheaps,pgfshade}
\\usepackage{marvosym}
\\usepackage{bm}
\DeclareMathAlphabet{\mathbbm}{U}{bbm}{m}{n}
\\usepackage{upgreek}
\\urlstyle{tt}
\\usepackage{lastpage}
\\usepackage{ulem}
\\usepackage{pdfpages}
\\usepackage{pgfpages}
\\usepackage{longtable}
\\usepackage{subfigure}
\\usepackage{multicol}
\\usepackage[numbered]{bookmark}
%%Make sure it comes last of your loaded packages
\\usepackage{hyperref}
%%%%%%%%%%%%%%%%%%
%%%% 
%%%%%%%%%%%%%%%%%%
\\DeclareMathOperator*{\\dif}{\\mathrm{d}}
\\DeclareMathOperator*{\\diff}{\\,\\dif}
\\DeclareMathOperator*{\\e}{\\mathrm{e}}
\\DeclareMathOperator*{\\E}{\\mathbb{E}}
\\DeclareMathOperator*{\\V}{\\mathbb{V}}
\\DeclareMathOperator*{\\defeq}{\\xlongequal{\\text{def}}}
\\newcommand*{\\set}[1]{\\left\\{ #1 \\right\\}}
\\newcommand*{\\Set}[2]{\\left\\{ \\, #1 \\colon #2 \\, \\right\\}}
\\newcommand*{\\abs}[1]{\\left\\lvert #1 \\right\\rvert}
\\newcommand*{\\p}[1]{\\Pr{\\left\\{ #1\\right\\}}}

\\newcommand\\independent{\\protect\\mathpalette{\\protect\\independenT}{\\perp}}
\\def\\independenT#1#2{\\mathrel{\\rlap{$#1#2$}\\mkern2mu{#1#2}}}

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
	pdftitle={Beamer Presentation},
	pdfsubject={Beamer Presentation},
	pdfauthor={tigernotes},
%%	pdfpagemode={FullScreen},
	pdfkeywords={acrobat, Beamer}%%,
%%	colorlinks={true},
%%	linkcolor={purple}
%% Predefined colors: red, green, blue, cyan, magenta, yellow, black, darkgray, gray, lightgray, orange, violet, purple, and brown
}
%%\\newenvironment{script}[1]
%%{\\block{}{#1}\\footnotesize\\semiverbatim}
%%{\\endsemiverbatim\\endblock}
%%\\newenvironment{out}
%%{\\exampleblock{}\\tiny\\semiverbatim}
%%{\\endsemiverbatim\\endexampleblock}

\\setbeamertemplate{bibliography item}[text]
\\makeatletter
\\renewcommand\\@biblabel[1]{#1.}
\\renewcommand\\@cite[1]{\\textsuperscript{#1}}
\\makeatother
\\setbeamertemplate{frametitle continuation}[from second]

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
%%\\useinnertheme{rectangles}
%%\\useoutertheme{infolines}

%%%%%%%%%%%%%%%%%%
%% Inner theme settings
%%%%%%%%%%%%%%%%%%

\\setbeamercovered{transparent}
%%\\setbeamertemplate{blocks}[rounded][shadow=true] %% format blocks
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
\\mode<handout>{
  \\pgfpagesuselayout{4 on 1}[letterpaper,landscape,border shrink=2.5mm]
}

\\mode<article>
{
  \\usepackage{times}
  \\usepackage[hmargin=1in, vmargin=1in]{geometry}
  \\definecolor{linkcolour}{rgb}{0,0.2,0.6}
  \\hypersetup{colorlinks, breaklinks, urlcolor=purple, linkcolor=linkcolour}
  \\usepackage{fancyhdr}
  \\usepackage{fancyvrb}

  \\renewcommand\\rmdefault{bch}
%%  \\pagestyle{fancy} %% fancy page: with header and footer
%%  \\setlength\\headheight{14pt}
%%  \\lhead{\\texttt{\\title, \\author}}
%%  \\rhead{\\texttt{\\today}}
%%  \\cfoot{\\thepage}
%%  \\renewcommand{\\headrulewidth}{0pt}
%%  \\renewcommand{\\footrulewidth}{0pt}
  \\pagestyle{plain}

%% frame split
\\usepackage{tikz}
\\defbeamertemplate<article>{frame begin}{lined}{\\par\\noindent\\rule{\\textwidth}{1pt}\\par}
\\defbeamertemplate<article>{frame end}{lined}{\\par\\noindent\\rule{\\textwidth}{1pt}\\par}
\\newcounter{framebox}
\\defbeamertemplate<article>{frame begin}{tikzed}{\\par\\noindent\\stepcounter{framebox}\\tikz[remember picture,overlay] \\path (-1ex,0) coordinate (frame top \\the\\value{framebox});}
\\defbeamertemplate<article>{frame end}{tikzed}{\\hspace*{\\fill}\\tikz[remember picture,overlay] \\draw (frame top \\the\\value{framebox}) rectangle (1ex,0);\\par}
\\setbeamertemplate{frame begin}[lined]
%%\\setbeamertemplate{frame end}[lined]
%%\\setbeamertemplate{frame begin}[tikzed]
%%\\setbeamertemplate{frame end}[tikzed]
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
}
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

DOC_PACKAGES = '''
\\usepackage[text={6.5in,8.9in}, marginparwidth=0.5in]{geometry}
\\usepackage{amsmath}
\\usepackage{booktabs}
\\usepackage{amssymb}
\\usepackage{amsthm}
\\usepackage{mathabx}
\\newcommand\hmmax{0} % default 3
\\usepackage{bm}
\\usepackage{fancyhdr}
\\usepackage{fancyvrb}
\\usepackage{shadow}
%%\\usepackage{graphicx}
\\usepackage[pdftex]{graphicx}
\\usepackage[dvipsnames]{xcolor}
\\usepackage{minted}
\\usepackage{upquote}
%%\\usepackage[utf8]{inputenc}
%%\\usepackage{ucs}
\\usepackage{titlesec}
\\usepackage{longtable}
\\usepackage{subfigure}
\\usepackage{float}
\\usepackage{varwidth}
\\usepackage[tikz]{bclogo}
'''

DOC_CONFIG = '''
\\DeclareMathOperator*{\\dif}{\\mathrm{d}}
\\DeclareMathOperator*{\\diff}{\\,\\dif}
\\DeclareMathOperator*{\\e}{\\mathrm{e}}
\\DeclareMathOperator*{\\E}{\\mathbb{E}}
\\DeclareMathOperator*{\\V}{\\mathbb{V}}
\\DeclareMathOperator*{\\defeq}{\\xlongequal{\\text{def}}}
\\newcommand*{\\set}[1]{\\left\\{ #1 \\right\\}}
\\newcommand*{\\Set}[2]{\\left\\{ \\, #1 \\colon #2 \\, \\right\\}}
\\newcommand*{\\abs}[1]{\\left\\lvert #1 \\right\\rvert}
\\newcommand*{\\p}[1]{\\Pr{\\left\\{ #1\\right\\}}}

\\newcommand{\\ie}{\\textit{i.e.}}

\\newcommand\\independent{\\protect\\mathpalette{\\protect\\independenT}{\\perp}}
\\def\\independenT#1#2{\\mathrel{\\rlap{$#1#2$}\\mkern2mu{#1#2}}}

\\newcommand*\\circled[1]{\\kern-2.5em
  \\put(0,4){\\color{black}\\circle*{18}}\\put(0,4){\\circle{16}}
  \\put(-3,0){\\color{white}\\\\bfseries\\large#1}}
\\linespread{1.1}
\\setlength{\\parskip}{8pt plus 1pt minus 1pt}
\\parindent 0ex
\\geometry{left=0.8in,right=0.8in,top=0.8in,bottom=0.8in}
\\renewcommand{\\labelitemii}{$\\blacktriangleright$}
\\renewcommand{\\labelitemiii}{$\\smalltriangleright$}
\\makeatletter
\\renewcommand\\@biblabel[1]{#1.}
\\renewcommand\\@cite[1]{\\textsuperscript{#1}}
\\makeatother
\\renewcommand{\\thesubfigure}{\\thefigure.\\arabic{subfigure}}
\\definecolor{bg}{rgb}{0.95,0.95,0.95}
\\definecolor{rblue}{rgb}{0,.14,.41}
\\definecolor{rgray}{RGB}{94,96,98}
\\definecolor{wwwcolor}{rgb}{0,0.2,0.6}
\\setcounter{secnumdepth}{3}
\\setcounter{tocdepth}{3}
\\titleformat{\\subsubsection}{\\color{rblue}\\normalfont\\bfseries}{$\\centerdot$}{.5em}{}
\\usepackage[bookmarksnumbered=true,pdfstartview=FitH]{hyperref}
\\hypersetup{colorlinks, breaklinks, urlcolor=wwwcolor, linkcolor=wwwcolor, citecolor=MidnightBlue}
'''
######################################################

MAIN_STY = r'''
@font-face {
  font-family: 'PT Sans';
  font-style: normal;
  font-weight: 400;
  src: local('PT Sans'), local('PTSans-Regular'), url(PTSans.woff) format('woff');
}
html {background: #FFFFFF}
/*
body {
	columns: 30em;
	column-gap: 20px;
	padding: 0;
	margin: 6em 3% 19em 3%;
	background: #fff;
	font-family: 'Lucida Grande', 'Lucida Sans', 'Lucida Sans Unicode', Tahoma, sans-serif;
	font-size: 10pt;
	line-height: 150%;
	text-align:justify;
	color: #555;
	position: relative;
	box-shadow: 0 .3em 1em #000
}
*/
body
{
	margin:40px 0;
	padding:0;
	font-family: 'PT Sans', 'Lucida Grande', 'Lucida Sans', 'Lucida Sans Unicode', Tahoma, sans-serif;
	font-size: 10pt;
	text-align:justify;
	line-height: 150%;
	color: #333;
}

table {border-spacing: 2px;}
td, th
{
	border: 0;
	padding: 10px;
	text-align: left;
}
td
{
	vertical-align:top;
}
th
{
	background-color:#eee;
}
td.flag
{
	font-family:monospace;
}
tr.dark
{
	background-color:#f9f9f9;
}

ol
{
	list-style-type: lower-greek;
	font-family: 'PT Sans', 'Lucida Grande';
}

a,
a:link,
a:visited,
a:active
{
	color: #3366CC;
	border-bottom: 1px dotted #3366CC;
	text-decoration:none;
}
a:hover
{
	border-bottom: none;
	color: #000030;
}

.normal
{
	font-family: 'PT Sans', Helvetica, Arial, sans-serif;
	font-size: 11pt;
}

.minorhead
{
	color: #666;
	font-family: monospace;
	line-height: 30px;
}

.gray
{
	color:#666;
	font-weight: bold;
	font-family:monospace;
	background: #eee;
	padding: 2px 6px 2px 6px;
	white-space: nowrap;
}

.three-col {
       -moz-column-count: 3;
       -moz-column-gap: 30px;
       -webkit-column-count: 3;
       -webkit-column-gap : 30px;
       -moz-column-rule-color:  #ccc;
       -moz-column-rule-style:  solid;
       -moz-column-rule-width:  1px;
       -webkit-column-rule-color:  #ccc;
       -webkit-column-rule-style: solid ;
       -webkit-column-rule-width:  1px;
}

.two-col {
       -moz-column-count: 2;
       -moz-column-gap: 30px;
       -webkit-column-count: 2;
       -webkit-column-gap : 30px;
       -moz-column-rule-color:  #ccc;
       -moz-column-rule-style:  solid;
       -moz-column-rule-width:  1px;
       -webkit-column-rule-color:  #ccc;
       -webkit-column-rule-style: solid ;
       -webkit-column-rule-width:  1px;
}

.frame
{
	margin: 0px auto 50px auto;
	width: 800px;
}

.content
{
	padding: 0 20px;
}

.title {
	column-span: all;
	margin: 0 -20px 0 -20px;
	padding: .6em 1em;
	border-left: solid transparent 30px;
	border-right: solid transparent 30px;
	text-align:center;
	line-height: 120%;
	color: #666;
	font-variant: small-caps;
	font-family: 'PT Sans', Georgia, Times, serif;
	background: #eee;
}

.author {
	color:#304860;
	text-align:center;
	font-family:"PT Sans", comic sans ms;
	font-size:small;
}

.superheading
{
    break-inside: avoid;
	margin: 1em 0 0 0;
	padding: .5em;
	font-size: 20pt;
	line-height: 120%;
	color: #666;
}

.heading
{
	margin-top: 30px;
	font-size: 14pt;
	line-height: 120%;
	color: #666;
}

.subheading
{
	margin-top: 20px;
	font-size: 12pt;
	color: #304860;
}

.subsubheading
{
	margin-top: 15px;
	font-size: 11pt;
	font-weight: bold;
	color: #304860;
	/* font-style: oblique; */
}

.download
{
	font-weight: normal;
	font-family: Georgia;
	background: #eee;
	padding:20px 20px;
	color: #666;
	text-align:center;
	font-style: italic;
}
.download:hover
{
	background:#fafafa;
}
.download a
{
	text-transform: uppercase;
	font-weight: bold;
	font-size: 12pt;
	text-shadow: 1px 1px 1px #999;
	border: none;
	font-style: normal;
}

#clear { clear:both; }

#form
{
	background-color: #f9f9f9;
	padding: 5px 20px 20px 20px;
}

#form .set
{
	float: left;
	margin-right: 20px;
}

#form .field
{
	border: 1px solid #ccc;
	padding: 1px;
	margin-top: 5px;
	width: 150px;
}

#form .text_input
{
	width: 146px;
}

#form #zoosbmt
{
	margin-top: 5px;
}

#wrapper {
	text-align: left;
    width:95%;
}

#toc {
	list-style: none;
	margin-bottom: 20px;
}
#toc li {
	/* background: url(dot.gif) repeat-x bottom left; */
	overflow: hidden;
	padding-bottom: 2px;
}
#toc a,
#toc span {
	display: inline-block;
	background: #fff;
	position: relative;
	bottom: -4px;
}
#toc a {
	float: right;
	padding: 0 0 3px 2px;
}
#toc span {
	float: left;
	padding: 0 2px 3px 0;
}

.tip {
	margin: 10px 0px 10px 0px;
	padding: 10px 5px 10px 15px;
    border-radius:12px;
	box-shadow: 3px 3px 2px #888888;
	background: #ddffdd no-repeat 20px;
}

.important {
	margin: 10px 0px 10px 0px;
	padding: 10px 5px 10px 15px;
    border-radius:12px;
	box-shadow: 3px 3px 2px #888888;
	background: lightblue no-repeat 20px;
}

.note {
	margin: 10px 0px 10px 0px;
	padding: 10px 5px 10px 15px;
    border-radius:12px;
	box-shadow: 3px 3px 2px #888888;
	background: #ffffcc no-repeat 20px;
}

.warning {
	margin: 10px 0px 10px 0px;
	padding: 10px 5px 10px 15px;
    border-radius:12px;
	box-shadow: 3px 3px 2px #888888;
	background: #ffdddd no-repeat 20px;
}
/* .textborder {border: 1px dashed rgb(0, 36, 105); padding: 2px;} */
.textborder {border: 1px dashed rgb(220, 20, 60); padding: 2px;}

textarea
{
    border:1px solid #999999;
    width:95%;
    margin:5px 0;
    padding:1%;
    font-size: small;
    font-family: "Lucida Console", Monaco, monospace;
}
kbd
{
    text-shadow: 0.2px 0.2px 0.2px;
}
'''

SYN_STY = r'''
.syntaxhighlighter a,
.syntaxhighlighter div,
.syntaxhighlighter code,
.syntaxhighlighter table,
.syntaxhighlighter table td,
.syntaxhighlighter table tr,
.syntaxhighlighter table tbody,
.syntaxhighlighter table thead,
.syntaxhighlighter table caption,
.syntaxhighlighter textarea {
  -moz-border-radius: 0 0 0 0 !important;
  -webkit-border-radius: 0 0 0 0 !important;
  background: none !important;
  border: 0 !important;
  bottom: auto !important;
  float: none !important;
  height: auto !important;
  left: auto !important;
  line-height: 1.6em !important;
  margin: 0 !important;
  outline: 0 !important;
  padding: 0 !important;
  position: static !important;
  right: auto !important;
  text-align: left !important;
  top: auto !important;
  vertical-align: baseline !important;
  width: auto !important;
  box-sizing: content-box !important;
  font-family: monospace !important;
  font-weight: normal !important;
  font-style: normal !important;
  font-size: medium !important;
  letter-spacing: -1px;
  /*min-height: inherit !important; */
  /*min-height: auto !important;*/
  direction: ltr !important;
}

.syntaxhighlighter {
  width: 100% !important;
  margin: 1em 0 1em 0 !important;
  position: relative !important;
  font-size: 1em !important;
}
.syntaxhighlighter code {
  display: inline !important;
}
.syntaxhighlighter.source {
}
.syntaxhighlighter .bold {
  font-weight: bold !important;
}
.syntaxhighlighter .italic {
  font-style: italic !important;
}
.syntaxhighlighter .line {
  white-space: pre !important;
}
.syntaxhighlighter table {
  width: 100% !important;
}
.syntaxhighlighter table caption {
  text-align: left !important;
  padding: .5em 0 0.5em 1em !important;
}
.syntaxhighlighter table td.code {
  width: 100% !important;
}
.syntaxhighlighter table td.code .container {
  position: relative !important;
}
.syntaxhighlighter table td.code .container textarea {
  box-sizing: border-box !important;
  position: absolute !important;
  left: 0 !important;
  top: 0 !important;
  width: 100% !important;
  height: 100% !important;
  border: none !important;
  background: white !important;
  padding-left: 1em !important;
  white-space: pre !important;
}
.syntaxhighlighter table td.gutter .line {
  text-align: right !important;
  padding: 0 0.5em 0 1em !important;
}
.syntaxhighlighter table td.code .line {
  padding: 0 1em !important;
}
.syntaxhighlighter.nogutter td.code .container textarea, .syntaxhighlighter.nogutter td.code .line {
  padding-left: 0em !important;
}
.syntaxhighlighter.show {
  display: block !important;
}
.syntaxhighlighter.collapsed table {
  display: none !important;
}
.syntaxhighlighter.collapsed .toolbar {
  padding: 0.1em 0.8em 0em 0.8em !important;
  font-size: 1em !important;
  position: static !important;
  width: auto !important;
  height: auto !important;
}
.syntaxhighlighter.collapsed .toolbar span {
  display: inline !important;
  margin-right: 1em !important;
}
.syntaxhighlighter.collapsed .toolbar span a {
  padding: 0 !important;
  display: none !important;
}
.syntaxhighlighter.collapsed .toolbar span a.expandSource {
  display: inline !important;
}
.syntaxhighlighter .toolbar {
  position: absolute !important;
  right: 1px !important;
  top: 1px !important;
  width: 11px !important;
  height: 11px !important;
  font-size: 10px !important;
  z-index: 10 !important;
}
.syntaxhighlighter .toolbar span.title {
  display: inline !important;
}
.syntaxhighlighter .toolbar a {
  display: block !important;
  text-align: center !important;
  text-decoration: none !important;
  padding-top: 1px !important;
}
.syntaxhighlighter .toolbar a.expandSource {
  display: none !important;
}
.syntaxhighlighter.ie {
  font-size: .9em !important;
  padding: 1px 0 1px 0 !important;
}
.syntaxhighlighter.ie .toolbar {
  line-height: 8px !important;
}
.syntaxhighlighter.ie .toolbar a {
  padding-top: 0px !important;
}
.syntaxhighlighter.printing .line.alt1 .content,
.syntaxhighlighter.printing .line.alt2 .content,
.syntaxhighlighter.printing .line.highlighted .number,
.syntaxhighlighter.printing .line.highlighted.alt1 .content,
.syntaxhighlighter.printing .line.highlighted.alt2 .content {
  background: none !important;
}
.syntaxhighlighter.printing .line .number {
  color: #bbbbbb !important;
}
.syntaxhighlighter.printing .line .content {
  color: black !important;
}
.syntaxhighlighter.printing .toolbar {
  display: none !important;
}
.syntaxhighlighter.printing a {
  text-decoration: none !important;
}
.syntaxhighlighter.printing .plain, .syntaxhighlighter.printing .plain a {
  color: black !important;
}
.syntaxhighlighter.printing .comments, .syntaxhighlighter.printing .comments a {
  color: #008200 !important;
}
.syntaxhighlighter.printing .string, .syntaxhighlighter.printing .string a {
  color: blue !important;
}
.syntaxhighlighter.printing .keyword {
  color: #006699 !important;
  font-weight: bold !important;
}
.syntaxhighlighter.printing .preprocessor {
  color: gray !important;
}
.syntaxhighlighter.printing .variable {
  color: #aa7700 !important;
}
.syntaxhighlighter.printing .value {
  color: #009900 !important;
}
.syntaxhighlighter.printing .functions {
  color: #ff1493 !important;
}
.syntaxhighlighter.printing .constants {
  color: #0066cc !important;
}
.syntaxhighlighter.printing .script {
  font-weight: bold !important;
}
.syntaxhighlighter.printing .color1, .syntaxhighlighter.printing .color1 a {
  color: gray !important;
}
.syntaxhighlighter.printing .color2, .syntaxhighlighter.printing .color2 a {
  color: #ff1493 !important;
}
.syntaxhighlighter.printing .color3, .syntaxhighlighter.printing .color3 a {
  color: red !important;
}
.syntaxhighlighter.printing .break, .syntaxhighlighter.printing .break a {
  color: black !important;
}

.syntaxhighlighter {
  background-color: white !important;
}
.syntaxhighlighter .line.alt1 {
  background-color: white !important;
}
.syntaxhighlighter .line.alt2 {
  background-color: white !important;
}
.syntaxhighlighter .line.highlighted.alt1, .syntaxhighlighter .line.highlighted.alt2 {
  background-color: #c3defe !important;
}
.syntaxhighlighter .line.highlighted.number {
  color: white !important;
}
.syntaxhighlighter table caption {
  color: black !important;
}
.syntaxhighlighter .gutter {
  color: #787878 !important;
}
.syntaxhighlighter .gutter .line {
  border-right: 3px solid #d4d0c8 !important;
}
.syntaxhighlighter .gutter .line.highlighted {
  background-color: #d4d0c8 !important;
  color: white !important;
}
.syntaxhighlighter.printing .line .content {
  border: none !important;
}
.syntaxhighlighter.collapsed {
  overflow: visible !important;
}
.syntaxhighlighter.collapsed .toolbar {
  color: #3f5fbf !important;
  background: white !important;
  border: 1px solid #d4d0c8 !important;
}
.syntaxhighlighter.collapsed .toolbar a {
  color: #3f5fbf !important;
}
.syntaxhighlighter.collapsed .toolbar a:hover {
  color: #aa7700 !important;
}
.syntaxhighlighter .toolbar {
  color: #a0a0a0 !important;
  background: #d4d0c8 !important;
  border: none !important;
}
.syntaxhighlighter .toolbar a {
  color: #a0a0a0 !important;
}
.syntaxhighlighter .toolbar a:hover {
  color: red !important;
}
.syntaxhighlighter .plain, .syntaxhighlighter .plain a {
  color: black !important;
}
.syntaxhighlighter .comments, .syntaxhighlighter .comments a {
  color: #3f5fbf !important;
}
.syntaxhighlighter .string, .syntaxhighlighter .string a {
  color: #2a00ff !important;
}
.syntaxhighlighter .keyword {
  color: #7f0055 !important;
}
.syntaxhighlighter .preprocessor {
  color: #646464 !important;
}
.syntaxhighlighter .variable {
  color: #aa7700 !important;
}
.syntaxhighlighter .value {
  color: #009900 !important;
}
.syntaxhighlighter .functions {
  color: #ff1493 !important;
}
.syntaxhighlighter .constants {
  color: #0066cc !important;
}
.syntaxhighlighter .script {
  font-weight: bold !important;
  color: #7f0055 !important;
  background-color: none !important;
}
.syntaxhighlighter .color1, .syntaxhighlighter .color1 a {
  color: gray !important;
}
.syntaxhighlighter .color2, .syntaxhighlighter .color2 a {
  color: #ff1493 !important;
}
.syntaxhighlighter .color3, .syntaxhighlighter .color3 a {
  color: red !important;
}

.syntaxhighlighter .keyword {
  font-weight: bold !important;
}
.syntaxhighlighter .xml .keyword {
  color: #3f7f7f !important;
  font-weight: normal !important;
}
.syntaxhighlighter .xml .color1, .syntaxhighlighter .xml .color1 a {
  color: #7f007f !important;
}
.syntaxhighlighter .xml .string {
  font-style: italic !important;
  color: #2a00ff !important;
}
'''
HTML_STYLE = MAIN_STY + SYN_STY
JS_SCRIPT = r'''
(function()
{
	// CommonJS
	typeof(require) != 'undefined' ? SyntaxHighlighter = require('shCore').SyntaxHighlighter : null;

	function Brush()
	{
		var keywords =	'if fi then elif else for do done until while break continue case function return in eq ne ge le';
		var commands =  'alias apropos awk basename bash bc bg builtin bzip2 cal cat cd cfdisk chgrp chmod chown chroot' +
						'cksum clear cmp comm command cp cron crontab csplit cut date dc dd ddrescue declare df ' +
						'diff diff3 dig dir dircolors dirname dirs du echo egrep eject enable env ethtool eval ' +
						'exec exit expand export expr false fdformat fdisk fg fgrep file find fmt fold format ' +
						'free fsck ftp gawk getopts grep groups gzip hash head history hostname id ifconfig ' +
						'import install join kill less let ln local locate logname logout look lpc lpr lprint ' +
						'lprintd lprintq lprm ls lsof make man mkdir mkfifo mkisofs mknod more mount mtools ' +
						'mv netstat nice nl nohup nslookup open op passwd paste pathchk ping popd pr printcap ' +
						'printenv printf ps pushd pwd quota quotacheck quotactl ram rcp read readonly renice ' +
						'remsync rm rmdir rsync screen scp sdiff sed select seq set sftp shift shopt shutdown ' +
						'sleep sort source split ssh strace su sudo sum symlink sync tail tar tee test time ' +
						'times touch top traceroute trap tr true tsort tty type ulimit umask umount unalias ' +
						'uname unexpand uniq units unset unshar useradd usermod users uuencode uudecode v vdir ' +
						'vi watch wc whereis which who whoami Wget xargs yes'
						;

		this.regexList = [
			{ regex: /^#!.*$/gm,											css: 'preprocessor bold' },
			{ regex: /\/[\w-\/]+/gm,										css: 'plain' },
			{ regex: SyntaxHighlighter.regexLib.singleLinePerlComments,		css: 'comments' },		// one line comments
			{ regex: SyntaxHighlighter.regexLib.doubleQuotedString,			css: 'string' },		// double quoted strings
			{ regex: SyntaxHighlighter.regexLib.singleQuotedString,			css: 'string' },		// single quoted strings
			{ regex: new RegExp(this.getKeywords(keywords), 'gm'),			css: 'keyword' },		// keywords
			{ regex: new RegExp(this.getKeywords(commands), 'gm'),			css: 'functions' }		// commands
			];
	}

	Brush.prototype	= new SyntaxHighlighter.Highlighter();
	Brush.aliases	= ['bash', 'shell'];

	SyntaxHighlighter.brushes.Bash = Brush;

	// CommonJS
	typeof(exports) != 'undefined' ? exports.Brush = Brush : null;
})();
eval(function(p,a,c,k,e,d){e=function(c){return(c<a?'':e(parseInt(c/a)))+((c=c%a)>35?String.fromCharCode(c+29):c.toString(36))};if(!''.replace(/^/,String)){while(c--){d[e(c)]=k[c]||e(c)}k=[function(e){return d[e]}];e=function(){return'\\w+'};c=1};while(c--){if(k[c]){p=p.replace(new RegExp('\\b'+e(c)+'\\b','g'),k[c])}}return p}('K M;I(M)1S 2U("2a\'t 4k M 4K 2g 3l 4G 4H");(6(){6 r(f,e){I(!M.1R(f))1S 3m("3s 15 4R");K a=f.1w;f=M(f.1m,t(f)+(e||""));I(a)f.1w={1m:a.1m,19:a.19?a.19.1a(0):N};H f}6 t(f){H(f.1J?"g":"")+(f.4s?"i":"")+(f.4p?"m":"")+(f.4v?"x":"")+(f.3n?"y":"")}6 B(f,e,a,b){K c=u.L,d,h,g;v=R;5K{O(;c--;){g=u[c];I(a&g.3r&&(!g.2p||g.2p.W(b))){g.2q.12=e;I((h=g.2q.X(f))&&h.P===e){d={3k:g.2b.W(b,h,a),1C:h};1N}}}}5v(i){1S i}5q{v=11}H d}6 p(f,e,a){I(3b.Z.1i)H f.1i(e,a);O(a=a||0;a<f.L;a++)I(f[a]===e)H a;H-1}M=6(f,e){K a=[],b=M.1B,c=0,d,h;I(M.1R(f)){I(e!==1d)1S 3m("2a\'t 5r 5I 5F 5B 5C 15 5E 5p");H r(f)}I(v)1S 2U("2a\'t W 3l M 59 5m 5g 5x 5i");e=e||"";O(d={2N:11,19:[],2K:6(g){H e.1i(g)>-1},3d:6(g){e+=g}};c<f.L;)I(h=B(f,c,b,d)){a.U(h.3k);c+=h.1C[0].L||1}Y I(h=n.X.W(z[b],f.1a(c))){a.U(h[0]);c+=h[0].L}Y{h=f.3a(c);I(h==="[")b=M.2I;Y I(h==="]")b=M.1B;a.U(h);c++}a=15(a.1K(""),n.Q.W(e,w,""));a.1w={1m:f,19:d.2N?d.19:N};H a};M.3v="1.5.0";M.2I=1;M.1B=2;K C=/\\$(?:(\\d\\d?|[$&`\'])|{([$\\w]+)})/g,w=/[^5h]+|([\\s\\S])(?=[\\s\\S]*\\1)/g,A=/^(?:[?*+]|{\\d+(?:,\\d*)?})\\??/,v=11,u=[],n={X:15.Z.X,1A:15.Z.1A,1C:1r.Z.1C,Q:1r.Z.Q,1e:1r.Z.1e},x=n.X.W(/()??/,"")[1]===1d,D=6(){K f=/^/g;n.1A.W(f,"");H!f.12}(),y=6(){K f=/x/g;n.Q.W("x",f,"");H!f.12}(),E=15.Z.3n!==1d,z={};z[M.2I]=/^(?:\\\\(?:[0-3][0-7]{0,2}|[4-7][0-7]?|x[\\29-26-f]{2}|u[\\29-26-f]{4}|c[A-3o-z]|[\\s\\S]))/;z[M.1B]=/^(?:\\\\(?:0(?:[0-3][0-7]{0,2}|[4-7][0-7]?)?|[1-9]\\d*|x[\\29-26-f]{2}|u[\\29-26-f]{4}|c[A-3o-z]|[\\s\\S])|\\(\\?[:=!]|[?*+]\\?|{\\d+(?:,\\d*)?}\\??)/;M.1h=6(f,e,a,b){u.U({2q:r(f,"g"+(E?"y":"")),2b:e,3r:a||M.1B,2p:b||N})};M.2n=6(f,e){K a=f+"/"+(e||"");H M.2n[a]||(M.2n[a]=M(f,e))};M.3c=6(f){H r(f,"g")};M.5l=6(f){H f.Q(/[-[\\]{}()*+?.,\\\\^$|#\\s]/g,"\\\\$&")};M.5e=6(f,e,a,b){e=r(e,"g"+(b&&E?"y":""));e.12=a=a||0;f=e.X(f);H b?f&&f.P===a?f:N:f};M.3q=6(){M.1h=6(){1S 2U("2a\'t 55 1h 54 3q")}};M.1R=6(f){H 53.Z.1q.W(f)==="[2m 15]"};M.3p=6(f,e,a,b){O(K c=r(e,"g"),d=-1,h;h=c.X(f);){a.W(b,h,++d,f,c);c.12===h.P&&c.12++}I(e.1J)e.12=0};M.57=6(f,e){H 6 a(b,c){K d=e[c].1I?e[c]:{1I:e[c]},h=r(d.1I,"g"),g=[],i;O(i=0;i<b.L;i++)M.3p(b[i],h,6(k){g.U(d.3j?k[d.3j]||"":k[0])});H c===e.L-1||!g.L?g:a(g,c+1)}([f],0)};15.Z.1p=6(f,e){H J.X(e[0])};15.Z.W=6(f,e){H J.X(e)};15.Z.X=6(f){K e=n.X.1p(J,14),a;I(e){I(!x&&e.L>1&&p(e,"")>-1){a=15(J.1m,n.Q.W(t(J),"g",""));n.Q.W(f.1a(e.P),a,6(){O(K c=1;c<14.L-2;c++)I(14[c]===1d)e[c]=1d})}I(J.1w&&J.1w.19)O(K b=1;b<e.L;b++)I(a=J.1w.19[b-1])e[a]=e[b];!D&&J.1J&&!e[0].L&&J.12>e.P&&J.12--}H e};I(!D)15.Z.1A=6(f){(f=n.X.W(J,f))&&J.1J&&!f[0].L&&J.12>f.P&&J.12--;H!!f};1r.Z.1C=6(f){M.1R(f)||(f=15(f));I(f.1J){K e=n.1C.1p(J,14);f.12=0;H e}H f.X(J)};1r.Z.Q=6(f,e){K a=M.1R(f),b,c;I(a&&1j e.58()==="3f"&&e.1i("${")===-1&&y)H n.Q.1p(J,14);I(a){I(f.1w)b=f.1w.19}Y f+="";I(1j e==="6")c=n.Q.W(J,f,6(){I(b){14[0]=1f 1r(14[0]);O(K d=0;d<b.L;d++)I(b[d])14[0][b[d]]=14[d+1]}I(a&&f.1J)f.12=14[14.L-2]+14[0].L;H e.1p(N,14)});Y{c=J+"";c=n.Q.W(c,f,6(){K d=14;H n.Q.W(e,C,6(h,g,i){I(g)5b(g){24"$":H"$";24"&":H d[0];24"`":H d[d.L-1].1a(0,d[d.L-2]);24"\'":H d[d.L-1].1a(d[d.L-2]+d[0].L);5a:i="";g=+g;I(!g)H h;O(;g>d.L-3;){i=1r.Z.1a.W(g,-1)+i;g=1Q.3i(g/10)}H(g?d[g]||"":"$")+i}Y{g=+i;I(g<=d.L-3)H d[g];g=b?p(b,i):-1;H g>-1?d[g+1]:h}})})}I(a&&f.1J)f.12=0;H c};1r.Z.1e=6(f,e){I(!M.1R(f))H n.1e.1p(J,14);K a=J+"",b=[],c=0,d,h;I(e===1d||+e<0)e=5D;Y{e=1Q.3i(+e);I(!e)H[]}O(f=M.3c(f);d=f.X(a);){I(f.12>c){b.U(a.1a(c,d.P));d.L>1&&d.P<a.L&&3b.Z.U.1p(b,d.1a(1));h=d[0].L;c=f.12;I(b.L>=e)1N}f.12===d.P&&f.12++}I(c===a.L){I(!n.1A.W(f,"")||h)b.U("")}Y b.U(a.1a(c));H b.L>e?b.1a(0,e):b};M.1h(/\\(\\?#[^)]*\\)/,6(f){H n.1A.W(A,f.2S.1a(f.P+f[0].L))?"":"(?:)"});M.1h(/\\((?!\\?)/,6(){J.19.U(N);H"("});M.1h(/\\(\\?<([$\\w]+)>/,6(f){J.19.U(f[1]);J.2N=R;H"("});M.1h(/\\\\k<([\\w$]+)>/,6(f){K e=p(J.19,f[1]);H e>-1?"\\\\"+(e+1)+(3R(f.2S.3a(f.P+f[0].L))?"":"(?:)"):f[0]});M.1h(/\\[\\^?]/,6(f){H f[0]==="[]"?"\\\\b\\\\B":"[\\\\s\\\\S]"});M.1h(/^\\(\\?([5A]+)\\)/,6(f){J.3d(f[1]);H""});M.1h(/(?:\\s+|#.*)+/,6(f){H n.1A.W(A,f.2S.1a(f.P+f[0].L))?"":"(?:)"},M.1B,6(){H J.2K("x")});M.1h(/\\./,6(){H"[\\\\s\\\\S]"},M.1B,6(){H J.2K("s")})})();1j 2e!="1d"&&(2e.M=M);K 1v=6(){6 r(a,b){a.1l.1i(b)!=-1||(a.1l+=" "+b)}6 t(a){H a.1i("3e")==0?a:"3e"+a}6 B(a){H e.1Y.2A[t(a)]}6 p(a,b,c){I(a==N)H N;K d=c!=R?a.3G:[a.2G],h={"#":"1c",".":"1l"}[b.1o(0,1)]||"3h",g,i;g=h!="3h"?b.1o(1):b.5u();I((a[h]||"").1i(g)!=-1)H a;O(a=0;d&&a<d.L&&i==N;a++)i=p(d[a],b,c);H i}6 C(a,b){K c={},d;O(d 2g a)c[d]=a[d];O(d 2g b)c[d]=b[d];H c}6 w(a,b,c,d){6 h(g){g=g||1P.5y;I(!g.1F){g.1F=g.52;g.3N=6(){J.5w=11}}c.W(d||1P,g)}a.3g?a.3g("4U"+b,h):a.4y(b,h,11)}6 A(a,b){K c=e.1Y.2j,d=N;I(c==N){c={};O(K h 2g e.1U){K g=e.1U[h];d=g.4x;I(d!=N){g.1V=h.4w();O(g=0;g<d.L;g++)c[d[g]]=h}}e.1Y.2j=c}d=e.1U[c[a]];d==N&&b!=11&&1P.1X(e.13.1x.1X+(e.13.1x.3E+a));H d}6 v(a,b){O(K c=a.1e("\\n"),d=0;d<c.L;d++)c[d]=b(c[d],d);H c.1K("\\n")}6 u(a,b){I(a==N||a.L==0||a=="\\n")H a;a=a.Q(/</g,"&1y;");a=a.Q(/ {2,}/g,6(c){O(K d="",h=0;h<c.L-1;h++)d+=e.13.1W;H d+" "});I(b!=N)a=v(a,6(c){I(c.L==0)H"";K d="";c=c.Q(/^(&2s;| )+/,6(h){d=h;H""});I(c.L==0)H d;H d+\'<17 1g="\'+b+\'">\'+c+"</17>"});H a}6 n(a,b){a.1e("\\n");O(K c="",d=0;d<50;d++)c+="                    ";H a=v(a,6(h){I(h.1i("\\t")==-1)H h;O(K g=0;(g=h.1i("\\t"))!=-1;)h=h.1o(0,g)+c.1o(0,b-g%b)+h.1o(g+1,h.L);H h})}6 x(a){H a.Q(/^\\s+|\\s+$/g,"")}6 D(a,b){I(a.P<b.P)H-1;Y I(a.P>b.P)H 1;Y I(a.L<b.L)H-1;Y I(a.L>b.L)H 1;H 0}6 y(a,b){6 c(k){H k[0]}O(K d=N,h=[],g=b.2D?b.2D:c;(d=b.1I.X(a))!=N;){K i=g(d,b);I(1j i=="3f")i=[1f e.2L(i,d.P,b.23)];h=h.1O(i)}H h}6 E(a){K b=/(.*)((&1G;|&1y;).*)/;H a.Q(e.3A.3M,6(c){K d="",h=N;I(h=b.X(c)){c=h[1];d=h[2]}H\'<a 2h="\'+c+\'">\'+c+"</a>"+d})}6 z(){O(K a=1E.36("1k"),b=[],c=0;c<a.L;c++)a[c].3s=="20"&&b.U(a[c]);H b}6 f(a){a=a.1F;K b=p(a,".20",R);a=p(a,".3O",R);K c=1E.4i("3t");I(!(!a||!b||p(a,"3t"))){B(b.1c);r(b,"1m");O(K d=a.3G,h=[],g=0;g<d.L;g++)h.U(d[g].4z||d[g].4A);h=h.1K("\\r");c.39(1E.4D(h));a.39(c);c.2C();c.4C();w(c,"4u",6(){c.2G.4E(c);b.1l=b.1l.Q("1m","")})}}I(1j 3F!="1d"&&1j M=="1d")M=3F("M").M;K e={2v:{"1g-27":"","2i-1s":1,"2z-1s-2t":11,1M:N,1t:N,"42-45":R,"43-22":4,1u:R,16:R,"3V-17":R,2l:11,"41-40":R,2k:11,"1z-1k":11},13:{1W:"&2s;",2M:R,46:11,44:11,34:"4n",1x:{21:"4o 1m",2P:"?",1X:"1v\\n\\n",3E:"4r\'t 4t 1D O: ",4g:"4m 4B\'t 51 O 1z-1k 4F: ",37:\'<!4T 1z 4S "-//4V//3H 4W 1.0 4Z//4Y" "1Z://2y.3L.3K/4X/3I/3H/3I-4P.4J"><1z 4I="1Z://2y.3L.3K/4L/5L"><3J><4N 1Z-4M="5G-5M" 6K="2O/1z; 6J=6I-8" /><1t>6L 1v</1t></3J><3B 1L="25-6M:6Q,6P,6O,6N-6F;6y-2f:#6x;2f:#6w;25-22:6v;2O-3D:3C;"><T 1L="2O-3D:3C;3w-32:1.6z;"><T 1L="25-22:6A-6E;">1v</T><T 1L="25-22:.6C;3w-6B:6R;"><T>3v 3.0.76 (72 73 3x)</T><T><a 2h="1Z://3u.2w/1v" 1F="38" 1L="2f:#3y">1Z://3u.2w/1v</a></T><T>70 17 6U 71.</T><T>6T 6X-3x 6Y 6D.</T></T><T>6t 61 60 J 1k, 5Z <a 2h="6u://2y.62.2w/63-66/65?64=5X-5W&5P=5O" 1L="2f:#3y">5R</a> 5V <2R/>5U 5T 5S!</T></T></3B></1z>\'}},1Y:{2j:N,2A:{}},1U:{},3A:{6n:/\\/\\*[\\s\\S]*?\\*\\//2c,6m:/\\/\\/.*$/2c,6l:/#.*$/2c,6k:/"([^\\\\"\\n]|\\\\.)*"/g,6o:/\'([^\\\\\'\\n]|\\\\.)*\'/g,6p:1f M(\'"([^\\\\\\\\"]|\\\\\\\\.)*"\',"3z"),6s:1f M("\'([^\\\\\\\\\']|\\\\\\\\.)*\'","3z"),6q:/(&1y;|<)!--[\\s\\S]*?--(&1G;|>)/2c,3M:/\\w+:\\/\\/[\\w-.\\/?%&=:@;]*/g,6a:{18:/(&1y;|<)\\?=?/g,1b:/\\?(&1G;|>)/g},69:{18:/(&1y;|<)%=?/g,1b:/%(&1G;|>)/g},6d:{18:/(&1y;|<)\\s*1k.*?(&1G;|>)/2T,1b:/(&1y;|<)\\/\\s*1k\\s*(&1G;|>)/2T}},16:{1H:6(a){6 b(i,k){H e.16.2o(i,k,e.13.1x[k])}O(K c=\'<T 1g="16">\',d=e.16.2x,h=d.2X,g=0;g<h.L;g++)c+=(d[h[g]].1H||b)(a,h[g]);c+="</T>";H c},2o:6(a,b,c){H\'<2W><a 2h="#" 1g="6e 6h\'+b+" "+b+\'">\'+c+"</a></2W>"},2b:6(a){K b=a.1F,c=b.1l||"";b=B(p(b,".20",R).1c);K d=6(h){H(h=15(h+"6f(\\\\w+)").X(c))?h[1]:N}("6g");b&&d&&e.16.2x[d].2B(b);a.3N()},2x:{2X:["21","2P"],21:{1H:6(a){I(a.V("2l")!=R)H"";K b=a.V("1t");H e.16.2o(a,"21",b?b:e.13.1x.21)},2B:6(a){a=1E.6j(t(a.1c));a.1l=a.1l.Q("47","")}},2P:{2B:6(){K a="68=0";a+=", 18="+(31.30-33)/2+", 32="+(31.2Z-2Y)/2+", 30=33, 2Z=2Y";a=a.Q(/^,/,"");a=1P.6Z("","38",a);a.2C();K b=a.1E;b.6W(e.13.1x.37);b.6V();a.2C()}}}},35:6(a,b){K c;I(b)c=[b];Y{c=1E.36(e.13.34);O(K d=[],h=0;h<c.L;h++)d.U(c[h]);c=d}c=c;d=[];I(e.13.2M)c=c.1O(z());I(c.L===0)H d;O(h=0;h<c.L;h++){O(K g=c[h],i=a,k=c[h].1l,j=3W 0,l={},m=1f M("^\\\\[(?<2V>(.*?))\\\\]$"),s=1f M("(?<27>[\\\\w-]+)\\\\s*:\\\\s*(?<1T>[\\\\w-%#]+|\\\\[.*?\\\\]|\\".*?\\"|\'.*?\')\\\\s*;?","g");(j=s.X(k))!=N;){K o=j.1T.Q(/^[\'"]|[\'"]$/g,"");I(o!=N&&m.1A(o)){o=m.X(o);o=o.2V.L>0?o.2V.1e(/\\s*,\\s*/):[]}l[j.27]=o}g={1F:g,1n:C(i,l)};g.1n.1D!=N&&d.U(g)}H d},1M:6(a,b){K c=J.35(a,b),d=N,h=e.13;I(c.L!==0)O(K g=0;g<c.L;g++){b=c[g];K i=b.1F,k=b.1n,j=k.1D,l;I(j!=N){I(k["1z-1k"]=="R"||e.2v["1z-1k"]==R){d=1f e.4l(j);j="4O"}Y I(d=A(j))d=1f d;Y 6H;l=i.3X;I(h.2M){l=l;K m=x(l),s=11;I(m.1i("<![6G[")==0){m=m.4h(9);s=R}K o=m.L;I(m.1i("]]\\>")==o-3){m=m.4h(0,o-3);s=R}l=s?m:l}I((i.1t||"")!="")k.1t=i.1t;k.1D=j;d.2Q(k);b=d.2F(l);I((i.1c||"")!="")b.1c=i.1c;i.2G.74(b,i)}}},2E:6(a){w(1P,"4k",6(){e.1M(a)})}};e.2E=e.2E;e.1M=e.1M;e.2L=6(a,b,c){J.1T=a;J.P=b;J.L=a.L;J.23=c;J.1V=N};e.2L.Z.1q=6(){H J.1T};e.4l=6(a){6 b(j,l){O(K m=0;m<j.L;m++)j[m].P+=l}K c=A(a),d,h=1f e.1U.5Y,g=J,i="2F 1H 2Q".1e(" ");I(c!=N){d=1f c;O(K k=0;k<i.L;k++)(6(){K j=i[k];g[j]=6(){H h[j].1p(h,14)}})();d.28==N?1P.1X(e.13.1x.1X+(e.13.1x.4g+a)):h.2J.U({1I:d.28.17,2D:6(j){O(K l=j.17,m=[],s=d.2J,o=j.P+j.18.L,F=d.28,q,G=0;G<s.L;G++){q=y(l,s[G]);b(q,o);m=m.1O(q)}I(F.18!=N&&j.18!=N){q=y(j.18,F.18);b(q,j.P);m=m.1O(q)}I(F.1b!=N&&j.1b!=N){q=y(j.1b,F.1b);b(q,j.P+j[0].5Q(j.1b));m=m.1O(q)}O(j=0;j<m.L;j++)m[j].1V=c.1V;H m}})}};e.4j=6(){};e.4j.Z={V:6(a,b){K c=J.1n[a];c=c==N?b:c;K d={"R":R,"11":11}[c];H d==N?c:d},3Y:6(a){H 1E.4i(a)},4c:6(a,b){K c=[];I(a!=N)O(K d=0;d<a.L;d++)I(1j a[d]=="2m")c=c.1O(y(b,a[d]));H J.4e(c.6b(D))},4e:6(a){O(K b=0;b<a.L;b++)I(a[b]!==N)O(K c=a[b],d=c.P+c.L,h=b+1;h<a.L&&a[b]!==N;h++){K g=a[h];I(g!==N)I(g.P>d)1N;Y I(g.P==c.P&&g.L>c.L)a[b]=N;Y I(g.P>=c.P&&g.P<d)a[h]=N}H a},4d:6(a){K b=[],c=2u(J.V("2i-1s"));v(a,6(d,h){b.U(h+c)});H b},3U:6(a){K b=J.V("1M",[]);I(1j b!="2m"&&b.U==N)b=[b];a:{a=a.1q();K c=3W 0;O(c=c=1Q.6c(c||0,0);c<b.L;c++)I(b[c]==a){b=c;1N a}b=-1}H b!=-1},2r:6(a,b,c){a=["1s","6i"+b,"P"+a,"6r"+(b%2==0?1:2).1q()];J.3U(b)&&a.U("67");b==0&&a.U("1N");H\'<T 1g="\'+a.1K(" ")+\'">\'+c+"</T>"},3Q:6(a,b){K c="",d=a.1e("\\n").L,h=2u(J.V("2i-1s")),g=J.V("2z-1s-2t");I(g==R)g=(h+d-1).1q().L;Y I(3R(g)==R)g=0;O(K i=0;i<d;i++){K k=b?b[i]:h+i,j;I(k==0)j=e.13.1W;Y{j=g;O(K l=k.1q();l.L<j;)l="0"+l;j=l}a=j;c+=J.2r(i,k,a)}H c},49:6(a,b){a=x(a);K c=a.1e("\\n");J.V("2z-1s-2t");K d=2u(J.V("2i-1s"));a="";O(K h=J.V("1D"),g=0;g<c.L;g++){K i=c[g],k=/^(&2s;|\\s)+/.X(i),j=N,l=b?b[g]:d+g;I(k!=N){j=k[0].1q();i=i.1o(j.L);j=j.Q(" ",e.13.1W)}i=x(i);I(i.L==0)i=e.13.1W;a+=J.2r(g,l,(j!=N?\'<17 1g="\'+h+\' 5N">\'+j+"</17>":"")+i)}H a},4f:6(a){H a?"<4a>"+a+"</4a>":""},4b:6(a,b){6 c(l){H(l=l?l.1V||g:g)?l+" ":""}O(K d=0,h="",g=J.V("1D",""),i=0;i<b.L;i++){K k=b[i],j;I(!(k===N||k.L===0)){j=c(k);h+=u(a.1o(d,k.P-d),j+"48")+u(k.1T,j+k.23);d=k.P+k.L+(k.75||0)}}h+=u(a.1o(d),c()+"48");H h},1H:6(a){K b="",c=["20"],d;I(J.V("2k")==R)J.1n.16=J.1n.1u=11;1l="20";J.V("2l")==R&&c.U("47");I((1u=J.V("1u"))==11)c.U("6S");c.U(J.V("1g-27"));c.U(J.V("1D"));a=a.Q(/^[ ]*[\\n]+|[\\n]*[ ]*$/g,"").Q(/\\r/g," ");b=J.V("43-22");I(J.V("42-45")==R)a=n(a,b);Y{O(K h="",g=0;g<b;g++)h+=" ";a=a.Q(/\\t/g,h)}a=a;a:{b=a=a;h=/<2R\\s*\\/?>|&1y;2R\\s*\\/?&1G;/2T;I(e.13.46==R)b=b.Q(h,"\\n");I(e.13.44==R)b=b.Q(h,"");b=b.1e("\\n");h=/^\\s*/;g=4Q;O(K i=0;i<b.L&&g>0;i++){K k=b[i];I(x(k).L!=0){k=h.X(k);I(k==N){a=a;1N a}g=1Q.4q(k[0].L,g)}}I(g>0)O(i=0;i<b.L;i++)b[i]=b[i].1o(g);a=b.1K("\\n")}I(1u)d=J.4d(a);b=J.4c(J.2J,a);b=J.4b(a,b);b=J.49(b,d);I(J.V("41-40"))b=E(b);1j 2H!="1d"&&2H.3S&&2H.3S.1C(/5s/)&&c.U("5t");H b=\'<T 1c="\'+t(J.1c)+\'" 1g="\'+c.1K(" ")+\'">\'+(J.V("16")?e.16.1H(J):"")+\'<3Z 5z="0" 5H="0" 5J="0">\'+J.4f(J.V("1t"))+"<3T><3P>"+(1u?\'<2d 1g="1u">\'+J.3Q(a)+"</2d>":"")+\'<2d 1g="17"><T 1g="3O">\'+b+"</T></2d></3P></3T></3Z></T>"},2F:6(a){I(a===N)a="";J.17=a;K b=J.3Y("T");b.3X=J.1H(a);J.V("16")&&w(p(b,".16"),"5c",e.16.2b);J.V("3V-17")&&w(p(b,".17"),"56",f);H b},2Q:6(a){J.1c=""+1Q.5d(1Q.5n()*5k).1q();e.1Y.2A[t(J.1c)]=J;J.1n=C(e.2v,a||{});I(J.V("2k")==R)J.1n.16=J.1n.1u=11},5j:6(a){a=a.Q(/^\\s+|\\s+$/g,"").Q(/\\s+/g,"|");H"\\\\b(?:"+a+")\\\\b"},5f:6(a){J.28={18:{1I:a.18,23:"1k"},1b:{1I:a.1b,23:"1k"},17:1f M("(?<18>"+a.18.1m+")(?<17>.*?)(?<1b>"+a.1b.1m+")","5o")}}};H e}();1j 2e!="1d"&&(2e.1v=1v);',62,441,'||||||function|||||||||||||||||||||||||||||||||||||return|if|this|var|length|XRegExp|null|for|index|replace|true||div|push|getParam|call|exec|else|prototype||false|lastIndex|config|arguments|RegExp|toolbar|code|left|captureNames|slice|right|id|undefined|split|new|class|addToken|indexOf|typeof|script|className|source|params|substr|apply|toString|String|line|title|gutter|SyntaxHighlighter|_xregexp|strings|lt|html|test|OUTSIDE_CLASS|match|brush|document|target|gt|getHtml|regex|global|join|style|highlight|break|concat|window|Math|isRegExp|throw|value|brushes|brushName|space|alert|vars|http|syntaxhighlighter|expandSource|size|css|case|font|Fa|name|htmlScript|dA|can|handler|gm|td|exports|color|in|href|first|discoveredBrushes|light|collapse|object|cache|getButtonHtml|trigger|pattern|getLineHtml|nbsp|numbers|parseInt|defaults|com|items|www|pad|highlighters|execute|focus|func|all|getDiv|parentNode|navigator|INSIDE_CLASS|regexList|hasFlag|Match|useScriptTags|hasNamedCapture|text|help|init|br|input|gi|Error|values|span|list|250|height|width|screen|top|500|tagName|findElements|getElementsByTagName|aboutDialog|_blank|appendChild|charAt|Array|copyAsGlobal|setFlag|highlighter_|string|attachEvent|nodeName|floor|backref|output|the|TypeError|sticky|Za|iterate|freezeTokens|scope|type|textarea|alexgorbatchev|version|margin|2010|005896|gs|regexLib|body|center|align|noBrush|require|childNodes|DTD|xhtml1|head|org|w3|url|preventDefault|container|tr|getLineNumbersHtml|isNaN|userAgent|tbody|isLineHighlighted|quick|void|innerHTML|create|table|links|auto|smart|tab|stripBrs|tabs|bloggerMode|collapsed|plain|getCodeLinesHtml|caption|getMatchesHtml|findMatches|figureOutLineNumbers|removeNestedMatches|getTitleHtml|brushNotHtmlScript|substring|createElement|Highlighter|load|HtmlScript|Brush|pre|expand|multiline|min|Can|ignoreCase|find|blur|extended|toLowerCase|aliases|addEventListener|innerText|textContent|wasn|select|createTextNode|removeChild|option|same|frame|xmlns|dtd|twice|1999|equiv|meta|htmlscript|transitional|1E3|expected|PUBLIC|DOCTYPE|on|W3C|XHTML|TR|EN|Transitional||configured|srcElement|Object|after|run|dblclick|matchChain|valueOf|constructor|default|switch|click|round|execAt|forHtmlScript|token|gimy|functions|getKeywords|1E6|escape|within|random|sgi|another|finally|supply|MSIE|ie|toUpperCase|catch|returnValue|definition|event|border|imsx|constructing|one|Infinity|from|when|Content|cellpadding|flags|cellspacing|try|xhtml|Type|spaces|2930402|hosted_button_id|lastIndexOf|donate|active|development|keep|to|xclick|_s|Xml|please|like|you|paypal|cgi|cmd|webscr|bin|highlighted|scrollbars|aspScriptTags|phpScriptTags|sort|max|scriptScriptTags|toolbar_item|_|command|command_|number|getElementById|doubleQuotedString|singleLinePerlComments|singleLineCComments|multiLineCComments|singleQuotedString|multiLineDoubleQuotedString|xmlComments|alt|multiLineSingleQuotedString|If|https|1em|000|fff|background|5em|xx|bottom|75em|Gorbatchev|large|serif|CDATA|continue|utf|charset|content|About|family|sans|Helvetica|Arial|Geneva|3em|nogutter|Copyright|syntax|close|write|2004|Alex|open|JavaScript|highlighter|July|02|replaceChild|offset|83'.split('|'),0,{}))
(function(){
                var corecss = document.createElement('link');
                var themecss = document.createElement('link');
                var corecssurl = "http://nosemaj.org/wordpress/wp-content/plugins/syntaxhighlighter/syntaxhighlighter3/styles/shCore.css?ver=3.0.83c";
                if ( corecss.setAttribute ) {
                                corecss.setAttribute( "rel", "stylesheet" );
                                corecss.setAttribute( "type", "text/css" );
                                corecss.setAttribute( "href", corecssurl );
                } else {
                                corecss.rel = "stylesheet";
                                corecss.href = corecssurl;
                }
                document.getElementsByTagName("head")[0].insertBefore( corecss, document.getElementById("syntaxhighlighteranchor") );
                var themecssurl = "http://nosemaj.org/wordpress/wp-content/plugins/syntaxhighlighter/syntaxhighlighter3/styles/shThemeEclipse.css?ver=3.0.83c";
                if ( themecss.setAttribute ) {
                                themecss.setAttribute( "rel", "stylesheet" );
                                themecss.setAttribute( "type", "text/css" );
                                themecss.setAttribute( "href", themecssurl );
                } else {
                                themecss.rel = "stylesheet";
                                themecss.href = themecssurl;
                }
                //document.getElementById("syntaxhighlighteranchor").appendChild(themecss);
                document.getElementsByTagName("head")[0].insertBefore( themecss, document.getElementById("syntaxhighlighteranchor") );
})();
        SyntaxHighlighter.config.strings.expandSource = '+ expand source';
        SyntaxHighlighter.config.strings.help = '?';
        SyntaxHighlighter.config.strings.alert = 'SyntaxHighlighter\n\n';
        SyntaxHighlighter.config.strings.noBrush = 'Can\'t find brush for: ';
        SyntaxHighlighter.config.strings.brushNotHtmlScript = 'Brush wasn\'t configured for html-script option: ';
        SyntaxHighlighter.defaults['pad-line-numbers'] = false;
        SyntaxHighlighter.defaults['toolbar'] = false;
        SyntaxHighlighter.all();
'''
from time import strftime, localtime
HTML_INDEX = {
'head':r'''
<!DOCTYPE html>
<html lang="en">
<head>
	<meta charset="utf-8">
	<title>Documentation Files Navigation</title>
	<style type="text/css"/>
* {
	/* Lazy reset */
	margin: 0;
	padding: 0;
}
body {
	background: #fff;
	color: #444;
	font-size: 14px;
	line-height: 1.5em;
	font-family: arial, sans-serif;
	text-align: center;
}
#wrapper {
	text-align: left;
	margin: 5em auto;
	width: 600px;
}

/* Font styles */
h1 {
	font-size: 18px;
	margin-bottom: 20px;
	text-align: center;
}
h4 {
	font-style: italic;
	margin-bottom: 5px;
}
a {
	color: #990000;
	text-decoration: none;
}
a:hover {
	color: #c40000;
	opacity: 0.7;
	-moz-opacity: 0.7;
	filter:alpha(opacity=70);
}
hr {
      border: 0;
      height: 2px;
      /* Mozilla */
      background: -moz-linear-gradient(left, #990000, white);
      /* Webkit */
      background: -webkit-gradient(linear, left top, right top,
         from(#990000), to(white));
      /* IE */
      filter: progid:DXImageTransform.Microsoft.gradient(
         gradientType=1, startColorstr=#990000, endColorstr=#FFFFFF);
}
/* Core nav styles */
#toc {
	list-style: none;
	margin-bottom: 20px;
}
#toc li {
	background: url(dot.gif) repeat-x bottom left;
	overflow: hidden;
	padding-bottom: 2px;
}
#toc a,
#toc span {
	display: inline-block;
	background: #fff;
	position: relative;
	bottom: -4px;
}
#toc a {
	float: right;
	padding: 0 0 3px 2px;
}
#toc span {
	float: left;
	padding: 0 2px 3px 0;
}
</style>
</head>
<body>
<div id="wrapper">
	<h1>Documentation Files Navigation</h1>
	<ul id="toc">
''',
'tail':'</ul><h4>Last updated: %s</h4></div></body></html>' % strftime("%a %d %b %Y %H:%M:%S", localtime())
        }
