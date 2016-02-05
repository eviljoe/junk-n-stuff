#!/usr/bin/env python3

import argparse
import atexit
import itertools
import json
import kutils
import os
import os.path
import re
from subprocess import Popen

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
        
    parser.add_argument("--dry-run", action="store_true", default=False, dest="dry_run",
                        help="Just output what actions will be peformed without actually performing them")
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
            raise FileNotFoundError(kutils.format_error("Root directory does not exist: {}".format(directory)))
        elif not os.path.isdir(directory):
            raise NotADirectoryError(kutils.format_error("Root directory is not a directory: {}".format(directory)))


# ##################### #
# NPM Install Functions #
# ##################### #


def do_npm_installs(opts):
    install_needed = False
    
    for root in opts.roots:
        package_json_dir, package_json = get_package_json(root)
        
        if needs_npm_install(package_json_dir, package_json):
            kutils.print_formatted("npm install required: {}".format(root), kutils.BOLD, kutils.CYAN)
            install_needed = True
    
    if not opts.dry_run and install_needed:
        npm_install(package_json_dir)


def get_package_json(root):
    package_json_file = "package.json"
    package_json_dir = kutils.find_file_up_hierarchy(root, package_json_file)
    package_json = None
    
    if package_json_dir is None:
        raise FileNotFoundError(kutils.format_error(
            'Could not check if npm install needed becuase "{}" could not be found.'.format(package_json_file)))
    
    with open(os.path.join(package_json_dir, package_json_file)) as package_json_data:
        package_json = json.load(package_json_data)
    
    return package_json_dir, package_json


def needs_npm_install(package_json_dir, package_json):
    return (dependencies_need_install("devDependencies", package_json_dir, package_json) or
            dependencies_need_install("dependencies", package_json_dir, package_json))


def dependencies_need_install(dependency_type, package_json_dir, package_json):
    it = iter(package_json.get(dependency_type, []))
    dep = next((dependency for dependency in it if dependency_needs_install(
        dependency_type, package_json_dir, package_json, dependency)), None)
    
    return dep is not None


def dependency_needs_install(dependency_type, package_json_dir, package_json, dependency):
    return not (is_dependency_installed(package_json_dir, dependency) and
                is_dependency_is_up_to_date(dependency_type, package_json_dir, package_json, dependency))


def is_dependency_installed(package_json_dir, dependency):
    installed = os.path.isdir(os.path.join(package_json_dir, "node_modules", str(dependency)))
    
    if not installed:
        print(kutils.format_string('Dependency not up to date: ', kutils.BOLD, kutils.MAGENTA), end="")
        print(dependency)
    
    return installed


def is_dependency_is_up_to_date(dependency_type, package_json_dir, package_json, dependency):
    expected_version = package_json[dependency_type][dependency]
    actual_version = None
    up_to_date = False
    
    try:
        with open(os.path.join(package_json_dir, "node_modules", dependency, "package.json")) as package_json_data:
            actual_version = json.load(package_json_data)["version"]
        
        up_to_date = is_version_is_up_to_date(expected_version, actual_version)
    except FileNotFoundError as e:  # Some packages don't actually have a package.json
        up_to_date = True

    if not up_to_date:
        print(kutils.format_string('Dependency not up to date: ', kutils.BOLD, kutils.MAGENTA), end="")
        print(dependency)

    return up_to_date


def is_version_is_up_to_date(expected_version, actual_version):
    up_to_date = False
    
    if expected_version.startswith("^") or expected_version.startswith("~"):
        e_major, e_minor, e_patch = parse_version(expected_version)
        a_major, a_minor, a_patch = parse_version(actual_version)
        
        # major version
        if e_major < a_major:
            up_to_date = True
        elif e_major > a_major:
            up_to_date = False
        # minor version
        elif e_minor < a_minor:
            up_to_date = True
        elif e_minor > a_minor:
            up_to_date = False
        # patch
        else:
            up_to_date = e_patch <= a_patch
    else:
        up_to_date = expected_version == actual_version
    
    return up_to_date


def parse_version(version):
    parts = version.split(sep=".")
    major = int(re.findall(r"\d+", parts[0])[0])
    minor = int(re.findall(r"\d+", parts[1])[0])
    patch = int(re.findall(r"\d+", parts[2])[0])
    
    return major, minor, patch


def npm_install(package_json_dir):
    popen = Popen(["npm", "install"], cwd=package_json_dir)
    popen.wait()


# ####################### #
# Process Mgmt. Functions #
# ####################### #


def start_processes(opts):
    process_count = 0
    
    for root in opts.roots:
        kutils.print_formatted("Starting Processes: {}".format(root), kutils.BOLD, kutils.CYAN)
        
        if not opts.no_gulp:
            start_gulp_process(opts, root)
            process_count += 1
            
        if not opts.no_karma:
            start_karma_process(opts, root)
            process_count += 1
        
        if process_count == 0:
            kutils.print_formatted("None", kutils.BOLD, kutils.RED)


def start_gulp_process(opts, cwd):
    global popens
    
    kutils.print_formatted("gulp watch", kutils.BOLD)
    
    if not opts.dry_run:
        popens.append(Popen(["gulp", "watch"], cwd=cwd))


def start_karma_process(opts, cwd):
    global popens
    karma_conf = "karma.conf.js"
    karma_conf_dir = kutils.find_file_up_hierarchy(cwd, karma_conf)

    if karma_conf_dir is None:
        raise FileNotFoundError(kutils.format_error(
            'Could not start karma because "{}" could not be found.'.format(karma_conf)))
    
    kutils.print_formatted("karma start", kutils.BOLD)
    
    if not opts.dry_run:
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
        kutils.print_formatted("Killing process: {}".format(" ".join(popen.args)), kutils.RED)
        popen.terminate()
        terminated = True
    
    return terminated


if __name__ == "__main__":
    main()
