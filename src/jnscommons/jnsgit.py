import shlex
import subprocess

_DIM = '\033[2m'
_PLAIN = '\033[0m'


def branch_name(cwd='.', dry_run=False, print_cmd=False) -> str:
    return _check_output(['git', 'rev-parse', '--abbrev-ref', 'HEAD'], cwd=cwd, dry_run=dry_run, print_cmd=print_cmd)


def checkout(branch_name, cwd='.', dry_run=False, print_cmd=False, strict=True) -> int:
    return _call(['git', 'checkout', branch_name], cwd=cwd, dry_run=dry_run, print_cmd=print_cmd, strict=strict)


def commit(msg=None, cwd='.', dry_run=False, print_cmd=False, strict=True) -> int:
    cmd = ['git', 'commit']

    if msg:
        cmd.append('--message')
        cmd.append(msg)

    return _call(cmd, cwd=cwd, dry_run=dry_run, print_cmd=print_cmd, strict=strict)


def commit_count_between(branch1, branch2, cwd='.', dry_run=False, print_cmd=False) -> int:
    count = _check_output(['git', 'rev-list', '--count', '{}...{}'.format(branch1, branch2)],
                          cwd=cwd, dry_run=dry_run, print_cmd=print_cmd)

    if not dry_run:
        count = int(count)

    return count


def last_commit_msg(cwd='.', dry_run=False, print_cmd=False) -> str:
    return _check_output(['git', 'log', '--format=%s', '-1'], cwd=cwd, dry_run=dry_run, print_cmd=print_cmd)


def rebase(upstream, branch=None, interactive=False, cwd='.', dry_run=False, print_cmd=False, strict=True) -> int:
    cmd = ['git', 'rebase']

    if interactive:
        cmd.append('--interactive')

    cmd.append(upstream)

    if branch:
        cmd.append(branch)

    return _call(cmd, cwd=cwd, dry_run=dry_run, print_cmd=print_cmd, strict=strict)


def status(cwd='.', dry_run=False, print_cmd=False, strict=True) -> int:
    return _call(['git', 'status'], cwd=cwd, dry_run=dry_run, print_cmd=print_cmd, strict=strict)


def stage_all(cwd='.', dry_run=False, print_cmd=False, strict=True) -> int:
    return _call(['git', 'add', '--all'], cwd=cwd, dry_run=dry_run, print_cmd=print_cmd, strict=strict)


def pull(cwd='.', dry_run=False, print_cmd=False, strict=True) -> int:
    return _call(['git', 'pull'], cwd=cwd, dry_run=dry_run, print_cmd=print_cmd, strict=strict)


def push(repository=None, branch=None, set_upstream=False, force=False, cwd='.', dry_run=False, print_cmd=False, strict=True) -> int:
    cmd = ['git', 'push']

    if force:
        cmd.append('--force')

    if set_upstream:
        cmd.append('--set-upstream')

    if repository:
        cmd.append(repository)

    if branch:
        cmd.append(branch)

    return _call(cmd, cwd=cwd, dry_run=dry_run, print_cmd=print_cmd, strict=strict)


def _call(cmd, cwd='.', dry_run=False, print_cmd=False, strict=True) -> int:
    exit_code = 0

    if print_cmd:
        _print_command(cmd)

    if not dry_run:
        if strict:
            exit_code = subprocess.check_call(cmd, cwd=cwd)
        else:
            exit_code = subprocess.call(cmd, cwd=cwd)

    return exit_code


def _check_output(cmd, cwd='.', dry_run=False, print_cmd=False) -> str:
    output = ''

    if print_cmd:
        _print_command(cmd)

    if not dry_run:
        output = subprocess.check_output(cmd, cwd=cwd).decode('utf-8').strip()

    return output


def _print_command(cmd) -> None:
    print(_DIM + ' '.join([shlex.quote(part) for part in cmd]) + _PLAIN, flush=True)
