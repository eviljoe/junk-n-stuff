#!/usr/bin/env python3

import sys
import itertools

def main():
    for s in sorted(itertools.islice(sys.argv, 1, None), key=str.lower):
        print(s)

if __name__ == "__main__": main()
