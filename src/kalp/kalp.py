#!/usr/bin/env python3

import argparse
import atexit
import os
import os.path
import signal

import knpm
import kutils
import kwatchdog


VERSION = '1.1.1'
WATCHDOGS = []


def main():
    atexit.register(terminate_watchdogs)
    signal.signal(signal.SIGINT, lambda signum, frame: terminate_watchdogs())
    
    opts = parse_args()
    maybe_do_npm_installs(opts)
    start_processes(opts)
    wait_on_watchdogs()


# ################# #
# Options Functions #
# ################# #


def parse_args():
    desc = "A utility to help manage `gulp watch' and `karma' in development enviornments\nVersion: {}".format(VERSION)
    parser = argparse.ArgumentParser(description=desc)
        
    parser.add_argument('--dry-run', action='store_true', default=False, dest='dry_run',
                        help='Just output what actions will be peformed without actually performing them')
    parser.add_argument('-G', '--no-gulp', action='store_true', default=False, dest='no_gulp',
                        help="Do not start the `karma' subprocess (default: %(default)s)")
    parser.add_argument('-K', '--no-karma', action='store_true', default=False, dest='no_karma',
                        help="Do not start the `gulp watch' subprocess (default: %(default)s)")
    parser.add_argument('-R', '--no-restart', action='store_true', default=False, dest='no_restart',
                        help="Do not restart the subprocesses when they die prematurely (default: %(default)s)")
    parser.add_argument('-r', '--root', action='append', default=[], metavar='ROOT', dest='roots',
                        help='Specify a root directory (default: .)')
    
    opts = parser.parse_args()
    opts.roots = [os.getcwd()] if not opts.roots else opts.roots
    validate_directories(opts.roots)
    opts.roots = [os.path.abspath(p) for p in opts.roots]
    
    return opts


def validate_directories(directories):
    for directory in directories:
        if not os.path.exists(directory):
            raise FileNotFoundError(kutils.format_error('Root directory does not exist: {}'.format(directory)))
        elif not os.path.isdir(directory):
            raise NotADirectoryError(kutils.format_error('Root directory is not a directory: {}'.format(directory)))


# ##################### #
# NPM Install Functions #
# ##################### #


def maybe_do_npm_installs(opts):
    for root in opts.roots:
        maybe_do_npm_install(root, opts)


def maybe_do_npm_install(root, opts):
    package_json_dir, package_json = knpm.get_package_json(root)
    uninstalled_deps = knpm.get_uninstalled_dependencies(package_json_dir, package_json)
    out_of_date_deps = knpm.get_out_of_date_dependencies(package_json_dir, package_json)
    has_uninstalled_deps = len(uninstalled_deps) > 0
    has_out_of_date_deps = len(out_of_date_deps) > 0
    
    if has_uninstalled_deps or has_out_of_date_deps:
        kutils.print_titled('npm install required: ', [kutils.BOLD, kutils.CYAN], root, [kutils.BOLD])
        
        if has_uninstalled_deps:
            kutils.print_titled(
                'uninstalled dependencies: ', [kutils.BOLD, kutils.MAGENTA], ', '.join(uninstalled_deps), [])
        
        if has_out_of_date_deps:
            kutils.print_titled(
                'out of date dependencies: ', [kutils.BOLD, kutils.MAGENTA], ', '.join(out_of_date_deps), [])
        
        if not opts.dry_run:
            knpm.npm_install(package_json_dir)


# ####################### #
# Process Mgmt. Functions #
# ####################### #


def start_processes(opts):
    for root in opts.roots:
        start_processes_for_root(opts, root)


def start_processes_for_root(opts, root):
    process_count = 0
    
    kutils.print_titled('starting subprocesses: ', [kutils.BOLD, kutils.CYAN], root, [kutils.BOLD])
    
    if not opts.no_gulp:
        start_gulp_process(opts, root)
        process_count += 1
    
    if not opts.no_karma:
        start_karma_process(opts, root)
        process_count += 1
    
    if process_count == 0:
        kutils.print_formatted('none', kutils.BOLD, kutils.RED)


def start_gulp_process(opts, cwd):
    start_watchdog(opts=opts, cmd=['gulp', 'watch'], cwd=cwd)


def start_karma_process(opts, cwd):
    karma_conf = 'karma.conf.js'
    karma_conf_dir = kutils.find_file_up_hierarchy(cwd, karma_conf)

    if karma_conf_dir is None:
        raise FileNotFoundError(kutils.format_error(
            'Could not start karma because "{}" could not be found.'.format(karma_conf)))
    
    start_watchdog(opts=opts, cmd=['karma', 'start'], cwd=karma_conf_dir)


def start_watchdog(opts, cmd, cwd):
    watchdog = kwatchdog.KWatchdogThread(cmd=cmd, cwd=cwd, keep_alive=not opts.no_restart, dry_run=opts.dry_run)
    watchdog.start()
    WATCHDOGS.append(watchdog)


def wait_on_watchdogs():
    for watchdog in WATCHDOGS:
        watchdog.join()


def terminate_watchdogs():
    for watchdog in WATCHDOGS:
        terminate_watchdog(watchdog)


def terminate_watchdog(watchdog):
    terminated = False
    
    if watchdog is not None and watchdog.is_alive():
        kutils.print_titled('killing process: ', [kutils.BOLD, kutils.RED], ' '.join(watchdog.cmd), [kutils.BOLD])
        watchdog.terminate()
        terminated = True
    
    return terminated


# ########## #
# Main Check #
# ########## #


if __name__ == '__main__':
    main()
