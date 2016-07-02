#!/usr/bin/env python3


import argparse

from jnscommons import jnsvalid

from unitelib import uniteutils


def main():
    opts = _parse_args()
    _validate_opts(opts)
    _extract(opts)


def _parse_args():
    parser = argparse.ArgumentParser(description='Extract archives in different formats')
    
    for archiver in uniteutils.ARCHIVERS:
        ext = archiver.file_extension()
        parser.add_argument('--{}'.format(ext.replace('.', '-')), action='store_const', const=ext, dest='format',
                            help='Extract files from a {} archive'.format(ext))
    
    parser.add_argument('--dry-run', action='store_true', default=False, dest='dry_run',
                        help='Output what actions will be performed without taking them (default: %(default)s)')
    parser.add_argument('--verbose', action='store_true', default=False, dest='verbose',
                        help='Print more information about what actions are being taken (default: %(default)s)')
    parser.add_argument('archive', nargs='*', default='',
                        help='The archive to be extracted')

    # JOE todo add epilog that says that if no format is specified, it will be determined using the archive file name
    # JOE todo add epilog that says the last format option that is found will be used
    
    return parser.parse_args()


def _validate_opts(opts):
    jnsvalid.validate_is_file(opts.archive)


def _extract(opts):
    uniteutils.get_archiver(opts.format, opts.archive).extract_archive(opts)


if __name__ == '__main__':
    main()
