#!/usr/bin/env python3

import argparse
import sys

from jnscommons import jnsgit


#############
# Constants #
#############


_GREEN = '\033[32m'
_PLAIN = '\033[0m'


###############
# Main Method #
###############


def main():
    exit_code = 0

    try:
        opts = parse_args()
        rebase_all(opts)
    except ExitCodeError as e:
        exit_code = e.exit_code
        print(str(e), file=sys.stderr, flush=True)

    sys.exit(exit_code)


########################
# CLI Option Functions #
########################


def parse_args():
    parser = argparse.ArgumentParser(description='Rebase a chain of branches')

    parser.add_argument('--dry-run', action='store_true', default=False, dest='dry_run',
                        help='Output what actions will be performed without taking them (default: %(default)s)')
    parser.add_argument('-i', '--interactive', action='store_true', default=False, dest='interactive',
                        help='Perform interactive rebases (default: %(default)s)')
    parser.add_argument('branches', metavar='branch', type=str, nargs='+',
                        help='The branches to be rebased upon each other.  The first branch will not be rebased.')

    return parser.parse_args()


########################
# Git Rebase Functions #
########################


def rebase_all(opts):
    index = 0

    while index < len(opts.branches) - 1:
        upstream_branch = opts.branches[index]
        downstream_branch = opts.branches[index + 1]
        index += 1

        print(f'{_GREEN}Rebasing {downstream_branch}{_PLAIN}', flush=True)
        rebase(opts, upstream_branch, downstream_branch)
        print(flush=True)


def rebase(opts, upstream_branch, downstream_branch):
    jnsgit.checkout(upstream_branch, dry_run=opts.dry_run, print_cmd=True, strict=True)
    jnsgit.pull(dry_run=opts.dry_run, print_cmd=True, strict=True)
    jnsgit.checkout(downstream_branch, dry_run=opts.dry_run, print_cmd=True, strict=True)
    jnsgit.pull(dry_run=opts.dry_run, print_cmd=True, strict=True)
    jnsgit.rebase(upstream_branch, interactive=opts.interactive, dry_run=opts.dry_run, print_cmd=True, strict=True)
    jnsgit.push(force=True, dry_run=opts.dry_run, print_cmd=True, strict=True)


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
