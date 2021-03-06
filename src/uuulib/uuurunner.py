import itertools
import shlex
import subprocess
import time

from jnscommons import jnsstr


class UUURunner:
    def __init__(self):
        self.run_count = 0
    
    def run(self, opts, cmds=None, cwd='.', title=None):
        start = time.perf_counter()
        
        if self.run_count > 0:
            print('----------', flush=True)
        
        if title:
            print(title, flush=True)
        
        self.run_count += 1
        self._run_cmds(opts, cmds, cwd)
        
        print(
            'finshed update in {}'.format(jnsstr.seconds_to_minutes_and_seconds(time.perf_counter() - start)),
            flush=True)

    def _run_cmds(self, opts, cmds, cwd='.'):
        exit_code = 0
        
        for cmd in itertools.takewhile(lambda c: exit_code == 0, cmds):
            exit_code = self._run_cmd(opts, cmd, cwd=cwd) if cmd else 0

    def _run_cmd(self, opts, cmd, cwd='.'):
        exit_code = 0
        
        if opts.verbose:
            print('{}'.format(' '.join([shlex.quote(token) for token in cmd])), flush=True)
        
        if not opts.dry_run:
            popen = subprocess.Popen(cmd, cwd=cwd)
            popen.wait()
            exit_code = popen.poll()
        
        return exit_code
