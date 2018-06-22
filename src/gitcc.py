#!/usr/bin/env python3

from jnscommons import jnsgit


def main():
    print(jnsgit.commit_count_between('master', jnsgit.branch_name()))


if __name__ == '__main__':
    main()
