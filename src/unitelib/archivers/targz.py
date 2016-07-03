from . import abstractarchiver


class TARGZArchiver(abstractarchiver.AbstractArchiver):
    def get_file_extensions(self):
        return ['tar.gz', 'tgz']
    
    def list_contents(self, opts):
        self.run_cmd(opts, ['tar', '--list', '--verbose', '--file', opts.archive, '--gzip'])
    
    def extract_archive(self, opts):
        self.run_cmd(opts, ['tar', '--extract', '--verbose', '--file', opts.archive, '--gzip'])
    
    def create_archive(self, opts):
        cmd = ['tar', '--create', '--verbose', '--file', opts.dest, '--gzip']
        cmd.extend(opts.files)
        
        self.run_cmd(opts, cmd)
