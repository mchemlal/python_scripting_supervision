"""Module de Supervision de données

-> giving a monitoring overview of my MacBook Machine

Copyright (c) 2021 Morade Chemlal
All Rights Reserved.
Released under the MIT license
DOC STRING

"""

#
# importing the libraries necessary to the module definition
#
import time
import mariadb
import psutil
import datetime


def get_battery_state():
    """
        Collect the battery state in real time in percent

        return: rate of use related to cpu
    """
    battery = psutil.sensors_battery().percent
    return battery


def get_cpu_percent():
    """
    Collect the cpu usage in percent

    return: rate of use related to cpu
    """

    return psutil.cpu_percent(interval=1, percpu=False)


def get_virtual_memory():
    """
    Collect the virtual memory readings

    if statement -> level over limit = warning statement

    return: memory readings
    """
    mem = psutil.virtual_memory()
    memory_stats = ["total -> " + str(mem.total) + " bytes",
                    "/ available -> " + str(mem.available) + " bytes",
                    "/ percent available -> " + str(mem.percent) + " %",
                    "/ memory used -> " + str(mem.used) + " bytes",
                    "/ memory left -> " + str(mem.free) + " bytes",
                    ]

    THRESHOLD = 100 * 1024 * 1024  # 100MB
    if mem.available <= THRESHOLD:
        print("warning")

    return memory_stats


"""
variables dedicated to be inserted into the fast strings in the VIRTUAL MEMORY query
"""
virtual_memory_total = psutil.virtual_memory().total
virtual_memory_available = psutil.virtual_memory().available
virtual_memory_percent = psutil.virtual_memory().percent
virtual_memory_used = psutil.virtual_memory().used
virtual_memory_free = psutil.virtual_memory().free


def get_disk_usage():
    """
        Collect readings related to disk usage

        if statement -> level over limit = warning statement

        return: disk usage
        """
    disk_usage = psutil.disk_usage('/')
    disk_stats = [
        " total available -> " + str(disk_usage.total) + " bytes",
        " used -> " + str(disk_usage.used) + " bytes",
        " available -> " + str(disk_usage.free) + " bytes",
        " used rate -> " + str(disk_usage.percent) + " %",
    ]

    if disk_usage.percent >= 80:
        print("you clear space in your machine")

    return disk_stats


"""
variables dedicated to be inserted into the fast strings in the DISK USAGE query 
"""
disk_usage_total = psutil.disk_usage('/').total
disk_usage_used = psutil.disk_usage('/').used
disk_usage_free = psutil.disk_usage('/').free
disk_usage_percent = psutil.disk_usage('/').percent


def get_net_io_counters_byte_sent():
    """
    collect the amount of network bytes sent
    return: bytes sent
    """
    return psutil.net_io_counters().bytes_sent


def get_net_io_counters_byte_recv():
    """
    collect the amount of network bytes received
    return: bytes received
    """
    return psutil.net_io_counters(pernic=False).bytes_recv


def insert_intodatabase_record(sql_statement):
    """"
    Function insert_intodatabase_record

    Handle the connection to mariadb

    @param: sql_statement
    """

    try:
        """
        connection details to the database
        """
        data_connect = mariadb.connect(
            user="root",
            password="Michel0405",
            host="localhost",
            port=3306,
            database="supervision"
        )
    except mariadb.Error as e:
        print("Connexion failed : " + e)
        return

    # create Cursor
    cursor = data_connect.cursor()

    # SQL execution
    cursor.execute(sql_statement)

    # commit the query
    data_connect.commit()

    # close de connection
    data_connect.close()


def main():
    """
    the main function dedicated  to executing the program
    """
    while True:
        #
        # calling function stored into variable
        #
        try:
            data_cpu = get_cpu_percent()
            data_memory = get_virtual_memory()
            data_disk = get_disk_usage()
            data_byte_sent = get_net_io_counters_byte_sent()
            data_byte_recv = get_net_io_counters_byte_recv()
            data_battery = get_battery_state()

            """
            while loop to loop over the overall readings every 10 seconds 
            """
            time.sleep(10)
            """
            data recorded into the data.txt file with the write() function
            using the variable writen above into the the fast strings down below
            """
            f = open("data.txt", "a+")
            f.write("\n")
            f.write("----------------**EACH SESSION IS REFRESHED EVERY 10 SECONDS**"
                    "--------------------------------------\n")
            f.write("< CPU READINGS >")
            f.write("\n")
            f.write(f"{datetime.datetime.now()} -> {data_cpu} \n")
            f.write("\n")
            f.write("< VIRTUAL MEMORY READINGS >")
            f.write("\n")
            f.write(f"{datetime.datetime.now()} -> {data_memory} \n")
            f.write("\n")
            f.write("< DISK READINGS >")
            f.write("\n")
            f.write(f"{datetime.datetime.now()} -> {data_disk} \n")
            f.write("\n")
            f.write("< NETWORK DATA >")
            f.write("\n")
            f.write(f"{datetime.datetime.now()} -> data received : {data_byte_recv} \n")
            f.write(f"{datetime.datetime.now()} -> data sent : {data_byte_sent} \n")
            f.write("\n")
            f.write("< BATTERY DATA > \n")
            f.write(f"{datetime.datetime.now()} -> {data_battery} % left \n")
            f.write("-----------------**HOLD ON THE NEXT BATCH LOADING IN THE NEXT 10 "
                    "SECONDS**------------------------------")
            f.write("\n")
            f.write("\n")
            """
            closing the access in writing into data.txt 
            """
            f.close()
            """
            inserting data to the VIRTUAL MEMORY TABLE
            """
            data_memory_query = f"INSERT INTO virtual_memory" \
                                f"(available, free, percent, total, used)" \
                                f"VALUES" \
                                f"({virtual_memory_available}, " \
                                f"{virtual_memory_free}," \
                                f"{virtual_memory_percent}," \
                                f"{virtual_memory_total}," \
                                f"{virtual_memory_used})"
            insert_intodatabase_record(data_memory_query)

            """
            inserting data to the DISK USAGE TABLE
            """
            data_memory_query = f"INSERT INTO disk_usage" \
                                f"(free, percent, total, used)" \
                                f"VALUES" \
                                f"({disk_usage_free}, " \
                                f"{disk_usage_percent}," \
                                f"{disk_usage_total}," \
                                f"{disk_usage_used})"
            insert_intodatabase_record(data_memory_query)

            """
            inserting data to the DESCENDING NETWORK TABLE
            """
            data_memory_query = f"INSERT INTO descending_network_flow" \
                                f"(byte_recv)" \
                                f"VALUES" \
                                f"({data_byte_recv})"

            insert_intodatabase_record(data_memory_query)

            """
            inserting data to the ASCENDING NETWORK TABLE
            """
            data_memory_query = f"INSERT INTO ascending_network_flow" \
                                f"(byte_sent)" \
                                f"VALUES" \
                                f"({data_byte_sent})"

            insert_intodatabase_record(data_memory_query)

            """
            inserting data to the CPU PERCENT TABLE
            """
            data_memory_query = f"INSERT INTO cpu_percent" \
                                f"(cpu)" \
                                f"VALUES" \
                                f"({data_cpu})"

            insert_intodatabase_record(data_memory_query)

            """
            inserting data to the BATTERY TABLE
            """
            data_memory_query = f"INSERT INTO battery" \
                                f"(battery_level)" \
                                f"VALUES" \
                                f"({data_battery})"

            insert_intodatabase_record(data_memory_query)

        except KeyboardInterrupt:
            break
        """
        exit condition 
        """


if __name__ == '__main__':
    main()
