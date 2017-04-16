#!/usr/bin/env python3


import multiprocessing
import os
import os.path

from jnscommons import jnsos

PROC_MEM_FILE = '/proc/meminfo'
PROC_CPU_FILE = '/proc/stat'

SYSMONITOR_CONFIG_DIR = os.path.join(os.path.expanduser('~'), '.jns/sysmonitor')
OLD_CPU_STAT_FILE = 'old-cpu-stat.txt'
OLD_CPU_USAGE_FILE = 'old-cpu-usage.txt'

# The time lengths in /proc/stat are mesured in 1/100ths of a second by default on x86 systems.  These variables are the
# minimum/maximum amount of time between reading the CPU stats that this script will allow.  If the time between
# readings is less than the minimum, the old CPU usage will be used.  If the time between readings is greater than this,
# the CPU usage will be `None'.
#
# The time lengths have to be multiplied by the number of CPU cores in the current computer.  This is becuase the master
# CPU stat line is just a sumation of all the individual CPU cores' stat lines.  So, with an 8 core machine, if a single
# second has passed between readings of the stats, each CPU stat line will have incremented by a second.  That means the
# total stat line will have incremented by 8 seconds.
_CPU_COUNT = multiprocessing.cpu_count()
CPU_STAT_MIN_TIME = 1000 * _CPU_COUNT
CPU_STAT_MAX_TIME = 5000 * _CPU_COUNT


def main():
    _validate_os()
    mem_usage = get_memory_usage()
    cpu_usage = get_cpu_usage()

    print("Mem: {}, CPU: {}".format(
        '--' if mem_usage is None else str(mem_usage) + '%',
        '--' if cpu_usage is None else str(cpu_usage) + '%'))


########################
# Validation Functions #
########################


def _validate_os():
    if not (jnsos.is_linux() or jnsos.is_cygwin()):
        raise OSError('Unsupported operating system: {}.  Only Linux and Cygwin are supported.')


##########################
# Memory Usage Functions #
##########################


def get_memory_usage():
    mem_total, mem_available = _read_meminfo()
    usage = None

    if mem_total and mem_available:
        usage = (mem_total - mem_available) / mem_total * 100

    return round(usage) if usage is not None else None


def _read_meminfo():
    mem_total = None
    mem_available = None  # This is not available in Cygwin, so we have to use MemFree instead
    mem_free = None

    with open(PROC_MEM_FILE, 'r') as f:
        line = f.readline()

        while (mem_total is None or mem_available is None or mem_free is None) and line:
            if line.startswith('MemTotal:'):
                mem_total = int(line.split()[1])
            elif line.startswith('MemAvailable:'):
                mem_available = int(line.split()[1])
            elif line.startswith('MemFree:'):
                mem_free = int(line.split()[1])

            line = f.readline()

    if not mem_available:
        mem_available = mem_free

    return mem_total, mem_available


#######################
# CPU Usage Functions #
#######################


def get_cpu_usage():
    raw_stat_old = _read_cpu_stat(os.path.join(SYSMONITOR_CONFIG_DIR, OLD_CPU_STAT_FILE))
    raw_stat_new = _read_cpu_stat(PROC_CPU_FILE)
    cpu_info_old = _get_cpu_info(raw_stat_old)
    cpu_info_new = _get_cpu_info(raw_stat_new)
    usage = None

    # If there is no old CPU stat reading, create one
    if raw_stat_old is None:
        _write_last_cpu_stat(raw_stat_new)

    # If there is not enough information to calculate the CPU usage.  This can happen if the old CPU info file is empty.
    # The old file can end up empty sometimes if the terminal is closed while this program is running.
    elif not _can_calculate_cpu_usage(cpu_info_old, cpu_info_new):
        _write_last_cpu_stat(raw_stat_new)

    # If we have all the information needed to calculate the CPU usage
    else:
        delta_total = cpu_info_new.total - cpu_info_old.total

        # Too little time has passed between readings
        if delta_total < CPU_STAT_MIN_TIME:
            usage = _read_last_cpu_usage()
        # Too much time has passed between readings
        elif delta_total > CPU_STAT_MAX_TIME:
            _write_last_cpu_stat(raw_stat_new)
        # An acceptable amount of time has passed between readings
        else:
            delta_idle = cpu_info_new.idle - cpu_info_old.idle
            usage = (delta_total - delta_idle) / delta_total * 100

            _write_last_cpu_usage(usage)
            _write_last_cpu_stat(raw_stat_new)

    return round(usage) if usage is not None else None


def _can_calculate_cpu_usage(cpu_info_old, cpu_info_new):
    return (cpu_info_old and
            cpu_info_old.idle and
            cpu_info_old.total and
            cpu_info_new and
            cpu_info_new.idle and
            cpu_info_new.total)


def _read_cpu_stat(stat_file):
    stat = None

    if os.path.exists(stat_file):
        with open(stat_file, 'r') as f:
            stat = f.read()

    return stat


def _write_last_cpu_stat(cpu_stat):
    _make_config_dir()
    with open(os.path.join(SYSMONITOR_CONFIG_DIR, OLD_CPU_STAT_FILE), 'w') as f:
        f.write(cpu_stat)


def _get_cpu_info(cpu_stat):
    cpu_info = None

    if cpu_stat:
        lines_it = iter(cpu_stat.splitlines())
        line = next(lines_it, None)

        while cpu_info is None and line:
            if line.startswith('cpu '):
                cpu_info = _read_cpu_stat_line(line)

            line = next(lines_it, None)

    return cpu_info


def _read_cpu_stat_line(line):
    parts = line.split()

    user, system, nice, idle = parts[1:5]

    if jnsos.is_linux():
        wait, irq, srq, zero = parts[5:9]
    else:
        wait, irq, srq, zero = [0, 0, 0, 0]

    return CPUInfo(
        user=int(user),
        system=int(system),
        nice=int(nice),
        idle=int(idle),
        wait=int(wait),
        irq=int(irq),
        srq=int(srq),
        zero=int(zero))


def _read_last_cpu_usage():
    usage = None
    usage_file = os.path.join(SYSMONITOR_CONFIG_DIR, OLD_CPU_USAGE_FILE)

    if os.path.exists(usage_file):
        with open(usage_file, 'r') as f:
            try:
                usage = float(f.readline())
            except ValueError:
                usage = None

    return usage


def _write_last_cpu_usage(usage):
    _make_config_dir()

    with open(os.path.join(SYSMONITOR_CONFIG_DIR, OLD_CPU_USAGE_FILE), 'w') as f:
        f.write(str(usage))

#####################
# Utility Functions #
#####################


def _make_config_dir():
    if not os.path.isdir(SYSMONITOR_CONFIG_DIR):
        os.makedirs(SYSMONITOR_CONFIG_DIR)


###########
# Classes #
###########


class CPUInfo:
    def __init__(self, user, system, nice, idle, wait, irq, srq, zero):
        self.user = user
        self.system = system
        self.nice = nice
        self.idle = idle
        self.wait = wait
        self.irq = irq
        self.srq = srq
        self.zero = zero
        self.total = user + system + nice + idle + wait + irq + srq + zero


if __name__ == '__main__':
    main()
