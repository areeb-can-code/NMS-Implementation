#!/usr/bin/python
# /home/net484/student/net484s08/hw03/hw03script.py
#
# Author: Areeb Abubaker (for an hw03)
# Date: 01/25/23
# Description: Listing the intrusions of the IP addresses sorted by their frequency from greatest to least
#
# Open the log file located in /var/log/secure.log
import pygeoip
import os


def print_intrusion_report(log_directory):
    """
    Prints a report of intrusion attempts from log files.

    Args:
        log_directory (str): The directory containing the log files.

    Returns:
        None
    """
    file_list = []
    countTable = {}

    # loop through all the files in the directory
    for file in os.listdir(log_directory):
        if file.startswith("secure"):
            syslog = log_directory + "/" + file
            if not file.endswith("gz"):
                file_list.append(syslog)

    # loop through all the files in file_list
    for log_file in file_list:
        with open(log_file) as fd:
            syslog = fd.readlines()

        for line in syslog:
            data = line.split()
            # Filter by only the data that has root attempts
            if len(data) >= 15 and data[14].__contains__("user=root"):
                rHost = str(data[13].split("=")[1])
                # if not rHost not in dictionary, then put it in and set it equal to 1
                if rHost not in countTable:
                    countTable.update({rHost: int(1)})
                else:  # otherwise update the count values
                    countTable.update({rHost: (countTable.get(rHost) + int(1))})

    # Sorting the table with a lambda function, in REVERSE ORDER
    countTableSort = dict(sorted(countTable.items(), key=lambda item: item[1], reverse=True))
    db = pygeoip.GeoIP('/home/spyrailkoala/Documents/BlizzardDepSeason/ChugChug/GeoLiteCity.dat')
    # Print report
    print(f'{str("Intrusion IP Address"):>60}', f'{str("Count"):>10}', f'{str("City"):>20}', f'{str("Country"):>25}')
    print(
        "----------------------------------------------------------------------------------------------------------------------")

    for key, value in countTableSort.items():
        if value >= 31:
            gi = db.record_by_addr(key)
            if gi is None:
                print(f'{str(key):>60}', f'{str(value):>10}', f'{str("None"):>18}', f'{str("None"):>28}')
            else:
                print(f'{str(key):>60}', f'{str(value):>10}',
                      f'{str((gi["city"])):>20}' f'{str((gi["country_code"])):>25}')


# example usage
log_directory = os.getcwd()
print_intrusion_report(log_directory)
