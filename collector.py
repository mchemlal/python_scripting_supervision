"""Supervision

Copyright (c) 2021 Thierry P.G. DECKER
All Rights Reserved.
Released under the MIT license

"""

import time

import psutil


def get_cpu_percent():
    """Get the net I/O counters
    """
    return psutil.cpu_percent(interval=None, percpu=True)


def get_memory_percent():
    p = psutil.Process()
    return p.memory_percent(memtype="rss")


def get_disk_usage():
    return psutil.disk_io_counters(perdisk=False, nowrap=True)


def get_net_io_counters_byte_sent():
    return psutil.net_io_counters(pernic=False).bytes_sent


def get_net_io_counters_byte_recv():
    return psutil.net_io_counters(pernic=False).bytes_recv


data = get_net_io_counters_byte_recv()
data_memory = get_memory_percent()
array_data = []

for index, line in enumerate(data):
    """f = open('data.txt', 'w')
    array_data.append(data)
    f.write(str(data) + '\n')
    f.close()"""
    print(data[index])


def main():
    print("hello world")


if __name__ == '__main__':
    main()
