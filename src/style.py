#!/usr/bin/env python
# -*- coding: utf-8 -*-
import os, codecs, re
from time import strftime, localtime
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
% Add UChicago definition, 2015
\\definecolor{ucMaroon}{RGB}{128,0,0}
\\definecolor{ucDarkGray}{RGB}{118,118,118}
\\definecolor{ucLightGray}{RGB}{214,214,206}

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

    def __institute_hack(self, item, institute):
        if institute == 'uchicago':
            item = re.sub(r'(.*?)title(.*?)}{fg=(.*?),', r'\1title\2}{fg=white,', item)
            item = re.sub(r'(.*?)title(.*?)}{fg=white, bg=(.*?)}', r'\1title\2}{fg=white, bg=ucMaroon}', item)
            # \\setbeamercolor{titlelike}{fg=riceblue, bg=white}
# \\setbeamercolor{frametitle}{fg=riceblue, bg=white}
# \\setbeamercolor{frametitle right}{fg=riceblue, bg=white}
            return item.replace('riceblue', 'ucMaroon').replace('ricegray', 'ucDarkGray')
        else:
            return item

    def put(self, institute = 'rice'):
        with codecs.open(os.path.join(self.outdir, 'beamercolorthemericeowl.sty'), 'w', encoding='UTF-8') as f:
            f.write(self.__institute_hack(self.beamercolorthemericeowl, institute))
        with codecs.open(os.path.join(self.outdir, 'beamerouterthemeinfolines.sty'), 'w', encoding='UTF-8') as f:
            f.write(self.beamerouterthemeinfolines)
        with codecs.open(os.path.join(self.outdir, 'beamerthemeBoadilla.sty'), 'w', encoding='UTF-8') as f:
            f.write(self.beamerthemeBoadilla)
        with codecs.open(os.path.join(self.outdir, 'beamerouterthemerice.sty'), 'w', encoding='UTF-8') as f:
            f.write(self.beamerouterthemerice)
        with codecs.open(os.path.join(self.outdir, 'beamerouterthemerice2.sty'), 'w', encoding='UTF-8') as f:
            f.write(self.beamerouterthemerice2)
        with codecs.open(os.path.join(self.outdir, 'beamerthemeRice.sty'), 'w', encoding='UTF-8') as f:
            f.write(self.__institute_hack(self.beamerthemeRice, institute))
        return

BM_MODE = {'presentation':'\\documentclass[ignorenonframetext,mathserif,12pt,dvipsnames]{beamer}\n\\mode<presentation>\n\\setbeamertemplate{blocks}[rounded][shadow=true]\n',
        'notes':'\\documentclass[letterpaper,10pt,dvipsnames]{extarticle}\n\\usepackage[noamsthm]{beamerarticle}\n\\mode<article>\n',
        'handout':'\\documentclass[ignorenonframetext,mathserif,handout,12pt,dvipsnames]{beamer}\n\\mode<handout>\n\\setbeamertemplate{blocks}[rounded][shadow=true]\n'
        }
BM_THEME = {'heavy': '\\usetheme[numbers]{Rice}\n\\usecolortheme{riceowl}\n',
        'compact': '\\usetheme{Boadilla}\n\\usecolortheme{riceowl}\n\\useinnertheme{rectangles}\n\\useoutertheme{infolines}\n',
        'plain': '\\usetheme{Boadilla}\n\\usecolortheme{dove}\n\\useinnertheme{rectangles}\n\\useoutertheme{infolines}\n'
        }
BM_CONFIG = '''
%%%%%%%%%%%%%%%%%%
%%%% Packages
%%%%%%%%%%%%%%%%%%
\\usepackage{amsmath}
\\usepackage{amssymb}
\\usepackage{mathtools}
\\usepackage{url}
%% \\usepackage{mathpazo}
%% \\usepackage{mathptmx}
\\usepackage{latexsym}
\\usepackage{fixltx2e}
\\usepackage{fancyvrb}
\\usepackage{graphicx}
\\usepackage{color}
\\usepackage{beamerthemesplit}
\\usepackage{pgf,pgfarrows,pgfnodes,pgfautomata,pgfheaps,pgfshade}
\\usepackage{marvosym}
\\usepackage[warn]{textcomp}
\\usepackage{bm}
\DeclareMathAlphabet{\mathbbm}{U}{bbm}{m}{n}
\\usepackage{upgreek}
\\urlstyle{tt}
\\usepackage{lastpage}
\\usepackage{ulem}
\\usepackage{pdfpages}
\\usepackage{pgfpages}
\\usepackage{longtable}
\\usepackage{seqsplit}
\\usepackage{array}
\\usepackage{subfigure}
\\usepackage{multicol}
\\usepackage{multirow}
\\usepackage[multidot]{grffile}
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
%\\newcolumntype{x}[1]{>{\\centering\\arraybackslash\\hspace{0pt}}p{#1}}
\\newcolumntype{x}[1]{>{\\centering\\let\\newline\\\\\\arraybackslash\\hspace{0pt}}m{#1}}


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
	pdfauthor={labnotes},
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

%%\\setbeamercovered{transparent}
\\setbeamercovered{invisible}
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
  \\usepackage[maxfloats=52]{morefloats}
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

BM_TITLE = '''
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
BM_THANK = '''
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
\\usepackage{mathtools}
\\usepackage{booktabs}
\\usepackage{amssymb}
\\usepackage{amsthm}
\\usepackage{mathabx}
\\usepackage{enumitem}
\\usepackage[warn]{textcomp}
\\newcommand\hmmax{0} % default 3
\\usepackage{bm}
\\usepackage{fixltx2e}
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
\\usepackage[explicit]{titlesec}
\\usepackage{sectsty}
\\usepackage{longtable}
\\usepackage{seqsplit}
\\usepackage{array}
\\usepackage{subfigure}
\\usepackage[multidot]{grffile}
\\usepackage{float}
\\usepackage{varwidth}
\\usepackage{tikz}
\\usepackage[tikz]{bclogo}
'''

DOC_CONFIG = '''
\\DeclareMathOperator*{\\dif}{\\mathrm{d}}
\\DeclareMathOperator*{\\diff}{\\,\\dif}
\\DeclareMathOperator*{\\e}{\\mathrm{e}}
\\DeclareMathOperator*{\\E}{\\mathbb{E}}
\\DeclareMathOperator*{\\V}{\\mathbb{V}}
\\DeclareMathOperator*{\\defeq}{\\xlongequal{\\text{def}}}
\\newcolumntype{x}[1]{>{\\centering\\let\\newline\\\\\\arraybackslash\\hspace{0pt}}m{#1}}
\\newcommand*{\\set}[1]{\\left\\{ #1 \\right\\}}
\\newcommand*{\\Set}[2]{\\left\\{ \\, #1 \\colon #2 \\, \\right\\}}
\\newcommand*{\\abs}[1]{\\left\\lvert #1 \\right\\rvert}
\\newcommand*{\\p}[1]{\\Pr{\\left\\{ #1\\right\\}}}

\\newcommand{\\ie}{\\textit{i.e.}}

%% Colored Blocks
\\newcommand{\\CBc}[2]{\\tikz \\node[circle,scale=0.5,color=white,fill=#1]{\\textbf{#2}};}
\\newcommand{\\CBr}[2]{\\tikz \\node[rectangle,scale=0.9,color=white,fill=#1]{\\textbf{#2}};}

\\newcommand\\independent{\\protect\\mathpalette{\\protect\\independenT}{\\perp}}
\\def\\independenT#1#2{\\mathrel{\\rlap{$#1#2$}\\mkern2mu{#1#2}}}

\\newcommand*\\circled[1]{\\kern-2.5em
  \\put(0,4){\\color{black}\\circle*{18}}\\put(0,4){\\circle{16}}
  \\put(-3,0){\\color{white}\\\\bfseries\\large#1}}
\\linespread{1.2}
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
\\definecolor{rblue}{RGB}{16,183,179}
\\definecolor{rred}{RGB}{255,87,87}
\\definecolor{rgray}{RGB}{94,96,98}
\\definecolor{dblue}{rgb}{0,0.2,0.6}
\\newcommand*\\chapterlabel{}
\\titleformat{\\chapter}
  {\\gdef\\chapterlabel{}
   \\normalfont\\sffamily\\Huge\\bfseries\\scshape}
  {\\gdef\\chapterlabel{\\thechapter\\ }}{0pt}
  {\\begin{tikzpicture}[remember picture,overlay]
    \\node[yshift=-3cm] at (current page.north west)
      {\\begin{tikzpicture}[remember picture, overlay]
        \\draw[fill=rgray] (0,0) rectangle
          (\\paperwidth,3cm);
        \\node[anchor=east,xshift=.9\\paperwidth,rectangle,
              rounded corners=20pt,inner sep=11pt,
              fill=rblue]
              {\\color{white}\\chapterlabel#1};
       \\end{tikzpicture}
      };
   \\end{tikzpicture}
  }
\\sectionfont{\\color{rgray}\\normalfont\\huge\\bfseries}
\\subsubsectionfont{\\color{dblue}\\normalfont\\bfseries}
\\setcounter{secnumdepth}{3}
\\setcounter{tocdepth}{3}
\\setlength{\\LTpre}{0pt}
\\setlength{\\LTpost}{0pt}
\\setlist[itemize]{noitemsep, topsep=0pt}
\\usepackage[bookmarksnumbered=true,pdfstartview=FitH]{hyperref}
\\hypersetup{colorlinks, breaklinks, urlcolor=dblue, linkcolor=dblue, citecolor=MidnightBlue}
'''
######################################################

