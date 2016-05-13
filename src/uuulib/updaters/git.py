from uuulib.updaters import abstractupdater
from jnscommons import jnsvalid


_CMD = 'git'


class GitUpdater(abstractupdater.AbstractRepoUpdater):
    def add_help_argument(self, parser):
        parser.add_argument('--' + _CMD, action='append', default=[], metavar='git_repo', dest='git_dirs',
                            help='Specify a git reposotory to be updated')
    
    def get_config_command(self):
        return _CMD
    
    def update_opts_for_command(self, opts, ccmd):
        self.update_opts_add_directory(ccmd=ccmd, directories=self.get_repos(opts))
    
    def validate_opts(self, opts):
        jnsvalid.validate_is_directories(opts.git_dirs)
    
    def get_config_directory(self):
        return '.' + _CMD
    
    def get_repo_type(self):
        return _CMD
    
    def get_repos(self, opts):
        return opts.git_dirs

    def get_update_cmd(self):
        return ['git', 'pull']
