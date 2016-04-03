from uuulib.updaters import abstractupdater
from jnscommons import jnsvalid


_CMD = 'gitd'


class GitdUpdater(abstractupdater.AbstractRepoDirUpdater):
    def add_help_argument(self, parser):
        parser.add_argument('--' + _CMD, action='append', default=[], metavar='git_repo_dir', dest='gitd_dirs',
                            help='Specify a directory that may contain one or more git reposotories to be updated')
    
    def get_config_command(self):
        return _CMD
    
    def update_opts_for_command(self, opts, ccmd):
        self.update_opts_add_directory(ccmd=ccmd, directories=self.get_repo_dirs(opts))
    
    def validate_opts(self, opts):
        jnsvalid.validate_is_directories(opts.gitd_dirs)
    
    def get_config_directory(self):
        return '.git'

    def get_repo_dirs(self, opts):
        return opts.gitd_dirs
    
    def get_repos(self, opts):
        return None
    
    def get_repo_type(self):
        return 'git'
    
    def get_update_cmd(self):
        return ['git', 'pull']
