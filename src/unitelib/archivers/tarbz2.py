from . import abstractarchiver


class TARBZ2Archiver(abstractarchiver.AbstractArchiver):
    def get_file_extensions(self):
        return ['tar.bz2', 'tbz', 'tb2', 'tbz2']
    
    def list_contents(self, opts):
        self.run_cmd(opts, ['tar', '--list', '--verbose', '--file', opts.archive, '--bzip2'])
    
    def extract_archive(self, opts):
        self.run_cmd(opts, ['tar', '--extract', '--verbose', '--file', opts.archive, '--bzip2'])
    
    def create_archive(self, opts):
        cmd = ['tar', '--create', '--verbose', '--file', opts.dest, '--bzip2']
        cmd.extend(opts.files)
        
        self.run_cmd(opts, cmd)
