from uuulib.updaters import abstractupdater
from jnscommons import jnsos


_CMD = 'atom'


class AtomUpdater(abstractupdater.AbstractUpdater):
    def add_help_argument(self, parser):
        parser.add_argument('--' + _CMD, action='store_true', default=False, dest='atom',
                            help="Specify that Atom's packages should be updated (default: %(default)s)")
    
    def get_config_command(self):
        return _CMD
    
    def update_opts_for_command(self, opts, ccmd):
        opts.atom = True
    
    def validate_opts(self, opts):
        return
    
    def update(self, opts, runner):
        if opts.atom:
            cmd = []
            
            if jnsos.is_cygwin():
                cmd.extend(['cmd', '/C', 'apm'])
            elif jnsos.is_windows():
                cmd.append('apm.cmd')
            elif jnsos.is_linux():
                cmd.append('apm')
            
            cmd.extend(['update', '--no-confirm'])

            runner.run(opts=opts, cmds=[cmd], title="updating atom's packages")
