import collections
import os
import re


def read_config_file(opts, config_file_name):
    if os.path.isfile(config_file_name):
        _parse_config_file(opts, config_file_name)


def _parse_config_file(opts, config_file_name):
    with open(config_file_name, 'r') as config_file:
        line_num = 0
        
        for line in config_file:
            line_num += 1
            
            ccmd = collections.namedtuple('ConfigCommand', ['cmd', 'arg', 'config_file_name', 'line_num'])
            ccmd.config_file_name = config_file_name
            ccmd.line_num = line_num
            
            _parse_config_file_line(opts, line, ccmd)


def _parse_config_file_line(opts, line, ccmd):
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
    
    _process_cmd(opts, ccmd)


# ################## #
# Command Processors #
# ################## #


def _process_cmd(opts, ccmd):
    if len(ccmd.cmd) > 0:
        processor = _PROCESSORS[ccmd.cmd.lower()]
        
        if processor is None:
            raise InvalidConfigError('[{}, line {}] Invalid Configuration command: {}'.format(
                ccmd.config_file_name, ccmd.line_num, ccmd.cmd))
        else:
            processor(opts, ccmd)


def _process_cmd_atom(opts, ccmd):  # pylint: disable=unused-argument
    opts.atom = True


def _process_cmd_git(opts, ccmd):
    _process_cmd_with_directory_arg(ccmd, opts.git_dirs)


def _process_cmd_gitd(opts, ccmd):
    _process_cmd_with_directory_arg(ccmd, opts.gitd_dirs)


def _process_cmd_pip(opts, ccmd):
    _process_cmd_with_arg(ccmd, opts.pip_packages)


def _process_cmd_pip3(opts, ccmd):
    _process_cmd_with_arg(ccmd, opts.pip3_packages)


def _process_cmd_svn(opts, ccmd):
    _process_cmd_with_directory_arg(ccmd, opts.svn_dirs)


def _process_cmd_svnd(opts, ccmd):
    _process_cmd_with_directory_arg(ccmd, opts.svnd_dirs)


def _process_cmd_with_directory_arg(ccmd, dirs):
    if len(ccmd.arg) == 0:
        raise InvalidConfigError('[{}, line {}] Configuration command requires directory: {}'.format(
            ccmd.config_file_name, ccmd.line_num, ccmd.cmd))

    dirs.append(_normalize_home_dir(ccmd.arg))


def _process_cmd_with_arg(ccmd, args):
    if len(ccmd.arg) == 0:
        raise InvalidConfigError('[{}, line {}] Configuration command requires argument: {}'.format(
            ccmd.config_file_name, ccmd.line_num, ccmd.cmd))

    args.append(ccmd.arg)


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


# ######### #
# Constants #
# ######### #

 
CMD_ATOM = 'atom'
CMD_GIT = 'git'
CMD_GITD = 'gitd'
CMD_PIP = 'pip'
CMD_PIP3 = 'pip3'
CMD_SVN = 'svn'
CMD_SVND = 'svnd'

_PROCESSORS = {
    CMD_ATOM: _process_cmd_atom,
    CMD_GIT: _process_cmd_git,
    CMD_GITD: _process_cmd_gitd,
    CMD_PIP: _process_cmd_pip,
    CMD_PIP3: _process_cmd_pip3,
    CMD_SVN: _process_cmd_svn,
    CMD_SVND: _process_cmd_svnd
}
