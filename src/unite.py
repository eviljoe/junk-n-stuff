#!/usr/bin/env python3


import argparse

from unitelib.archivers import targz
from unitelib.archivers import zzip


ARCHIVERS = dict([
    (targz.FILE_EXTENSION, targz.TARGZArchiver()),
    (zzip.FILE_EXTENSION, zzip.ZipArchiver())
])

DEFAULT_FORMAT = targz.FILE_EXTENSION


# ############### #
# Unite Functions #
# ############### #


def main():
    opts = _parse_args()
    _archive(opts)


def _parse_args():
    parser = argparse.ArgumentParser(description='Archive in different formats')
    
    for key in ARCHIVERS.keys():
        parser.add_argument('--{}'.format(key.replace('.', '-')), action='store_const', const=key, dest='format',
                            help='Add files to a {} archive'.format(key))
    
    parser.add_argument('--dry-run', action='store_true', default=False, dest='dry_run',
                        help='Output what actions will be performed without taking them (default: %(default)s)')
    parser.add_argument('archive', metavar='dest', default='',
                        help='The name of the archive to be created')
    parser.add_argument('files', nargs='*', metavar='file', default=[],
                        help='The files or directories to be added to the archive')

    opts = parser.parse_args()
    if not opts.format:
        opts.format = DEFAULT_FORMAT
    
    # JOE todo add epilog that says the last format option that is found will be used
    
    return opts


def _validate_opts(opts):
    # JOE todo make sure a destination is provided
    # JOE todo make sure at least one file to be archived has been provided
    # JOE todo make sure each file to be archived exists
    
    if not ARCHIVERS.get(opts.format):
        raise UnsupportedArchiveFormatError('Unsupported archive format: {}'.format(opts.format))


def _archive(opts):
    ARCHIVERS.get(opts.format).create_archive(opts)


# ########## #
# Exceptions #
# ########## #


class UnsupportedArchiveFormatError(Exception):
    pass


# #### #
# Main #
# #### #


if __name__ == '__main__':
    main()
