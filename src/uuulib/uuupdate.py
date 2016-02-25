import os
import subprocess

from jnscommons import jnsos


_cabal_packages_refreshed = False  # pylint: disable=invalid-name


def update(opts):
    count = 0
    
    for directory in opts.gitd_dirs:
        # pylint: disable=cell-var-from-loop
        count = _do_update(count, lambda: update_git_dir(opts, directory))
    
    for package in opts.cabal_packages:
        # pylint: disable=cell-var-from-loop
        count = _do_update(count, lambda: update_cabal(opts, package))
    
    for directory in opts.git_dirs:
        count = _do_update(count, lambda: update_git(opts, directory))
    
    for directory in opts.svnd_dirs:
        # pylint: disable=undefined-loop-variable
        count = _do_update(count, lambda: update_svn_dir(opts, directory))
    
    for directory in opts.svn_dirs:
        count = _do_update(count, lambda: update_svn(opts, directory))
    
    for package in opts.pip_packages:
        # pylint: disable=cell-var-from-loop,undefined-loop-variable
        count = _do_update(count, lambda: update_pip(opts, package, three=False))
    
    for package in opts.pip3_packages:
        count = _do_update(count, lambda: update_pip(opts, package, three=True))
    
    if opts.atom:
        count = _do_update(count, lambda: update_atom(opts))
    
    if count == 0:
        print('no updates specified')


def _do_update(update_count, updater):
    if update_count > 0:
        print('------------')
    
    updater()
    
    return update_count + 1

def update_atom(opts):
    cmd = []
    
    if jnsos.is_cygwin():
        cmd.extend(['cmd', '/C', 'apm'])
    elif jnsos.is_windows():
        cmd.append('apm.cmd')
    elif jnsos.is_linux():
        cmd.append('apm')
    
    cmd.extend(['update', '--no-confirm'])

    print('updating atom\'s packages')
    _run_cmd(opts, cmd)


def update_cabal(opts, package):
    global _cabal_packages_refreshed  # pylint: disable=global-statement,invalid-name
    
    if not _cabal_packages_refreshed:
        _run_cmd(opts, ['cabal', 'update'])
        _cabal_packages_refreshed = True
    
    _run_cmd(opts, ['cabal', 'install', package])


def update_pip(opts, package, three):
    cmd = ['pip3'] if three else ['pip']
    cmd.extend(['install', '--upgrade', package])
    
    print('updating pip{} package: {}'.format('3' if three else '', package))
    _run_cmd(opts, cmd=cmd)


def update_svn_dir(opts, directory):
    _update_repos_in_dir(opts, directory, update_svn)


def update_svn(opts, directory):
    _update_repo(opts, directory, 'svn', '.svn', ['svn', 'update'])


def update_git_dir(opts, directory):
    _update_repos_in_dir(opts, directory, update_git)


def update_git(opts, directory):
    _update_repo(opts, directory, 'git', '.git', ['git', 'pull'])


def _update_repos_in_dir(opts, directory, update_fn):
    for fname in os.listdir(path=directory):
        fname = os.path.join(directory, fname)
        
        if os.path.isdir(fname):
            update_fn(opts, fname)


def _update_repo(opts, directory, repo_type, config_directory, cmd):
    if os.path.exists(os.path.join(directory, config_directory)):
        print('updating {} repository: {}'.format(repo_type, directory))
        _run_cmd(opts, cmd, cwd=directory)
    else:
        print('skipping {} repository with no {} directory: {}'.format(repo_type, config_directory, directory))


def _run_cmd(opts, cmd, cwd='.'):
    exit_code = 0
    
    if not opts.dry_run:
        popen = subprocess.Popen(cmd, cwd=cwd)
        popen.wait()
        exit_code = popen.poll()
    
    return exit_code
