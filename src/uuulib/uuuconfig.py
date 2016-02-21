import collections
import os
import re


class UUUConfigFileReader:
    def __init__(self, config_file_name):
        self.config_file_name = config_file_name
        
    def read_config_file(self, opts):
        if os.path.isfile(self.config_file_name):
            self.parse_config_file(opts)

    def parse_config_file(self, opts):
        with open(self.config_file_name, 'r') as config_file:
            line_num = 0
            
            for line in config_file:
                line_num += 1
                ccmd = collections.namedtuple('ConfigCommand', ['cmd', 'arg', 'line_num'])
                ccmd.line_num = line_num
                
                self.parse_config_file_line(opts, line, ccmd)

    def parse_config_file_line(self, opts, line, ccmd):
        index = 0
        ccmd.cmd = ''
        ccmd.arg = ''
        
        # remove whitespace before command
        while not _at_eol(line, index) and re.match(r'\s', line[index]):
            index += 1
        
        # create command
        while not _at_eol(line, index) and re.match(r'\S', line[index]):
            ccmd.cmd += line[index]
            index += 1
        
        # remove whitespace between command and argument
        while not _at_eol(line, index) and re.match(r'\s', line[index]):
            index += 1
        
        # create argument
        while not _at_eol(line, index):
            ccmd.arg += line[index]
            index += 1
        
        self.update_opts_for_config_command(opts, ccmd)

    def update_opts_for_config_command(self, opts, ccmd):
        cmdl = ccmd.cmd.lower()
        
        if cmdl == 'atom':
            opts.atom = True
        elif len(cmdl) > 0:
            if cmdl == 'git':
                dirs = opts.git_dirs
            elif cmdl == 'gitd':
                dirs = opts.gitd_dirs
            elif cmdl == 'svn':
                dirs = opts.svn_dirs
            elif cmdl == 'svnd':
                dirs = opts.svnd_dirs
            else:
                raise InvalidConfigError('[{}, line {}] Invalid Configuration command: {}'.format(
                    self.config_file_name, ccmd.line_num, ccmd.cmd))
            
            self.update_opts_append_dir(dirs, ccmd)

    def update_opts_append_dir(self, dirs, ccmd):
        if len(ccmd.arg) == 0:
            raise InvalidConfigError('[{}, line {}] Configuration command requires directory: {}'.format(
                self.config_file_name, ccmd.line_num, ccmd.cmd))

        dirs.append(ccmd.arg)


# ################# #
# Utility Functions #
# ################# #


def _at_eol(line, index):
    return len(line) <= index or line[index] == '\n'


# ########## #
# Exceptions #
# ########## #


class InvalidConfigError(Exception):
    pass
