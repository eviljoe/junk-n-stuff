#!/usr/bin/env python3

import argparse
import re
import shlex
import subprocess
import sys


#############
# Constants #
#############


_DIM = '\033[2m'
_PLAIN = '\033[0m'
_MAX_GIT_SUBJECT_LENGTH = 50


###############
# Main Method #
###############


def main():
    exit_code = 0

    try:
        opts = parse_args()
        _git_stage_all(opts)
        _git_commit_next(opts)
    except ExitCodeError as e:
        exit_code = e.exit_code
        print(str(e), file=sys.stderr, flush=True)

    sys.exit(exit_code)


#######################
# Git Stage Functions #
#######################


def parse_args():
    parser = argparse.ArgumentParser(description='Create a commit with a throwaway message')

    parser.add_argument('--dry-run', action='store_true', default=False, dest='dry_run',
                        help='Output what actions will be performed without taking them (default: %(default)s)')

    return parser.parse_args()


#######################
# Git Stage Functions #
#######################


def _git_stage_all(opts):
    _call(opts, ['git', 'add', '--all'])


########################
# Git Commit Functions #
########################


def _git_commit_next(opts):
    _call(opts, ['git', 'commit', '--message', _get_commit_msg()])


def _get_commit_msg():
    branch = _get_branch()
    last_commit_msg = _get_last_commit_msg()
    commit_msg = ''

    if last_commit_msg.startswith(branch):
        commit_msg = _get_commit_msg_from_last(last_commit_msg)
    else:
        commit_msg = '{} 1'.format(branch)

    commit_msg = commit_msg.strip()
    if not commit_msg:
        raise ExitCodeError('Cannot auto-increment commit message from last: {}'.format(last_commit_msg))

    return commit_msg


def _get_branch():
    branch = _check_output(['git', 'rev-parse', '--abbrev-ref', 'HEAD'])

    if branch == 'master':
        raise ExitCodeError('Do not auto commit to master!')

    return branch


def _get_last_commit_msg():
    return _check_output(['git', 'log', '--format=%s', '-1'])


def _get_commit_msg_from_last(last_commit_msg):
    last_commit_msg_parts = last_commit_msg.split()
    last_commit_index = last_commit_msg_parts[-1]
    commit_msg = ''

    if re.match('[0-9]+', last_commit_index):
        commit_msg = _get_commit_msg_from_msg_and_index(
            ' '.join(last_commit_msg_parts[0:-1]),
            int(last_commit_index) + 1
        )

    return commit_msg


def _get_commit_msg_from_msg_and_index(msg, index):
    msg_len = len(msg)
    over_by = (msg_len + len(str(index)) + 1) - _MAX_GIT_SUBJECT_LENGTH

    if over_by > 0:
        msg = msg[0:msg_len - over_by - 3] + '...'

    return msg + ' ' + str(index)


#####################
# Utility Functions #
#####################


def _call(opts, cmd):
    _print_command(cmd)
    exit_code = 0

    if not opts.dry_run:
        exit_code = subprocess.call(cmd)

    return exit_code


def _check_output(cmd):
    return subprocess.check_output(cmd).decode('utf-8').strip()


def _print_command(cmd):
    print(_DIM + ' '.join([shlex.quote(part) for part in cmd]) + _PLAIN, flush=True)


###################
# Exit Code Error #
###################


class ExitCodeError(Exception):
    def __init__(self, message, exit_code=1):
        super().__init__(message)
        self.exit_code = exit_code


##############
# Main Check #
##############


if __name__ == '__main__':
    main()
