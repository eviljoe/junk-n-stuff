#!/usr/bin/env python3

from subprocess import Popen
import atexit

gulp_popen = None
karma_popen = None


def kill_subprocesses():
    if gulp_popen is not None and gulp_popen.pole() is not None:
        gulp_popen.terminate()
    if karma_popen is not None and karma_popen.pole() is not None:
        karma_popen.terminate()


gulp_popen = Popen(["gulp", "watch"])
karma_popen = Popen(["karma", "start"])

gulp_popen.wait()
karma_popen.wait()

atexit.register(kill_subprocesses)
