from uuulib.updaters import abstractupdater


_CMD = 'cabal'


class CabalUpdater(abstractupdater.AbstractUpdater):
    def __init__(self):
        self._cabal_packages_refreshed = False
    
    def add_help_argument(self, parser):
        parser.add_argument('--' + _CMD, action='append', default=[], metavar='cabal_pkg', dest='cabal_packages',
                            help='Specify a cabal package to be updated')
    
    def get_config_command(self):
        return _CMD
    
    def update_opts_for_command(self, opts, ccmd):
        self.update_opts_add_argument(ccmd=ccmd, arguments=opts.cabal_packages)
    
    def validate_opts(self, opts):
        return
    
    def is_root_required(self, opts):
        return False
    
    def update(self, opts, runner):
        for package in opts.cabal_packages:
            cmds = []
            
            if not self._cabal_packages_refreshed:
                cmds.append(['cabal', 'update'])
                self._cabal_packages_refreshed = True
            
            cmds.append(['cabal', 'install', package])
            runner.run(opts=opts, cmds=cmds, title='updating cabal package: {}'.format(package))
