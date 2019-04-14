#!/usr/bin/env python3
# Switch git branches by using a prompt

# pylint: disable=invalid-name


import collections
import subprocess
import sys

_GREEN = '\033[32m'
_PLAIN = '\033[0m'

_NO_ERROR = 0
_ERR_UNKNOWN = 1


def main():
    exit_code = _NO_ERROR

    try:
        _select_branch()
    except ExitCodeError as e:
        exit_code = e.exit_code
        print(str(e), file=sys.stderr)
    except KeyboardInterrupt:
        print('Keyboard interrupt caught.  Aborting!', file=sys.stderr)

    sys.exit(exit_code)


def _select_branch():
    Branch = collections.namedtuple('Branch', ['name', 'selected'])
    output = subprocess.check_output(['git', 'branch', '--list', '--no-color']).decode('utf-8')
    branches = [Branch(name=line[2:], selected=line.strip().startswith('*')) for line in output.splitlines()]
    max_branch = 0

    for i, branch in enumerate(branches):
        line = _GREEN if branch.selected else ''
        line += '{}: {}'.format(i + 1, branch.name)
        line += _PLAIN if branch.selected else ''

        print(line)
        max_branch += 1

    print('Select branch: ', end='')
    branch_index = _to_branch_num(input(), max_branch) - 1
    subprocess.call(['git', 'checkout', branches[branch_index].name])


def _to_branch_num(raw_input, max_num):
    if len(raw_input) == 0:
        raise ExitCodeError('No input.  Aborting!')

    try:
        branch_num = int(raw_input, 10)
    except ValueError as e:
        raise ExitCodeError('Branch index must be a number!') from e

    if branch_num > max_num or branch_num < 1:
        raise ExitCodeError('Branch index not valid')

    return branch_num


class ExitCodeError(Exception):
    def __init__(self, msg, exit_code=_ERR_UNKNOWN):
        super().__init__(msg)
        self.exit_code = exit_code


if __name__ == '__main__':
    main()
