#!/usr/bin/env python3


import argparse
import os
import re
import subprocess

import jnsutils


def main():
    opts = parse_args()
    read_config_file(opts)
    validate_opts(opts)
    update_all(opts)


# ############################## #
# Command Line Options Functions #
# ############################## #


def parse_args():
    parser = argparse.ArgumentParser(description='Update... all the things!')
    
    parser.add_argument('--atom', action='store_true', default=False, dest='atom',
                        help='Specify that Atom\'s packages should be updated (default: %(default)s)')
    parser.add_argument('--dry-run', action='store_true', default=False, dest='dry_run',
                        help='Ouput what actions will be performed without taking them (default: %(default)s)')
    parser.add_argument('--git', action='append', default=[], metavar='GIT_REPO', dest='git_dirs',
                        help='Specify a git reposotory to be updated')
    parser.add_argument('--gitd', action='append', default=[], metavar='GIT_REPO_DIR', dest='gitd_dirs',
                        help='Specify a directory that may contain one or more git reposotories to be updated')
    parser.add_argument('--svn', action='append', default=[], metavar='SVN_REPO', dest='svn_dirs',
                        help='Specify an svn reposotory to be updated')
    parser.add_argument('--svnd', action='append', default=[], metavar='SVN_REPO_DIR', dest='svnd_dirs',
                        help='Specify a directory that may contain one or more svn reposotories to be updated')
    
    opts = parser.parse_args()
    
    return opts


# ############################ #
# Configuration File Functions #
# ############################ #


def read_config_file(opts):
    config_file_name = os.path.join(os.path.expanduser('~'), '.jns', 'uuu')
    
    if os.path.isfile(config_file_name):
        parse_config_file(opts, config_file_name)


def parse_config_file(opts, config_file_name):
    with open(config_file_name, 'r') as config_file:
        line_num = 0
        
        for line in config_file:
            line_num += 1
            parse_config_file_line(opts, line, ConfigCommand(config_file_name, line_num))


def parse_config_file_line(opts, line, config_cmd):
    index = 0
    
    # remove whitespace before command
    while not at_eol(line, index) and re.match(r'\s', line[index]):
        index += 1
    
    # create command
    while not at_eol(line, index) and re.match(r'\S', line[index]):
        config_cmd.cmd += line[index]
        index += 1
    
    # remove whitespace between command and argument
    while not at_eol(line, index) and re.match(r'\s', line[index]):
        index += 1
    
    # create argument
    while not at_eol(line, index):
        config_cmd.arg += line[index]
        index += 1
    
    updates_opts_for_config_command(opts, config_cmd)


def at_eol(line, index):
    return len(line) <= index or line[index] == '\n'


def updates_opts_for_config_command(opts, config_cmd):
    cmdl = config_cmd.cmd.lower()
    
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
                config_cmd.config_file_name, config_cmd.line_num, config_cmd.cmd))
        
        update_opts_append_dir(dirs, config_cmd)


def update_opts_append_dir(dirs, config_cmd):
    if len(config_cmd.arg) == 0:
        raise InvalidConfigError('[{}, line {}] Configuration command requires directory: {}'.format(
            config_cmd.config_file_name, config_cmd.line_num, config_cmd.cmd))

    dirs.append(config_cmd.arg)


# #################### #
# Validation Functions #
# #################### #


def validate_opts(opts):
    jnsutils.validate_is_directories(opts.git_dirs)
    jnsutils.validate_is_directories(opts.gitd_dirs)
    jnsutils.validate_is_directories(opts.svn_dirs)
    jnsutils.validate_is_directories(opts.svnd_dirs)


# ################ #
# Update Functions #
# ################ #

def update_all(opts):
    for directory in opts.gitd_dirs:
        update_git_dir(opts, directory)
    
    for directory in opts.git_dirs:
        update_git(opts, directory)
    
    for directory in opts.svnd_dirs:
        update_svn_dir(opts, directory)
    
    for directory in opts.svn_dirs:
        update_svn(opts, directory)
    
    if opts.atom:
        update_atom(opts)


def update_atom(opts):
    print('updating atom\'s packages')
    run_cmd(opts, '.', ['apm', 'update', '--noconfirm'])


def update_svn_dir(opts, directory):
    update_repos_in_dir(opts, directory, update_svn)


def update_svn(opts, directory):
    update_repo(opts, directory, 'svn', '.svn', ['svn', 'update'])


def update_git_dir(opts, directory):
    update_repos_in_dir(opts, directory, update_git)


def update_git(opts, directory):
    update_repo(opts, directory, 'git', '.git', ['git', 'pull'])


def update_repos_in_dir(opts, directory, update_fn):
    for fname in os.listdir(path=directory):
        fname = os.path.join(directory, fname)
        
        if os.path.isdir(fname):
            update_fn(opts, fname)


def update_repo(opts, directory, repo_type, config_directory, cmd):
    if os.path.exists(os.path.join(directory, config_directory)):
        print('updating {} repository: {}'.format(repo_type, directory))
        run_cmd(opts, directory, cmd)
    else:
        print('skipping {} repository with no {} directory: {}'.format(repo_type, config_directory, directory))


# #################### #
# Subprocess Functions #
# #################### #


def run_cmd(opts, cwd, cmd):
    if not opts.dry_run:
        popen = subprocess.Popen(cmd, cwd=cwd)
        popen.wait()


# ########## #
# Exceptions #
# ########## #


class ConfigCommand:
    def __init__(self, config_file_name, line_num):
        self.config_file_name = config_file_name
        self.line_num = line_num
        self.cmd = ''
        self.arg = ''


# ########## #
# Exceptions #
# ########## #


class InvalidConfigError(Exception):
    pass


if __name__ == '__main__':
    main()
