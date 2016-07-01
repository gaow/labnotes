#!/usr/bin/env python
import sys, os
from collections import OrderedDict
from dsc import HTML_CSS, HTML_JS
from dsc.utils import flatten_list, make_html_name

def figs2html(content, to_file, title):
    '''
    section_content: ordered dictionaries,
    {'section 1': {'tab1': {'item1':[]}}}
    '''
    if not os.path.splitext(to_file)[1] == '.html':
        to_file = os.path.splitext(to_file)[0] + '.html'
    with open(to_file, 'w') as f:
        # header and style/scripts
        f.write('<!DOCTYPE html><html><head><title>{} | DSC2</title>\n'.format(title))
        f.write('<style type="text/css">\n')
        f.write(HTML_CSS)
        f.write('\n</style>\n<script type="text/javascript">\n')
        f.write(HTML_JS)
        f.write('</script></head><body><div class="accordion">\n')
        # sections
        for name, section in content.items():
            f.write('<div class="accodion-section">\n'
                    '<a class="accordion-section-title" href="#{1}">{0}</a>\n'
                    '<div id={1} class="accordion-section-content">\n'.format(name, make_html_name(name)))
            f.write('<div class="tabs">\n<ul class="tab-links">\n')
            for idx, key in enumerate(section.keys()):
                f.write('<li{2}><a href="#{0}">{1}</a></li>\n'.\
                        format(make_html_name(name + '_' + key), key,
                               ' class="active"' if idx == 0 else ''))
            f.write('</ul>\n<div class="tab-content">\n')
            for idx, key in enumerate(section.keys()):
                f.write('<div id="{0}" class="tab{1}">\n'.\
                        format(make_html_name(name + '_' + key), ' active' if idx == 0 else ''))
                for kk in section[key]:
                    f.write('\n<li>{}</li>'.format(kk))
                    for item in section[key][kk]:
                        f.write('\n<a class="fancybox-thumb" rel="{0}" href="{0}.png" title="{0}">' \
                                '<img width=300 src="{0}.png" alt="" /></a>'.format(item))
                f.write('\n</div>\n')
            f.write('</div></div></div></div>\n')
        f.write('\n</div></body></html>')

def md2dict(md_file):
    def load_data(tmp):
        if curr2 is None:
            return
        curr3 = ''
        for ii in tmp:
            if not ii.startswith('dsc'):
                curr3 = ii
                res[curr1][curr2][curr3] = []
            else:
                res[curr1][curr2][curr3].append(ii)
        return []
    #
    res = OrderedDict()
    curr1 = curr2 = None
    tmp = []
    with open(md_file) as f:
        lines = [x.strip() for x in f.readlines()]
    for idx, line in enumerate(lines):
        if line.startswith('### '):
            res[line[4:]] = OrderedDict()
            curr1 = line[4:]
        elif line.startswith('#### '):
            res[curr1][line[5:]] = OrderedDict()
            curr2 = line[5:]
        else:
            if line:
                tmp.append(line)
            if idx + 1 < len(lines) and lines[idx + 1].startswith('#'):
                tmp = load_data(tmp)
    load_data(tmp)
    return res

def pdf2png(data):
    for k in data:
        for kk in data[k]:
            for kkk in data[k][kk]:
                for item in data[k][kk][kkk]:
                    if not os.path.isfile(item + '.png'):
                        os.system('convert -density 200 {0}.pdf {0}.png'.format(item))
                    if os.path.isfile(item + '-1.png'):
                        os.rename(item + '-1.png', item + '.png')

if __name__ == '__main__':
    data = md2dict(sys.argv[1])
    pdf2png(data)
    figs2html(data, sys.argv[1], 'dr-tree benchmark')
