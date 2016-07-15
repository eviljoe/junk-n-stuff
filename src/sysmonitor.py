#!/usr/bin/env python3


import time

from jnscommons import jnsos


def main():
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
    
    with open('/proc/meminfo', 'r') as f:
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
    cpu_info_1 = _read_cpu_stat()
    usage = None
    
    if cpu_info_1.idle and cpu_info_1.total:
        time.sleep(0.25)
        cpu_info_2 = _read_cpu_stat()
        
        if cpu_info_2.idle and cpu_info_2.total:
            delta_idle = cpu_info_2.idle - cpu_info_1.idle
            delta_total = cpu_info_2.total - cpu_info_1.total
            usage = (delta_total - delta_idle) / delta_total * 100
    
    return round(usage) if usage is not None else None


def _read_cpu_stat():
    cpu_info = None
    
    with open('/proc/stat', 'r') as f:
        line = f.readline()
        
        while cpu_info is None and line:
            if line.startswith('cpu '):
                cpu_info = _read_cpu_stat_line(line)
            
            line = f.readline()
    
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
