#!/usr/bin/env python3

import argparse

from jnscommons import jnsgit


def main():
    opts = _parse_args()
    _count_commits(opts)


def _parse_args():
    parser = argparse.ArgumentParser(description='Count commits between branches.')

    parser.add_argument('--dry-run', action='store_true', default=False, dest='dry_run',
                        help='Output what actions will be performed without taking them (default: %(default)s)')
    parser.add_argument('--verbose', action='store_true', default=False, dest='verbose',
                        help='Print more output about what actions are being taken (default: %(default)s)')

    parser.add_argument('branch1', nargs='?', metavar='branchname1', default='master',
                        help='The left branch (default: %(default)s)')
    parser.add_argument('branch2', nargs='?', metavar='branchname2', default=jnsgit.branch_name(),
                        help='the right branch (default: %(default)s)')

    opts = parser.parse_args()
    opts.branch1 = opts.branch1.strip()
    opts.branch2 = opts.branch2.strip()

    return opts


def _count_commits(opts):
    count = jnsgit.commit_count_between(opts.branch1, opts.branch2, dry_run=opts.dry_run, print_cmd=opts.verbose)

    if not opts.dry_run:
        print(count)


if __name__ == '__main__':
    main()
