#!/usr/bin/env python3

import subprocess
import sys


def main():
    branch = check_output(['git', 'rev-parse', '--abbrev-ref', 'HEAD'])
    exit_code = 0

    if branch == 'master':
        print('Do not rebase master!', file=sys.stderr)
        exit_code = 1
    else:
        commit_count = int(check_output(['git', 'rev-list', '--count', 'master...{}'.format(branch)]))

        if commit_count > 1:
            check_call(['git', 'rebase', '--interactive', 'HEAD~{}'.format(commit_count)])
        else:
            print('Not enough commits on this branch to rebase: {}'.format(commit_count), file=sys.stderr)
            exit_code = 1

    sys.exit(exit_code)


def check_output(cmd):
    return subprocess.check_output(cmd).decode('utf-8').strip()


def check_call(cmd):
    subprocess.check_call(cmd)


if __name__ == '__main__':
    main()
