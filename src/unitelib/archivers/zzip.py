from . import abstractarchiver


class ZipArchiver(abstractarchiver.AbstractArchiver):
    def get_file_extensions(self):
        return ['zip']
    
    def list_contents(self, opts):
        self.run_cmd(opts, ['unzip', '-v', opts.archive])

    def extract_archive(self, opts):
        return self.run_cmd(opts, ['unzip', opts.archive])
    
    def create_archive(self, opts):
        cmd = ['zip', '--verbose', '--recurse-paths', opts.dest]
        cmd.extend(opts.files)
        
        return self.run_cmd(opts, cmd)
