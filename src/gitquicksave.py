#!/usr/bin/env python3

import argparse
import re
import sys

from jnscommons import jnsgit

#############
# Constants #
#############


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
    jnsgit.stage_all(dry_run=opts.dry_run, print_cmd=True)
    print()


########################
# Git Commit Functions #
########################


def _git_commit_next(opts):
    exit_code = jnsgit.commit(msg=_get_commit_msg(), dry_run=opts.dry_run, print_cmd=True, strict=False)

    if exit_code != 0:
        raise ExitCodeError('Commit failed', exit_code)


def _get_commit_msg():
    branch = _get_branch()
    last_commit_msg = jnsgit.last_commit_msg()

    if _can_increment_commit(last_commit_msg, branch):
        commit_msg = _get_incremented_commit_msg(last_commit_msg, branch)
    else:
        commit_msg = _get_numbered_commit_msg(branch, 1)

    commit_msg = commit_msg.strip()
    if not commit_msg:
        raise ExitCodeError('Cannot determine quick save commit message from last: {}'.format(last_commit_msg))

    return commit_msg


def _get_branch():
    branch = jnsgit.branch_name()

    if branch == 'master':
        raise ExitCodeError('Do not auto commit to master!')

    return branch


def _can_increment_commit(last_commit_msg, branch):
    return last_commit_msg.startswith(branch) or _is_truncated_commit_msg(last_commit_msg, branch)


def _is_truncated_commit_msg(msg, branch):
    truncated = False

    if len(msg) == _MAX_GIT_SUBJECT_LENGTH:
        regex = re.compile('\.\.\. [0-9]+$')
        match = regex.search(msg)

        if match:
            untruncated_msg = msg[0:match.start()]
            truncated = branch != untruncated_msg and branch.startswith(untruncated_msg)

    return truncated


def _get_incremented_commit_msg(last_commit_msg, branch):
    last_number = int(last_commit_msg.split()[-1])
    return _get_numbered_commit_msg(branch, last_number + 1)


def _get_numbered_commit_msg(branch, number):
    number_str = str(number)
    max_len = _MAX_GIT_SUBJECT_LENGTH - len(number_str) - 1
    return truncate(branch, max_len) + ' ' + number_str


def truncate(str, length):
    str_len = len(str)
    over_by = str_len - length

    if over_by > 0:
        str = str[0:str_len - over_by - 3] + '...'

    return str


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
