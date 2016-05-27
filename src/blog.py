#!/usr/bin/env python3
# -*- coding: utf-8 -*-
import os, glob, re, yaml, getpass, datetime
from distutils.dir_util import mkpath
from subprocess import check_output
from .parser import ParserCore
from .encoder import Html
from .style import BlogCSS
from .utils import env, cd, dict2str
from pysos import SoS_Script
from pysos.sos_executor import Sequential_Executor as SE

class BlogCFG:
    def __init__(self, config_file, date, post):
        d = yaml.load(open(os.path.expanduser(config_file)))
        for key in ['editor', 'blog_dir', 'blog_namespace', 'url', 'journal_path', 'blog_path',
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
    if fn.endswith('.notes'):
        fn = fn[:-6]
    env.logger.info("Editing ``{}.notes``".format(fn.replace(os.path.expanduser('~'), '~')))
    if config.editor == 'gw-emacs':
        os.system('''emacsclient -c -a 'emacs' {}.notes > /dev/null&'''.format(fn))
    else:
        os.system('{} {}.notes &'.format(config.editor, fn))

#
# Compile journal
#

def write_journal(config):
    html = '../{}.html'.format(config.month_name)
    contents = []
    for fn in sorted(glob.glob(os.path.join(config.path, "{}{}*.notes".format(config.year, config.month))),
                     reverse = True):
        runner = ParserCore([fn], 'html', 'short', 0, 0)
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

#
# Index blog
#

def get_private_posts(config):
    res = []
    for key, item in config.posts.items():
        if 'args' in item and '--permission' in item['args'].split():
            res.append('{}:{}'.format(item['date'][:6], key[1]))
    return res

def list2ndict(x, d, tail = 2):
    current_level = d
    for idx, part in enumerate(x):
        if part not in current_level:
            current_level[part] = {}
        if idx < (len(x) - tail - 1):
            current_level = current_level[part]
        else:
            if type(current_level[part]) is dict:
                current_level[part] = []
            current_level[part].append(x[-tail:])
            break

class TitleParser:
    def __init__(self, config):
        self.mark = '===='
        self.titlemap = {1:'###\n#!?????\n###', 2:'###\n#?????\n###', 3:'#!?????', 4:'#!!?????', 5:'#!!!?????'}
        self.top_sections = []
        self.config = config

    def ndict2notes(self, fout, d, level = 1):
        def fprint(i):
            fout.write('#{list\n')
            for ii in sorted(i):
                fout.write('#[{}|@{}:{}@]\n'.format(ii[0], self.config.blog_namespace, ii[1]))
            fout.write('#}\n')
        #
        keys = sorted(list(d.keys()), reverse = True) if all([x.isdigit() for x in list(d.keys()) if x.lower() not in self.top_sections]) else sorted(d.keys())
        for key in keys:
            if key == '209912':
                text = 'Pinned'
            else:
                text = key
            fout.write(self.titlemap[level].replace('?????', text.capitalize()) + '\n')
            if type(d[key]) is dict:
                self.ndict2notes(fout, d[key], level + 1)
            else:
                fprint(d[key])

    def GetTitles(self):
        self.titles = []
        for f in glob.glob('{}/20*/*/[!20]*.txt'.format(self.config.blog_dir)):
            cmd = 'grep "^{}" {}'.format(self.mark, f)
            year, month, name = f.split('/')[-3:]
            name = os.path.splitext(name)[0]
            month = self.config.monthlist.index(month) + 1
            month = '0{}'.format(month) if month < 10 else str(month)
            self.titles.append('{}{}:{}::{}'.format(year, month, name, check_output(cmd, shell=True).decode('utf-8').split('\n')[0]))

    def ParseTitles(self, exclude, private_posts):
        self.titles_private = {}
        self.titles_public = {}
        for item in self.titles:
            item = item.split('::')
            if item[0] in exclude:
                continue
            month, file_name = item[0].split(':')
            # dat = ("{} {}".format(self.config.monthlist[int(month[4:6]) - 1], month[:4]),
            #        re.sub(r'^(=+)|(=+)$', '', item[1]).strip(), item[0])
            dat = (month, re.sub(r'^(=+)|(=+)$', '', item[1]).strip(), item[0])
            if item[0] in private_posts:
                list2ndict(dat, self.titles_private)
            else:
                list2ndict(dat, self.titles_public)

    def WriteTitles(self, outfile):
        with open(outfile, 'w') as f:
            f.write('#{raw\n')
            f.write('<ifauth !gw>\nEntries are only visible to authorized members. Please login if you are one of them.\n</ifauth>\n<ifauth gw>\n')
            f.write('#}\n')
            f.write('###\n#!Public Posts\n###\n')
            self.ndict2notes(f, self.titles_public, level = 2)
            f.write('###\n#!Private Posts\n###\n')
            self.ndict2notes(f, self.titles_private, level = 2)
            f.write('#{$</ifauth>$}\n')

def update_blog_meta(config, exclude):
    private_posts = get_private_posts(config)
    tp = TitleParser(config)
    tp.GetTitles()
    tp.ParseTitles(exclude, private_posts)
    tp.WriteTitles(os.path.join(env.tmp_dir, 'blog.notes'))
    os.system('labnotes dokuwiki {} -o {} --compact_toc'.format(os.path.join(env.tmp_dir, 'blog.notes'),
                                                                os.path.join(config.blog_dir, 'blog.txt')))

#
# Compile blog
#

def upload_blog(config, user, args):
    if config.post == (None, None):
        return
    if len(args) == 0 or '-o' not in args:
        output = config.post[1]
    else:
        output = args.pop(args.index('-o') + 1)
        args.pop(args.index('-o'))
    # update post index
    flag = (config.post[0], output) not in config.posts
    if output != config.post[1]:
        config.posts[config.post[0], output] = {}
    config.posts[config.post[0], output]['date'] = config.time if config.post not in config.posts else \
                                                   config.posts[config.post]['date']
    if len(args) > 1:
        # overwrite args
        config.posts[config.post[0], output]['args'] = ' '.join(args)
    elif config.post in config.posts and 'args' in config.posts[config.post]:
        config.posts[config.post[0], output]['args'] = config.posts[config.post]['args']
    if output != config.post[1] and config.post in config.posts:
        # same post, new output
        env.logger.info('Post ``{}/{}`` is obsolete. Please manually delete it from ``{}``!'.\
                        format(config.posts[config.post]['date'], config.post[1], config.blog_dir))
        exclude = "{}:{}".format(config.posts[config.post]['date'], config.post[1])
        del config.posts[config.post]
        flag = True
    else:
        exclude = None
    # compile doc
    script = "[1]\ninput: '{}.notes'\noutput: '{}.txt'\ntask: workdir = '{}'\nrun:\n{}".\
             format(os.path.join(config.blog_dir, config.year, config.month_name, config.post[0]),
                    os.path.join(config.blog_dir, config.year, config.month_name, output),
                    config.blog_dir,
                    'labnotes dokuwiki {}.notes -o {}.txt {}'.\
                    format(os.path.join(config.year, config.month_name, config.post[0]),
                           os.path.join(config.year, config.month_name, output),
                           (config.posts[config.post[0], output]['args']
                            if 'args' in config.posts[config.post[0], output] else '').replace('@', "\\@")))
    SE(SoS_Script(script).workflow()).run()
    # update toc
    if flag:
        update_blog_meta(config, [exclude])
    # upload doc
    if not user:
        user = input("Username: ")
        passwd = getpass.getpass("Password: ")
        cmd = ("sshpass -p {0} rsync -auzP --rsync-path='mkdir -p {6}/{5} && rsync' {1}/{2}.txt "\
               "{3}@{4}/{5}/{7}.txt; ".\
               format(passwd, config.blog_dir, os.path.join(config.year, config.month_name, output),
                      user, config.blog_path, config.time[:6], config.blog_path.split(':')[1], output))
        if flag:
            cmd += ("sshpass -p {} scp {}/blog.txt {}@{}.txt".format(passwd, config.blog_dir, user, config.blog_path))
    else:
        cmd = ("rsync -auzP --rsync-path='mkdir -p {5}/{4} && rsync' {0}/{1}.txt {2}@{3}/{4}/{6}.txt; ".\
                  format(config.blog_dir, os.path.join(config.year, config.month_name, output),
                         user, config.blog_path, config.time[:6], config.blog_path.split(':')[1], output))
        if flag:
            cmd += ("scp {}/blog.txt {}@{}.txt".format(config.blog_dir, user, config.blog_path))
    env.logger.debug(cmd)
    os.system(cmd)
    if os.path.isfile(os.path.join(config.blog_dir, 'blog.txt')):
        os.remove(os.path.join(config.blog_dir, 'blog.txt'))
    # All good, update posts.yml
    with open(config.blog_index, 'w') as f:
        f.write(dict2str(config.posts))
