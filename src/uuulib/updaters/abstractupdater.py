import abc
import os.path


class AbstractUpdater(metaclass=abc.ABCMeta):
    
    @abc.abstractmethod
    def add_help_argument(self, parser):
        raise NotImplementedError()
    
    @abc.abstractmethod
    def get_config_command(self):
        raise NotImplementedError()
    
    @abc.abstractmethod
    def update_opts_for_command(self, opts, ccmd):
        raise NotImplementedError()
    
    @abc.abstractmethod
    def validate_opts(self, opts):
        raise NotImplementedError()
    
    @abc.abstractmethod
    def is_root_required(self, opts):
        raise NotImplementedError()
    
    @abc.abstractmethod
    def update(self, opts, runner):
        raise NotImplementedError()
    
    def is_config_command(self, ccmd):
        return ccmd.cmd.lower() == self.get_config_command()

    @staticmethod
    def update_opts_add_directory(ccmd, directories):
        _verify_has_argument(ccmd, argtype='directory')
        directories.append(_normalize_home_dir(ccmd.arg))

    @staticmethod
    def update_opts_set_file(ccmd, opts, argument_name):
        _verify_has_argument(ccmd, argtype='file')
        setattr(opts, argument_name, _normalize_home_dir(ccmd.arg))
    
    @staticmethod
    def update_opts_add_argument(ccmd, arguments):
        _verify_has_argument(ccmd)
        arguments.append(ccmd.arg)


class AbstractRepoUpdater(AbstractUpdater, metaclass=abc.ABCMeta):
    
    @abc.abstractmethod
    def get_repos(self, opts):
        raise NotImplementedError()
    
    @abc.abstractmethod
    def get_repo_type(self):
        raise NotImplementedError()
    
    @abc.abstractmethod
    def get_config_directory(self):
        raise NotImplementedError()
    
    @abc.abstractmethod
    def get_update_cmd(self):
        raise NotImplementedError()

    def is_root_required(self, opts):
        return False

    def update(self, opts, runner):
        for repo_dir in self.get_repos(opts):
            self.update_repo(opts=opts, runner=runner, directory=repo_dir, repo_type=self.get_repo_type(),
                             config_directory=self.get_config_directory(), cmd=self.get_update_cmd())

    @staticmethod
    def update_repo(opts, runner, directory, repo_type, config_directory, cmd):
        if os.path.exists(os.path.join(directory, config_directory)):
            runner.run(opts=opts, cmds=[cmd], cwd=directory,
                       title='updating {} repository: {}'.format(repo_type, directory))
        else:
            runner.run(opts=opts, title='skipping {} repository with no {} directory: {}'.format(
                repo_type, config_directory, directory))


class AbstractRepoDirUpdater(AbstractRepoUpdater, metaclass=abc.ABCMeta):
    
    @abc.abstractmethod
    def get_repo_dirs(self, opts):
        raise NotImplementedError()
    
    def is_root_required(self, opts):
        return False
    
    def update(self, opts, runner):
        for repo_dir in self.get_repo_dirs(opts):
            for repo in os.listdir(path=repo_dir):
                repo = os.path.join(repo_dir, repo)
                
                if os.path.isdir(repo):
                    self.update_repo(opts=opts, runner=runner, directory=repo, repo_type=self.get_repo_type(),
                                     config_directory=self.get_config_directory(), cmd=self.get_update_cmd())


# ################# #
# Utility Functions #
# ################# #


def _normalize_home_dir(directory):
    if directory == '~' or directory.startswith('~/') or directory.startswith('~\\'):
        directory = os.path.expanduser('~') + directory[1:]
    
    return directory


def _verify_has_argument(ccmd, argtype='argument'):
    if len(ccmd.arg) == 0:
        raise InvalidConfigError('[{}, line {}] Configuration command requires {}: {}'.format(
            ccmd.config_file_name, ccmd.line_num, argtype, ccmd.cmd))


# ########## #
# Exceptions #
# ########## #


class InvalidConfigError(Exception):
    pass
