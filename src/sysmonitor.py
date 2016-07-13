#!/usr/bin/env python3


def main():
    print("Mem: {}%, CPU: {}".format(get_memory_usage(), get_cpu_usage()))


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
    return None


#########################
# System Load Functions #
#########################


def get_system_load():
    pass  # JOE read from /proc/loadavg


if __name__ == '__main__':
    main()
