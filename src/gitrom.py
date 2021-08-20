#!/usr/bin/env python3

import argparse
import sys

from jnscommons import jnsgit


_PROTECTED_BRANCHES = ['master', 'main', 'dev', 'develop', 'development']


def main():
    exit_code = 0

    try:
        opts = _parse_args()
        _validate(opts)
        _rebase(opts)
    except ExitCodeError as e:
        exit_code = e.exit_code
        print(str(e), file=sys.stderr, flush=True)

    sys.exit(exit_code)


def _parse_args():
    parser = argparse.ArgumentParser(description='Rebase on master.')

    parser.add_argument('--dry-run', action='store_true', default=False, dest='dry_run',
                        help='Output what actions will be performed without taking them (default: %(default)s)')

    parser.add_argument('branch', nargs='?', metavar='branchname', default='master',
                        help='The branch to rebase on (default: %(default)s)')

    opts = parser.parse_args()
    opts.branch = opts.branch.strip()

    return opts


def _validate(opts):
    current_branch = jnsgit.branch_name()

    if current_branch in _PROTECTED_BRANCHES:
        raise ExitCodeError(f'Do not rebase {current_branch}!')

    if current_branch == opts.branch:
        raise ExitCodeError('Cannot rebase {} onto itself'.format(current_branch))


def _rebase(opts):
    current_branch = jnsgit.branch_name()

    jnsgit.checkout(opts.branch, dry_run=opts.dry_run, print_cmd=True)
    print()

    jnsgit.pull(dry_run=opts.dry_run, print_cmd=True)
    print()

    jnsgit.checkout(current_branch, dry_run=opts.dry_run, print_cmd=True)
    print()

    jnsgit.rebase(opts.branch, interactive=True, dry_run=opts.dry_run, print_cmd=True)


class ExitCodeError(Exception):
    def __init__(self, message, exit_code=1):
        super().__init__(message)
        self.exit_code = exit_code


if __name__ == '__main__':
    main()
