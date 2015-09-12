#!/usr/bin/env python3

import argparse
import atexit
import os
import os.path
from subprocess import Popen

BOLD = "\033[1m"
CYAN = "\033[36m"
RED = '\033[31m'
PLAIN = '\033[0m'

popens = []


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
    global popens
    
    print_formatted("gulp watch", BOLD)
    popens.append(Popen(["gulp", "watch"]))


def start_karma_process():
    global popens
    karma_conf = "karma.conf.js"
    karma_conf_dir = find_file_up_hierarchy(karma_conf)

    if karma_conf_dir is None:
        raise FileNotFoundError(
            RED + BOLD + 'Could not start karma because "' + karma_conf + '" could not be found.' + PLAIN)
    else:
        print_formatted("karma start", BOLD)
        popens.append(Popen(["karma", "start"], cwd=karma_conf_dir))


def find_file_up_hierarchy(file):
    next_path = os.getcwd()
    path = None
    found = False
    
    while not found and path != next_path:
        path = next_path
        found = file in os.listdir(path)
        next_path = os.path.dirname(path)
    
    return path if found else None


def wait_on_processes():
    for popen in popens:
        popen.wait()


def terminate_processes():
    for popen in popens:
        terminate_process(popen)


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
