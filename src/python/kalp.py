#!/usr/bin/env python3

import argparse
import atexit
import itertools
import json
import os
import os.path
from subprocess import Popen

BOLD = "\033[1m"
CYAN = "\033[36m"
RED = '\033[31m'
PLAIN = '\033[0m'
VERSION = 1.1

popens = []


def main():
    atexit.register(terminate_processes)
    opts = parse_args()
    do_npm_installs(opts)
    start_processes(opts)
    wait_on_processes()


# ################# #
# Options Functions #
# ################# #


def parse_args():
    desc = "A utility to help manage `gulp watch' and `karma' in development enviornments\nVersion: {}".format(VERSION)
    parser = argparse.ArgumentParser(description=desc)
        
    parser.add_argument("-G", "--no-gulp", action="store_true", default=False, dest="no_gulp",
                        help="Do not start the `karma' subprocess (default: %(default)s)")
    parser.add_argument("-K", "--no-karma", action="store_true", default=False, dest="no_karma",
                        help="Do not start the `gulp watch' subprocess (default: %(default)s)")
    parser.add_argument("-r", "--root", action="append", default=[], metavar="ROOT", dest="roots",
                        help="Specify a root directory (default: .)")
    
    opts = parser.parse_args()
    opts.roots = [os.getcwd()] if not opts.roots else opts.roots
    validate_directories(opts.roots)
    opts.roots = list(map(lambda root: os.path.abspath(root), opts.roots))
    
    return opts


def validate_directories(directories):
    for directory in directories:
        if not os.path.exists(directory):
            raise FileNotFoundError(format_error("Root directory does not exist: {}".format(directory)))
        elif not os.path.isdir(directory):
            raise NotADirectoryError(format_error("Root directory is not a directory: {}".format(directory)))


# ##################### #
# NPM Install Functions #
# ##################### #


def do_npm_installs(opts):
    for root in opts.roots:
        package_json_dir, package_json = get_package_json(root)
        
        if needs_npm_install(package_json_dir, package_json):
            print_formatted("npm install required: {}".format(root), BOLD, CYAN)
            npm_install(package_json_dir)


def get_package_json(root):
    package_json_file = "package.json"
    package_json_dir = find_file_up_hierarchy(root, package_json_file)
    package_json = None
    
    if package_json_dir is None:
        raise FileNotFoundError(format_error(
            'Could not check if npm install needed becuase "{}" could not be found.'.format(package_json_file)))
    
    with open(os.path.join(package_json_dir, package_json_file)) as package_json_data:
        package_json = json.load(package_json_data)
    
    return package_json_dir, package_json


def needs_npm_install(package_json_dir, package_json):
    return (dependencies_need_install("devDependencies", package_json_dir, package_json) or
            dependencies_need_install("dependencies", package_json_dir, package_json))


def dependencies_need_install(dependency_type, package_json_dir, package_json):
    need_install = False
    done = object()
    it = iter(package_json.get(dependency_type, []))
    dependency = next(it, done)
    
    print(dependency_type)
    
    while dependency is not done and not need_install:
        need_install = dependency_needs_install(dependency_type, package_json_dir, package_json, dependency)
        dependency = next(it, done)


def dependency_needs_install(dependency_type, package_json_dir, package_json, dependency):
    return not (dependency_installed(package_json_dir, dependency) and
                dependency_has_correct_version(dependency_type, package_json_dir, package_json, dependency))


def dependency_installed(package_json_dir, dependency):
    return os.path.isdir(os.path.join(package_json_dir, "node_modules", str(dependency)))


def dependency_has_correct_version(dependency_type, package_json_dir, package_json, dependency):
    print("type={}, dependency={}, version={}".format(dependency_type, dependency, package_json[dependency_type][dependency]))  # JOE o
    expected_version = package_json[dependency_type][dependency]
    actual_version = None
    correct = False
    
    with open(os.path.join(package_json_dir, "node_modules", dependency, "package.json")) as package_json_data:
        actual_version = json.load(package_json_data)["version"]
    
    return True
    
    
def npm_install(package_json_dir):
    popen = Popen(["npm", "install"], cwd=package_json_dir)
    popen.wait()


# ####################### #
# Process Mgmt. Functions #
# ####################### #


def start_processes(opts):
    process_count = 0
    
    for root in opts.roots:
        print_formatted("Starting Processes: {}".format(root), BOLD, CYAN)
        
        if not opts.no_gulp:
            start_gulp_process(root)
            process_count += 1
            
        if not opts.no_karma:
            start_karma_process(root)
            process_count += 1
        
        if process_count == 0:
            print_formatted("None", BOLD, RED)


def start_gulp_process(cwd):
    global popens
    
    print_formatted("gulp watch", BOLD)
    popens.append(Popen(["gulp", "watch"], cwd=cwd))


def start_karma_process(cwd):
    global popens
    karma_conf = "karma.conf.js"
    karma_conf_dir = find_file_up_hierarchy(cwd, karma_conf)

    if karma_conf_dir is None:
        raise FileNotFoundError(format_error(
            'Could not start karma because "{}" could not be found.'.format(karma_conf)))
    
    print_formatted("karma start", BOLD)
    popens.append(Popen(["karma", "start"], cwd=karma_conf_dir))


def wait_on_processes():
    for popen in popens:
        popen.wait()


def terminate_processes():
    for popen in popens:
        terminate_process(popen)


def terminate_process(popen):
    terminated = False
    
    if popen is not None and popen.poll() is None:
        print_formatted("Killing process: {}".format(" ".join(popen.args)), RED)
        popen.terminate()
        terminated = True
    
    return terminated


# ################# #
# Utility Functions #
# ################# #


def find_file_up_hierarchy(root, file):
    next_path = root
    path = None
    found = False
    
    while not found and path != next_path:
        path = next_path
        found = file in os.listdir(path)
        next_path = os.path.dirname(path)
    
    return path if found else None


def format_error(text):
    return format_string(text, BOLD, RED)


def format_string(text, *formats):
    return ''.join(formats) + text + PLAIN


def print_formatted(text, *formats):
    print(format_string(text, *formats))


if __name__ == "__main__":
    main()
