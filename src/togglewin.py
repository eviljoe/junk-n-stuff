#!/usr/bin/env python3

import argparse
import shlex
import subprocess
import sys

from jnscommons import jnsos


def main():
    opts = _parse_args()
    _validate()
    _toggle_window(opts)


# ########################## #
# Argument Parsing Functions #
# ########################## #


def _parse_args():
    parser = argparse.ArgumentParser(description='Toggles widow visibility and focus.')
    
    # positional arguments
    parser.add_argument('win_cmd', default=None, help='The name of the command that opened the window')

    # optional arguments
    parser.add_argument('--dry-run', action='store_true', default=False, dest='dry_run',
                        help='Just output what actions will be peformed without actually performing them ' +
                        '(default:  %(default)s)')
    parser.add_argument('-H', '--hide-if-active', action='store_true', default=False, dest='hide_if_active',
                        help="Hide the window when it is the currently active window (default:  %(default)s)")
    parser.add_argument('-V', '--verbose', action='store_true', default=False, dest='verbose',
                        help="Print more information about the actions that are being taken (default:  %(default)s)")
    
    return parser.parse_args()


# #################### #
# Validation Functions #
# #################### #


def _validate():
    _validate_os()


def _validate_os():
    if not (jnsos.is_linux() or jnsos.is_cygwin()):
        raise OSError('Unsupported operating system: {}.  Only Linux and Cygwin are supported.'.format(jnsos.OS))


# ####################### #
# Window Toggle Functions #
# ####################### #


def _toggle_window(opts):
    command_win_id = _get_command_window_id(opts)
    active_win_id = _get_active_window_id(opts)
    
    if command_win_id == '':
        print('Player has no visible window.  Showing player.')
        _show_window(opts)
    elif command_win_id == active_win_id:
        print('Player is active.  Hiding window.')
        _hide_window(opts, command_win_id)
    else:
        print('Player has a visible window.  Moving window to front.')
        _move_window_to_front(opts, command_win_id)


def _hide_window(opts, win_id):
    _run_cmd(opts, ['xdotool', 'windowunmap', win_id])


def _show_window(opts):
    _run_cmd(opts, [opts.win_cmd])
    _move_window_to_front(opts, _get_command_window_id(opts))


def _move_window_to_front(opts, win_id):
    _run_cmd(opts, ['xdotool', 'windowactivate', win_id])


def _get_active_window_id(opts):
    return _run_cmd(opts, ['xdotool', 'getactivewindow'])


def _get_command_window_id(opts):
    return _run_cmd(opts, ['xdotool', 'search', '--onlyvisible', '--pid', _get_pid_of_command(opts)])


def _get_pid_of_command(opts):
    processes = _run_cmd(opts, ['ps', '-eo', 'pid,comm', '--no-headers'])
    
    # TODO tb
    print('start')
    for p in processes.splitlines():
        print(str(p.index(' ')) +  ' ' + p[p.index(' ') + 1:])
    print('end')
    # TODO eb
    
    process_line = _get_matching_process_line(opts, processes)
    
    if process_line is None:
        raise OSError('No process associated with the given window command: {}'.format(opts.win_cmd))
    
    return process_line[:process_line.index(' ') - 1]


def _get_matching_process_line(opts, processes):
    line = next((p for p in processes.splitlines() if _is_process_line_matching(opts, p)), None)
    return line.strip() if line else None


def _is_process_line_matching(opts, line):
    line = line.strip()
    return line[line.index(' ') + 1:] == opts.win_cmd


# ####################### #
# Shell Command Functions #
# ####################### #


def _run_cmd(opts, cmd):
    output = ''
    
    if opts.verbose:
        print('{}'.format(' '.join([shlex.quote(token) for token in cmd])), flush=True)
    
    if not opts.dry_run:
        popen = subprocess.Popen(cmd, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
        
        stdout, stderr = popen.communicate()
        output = stdout.decode('utf-8')
        error = stderr.decode('utf-8')
        
        exit_code = popen.poll()
    
    _verify_command_successful(exit_code, error)
    
    return output


def _verify_command_successful(exit_code, error):
    if exit_code != 0:
        print('subprocess unsuccessful. exit code: {}, error: {}'.format(exit_code, error), file=sys.stderr)
        raise ChildProcessError(error)


if __name__ == '__main__':
    main()
