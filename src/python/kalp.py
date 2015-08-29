#!/usr/bin/env python3

import argparse
import atexit
from subprocess import Popen

BOLD = "\033[1m"
CYAN = "\033[36m"
RED = '\033[31m'
PLAIN = '\033[0m'

gulp_popen = None
karma_popen = None


def main():
    atexit.register(terminate_processes)
    opts = parse_args()
    start_processes(opts)
    wait_on_processes()


def parse_args():
    parser = argparse.ArgumentParser(
        description="A utility to help manage `gulp watch' and `karma' in development enviornments")
        
    parser.add_argument("-K", "--no-karma", action="store_true", default=False,
                        help="Do not start the `gulp watch' subprocess (default: %(default)s)")
    parser.add_argument("-G", "--no-gulp", action="store_true", default=False,
                        help="Do not start the `karma' subprocess (default: %(default)s)")
    
    return parser.parse_args()


def start_processes(opts):
    process_count = 0
    
    print_formatted("Starting Processes:", BOLD, CYAN)
    
    if not opts.no_gulp:
        start_gulp_process()
        process_count += 1
        
    if not opts.no_karma:
        start_karma_process()
        process_count += 1
    
    if process_count == 0:
        print_formatted("None", BOLD, RED)


def start_gulp_process():
    global gulp_popen
    
    print_formatted("gulp watch", BOLD)
    gulp_popen = Popen(["gulp", "watch"])


def start_karma_process():
    global karma_popen
    
    print_formatted("karma start", BOLD)
    karma_popen = Popen(["karma", "start"])


def wait_on_processes():
    if gulp_popen is not None:
        gulp_popen.wait()
    if karma_popen is not None:
        gulp_popen.wait()


def terminate_processes():
    terminate_process(gulp_popen)
    terminate_process(karma_popen)


def terminate_process(popen):
    terminated = False
    
    if popen is not None and popen.poll() is not None:
        print_formatted("Killing process: " + " ".join(popen.args()), RED)
        popen.terminate()
        terminated = True
    
    return terminated


def print_formatted(text, *formats):
    print(''.join(formats) + text + PLAIN)


if __name__ == "__main__":
    main()
