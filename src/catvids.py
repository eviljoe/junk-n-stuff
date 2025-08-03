#!/usr/bin/env python3

import argparse
import os
import os.path
import shlex
import shutil
import subprocess
import sys
import tempfile
from collections.abc import Sequence
from dataclasses import dataclass


class ExitCodeError(Exception):
    def __init__(self, message, exit_code):
        super().__init__(message)
        self.exit_code = exit_code


@dataclass
class CvOpts:
    dry_run: str
    source_directories: Sequence[str]


_CMD_FFMPEG = 'ffmpeg'
_DEFAULT_OUTPUT_EXTENSION = 'mp4'

_FORMAT_DIM = '\033[2m'
_FORMAT_PLAIN = '\033[0m'


def main() -> None:
    exit_code = 0

    try:
        opts = _parse_args()

        _validate_opts(opts)
        _concat_vids(opts)
    except ExitCodeError as e:
        print(str(e), file=sys.stdout, flush=True)
        exit_code = e.exit_code

    sys.exit(exit_code)


def _parse_args() -> CvOpts:
    parser = argparse.ArgumentParser(description='Concatenate videos')

    parser.add_argument('--dry-run', action='store_true', dest='dry_run', default=False,
                        help='Print the commands that will be executed but do not invoke them (default: %(default)s).')
    parser.add_argument(action='store', metavar='source_directory', dest='source_directories', nargs='+',
                        help='The source directory that contains the videos to be concatenated.')

    args = parser.parse_args()
    return CvOpts(
        dry_run=args.dry_run,
        source_directories=args.source_directories,
    )


def _validate_opts(opts: CvOpts) -> None:
    if shutil.which(_CMD_FFMPEG) is None:
        raise ExitCodeError(f'{_CMD_FFMPEG} must be installed an available on the system path', exit_code=1)

    for source_directory in opts.source_directories:
        if len(source_directory) == 0:
            raise ExitCodeError('A source directory must be specified.', exit_code=1)

        if not os.path.isdir(source_directory):
            raise ExitCodeError(
                f'The source directory must be a directory that exists. (source_directory={source_directory})',
                exit_code=1,
            )


def _concat_vids(opts: CvOpts) -> None:
    for source_directory in opts.source_directories:
        _concat_vids_for_source(opts, source_directory)
        print()

def _concat_vids_for_source(opts: CvOpts, source_directory: str) -> None:
    with tempfile.TemporaryDirectory() as temp_dir:
        listing_file_name = os.path.join(temp_dir, 'catvids-listing.txt')
        output_file_name = _get_output_file_name(source_directory)

        with open(listing_file_name, 'w', encoding='utf-8') as listing_file:
            for vid_file_name in sorted(os.listdir(source_directory)):
                listing_file.write(f"file '{os.path.abspath(os.path.join(source_directory, vid_file_name))}'\n")

        print(f'Listing for {output_file_name}:')
        with open(listing_file_name, 'r', encoding='utf-8') as listing_file:
            print(listing_file.read().strip())

        _run(
            opts,
            [
                _CMD_FFMPEG,
                '-f', 'concat',
                '-safe', '0',
                '-i', listing_file_name,
                '-c', 'copy',
                _get_output_file_name(source_directory),
            ]
        )


def _get_output_file_name(source_directory: str) -> str:
    abs_path = os.path.abspath(source_directory)
    base_name = os.path.basename(abs_path)
    parent_dir = os.path.dirname(abs_path)

    return f'{os.path.join(parent_dir, base_name)}.{_DEFAULT_OUTPUT_EXTENSION}'


def _run(opts: CvOpts, cmd: Sequence[str]) -> None:
    _print_dim(' '.join([shlex.quote(part) for part in cmd]))

    if not opts.dry_run:
        subprocess.run(cmd, check=True)


def _print_dim(output: str) -> None:
    print(_FORMAT_DIM + output + _FORMAT_PLAIN, flush=True)


if __name__ == '__main__':
    main()
