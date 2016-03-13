import itertools
import os
import shlex
import subprocess

from jnscommons import jnsos


class Updater():
    def __init__(self):
        self._cabal_packages_refreshed = False
        self._update_count = 0
    
    def update(self, opts):
        for directory in opts.gitd_dirs:
            self.update_git_dir(opts, directory)
        
        for package in opts.cabal_packages:
            # pylint: disable=cell-var-from-loop
            self.update_cabal(opts, package)
        
        for directory in opts.git_dirs:
            self.update_git(opts, directory)
        
        for directory in opts.svnd_dirs:
            # pylint: disable=undefined-loop-variable
            self.update_svn_dir(opts, directory)
        
        for directory in opts.svn_dirs:
            self.update_svn(opts, directory)
        
        for package in opts.pip_packages:
            # pylint: disable=cell-var-from-loop,undefined-loop-variable
            self.update_pip(opts, package, three=False)
        
        for package in opts.pip3_packages:
            self.update_pip(opts, package, three=True)
        
        if opts.init_jns:
            self.update_init_jns(opts)
        
        if opts.choco:
            self.update_choco(opts)
        
        if opts.cygwin_exe:
            self.update_cygwin(opts)
        
        if opts.atom:
            self.update_atom(opts)
        
        if self._update_count == 0:
            print('no updates specified')
    
    def update_atom(self, opts):
        cmd = []
        
        if jnsos.is_cygwin():
            cmd.extend(['cmd', '/C', 'apm'])
        elif jnsos.is_windows():
            cmd.append('apm.cmd')
        elif jnsos.is_linux():
            cmd.append('apm')
        
        cmd.extend(['update', '--no-confirm'])

        self._run_update(opts=opts, cmds=[cmd], title="updating atom's packages")

    def update_cabal(self, opts, package):
        cmds = []
        
        if not self._cabal_packages_refreshed:
            cmds.append(['cabal', 'update'])
            self._cabal_packages_refreshed = True
        
        cmds.append(['cabal', 'install', package])
        self._run_update(opts=opts, cmds=cmds, title='updating cabal package: {}'.format(package))

    def update_choco(self, opts):
        cmd = [
            'Powershell',
            '-Command',
            '& { Start-Process "choco" -ArgumentList @("update", "all") -Verb RunAs }'
        ]
        
        self._run_update(opts=opts, cmds=[cmd], title='updating chocolatey packages')
        
    def update_cygwin(self, opts):
        cmd = [opts.cygwin_exe, '-q']
        self._run_update(opts=opts, cmds=[cmd], title='updating Cygwin packages')
    
    def update_init_jns(self, opts):
        self._run_update(opts=opts, cmds=[['init-jns']], title='initializing junk-n-stuff')
    
    def update_pip(self, opts, package, three):
        cmd = ['pip3'] if three else ['pip']
        cmd.extend(['install', '--upgrade', package])
        
        self._run_update(opts=opts, cmds=[cmd],
                         title='updating pip{} package: {}'.format('3' if three else '', package))

    def update_svn_dir(self, opts, directory):
        self._update_repos_in_dir(opts, directory, self.update_svn)

    def update_svn(self, opts, directory):
        self._update_repo(opts, directory, 'svn', '.svn', ['svn', 'update'])

    def update_git_dir(self, opts, directory):
        self._update_repos_in_dir(opts, directory, self.update_git)

    def update_git(self, opts, directory):
        self._update_repo(opts, directory, 'git', '.git', ['git', 'pull'])

    def _update_repos_in_dir(self, opts, directory, update_fn):  # pylint: disable=no-self-use
        for fname in os.listdir(path=directory):
            fname = os.path.join(directory, fname)
            
            if os.path.isdir(fname):
                update_fn(opts, fname)

    def _update_repo(self, opts, directory, repo_type, config_directory, cmd):
        if os.path.exists(os.path.join(directory, config_directory)):
            self._run_update(opts=opts, cmds=[cmd], cwd=directory,
                             title='updating {} repository: {}'.format(repo_type, directory))
        else:
            self._run_update(opts=opts,
                             title='skipping {} repository with no {} directory: {}'.format(
                                 repo_type, config_directory, directory))
    
    def _run_update(self, opts, cmds=None, cwd='.', title=None):
        if self._update_count > 0:
            _print_separator()
        
        if title:
            print(title)
        
        self._update_count += 1
        
        return _run_cmds(opts, cmds, cwd)


def update(opts):
    return Updater().update(opts)


def _print_separator():
    print('----------')


def _run_cmds(opts, cmds, cwd='.'):
    exit_code = 0
    
    for cmd in itertools.takewhile(lambda c: exit_code == 0, cmds):
        exit_code = _run_cmd(opts, cmd, cwd=cwd) if cmd else 0


def _run_cmd(opts, cmd, cwd='.'):
    exit_code = 0
    
    if opts.verbose:
        print('{}'.format(' '.join([shlex.quote(token) for token in cmd])))
    
    if not opts.dry_run:
        popen = subprocess.Popen(cmd, cwd=cwd)
        popen.wait()
        exit_code = popen.poll()
    
    return exit_code
