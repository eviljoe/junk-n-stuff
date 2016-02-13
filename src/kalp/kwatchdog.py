import shlex
import subprocess
import threading

import kutils


class WatchdogThread(threading.Thread):
    def __init__(self, cmd, cwd, keep_alive, dry_run, wait_timeout):
        threading.Thread.__init__(self)
        self.cmd = cmd
        self.cwd = cwd
        self.keep_alive = keep_alive
        self.terminated = False
        self.dry_run = dry_run
        self.wait_timeout = wait_timeout
        self.popen = None
        self.shcmd = _get_shell_command(cmd)
        self.name = 'watchdog - {}'.format(self.shcmd)
    
    def run(self):
        self._watch_subprocess()

    def _watch_subprocess(self):
        kutils.print_titled('starting subprocess: ', [kutils.BOLD, kutils.MAGENTA], self.shcmd, [])
        
        if not self.dry_run:
            self._start_and_wait_on_subprocess()
            
            while self.keep_alive:
                kutils.print_formatted('restarting subprocess: {}'.format(self.shcmd), kutils.BOLD, kutils.RED_BG)
                self._start_and_wait_on_subprocess()

    def _start_and_wait_on_subprocess(self):
        if self.is_subprocess_alive():
            raise WatchdogAlreadyHasSubprocessException(
                'Watchdog "{}" already has a running subprocess'.format(self.name))
        else:
            self._start_subprocesse()
            self._wait_on_subprocess()
    
    def _start_subprocesse(self):
        self.popen = subprocess.Popen(self.cmd, cwd=self.cwd)
    
    def _wait_on_subprocess(self):
        while not self.terminated and self.is_subprocess_alive():
            try:
                self.popen.wait(timeout=self.wait_timeout)
            except subprocess.TimeoutExpired:
                pass
    
    def is_subprocess_alive(self):
        return self.popen is not None and self.popen.poll() is None
    
    def terminate(self):
        if not self.terminated:
            self.terminated = False
            self.keep_alive = False
            self.popen.terminate()


def _get_shell_command(cmd):
    return '' if cmd is None else ' '.join([shlex.quote(part) for part in cmd])
    

class WatchdogAlreadyHasSubprocessException(Exception):
    pass
