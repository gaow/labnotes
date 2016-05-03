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
\\usepackage{titlesec}
\\usepackage{longtable}
\\usepackage{seqsplit}
\\usepackage{subfigure}
\\usepackage[multidot]{grffile}
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
