from uuulib.updaters import abstractupdater


_CMD = 'pip'


class PipUpdater(abstractupdater.AbstractUpdater):
    def add_help_argument(self, parser):
        parser.add_argument('--' + _CMD, action='append', default=[], metavar='pip_pkg', dest='pip_packages',
                            help='Specify a pip package to be updated')

    def get_config_command(self):
        return _CMD
    
    def update_opts_for_command(self, opts, ccmd):
        self.update_opts_add_argument(ccmd=ccmd, arguments=opts.pip_packages)
    
    def validate_opts(self, opts):
        return
    
    def update(self, opts, runner):
        for package in opts.pip_packages:
            runner.run(opts=opts, cmds=[['pip', 'install', '--upgrade', package]],
                       title='updating pip package: {}'.format(package))
