from uuulib.updaters import abstractupdater
from jnscommons import jnsvalid


_CMD = 'svn'


class SVNUpdater(abstractupdater.AbstractRepoUpdater):
    def add_help_argument(self, parser):
        parser.add_argument('--' + _CMD, action='append', default=[], metavar='svn_repo', dest='svn_dirs',
                            help='Specify an SVN repository to be updated')
    
    def get_config_command(self):
        return _CMD
    
    def update_opts_for_command(self, opts, ccmd):
        self.update_opts_add_directory(ccmd=ccmd, directories=self.get_repos(opts))
    
    def validate_opts(self, opts):
        jnsvalid.validate_is_directories(opts.svn_dirs)
    
    def get_config_directory(self):
        return '.' + _CMD
    
    def get_repo_type(self):
        return _CMD
    
    def get_repos(self, opts):
        return opts.svn_dirs

    def get_update_cmd(self):
        return ['svn', 'update', '--non-interactive']
