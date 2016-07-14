#!/usr/bin/env python3


import time


def main():
    print("Mem: {}%, CPU: {}%".format(get_memory_usage(), get_cpu_usage()))


##########################
# Memory Usage Functions #
##########################


def get_memory_usage():
    mem_total, mem_available = _read_meminfo()
    mem_usage = None
    
    if mem_total and mem_available:
        mem_usage = (mem_total - mem_available) / mem_total
    
    return round(mem_usage * 100)


def _read_meminfo():
    mem_total = None
    mem_available = None
    
    with open('/proc/meminfo', 'r') as f:
        line = f.readline()
        
        while (mem_total is None or mem_available is None) and line is not None:
            if line.startswith('MemTotal:'):
                mem_total = int(line.split()[1])
            elif line.startswith('MemAvailable:'):
                mem_available = int(line.split()[1])
            
            line = f.readline()
    
    return mem_total, mem_available


#######################
# CPU Usage Functions #
#######################


def get_cpu_usage():
    cpu_info_1 = _read_cpu_stat()
    cpu_info_2 = None
    delta_idle = None
    delta_total = None
    usage = None
    
    time.sleep(0.25)
    cpu_info_2 = _read_cpu_stat()
    
    delta_idle = cpu_info_2.idle - cpu_info_1.idle
    delta_total = cpu_info_2.total - cpu_info_1.total
    usage = ((delta_total - delta_idle) / delta_total) * 100
    
    return round(usage)


def _read_cpu_stat():
    cpu_info = None
    
    with open('/proc/stat', 'r') as f:
        line = f.readline()
        
        while cpu_info is None and line is not None:
            if line.startswith('cpu '):
                cpu_info = _read_cpu_stat_line(line)
            
            line = f.readline()
    
    return cpu_info


def _read_cpu_stat_line(line):
    parts = line.split()
    
    return CPUInfo(
        user=int(parts[1]),
        system=int(parts[2]),
        nice=int(parts[3]),
        idle=int(parts[4]),
        wait=int(parts[5]),
        irq=int(parts[6]),
        srq=int(parts[7]),
        zero=int(parts[8]))


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
