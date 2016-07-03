import textwrap
import shutil

from . import abstractarchiver


class JARArchiver(abstractarchiver.AbstractArchiver):
    def get_file_extensions(self):
        return ['jar', 'war', 'ear']
    
    def list_contents(self, opts):
        print('\n/* *********** */\n/* MANIFEST.MF */\n/* *********** */\n')
        self.run_cmd(opts, ['unzip', '-p', opts.archive, 'META-INF/MANIFEST.MF'])
        
        print('/* ***** */\n/* FILES */\n/* ***** */\n')
        self.run_cmd(opts, ['jar', 'tvf', opts.archive])
    
    def extract_archive(self, opts):
        self.run_cmd(opts, ['unzip', opts.archive])
    
    def create_archive(self, opts):  # pylint: disable=unused-argument
        print(textwrap.fill(
            'Yeah... your expectations for this script were a bit high.  Use a dedicated tool for that.',
            width=shutil.get_terminal_size().columns))
