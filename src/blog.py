#!/usr/bin/env python3
# -*- coding: utf-8 -*-
import os, glob, yaml, getpass, datetime
from distutils.dir_util import mkpath
from .parser import ParserCore
from .encoder import Html
from .style import BlogCSS
from .utils import env, cd, dict2str
from pysos import SoS_Script
from pysos.sos_executor import Sequential_Executor as SE

class BlogCFG:
    def __init__(self, config_file, date, post):
        d = yaml.load(open(os.path.expanduser(config_file)))
        for key in ['editor', 'blog_dir', 'url', 'journal_path', 'blog_path',
                    'title', 'logo_img_name', 'background_img_name', 'media_url']:
            if key not in d:
                raise ValueError('Cannot find required key ``{}`` in ``{}``!'.format(key, config_file))
        for key, value in list(d.items()):
            setattr(self, key, value)
        self.blog_dir = os.path.expanduser(self.blog_dir)
        self.blog_index = self.blog_dir + '/posts.yml'
        if not os.path.isfile(self.blog_index):
            with open(self.blog_index, 'w') as f:
                f.write(dict2str({}))
        self.posts = yaml.load(open(self.blog_index))
        self.post = (post, post)
        for key in self.posts:
            if post in key:
                date = self.posts[key]['date']
                self.post = key
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

def edit_blog(config):
    mkpath(config.path)
    fn = os.path.join(config.path, config.time if config.post == (None, None) else config.post[0])
    if config.editor == 'gw-emacs':
        os.system('''emacsclient -c -a 'emacs' {}.notes > /dev/null&'''.format(fn))
    else:
        os.system('{} {}.notes &'.format(config.editor, fn))

def write_journal(config):
    html = '../{}.html'.format(config.month_name)
    contents = []
    for fn in sorted(glob.glob(os.path.join(config.path, "{}{}*.notes".format(config.year, config.month))),
                     reverse = True):
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
    page = BlogCSS(config.url, config.title, config.media_url, config.logo_img_name,
                   config.background_img_name)
    with open(html, 'w') as f:
        f.write(page.GetMeta('Entries of {}, {}'.format(config.month_name, config.year)) + \
                page.GetLeftColumn('Entries of {}'.format(config.year), links) + \
                page.GetRightColumn(contents))

def upload_journal(config, user):
    with cd(config.path):
        write_journal(config)
    if not user:
        user = input("Username: ")
        passwd = getpass.getpass("Password: ")
        cmd = ("sshpass -p {} rsync -auzP {}/* {}@{} --include '*/' --include '*.html' --exclude '*' --delete".\
                  format(passwd, config.blog_dir, user, config.journal_path))
    else:
        cmd = ("rsync -auzP {}/* {}@{} --include '*/' --include '*.html' --exclude '*' --delete".\
                  format(config.blog_dir, user, config.journal_path))
    env.logger.debug(cmd)
    os.system(cmd)


def upload_blog(config, user, args):
    if config.post == (None, None):
        return
    if len(args) == 0 or '-o' not in args:
        output = config.post[1]
    else:
        output = args.pop(args.index('-o') + 1)
        args.pop(args.index('-o'))
    # update post index
    if output != config.post[1]:
        config.posts[config.post[0], output] = {}
        config.posts[config.post[0], output]['date'] = config.time
    if len(args) > 1:
        config.posts[config.post[0], output]['args'] = args[1:]
    elif 'args' in config.posts[config.post]:
        config.posts[config.post[0], output]['args'] = config.posts[config.post]['args']
    # compile doc
    with cd(config.blog_dir):
        script = "[1]\ninput: '{}.notes'\noutput: '{}.txt'\nrun:\n{}".\
                 format(os.path.join(config.year, config.month_name, config.post[0]),
                        os.path.join(config.year, config.month_name, output),
                        'labnotes dokuwiki ${{input}} -o ${{output}} {}'.\
                        format((config.posts[config.post[0], output]['args']
                               if 'args' in config.posts[config.post[0], output]
                                else '').replace('@', "\\@")))
        SE(SoS_Script(script).workflow()).run()
    # upload doc
    if not user:
        user = input("Username: ")
        passwd = getpass.getpass("Password: ")
        cmd = ("sshpass -p {0} rsync -auzP --rsync-path='mkdir -p {6}/{5} && rsync' {1}/{2}.txt "\
               "{3}@{4}/{5}/{7}.txt ".\
               format(passwd, config.blog_dir, os.path.join(config.year, config.month_name, output),
                      user, config.blog_path, config.time[:6], config.blog_path.split(':')[1], output))
    else:
        cmd = ("rsync -auzP --rsync-path='mkdir -p {5}/{4} && rsync' {0}/{1}.txt {2}@{3}/{4}/{6}.txt ".\
                  format(config.blog_dir, os.path.join(config.year, config.month_name, output),
                         user, config.blog_path, config.time[:6], config.blog_path.split(':')[1], output))
    env.logger.debug(cmd)
    os.system(cmd)
    # All good, update posts.yml
    if output != config.post[1]:
        del config.posts[config.post]
    with open(config.blog_index, 'w') as f:
        f.write(dict2str(config.posts))
