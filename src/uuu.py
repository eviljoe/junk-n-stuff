#!/usr/bin/env python3


import argparse
import os.path
import sys
import textwrap

from jnsutils import jnsvutils
from uuulib import uuuconfig
from uuulib import uuupdate


def main():
    opts = parse_args()
    read_config_file(opts)
    validate_opts(opts)
    uuupdate.update(opts)


# In addition to the command line arguments, a configuration file can be used to specify the updates that
# should be made.  `uuu' will look for that file here:
#   ~/.jns/uuu
# Each line of the file should be in the following format:
#   <COMMAND> [ARGUMENT]
# For example, to specify a git repository:
#   git ~/Documents/git/junk-n-stuff
# For fommands without an argument, just specify the command.  For example:
#   atom


def parse_args():
    parser = argparse.ArgumentParser(description='Update... all the things!', epilog=create_help_epilog(),
                                     formatter_class=argparse.RawDescriptionHelpFormatter)
    
    parser.add_argument('--atom', action='store_true', default=False, dest='atom',
                        help='Specify that Atom\'s packages should be updated (default: %(default)s)')
    parser.add_argument('--dry-run', action='store_true', default=False, dest='dry_run',
                        help='Ouput what actions will be performed without taking them (default: %(default)s)')
    parser.add_argument('--git', action='append', default=[], metavar='GIT_REPO', dest='git_dirs',
                        help='Specify a git reposotory to be updated')
    parser.add_argument('--gitd', action='append', default=[], metavar='GIT_REPO_DIR', dest='gitd_dirs',
                        help='Specify a directory that may contain one or more git reposotories to be updated')
    parser.add_argument('--svn', action='append', default=[], metavar='SVN_REPO', dest='svn_dirs',
                        help='Specify an svn reposotory to be updated')
    parser.add_argument('--svnd', action='append', default=[], metavar='SVN_REPO_DIR', dest='svnd_dirs',
                        help='Specify a directory that may contain one or more svn reposotories to be updated')
    
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
    e.append(' * Empty lines and lines containing only whitespace are ignored.')
    e.append(' * Whitespace before and after the command is ignored')
    e.append(' * Arguments can contain whitespace but cannot start with a whitespace character')
    e.append(' * Whitespace at the end of an argument will be considered to be part of that argument')
    
    return '\n'.join(['\n'.join(textwrap.wrap(line, width=80)) for line in e])


def read_config_file(opts):
    uuuconfig.UUUConfigFileReader(os.path.join(os.path.expanduser('~'), '.jns', 'uuu')).read_config_file(opts)


def get_default_config_file_name():
    return os.path.join(os.path.expanduser('~'), '.jns', 'uuu')


def validate_opts(opts):
    jnsvutils.validate_is_directories(opts.git_dirs)
    jnsvutils.validate_is_directories(opts.gitd_dirs)
    jnsvutils.validate_is_directories(opts.svn_dirs)
    jnsvutils.validate_is_directories(opts.svnd_dirs)


if __name__ == '__main__':
    main()
