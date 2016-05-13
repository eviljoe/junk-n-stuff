from uuulib.updaters import abstractupdater
from jnscommons import jnsos


_CMD = 'cygwin'
_OPT_NAME = 'cygwin_exe'


class CygwinUpdater(abstractupdater.AbstractUpdater):
    def add_help_argument(self, parser):
        parser.add_argument('--' + _CMD, action='store', default=None, metavar='setup_exe', dest=_OPT_NAME,
                            help="Specify the location of Cygwin's setup-x86.exe or setup-x86_64.exe")
    
    def get_config_command(self):
        return _CMD
    
    def update_opts_for_command(self, opts, ccmd):
        self.update_opts_set_file(ccmd, opts, _OPT_NAME)
    
    def validate_opts(self, opts):
        if opts.choco and not (opts.dry_run or jnsos.is_windows() or jnsos.is_cygwin()):
            raise NotCygwinOSError(
                'Can only update Cygwin packages when in Windows, in Cygwin, or performing a dry run.')
    
    def is_root_required(self, opts):
        return False
    
    def update(self, opts, runner):
        if opts.cygwin_exe:
            cmds = [[opts.cygwin_exe, '--quiet-mode', '--no-desktop']]
            runner.run(opts=opts, cmds=cmds, title='updating cygwin packages')


class NotCygwinOSError(Exception):
    pass
