import sys
from subprocess import call

def getDocHead(args):
    if args.title != None:
        mytitle = list(args.title)
        mytitle = [w.replace('$', '\$') for w in mytitle]
        mytitle = [w.replace('_', '\_') for w in mytitle]
        mytitle = [w.replace('%', '\%') for w in mytitle]
        mytitle = [w.replace('&', '\&') for w in mytitle]
        mytitle = ''.join(mytitle)
    else:
        mytitle = args.title
    if args.author != None:
        myauthor = list(args.author)
        myauthor = [w.replace('$', '\$') for w in myauthor]
        myauthor = [w.replace('_', '\_') for w in myauthor]
        myauthor = [w.replace('%', '\%') for w in myauthor]
        myauthor = [w.replace('&', '\&') for w in myauthor]
        myauthor = ''.join(myauthor)
    else:
        myauthor = args.author
    docHead = ['\\documentclass[oneside, 10pt]{article}\n', '\\usepackage{geometry}\n', '\\usepackage{fullpage}\n', '\\usepackage{amsmath}\n', '\\usepackage{booktabs}\n', '\\usepackage{listings}\n', '\\usepackage{subfig}\n', '\\usepackage{amssymb}\n', '\\usepackage{amsthm}\n', '\\usepackage{bm}\n', '\\usepackage{extarrows}\n', '\\usepackage{fancyhdr}\n', '\\usepackage{fancyvrb}\n', '\\usepackage[pdftex]{graphicx}\n', '\\usepackage[pdfstartview=FitH]{hyperref}\n', '\\usepackage{ctable}\n', '\\usepackage[dvipsnames]{xcolor}\n', '\\usepackage{verbatim}\n', '\\usepackage{minted}\n', '\\usepackage{pdfpages}\n', '\\usepackage{titlesec}\n','\\renewcommand\\rmdefault{bch}\n', '\\newcommand{\\ie}{\\textit{i.e.}}\n', '\\newcommand\\me{\\mathrm{e}}\n', '\\newcommand\\mlog{\\mathrm{log}}\n', '\\linespread{1.1}\n', '\\setlength{\\parskip}{8pt plus1pt minus2pt}\n', '\\parindent 0ex\n', '\\geometry{left=0.8in,right=0.8in,top=0.8in,bottom=0.8in}', '\\titleformat{\\subsubsection}\n', '{\\color{MidnightBlue}\\normalfont\\large\\bfseries}\n', '{\\color{MidnightBlue}\\thesection}{1em}{}\n', '\\definecolor{bg}{rgb}{0.95,0.95,0.95}\n', '\\title{%s}\n' % mytitle, '\\author{%s}\n' % myauthor, '\\date{Compiled: \\today}\n', '\\raggedbottom\n', '\\begin{document}\n\n']
    return docHead

def recodeLatexKw(tmpline):
    tmpline = list(tmpline)
    tmpline = [w.replace('$', '\$') for w in tmpline]
    tmpline = [w.replace('{', '\{') for w in tmpline]
    tmpline = [w.replace('}', '\}') for w in tmpline]
    tmpline = [w.replace('%', '\%') for w in tmpline]
    tmpline = [w.replace('_', '\_') for w in tmpline]
    tmpline = [w.replace('&', '\&') for w in tmpline]
    tmpline = [w.replace('<', '$<$') for w in tmpline]
    tmpline = [w.replace('>', '$>$') for w in tmpline]
    if tmpline[0] != '#':
        tmpline = [w.replace('#', '\#') for w in tmpline]
    else:
        #FIXME
        pass 
    return ''.join(tmpline)
                
