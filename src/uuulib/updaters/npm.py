from uuulib.updaters import abstractupdater
from jnscommons import jnsos


_CMD = 'npm'


class NPMUpdater(abstractupdater.AbstractUpdater):
    def add_help_argument(self, parser):
        parser.add_argument('--' + _CMD, action='append', default=[], metavar='npm_pkg', dest='npm_packages',
                            help='Specify an npm package to be updated')

    def get_config_command(self):
        return _CMD
    
    def update_opts_for_command(self, opts, ccmd):
        self.update_opts_add_argument(ccmd=ccmd, arguments=opts.npm_packages)
    
    def validate_opts(self, opts):
        return
    
    def is_root_required(self, opts):
        return opts.npm_packages
    
    def update(self, opts, runner):
        if opts.npm_packages:
            cmd = ['sudo'] if jnsos.is_linux() else []
            cmd.extend(['npm', 'update', '-g'])
            cmd.extend(opts.npm_packages)
            
            runner.run(opts=opts, cmds=[cmd],
                       title='updating npm packages: {}'.format(', '.join(opts.npm_packages)))
