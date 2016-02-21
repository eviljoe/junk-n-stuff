import collections
import os
import re


CMD_ATOM = 'atom'
CMD_GIT = 'git'
CMD_GITD = 'gitd'
CMD_SVN = 'svn'
CMD_SVND = 'svnd'


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
        
        if cmdl == CMD_ATOM:
            opts.atom = True
        elif len(cmdl) > 0:
            dirs_for_cmd = {
                CMD_GIT: opts.git_dirs,
                CMD_GITD: opts.gitd_dirs,
                CMD_SVN: opts.svn_dirs,
                CMD_SVND: opts.svnd_dirs
            }
            
            if cmdl not in dirs_for_cmd:
                raise InvalidConfigError('[{}, line {}] Invalid Configuration command: {}'.format(
                    self.config_file_name, ccmd.line_num, ccmd.cmd))
            
            self.update_opts_append_dir(dirs_for_cmd[cmdl], ccmd)

    def update_opts_append_dir(self, dirs, ccmd):
        if len(ccmd.arg) == 0:
            raise InvalidConfigError('[{}, line {}] Configuration command requires directory: {}'.format(
                self.config_file_name, ccmd.line_num, ccmd.cmd))

        dirs.append(_normalize_home_dir(ccmd.arg))


# ################# #
# Utility Functions #
# ################# #


def _at_eol(line, index):
    return len(line) <= index or line[index] == '\n'


def _normalize_home_dir(directory):
    if directory == '~' or directory.startswith('~/') or directory.startswith('~\\'):
        directory = os.path.expanduser('~') + directory[1:]
    
    return directory


# ########## #
# Exceptions #
# ########## #


class InvalidConfigError(Exception):
    pass
