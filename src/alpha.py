#!/usr/bin/env python3

import argparse


def main():
    opts = parse_args()
    print_sorted(opts.words)
    

def parse_args():
    parser = argparse.ArgumentParser(description='Sorts the given words')
    
    parser.add_argument('words', nargs='*', metavar='word', default=[],
                        help='The words (or phrases) to be sorted')

    return parser.parse_args()


def print_sorted(words):
    for word in sorted(words, key=str.lower):
        print(word)


if __name__ == "__main__":
    main()
