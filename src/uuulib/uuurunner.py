import itertools
import shlex
import subprocess


class UUURunner:
    def __init__(self):
        self.run_count = 0
    
    def run(self, opts, cmds=None, cwd='.', title=None):
        if self.run_count > 0:
            print('----------')
        
        if title:
            print(title)
        
        self.run_count += 1
        self._run_cmds(opts, cmds, cwd)

    def _run_cmds(self, opts, cmds, cwd='.'):
        exit_code = 0
        
        for cmd in itertools.takewhile(lambda c: exit_code == 0, cmds):
            exit_code = self._run_cmd(opts, cmd, cwd=cwd) if cmd else 0

    def _run_cmd(self, opts, cmd, cwd='.'):
        exit_code = 0
        
        if opts.verbose:
            print('{}'.format(' '.join([shlex.quote(token) for token in cmd])))
        
        if not opts.dry_run:
            popen = subprocess.Popen(cmd, cwd=cwd)
            popen.wait()
            exit_code = popen.poll()
        
        return exit_code
