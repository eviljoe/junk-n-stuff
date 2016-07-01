from . import abstractarchiver


FILE_EXTENSION = 'tar.gz'


class TARGZArchiver(abstractarchiver.AbstractArchiver):
    def list_contents(self, opts):
        raise NotImplementedError()  # JOE todo
        
    def extract_archive(self, opts):
        raise NotImplementedError()  # JOE todo
        
    def create_archive(self, opts):
        raise NotImplementedError()  # JOE todo
