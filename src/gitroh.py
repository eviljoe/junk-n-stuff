#!/usr/bin/env python3

import argparse
import sys

from jnscommons import jnsgit


def main():
    exit_code = 0

    try:
        opts = _parse_args()
        _rebase_on_head(opts)
    except ExitCodeError as e:
        exit_code = e.exit_code
        print(str(e), file=sys.stderr, flush=True)

    sys.exit(exit_code)


def _parse_args():
    parser = argparse.ArgumentParser(
        description='Rebase on head.',
        epilog='NOTE: This script will only work if the the current branch has already been rebased on master.'
    )

    parser.add_argument('--dry-run', action='store_true', default=False, dest='dry_run',
                        help='Output what actions will be performed without taking them (default: %(default)s)')

    return parser.parse_args()


def _rebase_on_head(opts):
    branch = jnsgit.branch_name()

    if branch == 'master':
        raise ExitCodeError('Do not rebase master!')
    else:
        commit_count = jnsgit.commit_count_between('master', branch)

        if commit_count > 1:
            jnsgit.rebase('HEAD~{}'.format(commit_count), interactive=True, dry_run=opts.dry_run, print_cmd=True)
        else:
            raise ExitCodeError('Not enough commits on this branch to rebase: {}'.format(commit_count))


class ExitCodeError(Exception):
    def __init__(self, message, exit_code=1):
        super().__init__(message)
        self.exit_code = exit_code


if __name__ == '__main__':
    main()
