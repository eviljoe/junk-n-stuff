#!/usr/bin/env python3


import argparse

from jnscommons import jnsstr
from jnscommons import jnsvalid

from unitelib import uniteutils


def main():
    opts = _parse_args()
    _validate_opts(opts)
    _extract(opts)
    

def _parse_args():
    parser = argparse.ArgumentParser(description='Extract archives in different formats', epilog=_create_help_epilog(),
                                     formatter_class=argparse.RawDescriptionHelpFormatter)
    
    for archiver in uniteutils.ARCHIVERS:
        ext = archiver.get_file_extensions()[0]
        parser.add_argument('--{}'.format(ext.replace('.', '-')), action='store_const', const=ext, dest='format',
                            help='Extract files from a {} archive'.format(ext))
    
    parser.add_argument('--dry-run', action='store_true', default=False, dest='dry_run',
                        help='Output what actions will be performed without taking them (default: %(default)s)')
    parser.add_argument('-l', '--list', action='store_true', default=False, dest='list',
                        help='''
                            List the contents of the archive instead of extracting its contents
                            (default: %(default)s)
                        ''')
    parser.add_argument('--verbose', action='store_true', default=False, dest='verbose',
                        help='Print more information about what actions are being taken (default: %(default)s)')
    parser.add_argument('archive', default='', help='The archive to be extracted')

    return parser.parse_args()


def _create_help_epilog():
    return jnsstr.wrap_str_array([
        'The format of the archive to be extracted will be determined by first checking to see if a format is manually '
        'specified.  If more than one format is manually specified, the last one specified will be used.  If no format '
        'is specified, it will be determined by checking the specified archive\'s file extension.  If the format '
        'cannot be determined from the file extension, an error will be thrown.'
    ])


def _validate_opts(opts):
    jnsvalid.validate_is_file(opts.archive)


def _extract(opts):
    archiver = uniteutils.get_archiver(opts.format, opts.archive)
    
    if opts.list:
        archiver.list_contents(opts)
    else:
        archiver.extract_archive(opts)


if __name__ == '__main__':
    main()
