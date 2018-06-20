import os.path

from jnscommons import jnsos, jnsvalid
from uuulib.updaters import abstractupdater

_CMD = 'rustgit'
_DELIMITER = ','


class RustGitUpdater(abstractupdater.AbstractUpdater):
    def add_help_argument(self, parser):
        parser.add_argument('--' + _CMD, action='append', default=[],
                            metavar='git_url{}project_home{}exe_name'.format(_DELIMITER, _DELIMITER),
                            dest='rust_git_projects',
                            help='Specify a Rust+Git project to be updated.  See below for more information on the '
                                 'argument format.')

    def get_config_command(self):
        return _CMD
    
    def update_opts_for_command(self, opts, ccmd):
        self.update_opts_add_argument(ccmd=ccmd, arguments=opts.rust_git_projects)
    
    def validate_opts(self, opts):
        if opts.rust_git_projects:
            if not (jnsos.is_linux() or jnsos.is_cygwin()):
                raise OSError('The {} updater can only be used in Linux or Cygwin'.format(_CMD))

            for md in self._get_all_project_meta_data(opts):
                if os.path.exists(md.project_home):
                    jnsvalid.validate_is_directory(md.project_home)

    def is_root_required(self, opts):
        return opts.rust_git_projects
    
    def update(self, opts, runner):
        for md in self._get_all_project_meta_data(opts):
            cmds = [
                self._pull(md) if os.path.exists(md.project_home) else self._clone(md),
                self._build(md),
                self._install(md)
            ]
            runner.run(opts=opts, cmds=cmds, title='updating rust+git project: {}'.format(md.exe_name))

    def _get_all_project_meta_data(self, opts):
        return [self._get_project_meta_data(project) for project in opts.rust_git_projects]

    @staticmethod
    def _get_project_meta_data(project_string):
        parts = project_string.split(_DELIMITER)
        return RustGitProjectMetaData(
            git_url=parts[0].strip(),
            project_home=parts[1].strip(),
            exe_name=parts[2].strip()
        )

    @staticmethod
    def _clone(metadata):
        return ['git', 'clone', metadata.git_url, metadata.project_home]


    @staticmethod
    def _pull(metadata):
        return ['git', '-C', metadata.project_home, 'pull']

    @staticmethod
    def _build(metadata):
        return [
            'cargo',
            'build',
            '--manifest-path={}/Cargo.toml'.format(metadata.project_home),
            '--release'
        ]

    @staticmethod
    def _install(metadata):
        cmd = ['sudo'] if jnsos.is_linux() else []
        cmd.extend([
            'update-alternatives',
            '--install',
            '/usr/bin/{}'.format(metadata.exe_name),
            metadata.exe_name,
            '{}/target/release/{}'.format(metadata.project_home, metadata.exe_name),
            '100'
        ])

        return cmd


class RustGitProjectMetaData:
    def __init__(self, git_url, project_home, exe_name):
        self.git_url = git_url
        self.project_home = project_home
        self.exe_name = exe_name
