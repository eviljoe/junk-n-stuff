from uuulib.updaters import abstractupdater
from jnscommons import jnsos


_CMD = 'choco'


class ChocoUpdater(abstractupdater.AbstractUpdater):
    def add_help_argument(self, parser):
        parser.add_argument('--' + _CMD, action='store_true', default=False, dest='choco',
                            help='Specify that all Chocolatey packages should be updated (default: %(default)s)')
    
    def get_config_command(self):
        return _CMD
    
    def update_opts_for_command(self, opts, ccmd):
        opts.choco = True
    
    def validate_opts(self, opts):
        if opts.choco and not (opts.dry_run or jnsos.is_windows() or jnsos.is_cygwin()):
            raise NotChocoOSError(
                'Can only update Chocolatey packages when in Windows, in Cygwin, or performing a dry run.')
    
    def is_root_required(self, opts):
        return False
    
    def update(self, opts, runner):
        if opts.choco:
            cmds = [[
                'Powershell',
                '-Command',
                '& { Start-Process "choco" -ArgumentList @("upgrade", "all") -Verb RunAs }'
            ]]
            
            runner.run(opts=opts, cmds=cmds, title='updating chocolatey packages')


class NotChocoOSError(Exception):
    pass
