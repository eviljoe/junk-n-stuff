#!/usr/bin/env python3

import argparse
import sys


NO_ERROR = 0
ERR_INDEX_NOT_INTEGER = 1


def main():
    exit_code = NO_ERROR
    opts = parse_args()
    
    start, exit_code = to_int(opts.start, 'Start must be an integer')
    if exit_code == 0:
        end, exit_code = to_int(opts.end, 'End must be an integer')
    
    if exit_code == 0:
        print(opts.string.find(opts.sub, start, end))
    
    sys.exit(exit_code)


def parse_args():
    parser = argparse.ArgumentParser(description='Returns the index of a substring within a string.  Prints the index '
                                                 'if the substring can be found.  Prints -1 if the substring cannot be '
                                                 'found.')
    
    parser.add_argument('-s', '--start', dest='start', default=None, help='The starting index of the search')
    parser.add_argument('-e', '--end', dest='end', default=None, help='The ending index of the search')
    
    parser.add_argument('string', help='The string that is to be searched')
    parser.add_argument('sub', help='The substring to find within the string')
    
    return parser.parse_args()


def to_int(string, err):
    exit_code = NO_ERROR
    num = None
    
    if string is not None:
        try:
            num = int(string)
        except ValueError:
            exit_code = ERR_INDEX_NOT_INTEGER
            print(err, file=sys.stderr)
    
    return num, exit_code


if __name__ == '__main__':
    main()
