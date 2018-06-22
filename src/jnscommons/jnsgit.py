import shlex
import subprocess

_DIM = '\033[2m'
_PLAIN = '\033[0m'


def branch_name(cwd='.', dry_run=False, print_cmd=False):
    return _check_output(['git', 'rev-parse', '--abbrev-ref', 'HEAD'], cwd=cwd, dry_run=dry_run, print_cmd=print_cmd)


def commit(msg=None, cwd='.', dry_run=False, print_cmd=False, strict=True):
    cmd = ['git', 'commit']

    if msg:
        cmd.append('--message')
        cmd.append(msg)

    _call(cmd, cwd=cwd, dry_run=dry_run, print_cmd=print_cmd, strict=strict)


def commit_count_between(branch1, branch2, cwd='.', dry_run=False, print_cmd=False):
    return int(_check_output(['git', 'rev-list', '--count', '{}...{}'.format(branch1, branch2)],
                             cwd=cwd, dry_run=dry_run, print_cmd=print_cmd))


def last_commit_msg(cwd='.', dry_run=False, print_cmd=False):
    return _check_output(['git', 'log', '--format=%s', '-1'], cwd=cwd, dry_run=dry_run, print_cmd=print_cmd)


def rebase(upstream, branch=None, interactive=False, cwd='.', dry_run=False, print_cmd=False, strict=True):
    cmd = ['git', 'rebase']

    if interactive:
        cmd.append('--interactive')

    cmd.append(upstream)

    if branch:
        cmd.append(branch)

    _call(cmd, dry_run=dry_run, print_cmd=print_cmd, strict=strict)


def stage_all(cwd='.', dry_run=False, print_cmd=False, strict=True):
    _call(['git', 'add', '--all'], cwd=cwd, dry_run=dry_run, print_cmd=print_cmd, strict=strict)


def _call(cmd, cwd='.', dry_run=False, print_cmd=False, strict=True):
    exit_code = 0

    if print_cmd:
        _print_command(cmd)

    if not dry_run:
        if strict:
            exit_code = subprocess.check_call(cmd, cwd=cwd)
        else:
            exit_code = subprocess.call(cmd, cwd=cwd)

    return exit_code


def _check_output(cmd, cwd='.', dry_run=False, print_cmd=False):
    output = ''

    if print_cmd:
        _print_command(cmd)

    if not dry_run:
        output = subprocess.check_output(cmd, cwd=cwd).decode('utf-8').strip()

    return output


def _print_command(cmd):
    print(_DIM + ' '.join([shlex.quote(part) for part in cmd]) + _PLAIN, flush=True)
