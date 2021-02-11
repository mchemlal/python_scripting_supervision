"""Module name.

Copyright (c) 2021 Thierry P.G. DECKER
All Rights Reserved.
Released under the MIT license

"""

import time
import datetime

import psutil
import mariadb


def write_to_database(sql_statement):
    """Write to the database

    Args:
        sql_statement (str) : the SQL statement to execute
    """
    print(sql_statement)
    #
    # Connexion to DB
    #
    try:
        conn = mariadb.connect(
                user="root",
                password="zvxmhwfn",
                host="localhost",
                port=3306,
                database="live_demo"

        )
    except mariadb.Error as e:
        print(f"Error connecting to MariaDB Platform: {e}")
        return
    #
    # Cursor create
    #
    cur = conn.cursor()
    #
    # Execute SQL statement
    #
    cur.execute(sql_statement)
    #
    # Commit DB
    #
    conn.commit()
    #
    # Close connection
    #
    conn.close()


def get_cpu_percent():
    """Collect cpu usage

    Returns: Usage ratio of CPUs
    """
    return psutil.cpu_percent(
            interval=None,
            percpu=False
    )


def get_virtual_memory():
    """Get the virtual memory stats

    Returns: The virtual memory stats

    Available fields : total, availbale, percent, used, free
    """
    stats = psutil.virtual_memory()
    my_stats = [
        "total: " + str(stats.total),
        ", available: " + str(stats.available),
        ", percent: " + str(stats.percent),
        ", used: " + str(stats.used),
        ", free: " + str(stats.free),
    ]
    return "".join(my_stats)


def write_to_file(text):
    """Write string into a file

    Args:
        text (str): The text to insert into the file

    Returns: None
    """
    with open("my_file.txt", "a+") as file:
        file.write(text + "\n")


def main():
    """The main function"""
    while True:
        try:
            time.sleep(5)
            #
            # Gett CPU percent
            #
            cpu_percent = get_cpu_percent()
            #
            # Write to file
            #
            file_line = f"{datetime.datetime.now()}, CPU percent: {cpu_percent} %"
            write_to_file(file_line)
            #
            # Write to DB
            #
            sql_statement = f"INSERT INTO cpu_percent " \
                            f"(counter) " \
                            f"VALUES " \
                            f"({cpu_percent})"
            write_to_database(sql_statement)
            #
            # Get virtual memory stats
            #
            file_line = f"{datetime.datetime.now()}, Memory stats: {get_virtual_memory()}"
            write_to_file(file_line)

        except KeyboardInterrupt:
            break


if __name__ == '__main__':
    main()

