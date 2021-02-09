"""Supervision

Copyright (c) 2021 Thierry P.G. DECKER
All Rights Reserved.
Released under the MIT license

"""
import time

import mariadb
import psutil


def get_net_io_counters():
    """Get the net I/O counters
    """
    return psutil.net_io_counters(
        pernic=True,
        nowrap=False,
    )


def write_to_db(sqlstatement):
    """Write to MariaDB
    """
    try:
        conn = mariadb.connect(
            user="root",
            password="zvxmhwfn",
            host="127.0.0.1",
            port=3306,
            database="supervision"
        )
    except mariadb.Error as e:
        print(f"Error connecting to MariaDB Platform: {e}")
        return
    cur = conn.cursor()
    cur.execute(sqlstatement)
    conn.commit()
    conn.close()
    print(sqlstatement)


def main():
    """The main function"""
    while True:
        try:
            time.sleep(10)
            counters = get_net_io_counters()
            for nic_name in counters:
                host = "localhost"
                bytes_sent = counters[nic_name].bytes_sent
                sqlstatement = f"INSERT INTO " \
                               f"net_io_counter " \
                               f"(" \
                               f"host," \
                               f" nic, " \
                               f"bytes_sent" \
                               f") " \
                               f"VALUES (" \
                               f"'{host}'," \
                               f" '{nic_name}', " \
                               f"'{bytes_sent}')"
                write_to_db(sqlstatement)
        except KeyboardInterrupt:
            break


if __name__ == '__main__':
    main()
