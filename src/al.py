#!/usr/bin/env python3

import argparse
from datetime import datetime
import os
import os.path
import re

from jnscommons import jnsvalid
from jnscommons import jnsos


########
# Main #
########


def main():
    opts = _parse_args()
    _validate_opts(opts)
    _archive_logs(opts)


########################
# Validation Functions #
########################


def _parse_args():
    parser = argparse.ArgumentParser(description='Archives the logs!')

    parser.add_argument('--archive-dir', '-a', action='store', default=None, metavar='dir', dest='archive_dir',
                        help='The directory that contains the log archives', required=True)
    parser.add_argument('--dry-run', action='store_true', default=False, dest='dry_run',
                        help='Just output what actions will be peformed without actually performing them')
    parser.add_argument('--log-dir', '-l', action='store', default=None, metavar='dir', dest='log_dir',
                        help='The directory that contains the logs to be archived', required=True)
    parser.add_argument('--pattern', '-p', action='store', default=None, metavar='regex', dest='pattern',
                        help='A pattern matching the files that should be archived')
    parser.add_argument('--pattern-exclude', '-P', action='store', default=None, metavar='regex',
                        dest='pattern_exclude', help='A pattern matching the files that should not be archived')
    parser.add_argument('--ssh', '-s', action='store', default=None, metavar='host', dest='ssh',
                        help='The ssh host that the archive commands should be executed on')
    parser.add_argument('--verbose', action='store_true', default=False, dest='verbose',
                        help='Output more about what is happening')

    opts = parser.parse_args()
    opts.archive_subdir = _get_archive_subdir()
    
    return opts


def _validate_opts(opts):
    if opts.ssh:
        if jnsos.is_windows():
            raise NoSSHForOSError('The current OS does not support SSH: {}'.format(jnsos.OS))
    else:
        jnsvalid.validate_is_directory(opts.log_dir)
        jnsvalid.validate_is_directory(opts.archive_dir)
    
    if opts.pattern and opts.pattern_exclude:
        raise BothPatternsError('Cannot specify both --pattern and --pattern-exclude.')
    
    full_archive_dir = os.path.join(opts.archive_dir, opts.archive_subdir)
    if os.path.exists(full_archive_dir) and not os.path.isdir(full_archive_dir):
        raise ArchiveSubdirIsNotDirError(
            'The full archive path already exists, but is not a directory: {}'.format(full_archive_dir))
    
    if opts.pattern:
        re.compile(opts.pattern)

#######################
# Archiving Functions #
#######################


def _get_archive_subdir():
    return datetime.now().strftime('%Y-%m-%d--%H-%M-%S-%f')


def _archive_logs(opts):
    if opts.ssh:
        _archive_logs_ssh(opts)
    else:
        _archive_logs_local(opts)


def _file_matches_patterns(file_name, regex, regex_exclude):
    matches = True
    
    if regex:
        matches = regex.match(file_name)
    elif regex_exclude:
        matches = not regex_exclude.match(file_name)
    
    return matches


#############################
# Local Archiving Functions #
#############################


def _should_archive_local_file(file_dir, file_name, regex, regex_exclude):
    full_file = os.path.join(file_dir, file_name)
    
    return (
        _file_matches_patterns(file_name, regex, regex_exclude) and
        os.path.isfile(full_file) and
        not os.path.islink(full_file)
    )


def _archive_logs_local(opts):
    regex = re.compile(opts.pattern) if opts.pattern else None
    regex_exclude = re.compile(opts.pattern_exclude) if opts.pattern_exclude else None
    archive_dir = os.path.join(opts.archive_dir, opts.archive_subdir)
    first = True
    
    for file_name in os.listdir(opts.log_dir):
        if _should_archive_local_file(opts.log_dir, file_name, regex, regex_exclude):
            if first:
                _create_full_archive_dir(opts, archive_dir)
                first = False
            
            _archive_log_local(opts, opts.log_dir, file_name, archive_dir)
        elif opts.verbose:
            print('skipping: {}'.format(os.path.join(opts.log_dir, file_name)))


def _create_full_archive_dir(opts, archive_dir):
    print('using archive: {}'.format(archive_dir))
    
    if not opts.dry_run and not os.path.exists(archive_dir):
        os.makedirs(archive_dir)


def _archive_log_local(opts, log_dir, file_name, archive_dir):
    full_file = os.path.join(log_dir, file_name)
    
    print('archiving: {}'.format(full_file))
    
    if not opts.dry_run:
        os.rename(full_file, os.path.join(archive_dir, file_name))


#############################
# SSH Archiving Functions #
#############################


def _archive_logs_ssh(opts):
    pass


##########
# Errors #
##########


class BothPatternsError(Exception):
    pass


class ArchiveSubdirIsNotDirError(Exception):
    pass


class NoSSHForOSError(Exception):
    pass


##############
# Main Check #
##############


if __name__ == '__main__':
    main()
