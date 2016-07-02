#!/usr/bin/env python3


import argparse

from jnscommons import jnsvalid

from unitelib import uniteutils


def main():
    opts = _parse_args()
    _validate_opts(opts)
    _archive(opts)


def _parse_args():
    parser = argparse.ArgumentParser(description='Archive in different formats')
    
    for archiver in uniteutils.ARCHIVERS:
        ext = archiver.file_extension()
        parser.add_argument('--{}'.format(ext.replace('.', '-')), action='store_const', const=ext, dest='format',
                            help='Add files to a {} archive'.format(ext))
    
    parser.add_argument('--dry-run', action='store_true', default=False, dest='dry_run',
                        help='Output what actions will be performed without taking them (default: %(default)s)')
    parser.add_argument('--verbose', action='store_true', default=False, dest='verbose',
                        help='Print more information about what actions are being taken (default: %(default)s)')
    parser.add_argument('dest', metavar='dest_archive', default='',
                        help='The name of the archive to be created')
    parser.add_argument('files', nargs='*', metavar='file', default=[],
                        help='The files or directories to be added to the archive')

    # JOE todo add epilog that says that the format is determined in the following order:
    # 1. last manually specified format (e.g. if both --tar-gz --zip, then zip is used)
    # 2. determine format from dest_archive file name
    
    return parser.parse_args()


def _validate_opts(opts):
    # JOE todo make sure a destination is provided
    # JOE todo make sure at least one file to be archived has been provided
    jnsvalid.validate_all_exist(opts.files)


def _archive(opts):
    uniteutils.get_archiver(opts.format, opts.dest).create_archive(opts)


if __name__ == '__main__':
    main()
