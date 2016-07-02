from . import abstractarchiver


class TARGZArchiver(abstractarchiver.AbstractArchiver):
    @classmethod
    def file_extension(cls):
        return 'tar.gz'
    
    def list_contents(self, opts):
        raise NotImplementedError()  # JOE todo
    
    def extract_archive(self, opts):
        raise NotImplementedError()  # JOE todo
    
    def create_archive(self, opts):
        cmd = ['tar', '--create', '--verbose', '--gzip', '--file', opts.dest]
        cmd.extend(opts.files)
        
        self.run_cmd(opts, cmd)
