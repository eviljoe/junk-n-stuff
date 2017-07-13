from uuulib.updaters import abstractupdater
from jnscommons import jnsvalid


_CMD = 'svnd'


class SVNDUpdater(abstractupdater.AbstractRepoDirUpdater):
    def add_help_argument(self, parser):
        parser.add_argument('--' + _CMD, action='append', default=[], metavar='svn_repo_dir', dest='svnd_dirs',
                            help='Specify a directory that may contain one or more SVN reposotories to be updated')
    
    def get_config_command(self):
        return _CMD
    
    def update_opts_for_command(self, opts, ccmd):
        self.update_opts_add_directory(ccmd=ccmd, directories=self.get_repo_dirs(opts))
    
    def validate_opts(self, opts):
        jnsvalid.validate_is_directories(opts.svnd_dirs)
    
    def get_config_directory(self):
        return '.svn'

    def get_repo_dirs(self, opts):
        return opts.svnd_dirs
    
    def get_repos(self, opts):
        return None
    
    def get_repo_type(self):
        return 'svn'
    
    def get_update_cmd(self):
        return ['svn', 'update', '--non-interactive']