def getDocBody(args, extension):
    myDoc = getDocHead(args)
    if args.title != None:
        myDoc.append('\\maketitle\n')
    if extension == 'history':
        for fn in args.filename:
            try:
                open('.'.join([fn, extension]))
            except IOError as e:
                print("***{0}***".format(e))
                sys.exit(1)
            myDoc.append('\\inputminted[linenos, numberblanklines=true, fontsize=\\footnotesize]{bash}{%s}\n' % (fn + '.' + extension))
    else:
        for fn in args.filename:
            try:
                fob = open('.'.join([fn, extension]), 'r')
            except IOError as e:
                print("***{0}***".format(e))
                sys.exit(1)
            mylines =  fob.readlines()
            fob.close()
            
            index = 0
            while index < len(mylines):
                # Program source codes in this line
                if mylines[index].startswith('$'):
                    tmpline = ''.join(['\\mint[bgcolor=bg, numberblanklines=true, fontsize=\\footnotesize]{bash}|', mylines[index][1:-1], '|\n'])
                    if not (index == 0 or mylines[index-1].startswith('$')):
                        tmpline = ''.join(['\n', tmpline])
                    if not (index == len(mylines) - 1 or mylines[index+1].startswith('$')):
                        myDoc.append(''.join([tmpline, '\n']))
                    else:
                        myDoc.append(tmpline)
                    index += 1

                elif mylines[index].startswith('>>>'):
                    tmpline = ''.join(['\\mint[bgcolor=bg, numberblanklines=true, fontsize=\\footnotesize]{python}|', mylines[index][3:-1], '|\n'])
                    if not (index == 0 or mylines[index-1].startswith('>>>')):
                        tmpline = ''.join(['\n', tmpline])
                    if not (index == len(mylines) - 1 or mylines[index+1].startswith('>>>')):
                        myDoc.append(''.join([tmpline, '\n']))
                    else:
                        myDoc.append(tmpline)
                    index += 1
                    
                # Itemizations in this line (and its following lines)
                elif mylines[index].startswith('---'):
                    endIndex = None
                    try:
                        for i in range(index+1, len(mylines)):
                            if mylines[i].startswith('---'):
                                endIndex = i
                                break
                        if endIndex is None:
                            raise ValueError('symbol \'---\' must appear in pairs')
                    except ValueError as v:
                        print('***{0}***'.format(v))
                        sys.exit(1)
                    else:
                        myDoc.append('\\begin{itemize}\n')
                        hasItem = False
                        for i in range(index+1, endIndex):
                            if mylines[i].startswith('-'):
                                hasItem = True
                                mylines[i] = recodeLatexKw(mylines[i])
                                myDoc.append(' '.join(['\\item', mylines[i][1:]]))
                            else:
                                mylines[i] = recodeLatexKw(mylines[i])
                                myDoc.append(mylines[i])
                        if hasItem == False:
                            print('ERROR: missing \\item entries between lines {0} and {1}'.format(index, endIndex))
                            sys.exit(1) 
                        myDoc.append('\\end{itemize}\n')
                        index = endIndex + 1
                
                # section symbols in this line
                elif mylines[index].startswith('###') and mylines[index+1].startswith('#') and mylines[index+2].startswith('###'):
                    mylines[index+1] = recodeLatexKw(mylines[index+1])
                    myDoc.append(''.join(['\\section{', mylines[index+1][1:-1], '}\n']))
                    index += 3
                    
                elif mylines[index].startswith('#!-'):
                    mylines[index] = recodeLatexKw(mylines[index])
                    myDoc.append(''.join(['\\subsubsection*{', mylines[index][3:-1], '}\n']))
                    index += 1
                    
                elif mylines[index].startswith('#!'):
                    mylines[index] = recodeLatexKw(mylines[index])
                    myDoc.append(''.join(['\\subsection{', mylines[index][2:-1], '}\n']))
                    index += 1
                
                # Nothing special, just a plain line here   
                else:
                    if mylines[index] == '\n':
                        myDoc.append('\n')
                    else:
                        myDoc.append(recodeLatexKw(mylines[index])[:-1] + '\\\\' + '\n')
                    index += 1
                    
    myDoc.append('\\end{document}')
    tmpFilename = '-'.join(args.filename) + '_' + extension
    outFilename = tmpFilename + '.tex'
    fob = open(outFilename, 'w')
    fob.writelines(myDoc)
    fob.close()
    # Run LaTeX
    call(["pdflatex", "-shell-escape", outFilename])
    call(["pdflatex", "-shell-escape", outFilename])
    call(["rm", tmpFilename + '.aux'])
    call(["rm", tmpFilename + '.log'])
    call(["rm", tmpFilename + '.out'])
    try:
        open(tmpFilename + '.pyg')
    except IOError as e:
        sys.exit(1)
    call(["rm", tmpFilename + '.pyg'])
