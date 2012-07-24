import os, sys

def getfname(innames, outname):
	if not outname:
		fname = '-'.join([os.path.splitext(name)[0] for name in innames])
	else:
		fname = outname
	if fname.endswith('.pdf'):
		fname = fname.replace('.pdf', '')
	return fname

def wraptxt(line, sep, by):
    # will also remove blank lines, if any
    sline = ''
    i = 0
    for item in list(line):
        if item == '\n' and i == 0:
            # unnecessary wrap
            continue
        if item == '\n':
            # natural wrap
            sline += item
            i = 0
            continue
        j = 1
        if item == '\t':
            # assume 1 tab = 8 white spaces
            j = 9
        for k in range(j):
            if i == by:
                # time to wrap
                sline += item + sep + '\n'
                i = 0
                break
            else:
                i += 1
        if not i == 0:
            sline += item
    return sline
