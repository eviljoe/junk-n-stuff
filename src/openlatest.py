#!/usr/bin/env python3

import argparse
import itertools
import os
import os.path
import shlex
import subprocess
import sys

from jnscommons import jnsos
from jnscommons import jnsvalid


KEY_BY_MOD_TIME = 'latest-by-mod-time'
KEY_BY_NAME = 'latest-by-name'

OPEN_COMMANDS = {
    jnsos.OS_PREFIX_LINUX: ['xdg-open'],
    jnsos.OS_PREFIX_CYGWIN: ['cygstart'],
    jnsos.OS_PREFIX_DARWIN: ['open'],
    jnsos.OS_PREFIX_WINDOWS: ['start', '/b']
}


def main():
    opts = parse_args()
    validate_opts(opts)
    latest = get_latest_file(opts.directories, opts.include_hidden, opts.key)
    
    if latest is None:
        print('No latest file.', file=sys.stderr)
    else:
        open_file(opts, latest)
    

def parse_args():
    parser = argparse.ArgumentParser(description='Opens the most recently modified file in a directory.')
    
    # positional arguments
    parser.add_argument('directories', nargs='*', metavar='directory', default=[],
                        help='Directory to look in for the most recent file (default: .)')

    # optional arguments
    parser.add_argument('--dry-run', action='store_true', default=False, dest='dry_run',
                        help='Just output what actions will be peformed without actually performing them ' +
                        '(default:  %(default)s)')
    parser.add_argument('-H', '--include-hidden', action='store_true', default=False, dest='include_hidden',
                        help='Include hidden files when looking for the last modified one (default:  %(default)s)')
    parser.add_argument('-m', '--mtime', action='store_const', const=KEY_BY_MOD_TIME, dest='key',
                        help="find the latest using each file's modification time (default)")
    parser.add_argument('-n', '--name', action='store_const', const=KEY_BY_NAME, dest='key',
                        help="find the latest using each file's basename (case insensitive)")
    parser.add_argument('-o', '--os', action='store', default=get_default_os(), metavar='OS', dest='os',
                        help='Specify the operating system.  Can only be used during dry runs. (default:  %(default)s)')
    
    opts = parser.parse_args()
    opts.directories = set([os.getcwd()]) if not opts.directories else set(opts.directories)
    opts.key = KEY_BY_MOD_TIME if not opts.key else opts.key
    
    return opts


def validate_opts(opts):
    jnsvalid.validate_is_directories(opts.directories)
    
    if not opts.dry_run and opts.os and opts.os.lower() != get_default_os().lower():
        raise NotDryRunError('Cannot specify an OS unless performing a dry run.')


def get_latest_file(directories, include_hidden, key):
    if key == KEY_BY_MOD_TIME:
        key_fn = os.path.getmtime
    elif key == KEY_BY_NAME:
        key_fn = get_lower_basename
    else:
        raise UnsupportedKeyError('Could not the latest file for unsupported key: {}'.format(key))
    
    return max(get_files_in_directories(directories, include_hidden), key=key_fn, default=None)


def get_files_in_directories(directories, include_hidden):
    for directory in directories:
        for file_name in os.listdir(path=directory):
            file_name = os.path.join(directory, file_name)
            
            if should_check_file(file_name, include_hidden):
                yield file_name


def should_check_file(file_name, include_hidden):
    check = True if include_hidden else not os.path.basename(file_name)[0] == '.'
    check = check and os.path.isfile(file_name)
    return check


def get_lower_basename(file):
    return os.path.basename(file).lower()


def get_os(opts):
    return get_default_os() if opts.os is None or len(opts.os) == 0 else opts.os


def get_default_os():
    return jnsos.OS


def open_file(opts, file_name):
    op_sys = get_os(opts)
    open_cmd = get_open_command(op_sys)
    
    if open_cmd is None:
        raise UnsupportedOSError('Could not determine how to open a file for unsupported OS: {}'.format(op_sys))
    else:
        start_open_file_subprocess(opts, open_cmd, file_name)
    

def get_open_command(op_sys):
    key = next((k for k in OPEN_COMMANDS.keys() if jnsos.is_os(k, os=op_sys)), None)
    return None if key is None else OPEN_COMMANDS[key]


def start_open_file_subprocess(opts, cmd, file_name):
    cmds = list(itertools.chain(cmd, [file_name]))
    
    print(get_shell_command(cmds))
    
    return None if opts.dry_run else subprocess.Popen(cmds)


def get_shell_command(parts):
    return '' if parts is None else ' '.join([shlex.quote(part) for part in parts])


##########
# Errors #
##########


class UnsupportedOSError(Exception):
    pass


class UnsupportedKeyError(Exception):
    pass


class NotDryRunError(Exception):
    pass


if __name__ == '__main__':
    main()
