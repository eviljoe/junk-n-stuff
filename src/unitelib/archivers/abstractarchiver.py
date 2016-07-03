import abc
import shlex
import subprocess


class AbstractArchiver(metaclass=abc.ABCMeta):
    @abc.abstractmethod
    def get_file_extensions(self):
        raise NotImplementedError()
    
    @abc.abstractmethod
    def list_contents(self, opts):
        raise NotImplementedError()

    @abc.abstractmethod
    def extract_archive(self, opts):
        raise NotImplementedError()
    
    @abc.abstractmethod
    def create_archive(self, opts):
        raise NotImplementedError()
    
    def run_cmd(self, opts, cmd, cwd='.'):
        exit_code = 0
        
        if opts.verbose:
            print('{}'.format(' '.join([shlex.quote(token) for token in cmd])), flush=True)
        
        if not opts.dry_run:
            popen = subprocess.Popen(cmd, cwd=cwd)
            popen.wait()
            exit_code = popen.poll()
        
        return exit_code
