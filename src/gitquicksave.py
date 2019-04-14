#!/usr/bin/env python3

import argparse
import re
import sys

from jnscommons import jnsgit

#############
# Constants #
#############


_DEFAULT_REPOSITORY = 'origin'
_MAX_GIT_SUBJECT_LENGTH = 50

###############
# Main Method #
###############


def main():
    exit_code = 0

    try:
        opts = parse_args()
        quicksave(opts)
    except ExitCodeError as e:
        exit_code = e.exit_code
        print(str(e), file=sys.stderr, flush=True)

    sys.exit(exit_code)


def quicksave(opts):
    if opts.stage:
        _git_stage_all(opts)
        print()

    _git_commit_next(opts)

    if opts.push or opts.push_upstream:
        print()
        _git_push(opts, opts.push_upstream)


########################
# CLI Option Functions #
########################


def parse_args():
    parser = argparse.ArgumentParser(description='Create a commit with a throwaway message')

    parser.add_argument('--dry-run', action='store_true', default=False, dest='dry_run',
                        help='Output what actions will be performed without taking them (default: %(default)s)')
    parser.add_argument('--no-stage', action='store_false', default=True, dest='stage',
                        help='Do not stage any files before committing (default: stage before committing)')
    parser.add_argument('--number', action='store', default=None, dest='number',
                        help='Explicitly set the number to be used in the commit message')
    parser.add_argument('--push', '-p', action='store_true', default=False, dest='push',
                        help='Push after committing (default: %(default)s)')
    parser.add_argument('--pushu', '-P', action='store_true', default=False, dest='push_upstream',
                        help='Push and set upstream after committing (default: %(default)s)')

    return parser.parse_args()


#######################
# Misc. Git Functions #
#######################


def _git_stage_all(opts):
    jnsgit.stage_all(dry_run=opts.dry_run, print_cmd=True)


def _git_push(opts, set_upstream):
    if set_upstream:
        jnsgit.push(set_upstream=True, repository=_DEFAULT_REPOSITORY, branch=jnsgit.branch_name(),
                    dry_run=opts.dry_run, print_cmd=True)
    else:
        jnsgit.push(dry_run=opts.dry_run, print_cmd=True)


########################
# Git Commit Functions #
########################


def _git_commit_next(opts):
    msg = _get_numbered_commit_msg(_get_branch(), opts.number) if opts.number else _get_commit_msg()
    exit_code = jnsgit.commit(msg=msg, dry_run=opts.dry_run, print_cmd=True, strict=False)

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
        raise ExitCodeError('Do not quick save to master!')

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
    return _truncate(branch, max_len) + ' ' + number_str


#####################
# Utility Functions #
#####################


def _truncate(string, length):
    str_len = len(string)
    over_by = str_len - length

    if over_by > 0:
        string = string[0:str_len - over_by - 3] + '...'

    return string


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
