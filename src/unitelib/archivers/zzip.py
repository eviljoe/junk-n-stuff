from . import abstractarchiver


class ZipArchiver(abstractarchiver.AbstractArchiver):
    @classmethod
    def file_extension(cls):
        return 'zip'
    
    def list_contents(self, opts):
        raise NotImplementedError()  # JOE todo

    def extract_archive(self, opts):
        raise NotImplementedError()  # JOE todo
    
    def create_archive(self, opts):
        cmd = ['zip', '--verbose', '--recurse-paths', opts.dest]
        cmd.extend(opts.files)
        
        return self.run_cmd(opts, cmd)
