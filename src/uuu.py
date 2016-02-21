#!/usr/bin/env python3


import argparse
import os

from jnsutils import jnsvutils
from uuulib import uuuconfig
from uuulib import uuupdate


def main():
    opts = parse_args()
    read_config_file(opts)
    validate_opts(opts)
    uuupdate.update(opts)


def parse_args():
    parser = argparse.ArgumentParser(description='Update... all the things!')
    
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


def read_config_file(opts):
    uuuconfig.UUUConfigFileReader(os.path.join(os.path.expanduser('~'), '.jns', 'uuu')).read_config_file(opts)


def validate_opts(opts):
    jnsvutils.validate_is_directories(opts.git_dirs)
    jnsvutils.validate_is_directories(opts.gitd_dirs)
    jnsvutils.validate_is_directories(opts.svn_dirs)
    jnsvutils.validate_is_directories(opts.svnd_dirs)


if __name__ == '__main__':
    main()
