#!/usr/bin/env python3


import argparse
import os.path
import sys
import textwrap

from jnscommons import jnsos
from jnscommons import jnsvalid
from uuulib import uuuconfig
from uuulib import uuupdate


def main():
    opts = parse_args()
    
    if not opts.no_config:
        read_config_file(opts)
        
    validate_opts(opts)
    uuupdate.update(opts)


def parse_args():
    parser = argparse.ArgumentParser(description='Update... all the things!', epilog=create_help_epilog(),
                                     formatter_class=argparse.RawDescriptionHelpFormatter)
    
    parser.add_argument('--atom', action='store_true', default=False, dest='atom',
                        help="Specify that Atom's packages should be updated (default: %(default)s)")
    parser.add_argument('--cabal', action='append', default=[], metavar='cabal_pkg', dest='cabal_packages',
                        help='Specify a cabal package to be updated')
    parser.add_argument('--choco', action='store_true', default=False, dest='choco',
                        help='Specify that all Chocolatey packages should be updated (default: %(default)s)')
    parser.add_argument('--dry-run', action='store_true', default=False, dest='dry_run',
                        help='Ouput what actions will be performed without taking them (default: %(default)s)')
    parser.add_argument('--cygwin', action='store', default=None, metavar='setup_exe', dest='cygwin_exe',
                        help="Specify the location of Cygwin's setup-x86.exe or setup-x86_64.exe")
    parser.add_argument('--git', action='append', default=[], metavar='git_repo', dest='git_dirs',
                        help='Specify a git reposotory to be updated')
    parser.add_argument('--gitd', action='append', default=[], metavar='git_repo_dir', dest='gitd_dirs',
                        help='Specify a directory that may contain one or more git reposotories to be updated')
    parser.add_argument('--init-jns', action='store_true', default=False, dest='init_jns',
                        help="Invoke `init-jns' from junk-n-stuff (default: %(default)s)")
    parser.add_argument('--no-config', action='store_true', default=False, dest='no_config',
                        help='Do not read the configuration file (default: %(default)s)')
    parser.add_argument('--pip', action='append', default=[], metavar='pip_pkg', dest='pip_packages',
                        help='Specify a pip package to be updated')
    parser.add_argument('--pip3', action='append', default=[], metavar='pip3_pkg', dest='pip3_packages',
                        help='Specify a pip3 package to be updated')
    parser.add_argument('--svn', action='append', default=[], metavar='svn_repo', dest='svn_dirs',
                        help='Specify an svn reposotory to be updated')
    parser.add_argument('--svnd', action='append', default=[], metavar='svn_repo_dir', dest='svnd_dirs',
                        help='Specify a directory that may contain one or more svn reposotories to be updated')
    parser.add_argument('--verbose', action='store_true', default=False, dest='verbose',
                        help='Adds more output (default: %(default)s)')
    
    opts = parser.parse_args()
    
    return opts


def create_help_epilog():
    e = []
    e.append('CONFIGURATION FILE')
    e.append('In addition to the command line arguments, a configuration file can be used to  specify the updates that '
             'should be made.  `{}\' will look for that file here:'.format(os.path.basename(sys.argv[0])))
    e.append('  {}'.format(get_default_config_file_name()))
    e.append('Each line of the file should be in the following format:')
    e.append('  <COMMAND> [ARGUMENT]')
    e.append('The comamnds are the same as their corresponding command line argument, but without the leading --.  For '
             'example, to specify a git repository:')
    e.append('  git ~/Documents/git/junk-n-stuff')
    e.append('For commands without an argument, just specify the command.  For example:')
    e.append('  atom')
    e.append('')
    e.append('CONFIGURATION FILE NOTES')
    e.append(' * Empty lines and lines containing only whitespace are ignored')
    e.append(' * Lines whose command starts with # are ignored')
    e.append(' * Whitespace before and after the command is ignored')
    e.append(' * Arguments can contain whitespace but cannot start with a whitespace character')
    e.append(' * Whitespace at the end of an argument will be considered to be part of that argument')
    
    return '\n'.join(['\n'.join(textwrap.wrap(line, width=80)) for line in e])


def read_config_file(opts):
    uuuconfig.read_config_file(opts, os.path.join(os.path.expanduser('~'), '.jns', 'uuu'))


def get_default_config_file_name():
    return os.path.join(os.path.expanduser('~'), '.jns', 'uuu')


def validate_opts(opts):
    jnsvalid.validate_is_directories(opts.git_dirs)
    jnsvalid.validate_is_directories(opts.gitd_dirs)
    jnsvalid.validate_is_directories(opts.svn_dirs)
    jnsvalid.validate_is_directories(opts.svnd_dirs)
    jnsvalid.validate_is_file(opts.cygwin_exe)
    validate_can_update_choco(opts)
    

def validate_can_update_choco(opts):
    if opts.choco and not (opts.dry_run or jnsos.is_windows() or jnsos.is_cygwin()):
        raise NotChocoOSError(
            'Can only update Chocolatey packages when in Windows, in Cygwin, or performing a dry run.')


def validate_can_init_jns(opts):
    if opts.init_jns and not opts.dry_run and jnsos.is_windows():
        raise NotInitJNSOSError('Cannot initialize junk-n-stuff when in Windows unless performing a dry run')


class NotChocoOSError(Exception):
    pass


class NotInitJNSOSError(Exception):
    pass


if __name__ == '__main__':
    main()
