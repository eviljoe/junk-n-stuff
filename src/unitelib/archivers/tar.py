from . import abstractarchiver


class TARArchiver(abstractarchiver.AbstractArchiver):
    def get_file_extensions(self):
        return ['tar']
    
    def list_contents(self, opts):
        self.run_cmd(opts, ['tar', '--list', '--verbose', '--file', opts.archive])
    
    def extract_archive(self, opts):
        self.run_cmd(opts, ['tar', '--extract', '--verbose', '--file', opts.archive])
    
    def create_archive(self, opts):
        cmd = ['tar', '--create', '--verbose', '--file', opts.dest]
        cmd.extend(opts.files)
        
        self.run_cmd(opts, cmd)
