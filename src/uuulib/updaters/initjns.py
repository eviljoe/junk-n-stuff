from uuulib.updaters import abstractupdater


_CMD = 'init-jns'


class InitJNSUpdater(abstractupdater.AbstractUpdater):
    def add_help_argument(self, parser):
        parser.add_argument('--' + _CMD, action='store_true', default=False, dest='init_jns',
                            help="Invoke `init-jns' from junk-n-stuff (default: %(default)s)")
    
    def get_config_command(self):
        return _CMD
    
    def update_opts_for_command(self, opts, ccmd):
        opts.init_jns = True
    
    def validate_opts(self, opts):
        return
    
    def update(self, opts, runner):
        if opts.init_jns:
            runner.run(opts=opts, cmds=[['init-jns']], title='initializing junk-n-stuff')
