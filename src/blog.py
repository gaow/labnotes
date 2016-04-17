#!/usr/bin/env python3
# -*- coding: utf-8 -*-
import os, glob, yaml, getpass, datetime
from distutils.dir_util import mkpath
from .parser import ParserCore
from .encoder import Html
from .style import BlogCSS
from .utils import env, cd

class BlogCFG:
    def __init__(self, config_file, date):
        d = yaml.load(open(os.path.expanduser(config_file)))
        for key in ['editor', 'blog_dir', 'url', 'ssh_path',
                    'title', 'logo_img_name', 'background_img_name', 'media_url']:
            if key not in d:
                raise ValueError('Cannot find required key ``{}`` in ``{}``!'.format(key, config_file))
        for key, value in list(d.items()):
            setattr(self, key, value)
        self.blog_dir = os.path.expanduser(self.blog_dir)
        if date is None:
            # Figure out the date
            self.year = env.year
            self.month = env.month
            self.date = env.date
            self.month_name = env.month_name
            self.time = env.time
        else:
            self.time = date
            self.year = date[:4]
            self.month = date[4:6]
            self.date = date[6:]
            self.month_name = datetime.datetime.strptime(date, "%Y%m%d").strftime("%B")
        self.path = os.path.join(self.blog_dir, self.year, self.month_name)
        self.monthlist = ['January',
              'February',
              'March',
              'April',
              'May',
              'June',
              'July',
              'August',
              'September',
              'October',
              'November',
              'December']

    def show(self):
        print(self.time, self.year, self.month, self.date, self.month_name)

def write_blog(config):
    html = '../{}.html'.format(config.month_name)
    contents = []
    for fn in sorted(glob.glob(os.path.join(config.path, "*.notes")), reverse = True):
        runner = ParserCore([fn], 'html', 'short', 0)
        worker = Html('', '', '', False, 1, text_only = True)
        text = runner(worker)[0].strip().split('\n')
        # summary, date, text
        name = os.path.splitext(os.path.basename(fn))[0]
        contents.append((text[0][3:-4], '{}-{}-{}'.\
                              format(name[:4], name[4:6], name[6:]),
                              '\n'.join(text[1:])))
    links = []
    for item in config.monthlist:
        links.append((os.path.join('../', config.year, item + '.html'), item))
    page = BlogCSS(config.url, config.title, config.media_url, config.logo_img_name, config.background_img_name)
    with open(html, 'w') as f:
        f.write(page.GetMeta('Entries of {}, {}'.format(config.month_name, config.year)) + \
                page.GetLeftColumn('Entries of {}'.format(config.year), links) + \
                page.GetRightColumn(contents))
        
def upload_blog(config, user):
    with cd(config.path):
        write_blog(config)
    if not user:
        user = input("Username: ")
        passwd = getpass.getpass("Password: ")
        cmd = ("sshpass -p {} rsync -auzP {}/* {}@{} --include '*/' --include '*.html' --exclude '*' --delete".\
                  format(passwd, config.blog_dir, user, config.ssh_path))
        env.logger.debug(cmd)
    else:
        cmd = ("rsync -auzP {}/* {}@{} --include '*/' --include '*.html' --exclude '*' --delete".\
                  format(config.blog_dir, user, config.ssh_path))
        env.logger.debug(cmd)
    os.system(cmd)

def edit_blog(config):
    mkpath(config.path)
    if config.editor == 'gw-emacs':
        os.system('''emacsclient -c -F '((font . "Ubuntu Mono-14"))' -a 'emacs' {}.notes > /dev/null&'''.\
                  format(os.path.join(config.path, config.time)))
    else:
        os.system('{} {}.notes &'.format(config.editor, os.path.join(config.path, config.time)))