HTML_STYLE = r'''
@font-face {
  font-family: 'PT Sans';
  font-style: normal;
  font-weight: 400;
  src: local('PT Sans'), local('PTSans-Regular'), url(http://themes.googleusercontent.com/static/fonts/ptsans/v4/LKf8nhXsWg5ybwEGXk8UBQ.woff) format('woff');
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
	font-size: 11pt;
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
	font-size: 11pt;
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

em
{
	font-family: Georgia, Helvetica, Arial, sans-serif;
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

HTML_STYLE_LIGHT = r'''
@font-face {
  font-family: 'PT Sans';
  font-style: normal;
  font-weight: 400;
  src: local('PT Sans'), local('PTSans-Regular'), url(http://themes.googleusercontent.com/static/fonts/ptsans/v4/LKf8nhXsWg5ybwEGXk8UBQ.woff) format('woff');
}
body
{
	margin:40px 0;
	padding:0;
	font-family: 'PT Sans', 'Lucida Grande', 'Lucida Sans', 'Lucida Sans Unicode', Tahoma, sans-serif;
	font-size: 11pt;
	text-align:justify;
	line-height: 150%;
	color: #333;
}

em
{
    font-style: italic;
	font-family: Georgia, Helvetica, Arial, sans-serif;
	font-size: 11pt;
}

ol {list-style-type: circle;}

.minorhead
{
	color: #666;
	font-family: monospace;
	line-height: 30px;
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

#wrapper {
	text-align: left;
    width:95%;
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

HTML_SYN = r'''
<link rel="stylesheet" href="//cdnjs.cloudflare.com/ajax/libs/highlight.js/8.8.0/styles/solarized_light.min.css">
<script src="//cdnjs.cloudflare.com/ajax/libs/highlight.js/8.8.0/highlight.min.js"></script>
<script>hljs.initHighlightingOnLoad();</script>
<script type="text/javascript" src="http://cdn.mathjax.org/mathjax/latest/MathJax.js?config=TeX-AMS-MML_HTMLorMML"></script>
'''

HTML_INDEX = {
'head':r'''
<!DOCTYPE html>
<html lang="en">
<head>
	<meta charset="utf-8">
	<title>DOCTITLE_PH</title>
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
	<h1>DOCTITLE_PH</h1>
	<ul id="toc">
''',
'tail':'</ul><h4>Last updated: %s</h4></div></body></html>' % strftime("%a %d %b %Y %H:%M:%S", localtime())
        }

class BlogCSS:
        def __init__(self, url, title, media_path, logo = 'logo.png', background = 'bg.jpg'):
            self.title = title
            self.logo = os.path.join(media_path, logo)
            self.bg = os.path.join(media_path, background)
            self.url = url

        def GetMeta(self, title):
            return '''
<!DOCTYPE HTML PUBLIC "-//W3C//DTD HTML 4.01 Transitional//EN">
<html>
<head>
  <meta http-equiv="content-type"
 content="text/html; charset=ISO-8859-1">
  <title>{0}</title>
<style>
{6}
</style>
{5}
</head>
<body vlink="#000000" alink="#000000" background="{4}"
 bgcolor="#fefefe" link="#000000" text="#000000">
<center>
<br>
<br>
<br>
<table width="85%" border="0" cellpadding="0" cellspacing="0">
  <tbody>
    <tr>
      <td colspan="3">
      <table width="95%" cellpadding="0" cellspacing="0">
        <tbody>
          <tr>
            <td width="55%" align="center" valign="bottom">
            <table width="80%" cellpadding="0">
              <tbody>
                <tr>
                  <td bgcolor="#000000">
                  <table width="100%" cellpadding="6">
                    <tbody>
                      <tr>
                        <td bgcolor="#fefefe"><!--Document Title-->
                        <center><b>{1}</b><br></center>
                        </td>
                      </tr>
                    </tbody>
                  </table>
                  </td>
                </tr>
              </tbody>
            </table>
            </td>
            <td align="right" valign="bottom">
            <table cellpadding="0">
              <tbody>
                <tr>
                  <td bgcolor="#000000">
                  <table cellpadding="0">
                    <tbody>
                      <tr>
                        <td bgcolor="#ffffff"><a href="{2}"><img style="border: 0px solid ; " alt="Site Logo" src="{3}"></a></td>
                      </tr>
                    </tbody>
                  </table>
                  </td>
                </tr>
              </tbody>
            </table>
            </td>
          </tr>
          <tr>
            <td colspan="2"><br>
            </td>
          </tr>
        </tbody>
      </table>
      </td>
    </tr>
            '''.format(title, self.title, self.url,
                       self.logo, self.bg, HTML_SYN, HTML_STYLE_LIGHT)

        def GetLeftColumn(self, title, links):
            contents = '\n'.join(['<p><center><font size="-1"><b><a href="{0}">{1}</a></b></font></center></p>'.format(x[0], x[1]) for x in links])
            return '''
    <tr valign="top">
      <td width="10%">
      <table width="100%" cellpadding="0">
        <tbody>
          <tr>
            <td bgcolor="#000000">
            <table width="100%" cellpadding="14">
              <tbody>
                <tr>
                  <td bgcolor="#fefefe">
                  <center><font size="-1"><b>{0}</b></font></center>
                  </td>
                </tr>
              </tbody>
            </table>
            </td>
          </tr>
        </tbody>
      </table>
      <table width="100%" cellpadding="0">
        <tbody>
          <tr>
            <td bgcolor="#000000">
            <table width="100%" cellpadding="14">
              <tbody>
                <tr>
                  <td bgcolor="#fefefe">
                {1}
                  </td>
                </tr>
              </tbody>
            </table>
            </td>
          </tr>
        </tbody>
      </table>
      <p> </p>
      </td>
      <td> &nbsp; </td>
            '''.format(title, contents)


        def GetRightColumn(self, contents):
                '''input format [(summary, date, text)], properly ordered'''
                start = '<td><!--Document Contents-->\n'
                end = '''
    </td>
    </tr>
    <tr valign="top">
      <td colspan="3" align="right">
      <table width="" cellpadding="0">
        <tbody>
          <tr>
            <td bgcolor="#000000">
            <table width="100%" cellpadding="4">
              <tbody>
                <tr>
                  <td bgcolor="#fefefe"><font size="-2">Page design is adapted from Slackware&reg; homepage, 2010</font> </td>
                </tr>
              </tbody>
            </table>
            </td>
          </tr>
        </tbody>
      </table>
      </td>
    </tr>
  </tbody>
</table>
</center>
</body>
                '''
                text = ''
                for item in contents:
                        text += '''
        <center><!--entry start-->
      <table width="100%" border="0" cellpadding="0" cellspacing="0">
        <tbody>
          <tr>
            <td colspan="2">
            <table width="100%" cellpadding="0">
              <tbody>
                <tr>
                  <td bgcolor="#000000">
                  <table width="100%" cellpadding="4">
                    <tbody>
                      <tr>
                        <td bgcolor="#fefefe"> &nbsp; <b> {0} <b> </b></b></td>
                      </tr>
                    </tbody>
                  </table>
                  </td>
                </tr>
              </tbody>
            </table>
            </td>
          </tr>
          <tr>
            <td valign="top">
            <table width="100%" cellpadding="0">
              <tbody>
                <tr>
                  <td bgcolor="#000000">
                  <table width="100%" cellpadding="14">
                    <tbody>
                      <tr>
                        <td bgcolor="#fefefe">
                        {2}
                        </td>
                      </tr>
                    </tbody>
                  </table>
                  </td>
                </tr>
              </tbody>
            </table>
            </td>
            <td width="20%" valign="top">
            <table width="100%" cellpadding="0">
              <tbody>
                <tr>
                  <td bgcolor="#000000">
                  <table width="100%" cellpadding="4">
                    <tbody>
                      <tr>
                        <td bgcolor="#fefefe">
                        <center><font size="-1"><b>{1}</b></font></center>
                        </td>
                      </tr>
                    </tbody>
                  </table>
                  </td>
                </tr>
              </tbody>
            </table>
            </td>
          </tr>
          <tr>
            <td colspan="2"><br>
            </td>
          </tr>
        </tbody>
      </table>
      </center><!--entry end-->
                        '''.format(item[0], item[1], item[2])
                return start + text + end

class minted:
    def __init__(self, outdir):
        self.outdir = outdir
        self.sty = r'''%%
%% This is file `minted.sty',
%% generated with the docstrip utility.
%%
%% The original source files were:
%%
%% minted.dtx  (with options: `package')
%% Copyright 2013--2017 Geoffrey M. Poore
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
%% The Current Maintainer of this work is Geoffrey Poore.
%% 
%% This work consists of the files minted.dtx and minted.ins
%% and the derived file minted.sty.
\NeedsTeXFormat{LaTeX2e}
\ProvidesPackage{minted}
    [2017/09/03 v2.5.1dev Yet another Pygments shim for LaTeX]
\RequirePackage{keyval}
\RequirePackage{kvoptions}
\RequirePackage{fvextra}
\RequirePackage{ifthen}
\RequirePackage{calc}
\IfFileExists{shellesc.sty}
 {\RequirePackage{shellesc}
  \@ifpackagelater{shellesc}{2016/04/29}
   {}
   {\protected\def\ShellEscape{\immediate\write18 }}}
 {\protected\def\ShellEscape{\immediate\write18 }}
\RequirePackage{ifplatform}
\RequirePackage{pdftexcmds}
\RequirePackage{etoolbox}
\RequirePackage{xstring}
\RequirePackage{lineno}
\RequirePackage{framed}
\AtEndPreamble{%
  \@ifpackageloaded{color}{}{%
    \@ifpackageloaded{xcolor}{}{\RequirePackage{xcolor}}}%
}
\DeclareVoidOption{chapter}{\def\minted@float@within{chapter}}
\DeclareVoidOption{section}{\def\minted@float@within{section}}
\DeclareBoolOption{newfloat}
\DeclareBoolOption[true]{cache}
\StrSubstitute{\jobname}{ }{_}[\minted@jobname]
\StrSubstitute{\minted@jobname}{*}{_}[\minted@jobname]
\StrSubstitute{\minted@jobname}{"}{}[\minted@jobname]
\StrSubstitute{\minted@jobname}{'}{_}[\minted@jobname]
\newcommand{\minted@cachedir}{\detokenize{_}minted-\minted@jobname}
\let\minted@cachedir@windows\minted@cachedir
\define@key{minted}{cachedir}{%
  \@namedef{minted@cachedir}{#1}%
  \StrSubstitute{\minted@cachedir}{/}{\@backslashchar}[\minted@cachedir@windows]}
\DeclareBoolOption{finalizecache}
\DeclareBoolOption{frozencache}
\let\minted@outputdir\@empty
\let\minted@outputdir@windows\@empty
\define@key{minted}{outputdir}{%
  \@namedef{minted@outputdir}{#1/}%
  \StrSubstitute{\minted@outputdir}{/}%
    {\@backslashchar}[\minted@outputdir@windows]}
\DeclareBoolOption{kpsewhich}
\DeclareBoolOption{langlinenos}
\DeclareBoolOption{draft}
\DeclareComplementaryOption{final}{draft}
\ProcessKeyvalOptions*
\ifthenelse{\boolean{minted@newfloat}}{\RequirePackage{newfloat}}{\RequirePackage{float}}
\ifcsname tikzifexternalizing\endcsname
  \tikzifexternalizing{\minted@drafttrue\minted@cachefalse}{}
\else
  \ifcsname tikzexternalrealjob\endcsname
    \minted@drafttrue
    \minted@cachefalse
  \else
  \fi
\fi
\ifthenelse{\boolean{minted@finalizecache}}%
 {\ifthenelse{\boolean{minted@frozencache}}%
   {\PackageError{minted}%
     {Options "finalizecache" and "frozencache" are not compatible}%
     {Options "finalizecache" and "frozencache" are not compatible}}%
   {}}%
 {}
\ifthenelse{\boolean{minted@cache}}%
 {\ifthenelse{\boolean{minted@frozencache}}%
   {}%
   {\AtEndOfPackage{\ProvideDirectory{\minted@outputdir\minted@cachedir}}}}%
 {}
\newcommand{\minted@input}[1]{%
  \IfFileExists{#1}%
   {\input{#1}}%
   {\PackageError{minted}{Missing Pygments output; \string\inputminted\space
     was^^Jprobably given a file that does not exist--otherwise, you may need
     ^^Jthe outputdir package option, or may be using an incompatible build
     tool,^^Jor may be using frozencache with a missing file}%
    {This could be caused by using -output-directory or -aux-directory
     ^^Jwithout setting minted's outputdir, or by using a build tool that
     ^^Jchanges paths in ways minted cannot detect,
     ^^Jor using frozencache with a missing file.}}%
}
\newcommand{\minted@infile}{\minted@jobname.out.pyg}
\newcommand{\minted@cachelist}{}
\newcommand{\minted@addcachefile}[1]{%
  \expandafter\long\expandafter\gdef\expandafter\minted@cachelist\expandafter{%
    \minted@cachelist,^^J%
    \space\space#1}%
  \expandafter\gdef\csname minted@cached@#1\endcsname{}%
}
\newcommand{\minted@savecachelist}{%
  \ifdefempty{\minted@cachelist}{}{%
    \immediate\write\@mainaux{%
      \string\gdef\string\minted@oldcachelist\string{%
        \minted@cachelist\string}}%
  }%
}
\newcommand{\minted@cleancache}{%
  \ifcsname minted@oldcachelist\endcsname
    \def\do##1{%
      \ifthenelse{\equal{##1}{}}{}{%
        \ifcsname minted@cached@##1\endcsname\else
          \DeleteFile[\minted@outputdir\minted@cachedir]{##1}%
        \fi
      }%
    }%
    \expandafter\docsvlist\expandafter{\minted@oldcachelist}%
  \else
  \fi
}
\ifthenelse{\boolean{minted@draft}}%
 {\AtEndDocument{%
    \ifcsname minted@oldcachelist\endcsname
      \StrSubstitute{\minted@oldcachelist}{,}{,^^J }[\minted@cachelist]
      \minted@savecachelist
    \fi}}%
 {\ifthenelse{\boolean{minted@frozencache}}%
   {\AtEndDocument{%
      \ifcsname minted@oldcachelist\endcsname
        \StrSubstitute{\minted@oldcachelist}{,}{,^^J }[\minted@cachelist]
        \minted@savecachelist
      \fi}}%
   {\AtEndDocument{%
    \minted@savecachelist
    \minted@cleancache}}}%
\ifwindows
  \providecommand{\DeleteFile}[2][]{%
    \ifthenelse{\equal{#1}{}}%
      {\IfFileExists{#2}{\ShellEscape{del #2}}{}}%
      {\IfFileExists{#1/#2}{%
        \StrSubstitute{#1}{/}{\@backslashchar}[\minted@windir]
        \ShellEscape{del \minted@windir\@backslashchar #2}}{}}}
\else
  \providecommand{\DeleteFile}[2][]{%
    \ifthenelse{\equal{#1}{}}%
      {\IfFileExists{#2}{\ShellEscape{rm #2}}{}}%
      {\IfFileExists{#1/#2}{\ShellEscape{rm #1/#2}}{}}}
\fi
\ifwindows
  \newcommand{\ProvideDirectory}[1]{%
    \StrSubstitute{#1}{/}{\@backslashchar}[\minted@windir]
    \ShellEscape{if not exist \minted@windir\space mkdir \minted@windir}}
\else
  \newcommand{\ProvideDirectory}[1]{%
    \ShellEscape{mkdir -p #1}}
\fi
\newboolean{AppExists}
\newread\minted@appexistsfile
\newcommand{\TestAppExists}[1]{
  \ifwindows
    \DeleteFile{\minted@jobname.aex}
    \ShellEscape{for \string^\@percentchar i in (#1.exe #1.bat #1.cmd)
      do set > \minted@jobname.aex <nul: /p
      x=\string^\@percentchar \string~$PATH:i>> \minted@jobname.aex}
    %$ <- balance syntax highlighting
    \immediate\openin\minted@appexistsfile\minted@jobname.aex
    \expandafter\def\expandafter\@tmp@cr\expandafter{\the\endlinechar}
    \endlinechar=-1\relax
    \readline\minted@appexistsfile to \minted@apppathifexists
    \endlinechar=\@tmp@cr
    \ifthenelse{\equal{\minted@apppathifexists}{}}
     {\AppExistsfalse}
     {\AppExiststrue}
    \immediate\closein\minted@appexistsfile
    \DeleteFile{\minted@jobname.aex}
  \else
    \ShellEscape{which #1 && touch \minted@jobname.aex}
    \IfFileExists{\minted@jobname.aex}
      {\AppExiststrue
        \DeleteFile{\minted@jobname.aex}}
      {\AppExistsfalse}
  \fi
}
\newcommand{\minted@optlistcl@g}{}
\newcommand{\minted@optlistcl@g@i}{}
\let\minted@lang\@empty
\newcommand{\minted@optlistcl@lang}{}
\newcommand{\minted@optlistcl@lang@i}{}
\newcommand{\minted@optlistcl@cmd}{}
\newcommand{\minted@optlistfv@g}{}
\newcommand{\minted@optlistfv@g@i}{}
\newcommand{\minted@optlistfv@lang}{}
\newcommand{\minted@optlistfv@lang@i}{}
\newcommand{\minted@optlistfv@cmd}{}
\newcommand{\minted@configlang}[1]{%
  \def\minted@lang{#1}%
  \ifcsname minted@optlistcl@lang\minted@lang\endcsname\else
    \expandafter\gdef\csname minted@optlistcl@lang\minted@lang\endcsname{}%
  \fi
  \ifcsname minted@optlistcl@lang\minted@lang @i\endcsname\else
    \expandafter\gdef\csname minted@optlistcl@lang\minted@lang @i\endcsname{}%
  \fi
  \ifcsname minted@optlistfv@lang\minted@lang\endcsname\else
    \expandafter\gdef\csname minted@optlistfv@lang\minted@lang\endcsname{}%
  \fi
  \ifcsname minted@optlistfv@lang\minted@lang @i\endcsname\else
    \expandafter\gdef\csname minted@optlistfv@lang\minted@lang @i\endcsname{}%
  \fi
}
\newcommand{\minted@addto@optlistcl}[2]{%
  \expandafter\def\expandafter#1\expandafter{#1%
    \detokenize{#2}\space}}
\newcommand{\minted@addto@optlistcl@lang}[2]{%
  \expandafter\let\expandafter\minted@tmp\csname #1\endcsname
  \expandafter\def\expandafter\minted@tmp\expandafter{\minted@tmp%
    \detokenize{#2}\space}%
  \expandafter\let\csname #1\endcsname\minted@tmp}
\newcommand{\minted@def@optcl}[4][]{%
  \ifthenelse{\equal{#1}{}}%
    {\define@key{minted@opt@g}{#2}{%
        \minted@addto@optlistcl{\minted@optlistcl@g}{#3=#4}%
        \@namedef{minted@opt@g:#2}{#4}}%
      \define@key{minted@opt@g@i}{#2}{%
        \minted@addto@optlistcl{\minted@optlistcl@g@i}{#3=#4}%
        \@namedef{minted@opt@g@i:#2}{#4}}%
      \define@key{minted@opt@lang}{#2}{%
        \minted@addto@optlistcl@lang{minted@optlistcl@lang\minted@lang}{#3=#4}%
        \@namedef{minted@opt@lang\minted@lang:#2}{#4}}%
      \define@key{minted@opt@lang@i}{#2}{%
        \minted@addto@optlistcl@lang{%
          minted@optlistcl@lang\minted@lang @i}{#3=#4}%
        \@namedef{minted@opt@lang\minted@lang @i:#2}{#4}}%
      \define@key{minted@opt@cmd}{#2}{%
        \minted@addto@optlistcl{\minted@optlistcl@cmd}{#3=#4}%
        \@namedef{minted@opt@cmd:#2}{#4}}}%
    {\define@key{minted@opt@g}{#2}[#1]{%
        \minted@addto@optlistcl{\minted@optlistcl@g}{#3=#4}%
        \@namedef{minted@opt@g:#2}{#4}}%
      \define@key{minted@opt@g@i}{#2}[#1]{%
        \minted@addto@optlistcl{\minted@optlistcl@g@i}{#3=#4}%
        \@namedef{minted@opt@g@i:#2}{#4}}%
      \define@key{minted@opt@lang}{#2}[#1]{%
        \minted@addto@optlistcl@lang{minted@optlistcl@lang\minted@lang}{#3=#4}%
        \@namedef{minted@opt@lang\minted@lang:#2}{#4}}%
      \define@key{minted@opt@lang@i}{#2}[#1]{%
        \minted@addto@optlistcl@lang{%
          minted@optlistcl@lang\minted@lang @i}{#3=#4}%
        \@namedef{minted@opt@lang\minted@lang @i:#2}{#4}}%
      \define@key{minted@opt@cmd}{#2}[#1]{%
        \minted@addto@optlistcl{\minted@optlistcl@cmd}{#3=#4}%
        \@namedef{minted@opt@cmd:#2}{#4}}}%
}
\edef\minted@hashchar{\string#}
\edef\minted@dollarchar{\string$}
\edef\minted@ampchar{\string&}
\edef\minted@underscorechar{\string_}
\edef\minted@tildechar{\string~}
\edef\minted@leftsquarebracket{\string[}
\edef\minted@rightsquarebracket{\string]}
\newcommand{\minted@escchars}{%
  \let\#\minted@hashchar
  \let\%\@percentchar
  \let\{\@charlb
  \let\}\@charrb
  \let\$\minted@dollarchar
  \let\&\minted@ampchar
  \let\_\minted@underscorechar
  \let\\\@backslashchar
  \let~\minted@tildechar
  \let\~\minted@tildechar
  \let\[\minted@leftsquarebracket
  \let\]\minted@rightsquarebracket
} %$ <- highlighting
\newcommand{\minted@addto@optlistcl@e}[2]{%
  \begingroup
  \minted@escchars
  \xdef\minted@xtmp{#2}%
  \endgroup
  \expandafter\minted@addto@optlistcl@e@i\expandafter{\minted@xtmp}{#1}}
\def\minted@addto@optlistcl@e@i#1#2{%
  \expandafter\def\expandafter#2\expandafter{#2#1\space}}
\newcommand{\minted@addto@optlistcl@lang@e}[2]{%
  \begingroup
  \minted@escchars
  \xdef\minted@xtmp{#2}%
  \endgroup
  \expandafter\minted@addto@optlistcl@lang@e@i\expandafter{\minted@xtmp}{#1}}
\def\minted@addto@optlistcl@lang@e@i#1#2{%
  \expandafter\let\expandafter\minted@tmp\csname #2\endcsname
  \expandafter\def\expandafter\minted@tmp\expandafter{\minted@tmp#1\space}%
  \expandafter\let\csname #2\endcsname\minted@tmp}
\newcommand{\minted@def@optcl@e}[4][]{%
  \ifthenelse{\equal{#1}{}}%
    {\define@key{minted@opt@g}{#2}{%
        \minted@addto@optlistcl@e{\minted@optlistcl@g}{#3=#4}%
        \@namedef{minted@opt@g:#2}{#4}}%
      \define@key{minted@opt@g@i}{#2}{%
        \minted@addto@optlistcl@e{\minted@optlistcl@g@i}{#3=#4}%
        \@namedef{minted@opt@g@i:#2}{#4}}%
      \define@key{minted@opt@lang}{#2}{%
        \minted@addto@optlistcl@lang@e{minted@optlistcl@lang\minted@lang}{#3=#4}%
        \@namedef{minted@opt@lang\minted@lang:#2}{#4}}%
      \define@key{minted@opt@lang@i}{#2}{%
        \minted@addto@optlistcl@lang@e{%
          minted@optlistcl@lang\minted@lang @i}{#3=#4}%
        \@namedef{minted@opt@lang\minted@lang @i:#2}{#4}}%
      \define@key{minted@opt@cmd}{#2}{%
        \minted@addto@optlistcl@e{\minted@optlistcl@cmd}{#3=#4}%
        \@namedef{minted@opt@cmd:#2}{#4}}}%
    {\define@key{minted@opt@g}{#2}[#1]{%
        \minted@addto@optlistcl@e{\minted@optlistcl@g}{#3=#4}%
        \@namedef{minted@opt@g:#2}{#4}}%
      \define@key{minted@opt@g@i}{#2}[#1]{%
        \minted@addto@optlistcl@e{\minted@optlistcl@g@i}{#3=#4}%
        \@namedef{minted@opt@g@i:#2}{#4}}%
      \define@key{minted@opt@lang}{#2}[#1]{%
        \minted@addto@optlistcl@lang@e{minted@optlistcl@lang\minted@lang}{#3=#4}%
        \@namedef{minted@opt@lang\minted@lang:#2}{#4}}%
      \define@key{minted@opt@lang@i}{#2}[#1]{%
        \minted@addto@optlistcl@lang@e{%
          minted@optlistcl@lang\minted@lang @i}{#3=#4}%
        \@namedef{minted@opt@lang\minted@lang @i:#2}{#4}}%
      \define@key{minted@opt@cmd}{#2}[#1]{%
        \minted@addto@optlistcl@e{\minted@optlistcl@cmd}{#3=#4}%
        \@namedef{minted@opt@cmd:#2}{#4}}}%
}
\newcommand{\minted@def@optcl@switch}[2]{%
  \define@booleankey{minted@opt@g}{#1}%
    {\minted@addto@optlistcl{\minted@optlistcl@g}{#2=True}%
      \@namedef{minted@opt@g:#1}{true}}
    {\minted@addto@optlistcl{\minted@optlistcl@g}{#2=False}%
      \@namedef{minted@opt@g:#1}{false}}
  \define@booleankey{minted@opt@g@i}{#1}%
    {\minted@addto@optlistcl{\minted@optlistcl@g@i}{#2=True}%
      \@namedef{minted@opt@g@i:#1}{true}}
    {\minted@addto@optlistcl{\minted@optlistcl@g@i}{#2=False}%
      \@namedef{minted@opt@g@i:#1}{false}}
  \define@booleankey{minted@opt@lang}{#1}%
    {\minted@addto@optlistcl@lang{minted@optlistcl@lang\minted@lang}{#2=True}%
      \@namedef{minted@opt@lang\minted@lang:#1}{true}}
    {\minted@addto@optlistcl@lang{minted@optlistcl@lang\minted@lang}{#2=False}%
      \@namedef{minted@opt@lang\minted@lang:#1}{false}}
  \define@booleankey{minted@opt@lang@i}{#1}%
    {\minted@addto@optlistcl@lang{minted@optlistcl@lang\minted@lang @i}{#2=True}%
      \@namedef{minted@opt@lang\minted@lang @i:#1}{true}}
    {\minted@addto@optlistcl@lang{minted@optlistcl@lang\minted@lang @i}{#2=False}%
      \@namedef{minted@opt@lang\minted@lang @i:#1}{false}}
  \define@booleankey{minted@opt@cmd}{#1}%
      {\minted@addto@optlistcl{\minted@optlistcl@cmd}{#2=True}%
        \@namedef{minted@opt@cmd:#1}{true}}
      {\minted@addto@optlistcl{\minted@optlistcl@cmd}{#2=False}%
        \@namedef{minted@opt@cmd:#1}{false}}
}
\newcommand{\minted@def@optfv}[1]{%
  \define@key{minted@opt@g}{#1}{%
    \expandafter\def\expandafter\minted@optlistfv@g\expandafter{%
      \minted@optlistfv@g#1={##1},}%
    \@namedef{minted@opt@g:#1}{##1}}
  \define@key{minted@opt@g@i}{#1}{%
    \expandafter\def\expandafter\minted@optlistfv@g@i\expandafter{%
      \minted@optlistfv@g@i#1={##1},}%
    \@namedef{minted@opt@g@i:#1}{##1}}
  \define@key{minted@opt@lang}{#1}{%
    \expandafter\let\expandafter\minted@tmp%
      \csname minted@optlistfv@lang\minted@lang\endcsname
    \expandafter\def\expandafter\minted@tmp\expandafter{%
      \minted@tmp#1={##1},}%
    \expandafter\let\csname minted@optlistfv@lang\minted@lang\endcsname%
      \minted@tmp
    \@namedef{minted@opt@lang\minted@lang:#1}{##1}}
  \define@key{minted@opt@lang@i}{#1}{%
    \expandafter\let\expandafter\minted@tmp%
      \csname minted@optlistfv@lang\minted@lang @i\endcsname
    \expandafter\def\expandafter\minted@tmp\expandafter{%
      \minted@tmp#1={##1},}%
    \expandafter\let\csname minted@optlistfv@lang\minted@lang @i\endcsname%
      \minted@tmp
    \@namedef{minted@opt@lang\minted@lang @i:#1}{##1}}
  \define@key{minted@opt@cmd}{#1}{%
    \expandafter\def\expandafter\minted@optlistfv@cmd\expandafter{%
      \minted@optlistfv@cmd#1={##1},}%
    \@namedef{minted@opt@cmd:#1}{##1}}
}
\newcommand{\minted@def@optfv@switch}[1]{%
  \define@booleankey{minted@opt@g}{#1}%
    {\expandafter\def\expandafter\minted@optlistfv@g\expandafter{%
      \minted@optlistfv@g#1=true,}%
     \@namedef{minted@opt@g:#1}{true}}%
    {\expandafter\def\expandafter\minted@optlistfv@g\expandafter{%
      \minted@optlistfv@g#1=false,}%
     \@namedef{minted@opt@g:#1}{false}}%
  \define@booleankey{minted@opt@g@i}{#1}%
    {\expandafter\def\expandafter\minted@optlistfv@g@i\expandafter{%
      \minted@optlistfv@g@i#1=true,}%
     \@namedef{minted@opt@g@i:#1}{true}}%
    {\expandafter\def\expandafter\minted@optlistfv@g@i\expandafter{%
      \minted@optlistfv@g@i#1=false,}%
     \@namedef{minted@opt@g@i:#1}{false}}%
  \define@booleankey{minted@opt@lang}{#1}%
    {\expandafter\let\expandafter\minted@tmp%
        \csname minted@optlistfv@lang\minted@lang\endcsname
      \expandafter\def\expandafter\minted@tmp\expandafter{%
        \minted@tmp#1=true,}%
      \expandafter\let\csname minted@optlistfv@lang\minted@lang\endcsname%
        \minted@tmp
     \@namedef{minted@opt@lang\minted@lang:#1}{true}}%
    {\expandafter\let\expandafter\minted@tmp%
        \csname minted@optlistfv@lang\minted@lang\endcsname
      \expandafter\def\expandafter\minted@tmp\expandafter{%
        \minted@tmp#1=false,}%
      \expandafter\let\csname minted@optlistfv@lang\minted@lang\endcsname%
        \minted@tmp
     \@namedef{minted@opt@lang\minted@lang:#1}{false}}%
  \define@booleankey{minted@opt@lang@i}{#1}%
    {\expandafter\let\expandafter\minted@tmp%
        \csname minted@optlistfv@lang\minted@lang @i\endcsname
      \expandafter\def\expandafter\minted@tmp\expandafter{%
        \minted@tmp#1=true,}%
      \expandafter\let\csname minted@optlistfv@lang\minted@lang @i\endcsname%
        \minted@tmp
     \@namedef{minted@opt@lang\minted@lang @i:#1}{true}}%
    {\expandafter\let\expandafter\minted@tmp%
        \csname minted@optlistfv@lang\minted@lang @i\endcsname
      \expandafter\def\expandafter\minted@tmp\expandafter{%
        \minted@tmp#1=false,}%
      \expandafter\let\csname minted@optlistfv@lang\minted@lang @i\endcsname%
        \minted@tmp
     \@namedef{minted@opt@lang\minted@lang @i:#1}{false}}%
  \define@booleankey{minted@opt@cmd}{#1}%
    {\expandafter\def\expandafter\minted@optlistfv@cmd\expandafter{%
      \minted@optlistfv@cmd#1=true,}%
     \@namedef{minted@opt@cmd:#1}{true}}%
    {\expandafter\def\expandafter\minted@optlistfv@cmd\expandafter{%
      \minted@optlistfv@cmd#1=false,}%
     \@namedef{minted@opt@cmd:#1}{false}}%
}
\newboolean{minted@isinline}
\newcommand{\minted@fvset}{%
  \expandafter\fvset\expandafter{\minted@optlistfv@g}%
  \expandafter\let\expandafter\minted@tmp%
    \csname minted@optlistfv@lang\minted@lang\endcsname
  \expandafter\fvset\expandafter{\minted@tmp}%
  \ifthenelse{\boolean{minted@isinline}}%
   {\expandafter\fvset\expandafter{\minted@optlistfv@g@i}%
    \expandafter\let\expandafter\minted@tmp%
      \csname minted@optlistfv@lang\minted@lang @i\endcsname
    \expandafter\fvset\expandafter{\minted@tmp}}%
   {}%
  \expandafter\fvset\expandafter{\minted@optlistfv@cmd}%
}
\newcommand{\minted@def@opt}[2][]{%
  \define@key{minted@opt@g}{#2}{%
    \@namedef{minted@opt@g:#2}{##1}}
  \define@key{minted@opt@g@i}{#2}{%
    \@namedef{minted@opt@g@i:#2}{##1}}
  \define@key{minted@opt@lang}{#2}{%
    \@namedef{minted@opt@lang\minted@lang:#2}{##1}}
  \define@key{minted@opt@lang@i}{#2}{%
    \@namedef{minted@opt@lang\minted@lang @i:#2}{##1}}
  \define@key{minted@opt@cmd}{#2}{%
    \@namedef{minted@opt@cmd:#2}{##1}}
  \ifstrempty{#1}{}{\@namedef{minted@opt@g:#2}{#1}}%
}
\newcommand{\minted@checkstyle}[1]{%
  \ifcsname minted@styleloaded@\ifstrempty{#1}{default-pyg-prefix}{#1}\endcsname\else
    \ifstrempty{#1}{}{\ifcsname PYG\endcsname\else\minted@checkstyle{}\fi}%
    \expandafter\gdef%
      \csname minted@styleloaded@\ifstrempty{#1}{default-pyg-prefix}{#1}\endcsname{}%
    \ifthenelse{\boolean{minted@cache}}%
     {\IfFileExists
       {\minted@outputdir\minted@cachedir/\ifstrempty{#1}{default-pyg-prefix}{#1}.pygstyle}%
       {}%
       {%
        \ifthenelse{\boolean{minted@frozencache}}%
         {\PackageError{minted}%
           {Missing style definition for #1 with frozencache}%
           {Missing style definition for #1 with frozencache}}%
         {\ifwindows
            \ShellEscape{%
              \MintedPygmentize\space -S \ifstrempty{#1}{default}{#1} -f latex
              -P commandprefix=PYG#1
              > \minted@outputdir@windows\minted@cachedir@windows\@backslashchar%
                   \ifstrempty{#1}{default-pyg-prefix}{#1}.pygstyle}%
          \else
            \ShellEscape{%
              \MintedPygmentize\space -S \ifstrempty{#1}{default}{#1} -f latex
              -P commandprefix=PYG#1
              > \minted@outputdir\minted@cachedir/%
                   \ifstrempty{#1}{default-pyg-prefix}{#1}.pygstyle}%
          \fi}%
        }%
        \begingroup
        \let\def\gdef
        \catcode\string``=12
        \catcode`\_=11
        \catcode`\-=11
        \catcode`\%=14
        \endlinechar=-1\relax
        \minted@input{%
          \minted@outputdir\minted@cachedir/\ifstrempty{#1}{default-pyg-prefix}{#1}.pygstyle}%
        \endgroup
        \minted@addcachefile{\ifstrempty{#1}{default-pyg-prefix}{#1}.pygstyle}}%
     {%
        \ifwindows
          \ShellEscape{%
            \MintedPygmentize\space -S \ifstrempty{#1}{default}{#1} -f latex
            -P commandprefix=PYG#1 > \minted@outputdir@windows\minted@jobname.out.pyg}%
        \else
          \ShellEscape{%
            \MintedPygmentize\space -S \ifstrempty{#1}{default}{#1} -f latex
            -P commandprefix=PYG#1 > \minted@outputdir\minted@jobname.out.pyg}%
        \fi
        \begingroup
        \let\def\gdef
        \catcode\string``=12
        \catcode`\_=11
        \catcode`\-=11
        \catcode`\%=14
        \endlinechar=-1\relax
        \minted@input{\minted@outputdir\minted@jobname.out.pyg}%
        \endgroup}%
    \ifstrempty{#1}{\minted@patch@PYGZsq}{}%
  \fi
}
\ifthenelse{\boolean{minted@draft}}{\renewcommand{\minted@checkstyle}[1]{}}{}
\newcommand{\minted@patch@PYGZsq}{%
  \ifcsname PYGZsq\endcsname
    \expandafter\ifdefstring\expandafter{\csname PYGZsq\endcsname}{\char`\'}%
     {\minted@patch@PYGZsq@i}%
     {}%
  \fi
}
\begingroup
\catcode`\'=\active
\gdef\minted@patch@PYGZsq@i{\gdef\PYGZsq{'}}
\endgroup
\ifthenelse{\boolean{minted@draft}}{}{\AtBeginDocument{\minted@patch@PYGZsq}}
\newcommand{\minted@def@opt@switch}[2][false]{%
  \define@booleankey{minted@opt@g}{#2}%
    {\@namedef{minted@opt@g:#2}{true}}%
    {\@namedef{minted@opt@g:#2}{false}}
  \define@booleankey{minted@opt@g@i}{#2}%
    {\@namedef{minted@opt@g@i:#2}{true}}%
    {\@namedef{minted@opt@g@i:#2}{false}}
  \define@booleankey{minted@opt@lang}{#2}%
    {\@namedef{minted@opt@lang\minted@lang:#2}{true}}%
    {\@namedef{minted@opt@lang\minted@lang:#2}{false}}
  \define@booleankey{minted@opt@lang@i}{#2}%
    {\@namedef{minted@opt@lang\minted@lang @i:#2}{true}}%
    {\@namedef{minted@opt@lang\minted@lang @i:#2}{false}}
  \define@booleankey{minted@opt@cmd}{#2}%
    {\@namedef{minted@opt@cmd:#2}{true}}%
    {\@namedef{minted@opt@cmd:#2}{false}}%
  \@namedef{minted@opt@g:#2}{#1}%
}
\def\minted@get@opt#1#2{%
  \ifcsname minted@opt@cmd:#1\endcsname
    \csname minted@opt@cmd:#1\endcsname
  \else
    \ifminted@isinline
      \ifcsname minted@opt@lang\minted@lang @i:#1\endcsname
        \csname minted@opt@lang\minted@lang @i:#1\endcsname
      \else
        \ifcsname minted@opt@g@i:#1\endcsname
          \csname minted@opt@g@i:#1\endcsname
        \else
          \ifcsname minted@opt@lang\minted@lang:#1\endcsname
            \csname minted@opt@lang\minted@lang:#1\endcsname
          \else
            \ifcsname minted@opt@g:#1\endcsname
              \csname minted@opt@g:#1\endcsname
            \else
              #2%
            \fi
          \fi
        \fi
      \fi
    \else
      \ifcsname minted@opt@lang\minted@lang:#1\endcsname
        \csname minted@opt@lang\minted@lang:#1\endcsname
      \else
        \ifcsname minted@opt@g:#1\endcsname
          \csname minted@opt@g:#1\endcsname
        \else
          #2%
        \fi
      \fi
    \fi
  \fi
}%
\minted@def@optcl{encoding}{-P encoding}{#1}
\minted@def@optcl{outencoding}{-P outencoding}{#1}
\minted@def@optcl@e{escapeinside}{-P "escapeinside}{#1"}
\minted@def@optcl@switch{stripnl}{-P stripnl}
\minted@def@optcl@switch{stripall}{-P stripall}
\minted@def@optcl@switch{python3}{-P python3}
\minted@def@optcl@switch{funcnamehighlighting}{-P funcnamehighlighting}
\minted@def@optcl@switch{startinline}{-P startinline}
\ifthenelse{\boolean{minted@draft}}%
  {\minted@def@optfv{gobble}}%
  {\minted@def@optcl{gobble}{-F gobble:n}{#1}}
\minted@def@optcl{codetagify}{-F codetagify:codetags}{#1}
\minted@def@optcl{keywordcase}{-F keywordcase:case}{#1}
\minted@def@optcl@switch{texcl}{-P texcomments}
\minted@def@optcl@switch{texcomments}{-P texcomments}
\minted@def@optcl@switch{mathescape}{-P mathescape}
\minted@def@optfv@switch{linenos}
\minted@def@opt{style}
\minted@def@optfv{frame}
\minted@def@optfv{framesep}
\minted@def@optfv{framerule}
\minted@def@optfv{rulecolor}
\minted@def@optfv{numbersep}
\minted@def@optfv{numbers}
\minted@def@optfv{firstnumber}
\minted@def@optfv{stepnumber}
\minted@def@optfv{firstline}
\minted@def@optfv{lastline}
\minted@def@optfv{baselinestretch}
\minted@def@optfv{xleftmargin}
\minted@def@optfv{xrightmargin}
\minted@def@optfv{fillcolor}
\minted@def@optfv{tabsize}
\minted@def@optfv{fontfamily}
\minted@def@optfv{fontsize}
\minted@def@optfv{fontshape}
\minted@def@optfv{fontseries}
\minted@def@optfv{formatcom}
\minted@def@optfv{label}
\minted@def@optfv{labelposition}
\minted@def@optfv{highlightlines}
\minted@def@optfv{highlightcolor}
\minted@def@optfv{space}
\minted@def@optfv{spacecolor}
\minted@def@optfv{tab}
\minted@def@optfv{tabcolor}
\minted@def@optfv{highlightcolor}
\minted@def@optfv@switch{beameroverlays}
\minted@def@optfv@switch{curlyquotes}
\minted@def@optfv@switch{numberfirstline}
\minted@def@optfv@switch{numberblanklines}
\minted@def@optfv@switch{stepnumberfromfirst}
\minted@def@optfv@switch{stepnumberoffsetvalues}
\minted@def@optfv@switch{showspaces}
\minted@def@optfv@switch{resetmargins}
\minted@def@optfv@switch{samepage}
\minted@def@optfv@switch{showtabs}
\minted@def@optfv@switch{obeytabs}
\minted@def@optfv@switch{breaklines}
\minted@def@optfv@switch{breakbytoken}
\minted@def@optfv@switch{breakbytokenanywhere}
\minted@def@optfv{breakindent}
\minted@def@optfv{breakindentnchars}
\minted@def@optfv@switch{breakautoindent}
\minted@def@optfv{breaksymbol}
\minted@def@optfv{breaksymbolsep}
\minted@def@optfv{breaksymbolsepnchars}
\minted@def@optfv{breaksymbolindent}
\minted@def@optfv{breaksymbolindentnchars}
\minted@def@optfv{breaksymbolleft}
\minted@def@optfv{breaksymbolsepleft}
\minted@def@optfv{breaksymbolsepleftnchars}
\minted@def@optfv{breaksymbolindentleft}
\minted@def@optfv{breaksymbolindentleftnchars}
\minted@def@optfv{breaksymbolright}
\minted@def@optfv{breaksymbolsepright}
\minted@def@optfv{breaksymbolseprightnchars}
\minted@def@optfv{breaksymbolindentright}
\minted@def@optfv{breaksymbolindentrightnchars}
\minted@def@optfv{breakbefore}
\minted@def@optfv{breakbeforesymbolpre}
\minted@def@optfv{breakbeforesymbolpost}
\minted@def@optfv@switch{breakbeforegroup}
\minted@def@optfv{breakafter}
\minted@def@optfv@switch{breakaftergroup}
\minted@def@optfv{breakaftersymbolpre}
\minted@def@optfv{breakaftersymbolpost}
\minted@def@optfv@switch{breakanywhere}
\minted@def@optfv{breakanywheresymbolpre}
\minted@def@optfv{breakanywheresymbolpost}
\minted@def@opt{bgcolor}
\minted@def@opt@switch{autogobble}
\newcommand{\minted@encoding}{\minted@get@opt{encoding}{UTF8}}
\newenvironment{minted@snugshade*}[1]{%
  \def\FrameCommand##1{\hskip\@totalleftmargin
    \colorbox{#1}{##1}%
    \hskip-\linewidth \hskip-\@totalleftmargin \hskip\columnwidth}%
  \MakeFramed{\advance\hsize-\width
    \@totalleftmargin\z@ \linewidth\hsize
    \advance\labelsep\fboxsep
    \@setminipage}%
 }{\par\unskip\@minipagefalse\endMakeFramed}
\newsavebox{\minted@bgbox}
\newenvironment{minted@colorbg}[1]{%
  \setlength{\OuterFrameSep}{0pt}%
  \let\minted@tmp\FV@NumberSep
  \edef\FV@NumberSep{%
    \the\numexpr\dimexpr\minted@tmp+\number\fboxsep\relax sp\relax}%
  \medskip
  \begin{minted@snugshade*}{#1}}
 {\end{minted@snugshade*}%
  \medskip\noindent}
\newwrite\minted@code
\newcommand{\minted@savecode}[1]{
  \immediate\openout\minted@code\minted@jobname.pyg\relax
  \immediate\write\minted@code{\expandafter\detokenize\expandafter{#1}}%
  \immediate\closeout\minted@code}
\newcounter{minted@FancyVerbLineTemp}
\newcommand{\minted@write@detok}[1]{%
  \immediate\write\FV@OutFile{\detokenize{#1}}}
\newcommand{\minted@FVB@VerbatimOut}[1]{%
  \setcounter{minted@FancyVerbLineTemp}{\value{FancyVerbLine}}%
  \@bsphack
  \begingroup
    \FV@UseKeyValues
    \FV@DefineWhiteSpace
    \def\FV@Space{\space}%
    \FV@DefineTabOut
    \let\FV@ProcessLine\minted@write@detok
    \immediate\openout\FV@OutFile #1\relax
    \let\FV@FontScanPrep\relax
    \let\@noligs\relax
    \FV@Scan}
\newcommand{\minted@FVE@VerbatimOut}{%
  \immediate\closeout\FV@OutFile\endgroup\@esphack
  \setcounter{FancyVerbLine}{\value{minted@FancyVerbLineTemp}}}%
\ifcsname MintedPygmentize\endcsname\else
  \newcommand{\MintedPygmentize}{pygmentize}
\fi
\newcounter{minted@pygmentizecounter}
\newcommand{\minted@pygmentize}[2][\minted@outputdir\minted@jobname.pyg]{%
  \minted@checkstyle{\minted@get@opt{style}{default}}%
  \stepcounter{minted@pygmentizecounter}%
  \ifthenelse{\equal{\minted@get@opt{autogobble}{false}}{true}}%
    {\def\minted@codefile{\minted@outputdir\minted@jobname.pyg}}%
    {\def\minted@codefile{#1}}%
  \ifthenelse{\boolean{minted@isinline}}%
    {\def\minted@optlistcl@inlines{%
      \minted@optlistcl@g@i
      \csname minted@optlistcl@lang\minted@lang @i\endcsname}}%
    {\let\minted@optlistcl@inlines\@empty}%
  \def\minted@cmd{%
    \ifminted@kpsewhich
      \ifwindows
        \detokenize{for /f "usebackq tokens=*"}\space\@percentchar\detokenize{a in (`kpsewhich}\space\minted@codefile\detokenize{`) do}\space
      \fi
    \fi
    \MintedPygmentize\space -l #2
    -f latex -P commandprefix=PYG -F tokenmerge
    \minted@optlistcl@g \csname minted@optlistcl@lang\minted@lang\endcsname
    \minted@optlistcl@inlines
    \minted@optlistcl@cmd -o \minted@outputdir\minted@infile\space
    \ifminted@kpsewhich
      \ifwindows
        \@percentchar\detokenize{a}%
      \else
        \detokenize{`}kpsewhich \minted@codefile\space
          \detokenize{||} \minted@codefile\detokenize{`}%
      \fi
    \else
      \minted@codefile
    \fi}%
  % For debugging, uncomment: %%%%
  % \immediate\typeout{\minted@cmd}%
  % %%%%
  \ifthenelse{\boolean{minted@cache}}%
    {%
      \ifminted@frozencache
      \else
        \ifx\XeTeXinterchartoks\minted@undefined
          \ifthenelse{\equal{\minted@get@opt{autogobble}{false}}{true}}%
            {\edef\minted@hash{\pdf@filemdfivesum{#1}%
              \pdf@mdfivesum{\minted@cmd autogobble(\ifx\FancyVerbStartNum\z@ 0\else\FancyVerbStartNum\fi-\ifx\FancyVerbStopNum\z@ 0\else\FancyVerbStopNum\fi)}}}%
            {\edef\minted@hash{\pdf@filemdfivesum{#1}%
              \pdf@mdfivesum{\minted@cmd}}}%
        \else
          \ifx\mdfivesum\minted@undefined
            \immediate\openout\minted@code\minted@jobname.mintedcmd\relax
            \immediate\write\minted@code{\minted@cmd}%
            \ifthenelse{\equal{\minted@get@opt{autogobble}{false}}{true}}%
              {\immediate\write\minted@code{autogobble(\ifx\FancyVerbStartNum\z@ 0\else\FancyVerbStartNum\fi-\ifx\FancyVerbStopNum\z@ 0\else\FancyVerbStopNum\fi)}}{}%
            \immediate\closeout\minted@code
            \edef\minted@argone@esc{#1}%
            \StrSubstitute{\minted@argone@esc}{\@backslashchar}{\@backslashchar\@backslashchar}[\minted@argone@esc]%
            \StrSubstitute{\minted@argone@esc}{"}{\@backslashchar"}[\minted@argone@esc]%
            \edef\minted@tmpfname@esc{\minted@outputdir\minted@jobname}%
            \StrSubstitute{\minted@tmpfname@esc}{\@backslashchar}{\@backslashchar\@backslashchar}[\minted@tmpfname@esc]%
            \StrSubstitute{\minted@tmpfname@esc}{"}{\@backslashchar"}[\minted@tmpfname@esc]%
            %Cheating a little here by using ASCII codes to write `{` and `}`
            %in the Python code
            \def\minted@hashcmd{%
              \detokenize{python -c "import hashlib; import os;
                hasher = hashlib.sha1();
                f = open(os.path.expanduser(os.path.expandvars(\"}\minted@tmpfname@esc.mintedcmd\detokenize{\")), \"rb\");
                hasher.update(f.read());
                f.close();
                f = open(os.path.expanduser(os.path.expandvars(\"}\minted@argone@esc\detokenize{\")), \"rb\");
                hasher.update(f.read());
                f.close();
                f = open(os.path.expanduser(os.path.expandvars(\"}\minted@tmpfname@esc.mintedmd5\detokenize{\")), \"w\");
                macro = \"\\edef\\minted@hash\" + chr(123) + hasher.hexdigest() + chr(125) + \"\";
                f.write(\"\\makeatletter\" + macro + \"\\makeatother\\endinput\n\");
                f.close();"}}%
            \ShellEscape{\minted@hashcmd}%
            \minted@input{\minted@outputdir\minted@jobname.mintedmd5}%
          \else
            \ifthenelse{\equal{\minted@get@opt{autogobble}{false}}{true}}%
             {\edef\minted@hash{\mdfivesum file {#1}%
                \mdfivesum{\minted@cmd autogobble(\ifx\FancyVerbStartNum\z@ 0\else\FancyVerbStartNum\fi-\ifx\FancyVerbStopNum\z@ 0\else\FancyVerbStopNum\fi)}}}%
             {\edef\minted@hash{\mdfivesum file {#1}%
                \mdfivesum{\minted@cmd}}}%
          \fi
        \fi
        \edef\minted@infile{\minted@cachedir/\minted@hash.pygtex}%
        \IfFileExists{\minted@infile}{}{%
          \ifthenelse{\equal{\minted@get@opt{autogobble}{false}}{true}}{%
            \minted@autogobble{#1}}{}%
          \ShellEscape{\minted@cmd}}%
      \fi
      \ifthenelse{\boolean{minted@finalizecache}}%
       {%
          \edef\minted@cachefilename{listing\arabic{minted@pygmentizecounter}.pygtex}%
          \edef\minted@actualinfile{\minted@cachedir/\minted@cachefilename}%
          \ifwindows
            \StrSubstitute{\minted@infile}{/}{\@backslashchar}[\minted@infile@windows]
            \StrSubstitute{\minted@actualinfile}{/}{\@backslashchar}[\minted@actualinfile@windows]
            \ShellEscape{move /y \minted@outputdir\minted@infile@windows\space\minted@outputdir\minted@actualinfile@windows}%
          \else
            \ShellEscape{mv -f \minted@outputdir\minted@infile\space\minted@outputdir\minted@actualinfile}%
          \fi
          \let\minted@infile\minted@actualinfile
          \expandafter\minted@addcachefile\expandafter{\minted@cachefilename}%
       }%
       {\ifthenelse{\boolean{minted@frozencache}}%
         {%
            \edef\minted@cachefilename{listing\arabic{minted@pygmentizecounter}.pygtex}%
            \edef\minted@infile{\minted@cachedir/\minted@cachefilename}%
            \expandafter\minted@addcachefile\expandafter{\minted@cachefilename}}%
         {\expandafter\minted@addcachefile\expandafter{\minted@hash.pygtex}}%
       }%
      \minted@inputpyg}%
    {%
      \ifthenelse{\equal{\minted@get@opt{autogobble}{false}}{true}}{%
        \minted@autogobble{#1}}{}%
      \ShellEscape{\minted@cmd}%
      \minted@inputpyg}%
}
\def\minted@autogobble#1{%
  \edef\minted@argone@esc{#1}%
  \StrSubstitute{\minted@argone@esc}{\@backslashchar}{\@backslashchar\@backslashchar}[\minted@argone@esc]%
  \StrSubstitute{\minted@argone@esc}{"}{\@backslashchar"}[\minted@argone@esc]%
  \edef\minted@tmpfname@esc{\minted@outputdir\minted@jobname}%
  \StrSubstitute{\minted@tmpfname@esc}{\@backslashchar}{\@backslashchar\@backslashchar}[\minted@tmpfname@esc]%
  \StrSubstitute{\minted@tmpfname@esc}{"}{\@backslashchar"}[\minted@tmpfname@esc]%
  %Need a version of open() that supports encoding under Python 2
  \edef\minted@autogobblecmd{%
    \ifminted@kpsewhich
      \ifwindows
        \detokenize{for /f "usebackq tokens=*" }\@percentchar\detokenize{a in (`kpsewhich} #1\detokenize{`) do}\space
      \fi
    \fi
    \detokenize{python -c "import sys; import os;
    import textwrap;
    from io import open;
    fname = }%
      \ifminted@kpsewhich
        \detokenize{sys.argv[1];}\space%
      \else
        \detokenize{os.path.expanduser(os.path.expandvars(\"}\minted@argone@esc\detokenize{\"));}\space%
      \fi
    \detokenize{f = open(fname, \"r\", encoding=\"}\minted@encoding\detokenize{\") if os.path.isfile(fname) else None;
    t = f.readlines() if f is not None else None;
    t_opt = t if t is not None else [];
    f.close() if f is not None else None;
    tmpfname = os.path.expanduser(os.path.expandvars(\"}\minted@tmpfname@esc.pyg\detokenize{\"));
    f = open(tmpfname, \"w\", encoding=\"}\minted@encoding\detokenize{\") if t is not None else None;
    fvstartnum = }\ifx\FancyVerbStartNum\z@ 0\else\FancyVerbStartNum\fi\detokenize{;
    fvstopnum = }\ifx\FancyVerbStopNum\z@ 0\else\FancyVerbStopNum\fi\detokenize{;
    s = fvstartnum-1 if fvstartnum != 0 else 0;
    e = fvstopnum if fvstopnum != 0 else len(t_opt);
    [f.write(textwrap.dedent(\"\".join(x))) for x in (t_opt[0:s], t_opt[s:e], t_opt[e:]) if x and t is not None];
    f.close() if t is not None else os.remove(tmpfname);"}%
    \ifminted@kpsewhich
      \ifwindows
        \space\@percentchar\detokenize{a}%
      \else
        \space\detokenize{`}kpsewhich #1\space\detokenize{||} #1\detokenize{`}%
      \fi
    \fi
  }%
  \ShellEscape{\minted@autogobblecmd}%
}
\newcommand{\minted@inputpyg}{%
  \expandafter\let\expandafter\minted@PYGstyle%
    \csname PYG\minted@get@opt{style}{default}\endcsname
  \VerbatimPygments{\PYG}{\minted@PYGstyle}%
  \ifthenelse{\boolean{minted@isinline}}%
   {\ifthenelse{\equal{\minted@get@opt{breaklines}{false}}{true}}%
    {\let\FV@BeginVBox\relax
     \let\FV@EndVBox\relax
     \def\FV@BProcessLine##1{\FancyVerbFormatLine{##1}}%
     \minted@inputpyg@inline}%
    {\minted@inputpyg@inline}}%
   {\minted@inputpyg@block}%
}
\def\minted@inputpyg@inline{%
  \ifthenelse{\equal{\minted@get@opt{bgcolor}{}}{}}%
   {\minted@input{\minted@outputdir\minted@infile}}%
   {\colorbox{\minted@get@opt{bgcolor}{}}{%
      \minted@input{\minted@outputdir\minted@infile}}}%
}
\def\minted@inputpyg@block{%
  \ifthenelse{\equal{\minted@get@opt{bgcolor}{}}{}}%
   {\minted@input{\minted@outputdir\minted@infile}}%
   {\begin{minted@colorbg}{\minted@get@opt{bgcolor}{}}%
    \minted@input{\minted@outputdir\minted@infile}%
    \end{minted@colorbg}}}
\newcommand{\minted@langlinenoson}{%
  \ifcsname c@minted@lang\minted@lang\endcsname\else
    \newcounter{minted@lang\minted@lang}%
  \fi
  \setcounter{minted@FancyVerbLineTemp}{\value{FancyVerbLine}}%
  \setcounter{FancyVerbLine}{\value{minted@lang\minted@lang}}%
}
\newcommand{\minted@langlinenosoff}{%
  \setcounter{minted@lang\minted@lang}{\value{FancyVerbLine}}%
  \setcounter{FancyVerbLine}{\value{minted@FancyVerbLineTemp}}%
}
\ifthenelse{\boolean{minted@langlinenos}}{}{%
  \let\minted@langlinenoson\relax
  \let\minted@langlinenosoff\relax
}
\newcommand{\setminted}[2][]{%
  \ifthenelse{\equal{#1}{}}%
    {\setkeys{minted@opt@g}{#2}}%
    {\minted@configlang{#1}%
      \setkeys{minted@opt@lang}{#2}}}
\newcommand{\setmintedinline}[2][]{%
  \ifthenelse{\equal{#1}{}}%
    {\setkeys{minted@opt@g@i}{#2}}%
    {\minted@configlang{#1}%
      \setkeys{minted@opt@lang@i}{#2}}}
\setmintedinline[php]{startinline=true}
\setminted{tabcolor=black}
\newcommand{\usemintedstyle}[2][]{\setminted[#1]{style=#2}}
\begingroup
\catcode`\ =\active
\catcode`\^^I=\active
\gdef\minted@defwhitespace@retok{\def {\noexpand\FV@Space}\def^^I{\noexpand\FV@Tab}}%
\endgroup
\newcommand{\minted@writecmdcode}[1]{%
  \immediate\openout\minted@code\minted@jobname.pyg\relax
  \immediate\write\minted@code{\detokenize{#1}}%
  \immediate\closeout\minted@code}
\newrobustcmd{\mintinline}[2][]{%
  \begingroup
  \setboolean{minted@isinline}{true}%
  \minted@configlang{#2}%
  \setkeys{minted@opt@cmd}{#1}%
  \minted@fvset
  \begingroup
  \let\do\@makeother\dospecials
  \catcode`\{=1
  \catcode`\}=2
  \catcode`\^^I=\active
  \@ifnextchar\bgroup
    {\minted@inline@iii}%
    {\catcode`\{=12\catcode`\}=12
      \minted@inline@i}}
\def\minted@inline@i#1{%
  \endgroup
  \def\minted@inline@ii##1#1{%
    \minted@inline@iii{##1}}%
  \begingroup
  \let\do\@makeother\dospecials
  \catcode`\^^I=\active
  \minted@inline@ii}
\ifthenelse{\boolean{minted@draft}}%
  {\newcommand{\minted@inline@iii}[1]{%
    \endgroup
    \begingroup
    \minted@defwhitespace@retok
    \everyeof{\noexpand}%
    \endlinechar-1\relax
    \let\do\@makeother\dospecials
    \catcode`\ =\active
    \catcode`\^^I=\active
    \xdef\minted@tmp{\scantokens{#1}}%
    \endgroup
    \let\FV@Line\minted@tmp
    \def\FV@SV@minted@tmp{%
      \FV@Gobble
      \expandafter\FV@ProcessLine\expandafter{\FV@Line}}%
    \ifthenelse{\equal{\minted@get@opt{breaklines}{false}}{true}}%
     {\let\FV@BeginVBox\relax
      \let\FV@EndVBox\relax
      \def\FV@BProcessLine##1{\FancyVerbFormatLine{##1}}%
      \BUseVerbatim{minted@tmp}}%
     {\BUseVerbatim{minted@tmp}}%
    \endgroup}}%
  {\newcommand{\minted@inline@iii}[1]{%
    \endgroup
    \minted@writecmdcode{#1}%
    \RecustomVerbatimEnvironment{Verbatim}{BVerbatim}{}%
    \setcounter{minted@FancyVerbLineTemp}{\value{FancyVerbLine}}%
    \minted@pygmentize{\minted@lang}%
    \setcounter{FancyVerbLine}{\value{minted@FancyVerbLineTemp}}%
    \endgroup}}
\newrobustcmd{\mint}[2][]{%
  \begingroup
  \minted@configlang{#2}%
  \setkeys{minted@opt@cmd}{#1}%
  \minted@fvset
  \begingroup
  \let\do\@makeother\dospecials
  \catcode`\{=1
  \catcode`\}=2
  \catcode`\^^I=\active
  \@ifnextchar\bgroup
    {\mint@iii}%
    {\catcode`\{=12\catcode`\}=12
      \mint@i}}
\def\mint@i#1{%
  \endgroup
  \def\mint@ii##1#1{%
    \mint@iii{##1}}%
  \begingroup
  \let\do\@makeother\dospecials
  \catcode`\^^I=\active
  \mint@ii}
\ifthenelse{\boolean{minted@draft}}%
  {\newcommand{\mint@iii}[1]{%
    \endgroup
    \begingroup
    \minted@defwhitespace@retok
    \everyeof{\noexpand}%
    \endlinechar-1\relax
    \let\do\@makeother\dospecials
    \catcode`\ =\active
    \catcode`\^^I=\active
    \xdef\minted@tmp{\scantokens{#1}}%
    \endgroup
    \let\FV@Line\minted@tmp
    \def\FV@SV@minted@tmp{%
      \FV@CodeLineNo=1\FV@StepLineNo
      \FV@Gobble
      \expandafter\FV@ProcessLine\expandafter{\FV@Line}}%
    \minted@langlinenoson
    \UseVerbatim{minted@tmp}%
    \minted@langlinenosoff
    \endgroup}}%
  {\newcommand{\mint@iii}[1]{%
    \endgroup
    \minted@writecmdcode{#1}%
    \minted@langlinenoson
    \minted@pygmentize{\minted@lang}%
    \minted@langlinenosoff
    \endgroup}}
\ifthenelse{\boolean{minted@draft}}%
  {\newenvironment{minted}[2][]
    {\VerbatimEnvironment
      \minted@configlang{#2}%
      \setkeys{minted@opt@cmd}{#1}%
      \minted@fvset
      \minted@langlinenoson
      \begin{Verbatim}}%
    {\end{Verbatim}%
      \minted@langlinenosoff}}%
  {\newenvironment{minted}[2][]
    {\VerbatimEnvironment
      \let\FVB@VerbatimOut\minted@FVB@VerbatimOut
      \let\FVE@VerbatimOut\minted@FVE@VerbatimOut
      \minted@configlang{#2}%
      \setkeys{minted@opt@cmd}{#1}%
      \minted@fvset
      \begin{VerbatimOut}[codes={\catcode`\^^I=12},firstline,lastline]{\minted@jobname.pyg}}%
    {\end{VerbatimOut}%
        \minted@langlinenoson
        \minted@pygmentize{\minted@lang}%
        \minted@langlinenosoff}}
\ifthenelse{\boolean{minted@draft}}%
  {\newcommand{\inputminted}[3][]{%
    \begingroup
    \minted@configlang{#2}%
    \setkeys{minted@opt@cmd}{#1}%
    \minted@fvset
    \VerbatimInput{#3}%
    \endgroup}}%
  {\newcommand{\inputminted}[3][]{%
    \begingroup
    \minted@configlang{#2}%
    \setkeys{minted@opt@cmd}{#1}%
    \minted@fvset
    \minted@pygmentize[#3]{#2}%
    \endgroup}}
\newcommand{\newminted}[3][]{
  \ifthenelse{\equal{#1}{}}
    {\def\minted@envname{#2code}}
    {\def\minted@envname{#1}}
  \newenvironment{\minted@envname}
    {\VerbatimEnvironment
      \begin{minted}[#3]{#2}}
    {\end{minted}}
  \newenvironment{\minted@envname *}[1]
    {\VerbatimEnvironment\begin{minted}[#3,##1]{#2}}
    {\end{minted}}}
\newcommand{\newmint}[3][]{
  \ifthenelse{\equal{#1}{}}
    {\def\minted@shortname{#2}}
    {\def\minted@shortname{#1}}
  \expandafter\newcommand\csname\minted@shortname\endcsname[2][]{
    \mint[#3,##1]{#2}##2}}
\newcommand{\newmintedfile}[3][]{
  \ifthenelse{\equal{#1}{}}
    {\def\minted@shortname{#2file}}
    {\def\minted@shortname{#1}}
  \expandafter\newcommand\csname\minted@shortname\endcsname[2][]{
    \inputminted[#3,##1]{#2}{##2}}}
\newcommand{\newmintinline}[3][]{%
  \ifthenelse{\equal{#1}{}}%
    {\def\minted@shortname{#2inline}}%
    {\def\minted@shortname{#1}}%
    \expandafter\newrobustcmd\csname\minted@shortname\endcsname{%
      \begingroup
      \let\do\@makeother\dospecials
      \catcode`\{=1
      \catcode`\}=2
      \@ifnextchar[{\endgroup\minted@inliner[#3][#2]}%
        {\endgroup\minted@inliner[#3][#2][]}}%
    \def\minted@inliner[##1][##2][##3]{\mintinline[##1,##3]{##2}}%
}
\ifthenelse{\boolean{minted@newfloat}}%
 {\@ifundefined{minted@float@within}%
    {\DeclareFloatingEnvironment[fileext=lol,placement=tbp]{listing}}%
    {\def\minted@tmp#1{%
       \DeclareFloatingEnvironment[fileext=lol,placement=tbp, within=#1]{listing}}%
     \expandafter\minted@tmp\expandafter{\minted@float@within}}}%
 {\@ifundefined{minted@float@within}%
    {\newfloat{listing}{tbp}{lol}}%
    {\newfloat{listing}{tbp}{lol}[\minted@float@within]}}
\ifminted@newfloat\else
\newcommand{\listingscaption}{Listing}
\floatname{listing}{\listingscaption}
\newcommand{\listoflistingscaption}{List of Listings}
\providecommand{\listoflistings}{\listof{listing}{\listoflistingscaption}}
\fi
\AtEndOfPackage{%
  \ifthenelse{\boolean{minted@draft}}%
   {}%
   {%
    \ifthenelse{\boolean{minted@frozencache}}{}{%
      \ifnum\pdf@shellescape=1\relax\else
        \PackageError{minted}%
         {You must invoke LaTeX with the
          -shell-escape flag}%
         {Pass the -shell-escape flag to LaTeX. Refer to the minted.sty
          documentation for more information.}%
      \fi}%
   }%
}
\AtEndPreamble{%
  \ifthenelse{\boolean{minted@draft}}%
   {}%
   {%
    \ifthenelse{\boolean{minted@frozencache}}{}{%
      \TestAppExists{\MintedPygmentize}%
      \ifAppExists\else
        \PackageError{minted}%
         {You must have `pygmentize' installed
          to use this package}%
         {Refer to the installation instructions in the minted
          documentation for more information.}%
      \fi}%
  }%
}
\AfterEndDocument{%
  \ifthenelse{\boolean{minted@draft}}%
   {}%
   {\ifthenelse{\boolean{minted@frozencache}}%
     {}
     {\ifx\XeTeXinterchartoks\minted@undefined
      \else
        \DeleteFile[\minted@outputdir]{\minted@jobname.mintedcmd}%
        \DeleteFile[\minted@outputdir]{\minted@jobname.mintedmd5}%
      \fi
      \DeleteFile[\minted@outputdir]{\minted@jobname.pyg}%
      \DeleteFile[\minted@outputdir]{\minted@jobname.out.pyg}%
     }%
   }%
}
\endinput
%%
%% End of file `minted.sty'.
'''
    def put(self):
        with codecs.open(os.path.join(self.outdir, 'minted.sty'), 'w', encoding='UTF-8') as f:
            f.write(self.sty)
