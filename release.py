# $File: release.py $
# $LastChangedDate:  $
# $Rev:  $
# Copyright (c) 2012, Gao Wang <ewanggao@gmail.com>
# GNU General Public License (http://www.gnu.org/licenses/gpl.html)

import os
import sys
import subprocess
import shutil
import argparse
import zipfile
import platform
import time

PROJECT="tigernotes"

def ModifyVersion(version):
    if version is not None:
        with open('src/__init__.py', 'r') as init_file:
            content = init_file.readlines()
            new_content = ''.join(["VERSION='{0}'\n".format(version) if x.startswith('VERSION') else x for x in content])
        with open('src/__init__.py', 'w') as init_file:
            init_file.write(new_content)
    from src import VERSION
    return VERSION

def SetUpEnvironment(version):
    #
    if version.endswith('svn'):
        print('WARNING: You are releasing a subversion version.')
        print('To make a formal release, you will need to add an option --version=<VERSION>')
    #
    if os.path.isdir('dist'):
        shutil.rmtree('dist')
    with open("VERSION", 'w') as f:
        f.write("{0} version {1}, release {2}".format(PROJECT, version,
                                                      time.asctime( time.localtime(time.time()) )))

def GenerateSWIGWrappers():
    pass

def InstallPackage(extra_args):
    try:
        print('Building and installing {0} ...'.format(PROJECT))
        with open(os.devnull, 'w') as fnull:
            ret = subprocess.call('python setup.py install ' + ' '.join(extra_args), shell=True, stdout=fnull)
            if ret != 0:
                sys.exit('Failed to build and install {0}.'.format(PROJECT))
    except Exception as e:
        sys.exit('Failed to build and install {0}: {1}'.format(PROJECT, e))


def BuildSourcePackage(version):
    try:
        print('Building source package of {0} version {1} ...'.format(PROJECT, version))
        with open(os.devnull, 'w') as fnull:
            ret = subprocess.call('python setup.py sdist', shell=True, stdout=fnull)
            if ret != 0:
                sys.exit('Failed to build source package of {0}.'.format(PROJECT))
    except Exception as e:
        sys.exit('Failed to build source pacakge of {0}: {1}'.format(PROJECT, e))

def ObtainPyInstaller(pyinstaller_dir):
    # check if pyinstaller is available
    #   if not, use git clone to get it
    #   if yes, try to update to the newest version
    pyinstaller_dir = os.path.expanduser(pyinstaller_dir.rstrip('/'))
    if pyinstaller_dir.endswith('pyinstaller'): pyinstaller_dir = pyinstaller_dir[:-12]
    if not os.path.isdir(pyinstaller_dir): pyinstaller_dir = os.getcwd()
    git_dir = os.path.join(pyinstaller_dir, 'pyinstaller')
    curdir = os.getcwd()
    if not os.path.isdir(git_dir):
        try:
            print('Downloading pyinstaller...')
            with open(os.devnull, 'w') as fnull:
                ret = subprocess.call('git clone git://github.com/pyinstaller/pyinstaller.git {0}'.format(git_dir), shell=True, stdout=fnull)
                if ret != 0:
                    sys.exit('Failed to clone pyinstaller. Please check if you have git installed.'
                        'You can also get pyinstaller manually anf decompress it under the pyinstaller directory.')
        except Exception as e:
            sys.exit('Failed to clone pyinstaller: {0}'.format(e) + 
                'You can get pyinstaller manually anf decompress it under the pyinstaller directory '
                'if you are having trouble getting git installed.')
    else:
        os.chdir(git_dir)
        try:
            print('Updating pyinstaller ...')
            with open(os.devnull, 'w') as fnull:
                ret = subprocess.call('git pull', shell=True, stdout=fnull)
                if ret != 0:
                    print('Failed to get latest version of pyinstaller. Using existing version.')
        except Exception as e:
            print('Failed to get latest version of pyinstaller ({0}). Using existing version.'.format(e))
        os.chdir(curdir)
    return git_dir

def BuildExecutables(version, git_dir):
    # use py installer to create executable
    for exe in ['{0}'.format(PROJECT)]:
        try:
            print('Building executable {0} ...'.format(exe))
            with open(os.devnull, 'w') as fnull:
                ret = subprocess.call('python {0} -F --log-level=ERROR {1} '.format(os.path.join(git_dir, 'pyinstaller.py'), os.path.join(os.getcwd(),'src', exe)), shell=True, stdout=fnull)
                if ret != 0:
                    sys.exit('Failed to create executable for command {0}'.format(exe))
        except Exception as e:
            sys.exit('Failed to create executable for command {0}: {1}'.format(exe, e))
    # after the creation of commands, create a zip file with OS and version information
    zipfilename = os.path.join('dist', '{0}-{1}.{2}.{3}.zip'.format(PROJECT, 'stable', platform.system(), platform.machine()))
    print('Adding executables to file {0}'.format(zipfilename))
    with zipfile.ZipFile(zipfilename, 'w') as dist_file:
        cmd = '{0}.exe'.format(PROJECT) if os.name == 'win32' else PROJECT
        dist_file.write(os.path.join('dist', cmd), cmd)
    os.remove(os.path.join('dist', cmd))

def TagRelease(version):
    try:
        ret = subprocess.check_output(['svn', 'diff'], shell=True)
        if ret:
            sys.exit('Cannot tag release because there is uncommitted changes. Please commit the changes and try again.')
        with open(os.devnull, 'w') as fnull:
            print('Tagging release {0}...'.format(version))
            ret = subprocess.call('svn copy svn+ssh://wanggao@bioinformatics.org/svnroot/spower/trunk '
                'svn+ssh://wanggao@bioinformatics.org/svnroot/spower/trunk/tag/v{0} '
                ' -m "Version {1} released at {2}"'.format(version, version, time.asctime()),
                shell=True, stdout=fnull)
            if ret != 0:
                sys.exit('Failed to tag release {0}.'.format(version))
    except Exception as e:
        sys.exit('Failed to tag release {0}: {1}'.format(version, e))

def CleanUpEnvironment(purge):
    for item in ["MANIFEST", "{0}.spec".format(PROJECT)]:
        os.remove(item)
    if os.path.isdir('build') and purge:
        print('Removing directory build')
        shutil.rmtree('build')


if __name__ == '__main__':
    parser = argparse.ArgumentParser(description='''Create source distribution and executables for
        a variant tools release. In addition to optional parameters version and tag, extra parameters
        would be specified and will be passed directly to the 'python setup.py install' process. ''')
    parser.add_argument('--version',
        help='Modify source/__init__.py to the specified version string and make the release.')
    # parser.add_argument('--tag', action='store_true',
    #     help='If specified, tag this release')
    # parser.add_argument('--purge', action='store_true',
    #     help='If specified, remove build directory after installation')
    parser.add_argument('--pyinstaller_dir', default = '.',
        help='path to the directory where pyinstaller git clone is located.')
    # allow recognied parameters to be set to the build process
    args, argv = parser.parse_known_args()
    #
    version = ModifyVersion(args.version)
    SetUpEnvironment(version)
    GenerateSWIGWrappers()
    InstallPackage(argv)
    BuildSourcePackage(version)
    pyinstaller_dir = ObtainPyInstaller(args.pyinstaller_dir)
    BuildExecutables(version, pyinstaller_dir)
    # if everything is OK, tag the release
    # if args.tag:
    #     TagRelease(version)
    CleanUpEnvironment(True)
    # if everything is done
    print('Source packages and executables are successfully generated and saved to directory dist')
