import shlex
import subprocess
import threading

import kutils


class KWatchdogThread(threading.Thread):
    def __init__(self, cmd, cwd, keep_alive, dry_run):
        threading.Thread.__init__(self)
        self.cmd = cmd
        self.cwd = cwd
        self.keep_alive = keep_alive
        self.dry_run = dry_run
        self.popen = None
        self.shcmd = self._get_shell_command(cmd)
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
                'Watchdog "{}" already has running subprocess'.format(self.name))
        else:
            self.popen = subprocess.Popen(self.cmd, cwd=self.cwd)
            self.popen.wait()
    
    def is_subprocess_alive(self):
        return self.popen is not None and self.popen.poll() is None
    
    def terminate(self):
        self.keep_alive = False
        self.popen.terminate()
    
    def _get_shell_command(self, cmd):
        return '' if cmd is None else ' '.join([shlex.quote(part) for part in cmd])
    

class WatchdogAlreadyHasSubprocessException(Exception):
    pass
