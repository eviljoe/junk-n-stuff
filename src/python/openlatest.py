#!/usr/bin/env python3


import argparse
import os
import os.path
import platform
import subprocess
import sys


def main():
    opts = parse_args()
    validate_opts(opts)
    latest = get_latest_file(opts.directories, opts.include_hidden)
    
    if latest is None:
        print('No latest file.', file=sys.stderr)
    else:
        open_file(latest)
    

def parse_args():
    parser = argparse.ArgumentParser(description='Opens the most recently modified file in a directory.')
    
    parser.add_argument('-H', '--include-hidden', action='store_true', default=False, dest='include_hidden',
                        help='Include hidden files when looking for the last modified one (default:  %(default)s))')
    parser.add_argument('directories', nargs='*', metavar='directory', default=[],
                        help='Directory to look in for the most recent file (default: .)')
    
    opts = parser.parse_args()
    opts.directories = set([os.getcwd()]) if not opts.directories else set(opts.directories)
    
    return opts


def validate_opts(opts):
    for directory in opts.directories:
        if not os.path.exists(directory):
            raise FileNotFoundError('Directory does not exist: {}'.format(directory))
        elif not os.path.isdir(directory):
            raise NotADirectoryError('Directory is not a directory: {}'.format(directory))


def get_latest_file(directories, include_hidden):
    return max(get_files_in_directories(directories, include_hidden), key=os.path.getmtime, default=None)


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


def open_file(file_name):
    system = platform.system()
    systeml = system.lower()
    
    if systeml.startswith('linux'):
        open_file_subprocess('xdg-open', file_name)
    elif systeml.startswith('darwin'):
        open_file_subprocess('open', file_name)
    elif systeml.startswith('windows'):
        open_file_windows(file_name)
    else:
        raise UnsupportedOSError('Could not determine how to open a file for unsupported OS: {}'.format(system))

    
def open_file_windows(file_name):
    # pylint: disable=E1101
    # os.startfile(...) only exists in Windows
    return os.startfile(file_name)


def open_file_subprocess(cmd, file_name):
    return subprocess.Popen([cmd, file_name])


class UnsupportedOSError(Exception):
    pass


if __name__ == '__main__':
    main()
