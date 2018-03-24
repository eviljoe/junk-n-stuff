#!/usr/bin/env python3

import argparse
import os
import os.path
import shlex
import subprocess
import sys

from jnscommons import jnsstr


# ######### #
# Constants #
# ######### #


DEFAULT_EDITOR = 'vim'

NO_ERROR = 0
ERR_CHEATSHEET_NOT_FOUND = 2


# #### #
# Main #
# #### #


def main():
    sys.exit(_perform_action(_parse_opts()))


# ########################## #
# Argument Parsing Functions #
# ########################## #


def _parse_opts():
    parser = argparse.ArgumentParser(description='View cheatsheets', epilog=_create_help_epilog(),
                                     formatter_class=argparse.RawDescriptionHelpFormatter)

    # positional arguments
    parser.add_argument('cheatsheet', nargs='?', metavar='cheatsheet', default='',
                        help='The cheatsheet to be viewed')

    # optional arguments
    parser.add_argument('-l', '--list', action='store_true', default=False, dest='list_cheatsheets',
                        help='List the available cheatsheets (default:  %(default)s)')
    parser.add_argument('-p', '--list-path', action='store_true', default=False, dest='list_paths',
                        help='Display the paths that will be searched to find the cheatsheets (default:  %(default)s)')

    return parser.parse_args()


def _create_help_epilog():
    e = []
    e.append('PATH')
    e.append('The cheatsheets that can be viewed are are searched for using on one or more paths.  The following ')
    e.append('directory will always be one of the paths:')
    e.append('  {}'.format(_get_jns_cheatsheets_path()))
    e.append('The configuration file should be used to specify additional paths.  If the requested cheatsheet is ')
    e.append('contained in more than one path, the cheatsheet in the first path found will be used.')
    e.append('')
    e.append('CONFIGURATION FILE')
    e.append('A configuration file can be used to  specify paths that will be searched in order to find the '
             ' cheatsheets be made.  `{}\' will look for that file here:'.format(os.path.basename(sys.argv[0])))
    e.append('  {}'.format(_get_config_file_name()))
    e.append('Each line of the file should contain a single path.')
    e.append('')
    e.append('CONFIGURATION FILE NOTES')
    e.append(' * Empty lines and lines containing only whitespace are ignored')
    e.append(' * Lines that start with # are ignored')
    e.append(' * Whitespace before and after the path is ignored')
    e.append(' * Paths can contain whitespace but cannot start or end with a whitespace character')
    e.append(' * The paths will be searched for the requested cheatsheet in the order that they are specified')
    e.append(' * The default path will be searched first')

    return jnsstr.wrap_str_array(e)


# ################ #
# Action Functions #
# ################ #


def _perform_action(opts):
    err = NO_ERROR

    if opts.list_cheatsheets:
        err = _perform_list_cheatsheets()
    elif opts.list_paths:
        err = _perform_list_paths()
    else:
        err = _perform_view_cheatsheet(opts)

    return err


def _perform_list_cheatsheets():
    for path in _get_paths():
        print('\n'.join(_get_cheatsheets_in_path(path)))

    return NO_ERROR


def _is_cheatsheet_file(path, file_name):
    return os.path.isfile(os.path.join(path, file_name)) and not file_name.startswith('.')


def _perform_list_paths():
    print('\n'.join(_get_paths()))
    return NO_ERROR


def _perform_view_cheatsheet(opts):
    err = NO_ERROR
    path, file_name = next(
        ((p, f) for p in _get_paths() for f in os.listdir(p) if _is_requested_cheatsheet(opts, p, f)),
        (None, None)
    )

    if path and file_name:
        err = _launch_cheatsheet_in_editor(path, file_name)
    else:
        print('Cheatsheet not found in any paths:\n{}'.format('\n'.join(_get_paths())), file=sys.stderr)
        err = ERR_CHEATSHEET_NOT_FOUND

    return err

# ############################## #
# Cheatsheet Launching Functions #
# ############################## #


def _launch_cheatsheet_in_editor(path, cheatsheet_file):
    cmd = _get_editor_command()
    cmd.append(os.path.join(path, cheatsheet_file))

    return subprocess.call(cmd)


def _is_requested_cheatsheet(opts, path, file_name):
    return _is_cheatsheet_file(path, file_name) and (
        opts.cheatsheet == file_name or
        opts.cheatsheet == os.path.splitext(file_name)[0]
    )


# ############## #
# Path Functions #
# ############## #


def _get_paths():
    paths = []

    paths.append(_get_jns_cheatsheets_path())
    paths.extend(_get_config_file_paths())

    return paths


def _get_jns_cheatsheets_path():
    return os.path.normpath(os.path.join(
        os.path.dirname(os.path.realpath(sys.argv[0])),
        '..',
        'cheatsheets'
    ))


def _get_config_file_paths():
    config_file_name = _get_config_file_name()
    paths = []

    if os.path.exists(config_file_name):
        with open(config_file_name, encoding='utf-8') as config_file:
            paths = _read_config_file_paths(config_file)

    return paths


def _get_config_file_name():
    return os.path.join(_get_home_dir(), '.jns', 'cheat')


def _read_config_file_paths(config_file):
    paths = []

    for line in config_file.readlines():
        path = _get_path_from_config_line(line)

        if path:
            paths.append(path)

    return paths


def _get_path_from_config_line(line):
    path = None
    line = line.strip()

    if len(line) > 0 and line[0] != '#':
        path = _normalize_home_dir(line)

    return path


def _get_cheatsheets_in_path(path):
    return [f for f in os.listdir(path) if _is_cheatsheet_file(path, f)]


# ####################### #
# Misc. Utility Functions #
# ####################### #


def _normalize_home_dir(directory):
    if directory == '~' or directory.startswith('~/') or directory.startswith('~\\'):
        directory = _get_home_dir() + directory[1:]

    return directory


def _get_home_dir():
    return os.path.expanduser('~')


def _get_editor_command():
    return shlex.split(os.environ.get('EDITOR', DEFAULT_EDITOR))


if __name__ == '__main__':
    main()
