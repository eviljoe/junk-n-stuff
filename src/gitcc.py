#!/usr/bin/env python3

import subprocess


def main():
    branch = check_output(['git', 'rev-parse', '--abbrev-ref', 'HEAD'])
    commit_count = check_output(['git', 'rev-list', '--count', 'master...{}'.format(branch)])
    print(commit_count)


def check_output(cmd):
    return subprocess.check_output(cmd).decode('utf-8').strip()


if __name__ == '__main__':
    main()
