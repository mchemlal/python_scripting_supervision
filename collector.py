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
    return psutil.cpu_percent(interval=0.1, percpu=True)


def get_memory_percent():
    p = psutil.Process()
    return p.memory_percent(memtype="rss")


def get_disk_usage():
    return psutil.disk_io_counters(perdisk=False, nowrap=True)


def get_net_io_counters_byte_sent():
    return psutil.net_io_counters(pernic=False).bytes_sent


def get_net_io_counters_byte_recv():
    return psutil.net_io_counters(pernic=False).bytes_recv


def main():
    if __name__ == '__main__':
        main()
