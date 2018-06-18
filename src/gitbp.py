#!/usr/bin/env python3
# Switch git branches by using a prompt

# pylint: disable=invalid-name


import collections
import subprocess


_GREEN = '\033[32m'
_PLAIN = '\033[0m'


def main():
    Branch = collections.namedtuple('Branch', ['name', 'selected'])
    output = subprocess.check_output(['git', 'branch', '--list', '--no-color']).decode('utf-8')
    branches = [
        Branch(name=line[2:], selected=line.strip().startswith('*'))
        for line in output.splitlines()
    ]

    for i, branch in enumerate(branches):
        line = _GREEN if branch.selected else ''
        line += '{}: {}'.format(i + 1, branch.name)
        line += _PLAIN if branch.selected else ''

        print(line)

    print('Select branch: ', end='')
    branch_index = int(input(), 10) - 1
    subprocess.call(['git', 'checkout', branches[branch_index].name])


if __name__ == '__main__':
    main()
