from uuulib.updaters import abstractupdater
from jnscommons import jnsos


_CMD = 'pip3'


class PipUpdater(abstractupdater.AbstractUpdater):
    def add_help_argument(self, parser):
        parser.add_argument('--' + _CMD, action='append', default=[], metavar='pip3_pkg', dest='pip3_packages',
                            help='Specify a pip3 package to be updated')

    def get_config_command(self):
        return _CMD
    
    def update_opts_for_command(self, opts, ccmd):
        self.update_opts_add_argument(ccmd=ccmd, arguments=opts.pip3_packages)
    
    def validate_opts(self, opts):
        return
    
    def is_root_required(self, opts):
        return len(opts.pip3_packages) > 0
    
    def update(self, opts, runner):
        for package in opts.pip3_packages:
            cmd = ['sudo'] if jnsos.is_linux() else []
            cmd.extend(['pip3', 'install', '--upgrade', package])
            
            runner.run(opts=opts, cmds=[cmd],
                       title='updating pip3 package: {}'.format(package))
