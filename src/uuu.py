#!/usr/bin/env python3


import argparse
import os.path
import sys
import textwrap

from uuulib import uuuconfig
from uuulib import uuurunner
from uuulib.updaters import atom
from uuulib.updaters import cabal
from uuulib.updaters import choco
from uuulib.updaters import cygwin
from uuulib.updaters import git
from uuulib.updaters import gitd
from uuulib.updaters import initjns
from uuulib.updaters import pip
from uuulib.updaters import pip3
from uuulib.updaters import svn
from uuulib.updaters import svnd


UPDATERS = [
    svn.SVNUpdater(),
    svnd.SVNDUpdater(),
    git.GitUpdater(),
    gitd.GitdUpdater(),
    initjns.InitJNSUpdater(),
    pip.PipUpdater(),
    pip3.PipUpdater(),
    cabal.CabalUpdater(),
    choco.ChocoUpdater(),
    cygwin.CygwinUpdater(),
    atom.AtomUpdater()
]


def main():
    opts = parse_args()
    
    if not opts.no_config:
        read_config_file(opts)
        
    validate_opts(opts)
    update(opts)


def parse_args():
    parser = argparse.ArgumentParser(description='Update... all the things!', epilog=create_help_epilog(),
                                     formatter_class=argparse.RawDescriptionHelpFormatter)

    for updater in UPDATERS:
        updater.add_help_argument(parser)
    
    parser.add_argument('--dry-run', action='store_true', default=False, dest='dry_run',
                        help='Ouput what actions will be performed without taking them (default: %(default)s)')
    parser.add_argument('--no-config', action='store_true', default=False, dest='no_config',
                        help='Do not read the configuration file (default: %(default)s)')
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
    uuuconfig.read_config_file(updaters=UPDATERS, opts=opts,
                               config_file_name=os.path.join(os.path.expanduser('~'), '.jns', 'uuu'))


def get_default_config_file_name():
    return os.path.join(os.path.expanduser('~'), '.jns', 'uuu')


def validate_opts(opts):
    for updater in UPDATERS:
        updater.validate_opts(opts)


def update(opts):
    runner = uuurunner.UUURunner()
    
    for updater in UPDATERS:
        updater.update(opts=opts, runner=runner)


if __name__ == '__main__':
    main()
