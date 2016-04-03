import collections
import os
import re


def read_config_file(updaters, opts, config_file_name):
    if os.path.isfile(config_file_name):
        _parse_config_file(updaters=updaters, opts=opts, config_file_name=config_file_name)


def _parse_config_file(updaters, opts, config_file_name):
    with open(config_file_name, 'r') as config_file:
        line_num = 0
        
        for line in config_file:
            line_num += 1
            
            ccmd = collections.namedtuple('ConfigCommand', ['cmd', 'arg', 'config_file_name', 'line_num'])
            ccmd.config_file_name = config_file_name
            ccmd.line_num = line_num
            
            _parse_config_file_line(line, ccmd)
            _process_cmd(updaters, opts, ccmd)


def _parse_config_file_line(line, ccmd):
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


# ################## #
# Command Processors #
# ################## #


def _process_cmd(updaters, opts, ccmd):
    if _should_process_cmd(ccmd.cmd):
        updater = _get_updater_for_command(updaters, ccmd)
        
        if updater is None:
            raise InvalidConfigError('[{}, line {}] Invalid Configuration command: {}'.format(
                ccmd.config_file_name, ccmd.line_num, ccmd.cmd))
        
        updater.update_opts_for_command(opts, ccmd)


def _get_updater_for_command(updaters, ccmd):
    return next(iter([u for u in updaters if u.get_config_command().lower() == ccmd.cmd.lower()]), None)


def _should_process_cmd(cmd):
    return len(cmd) > 0 and not cmd.startswith('#')


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
