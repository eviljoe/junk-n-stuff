import os
import platform
import subprocess


def update(opts):
    attempted_updates = False
    
    for directory in opts.gitd_dirs:
        update_git_dir(opts, directory)
        attempted_updates = True
    
    for directory in opts.git_dirs:
        update_git(opts, directory)
        attempted_updates = True
    
    for directory in opts.svnd_dirs:
        update_svn_dir(opts, directory)
        attempted_updates = True
    
    for directory in opts.svn_dirs:
        update_svn(opts, directory)
        attempted_updates = True
    
    if opts.atom:
        update_atom(opts)
        attempted_updates = True
    
    if not attempted_updates:
        print('no updates specified')


def update_atom(opts):
    cmd = []
    
    if platform.system().lower().startswith('cygwin'):
        cmd.extend(['cmd', '/C'])
    
    cmd.extend(['apm', 'update', '--no-confirm'])

    print('updating atom\'s packages')
    run_cmd(opts, '.', cmd)


def update_svn_dir(opts, directory):
    update_repos_in_dir(opts, directory, update_svn)


def update_svn(opts, directory):
    update_repo(opts, directory, 'svn', '.svn', ['svn', 'update'])


def update_git_dir(opts, directory):
    update_repos_in_dir(opts, directory, update_git)


def update_git(opts, directory):
    update_repo(opts, directory, 'git', '.git', ['git', 'pull'])


def update_repos_in_dir(opts, directory, update_fn):
    for fname in os.listdir(path=directory):
        fname = os.path.join(directory, fname)
        
        if os.path.isdir(fname):
            update_fn(opts, fname)


def update_repo(opts, directory, repo_type, config_directory, cmd):
    if os.path.exists(os.path.join(directory, config_directory)):
        print('updating {} repository: {}'.format(repo_type, directory))
        run_cmd(opts, directory, cmd)
    else:
        print('skipping {} repository with no {} directory: {}'.format(repo_type, config_directory, directory))


def run_cmd(opts, cwd, cmd):
    if not opts.dry_run:
        popen = subprocess.Popen(cmd, cwd=cwd)
        popen.wait()
