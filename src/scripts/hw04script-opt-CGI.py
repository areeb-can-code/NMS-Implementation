#!/usr/bin/python
#
#	Location: ~net484s08/hw04/hw04script.py
#	Author: Areeb Abubaker
#	Date: 02 / 01 / 23
#	Description: analyze the secure log to get user login information
#	Usage: python hw04script.py
#
print("Content-type:text/html\n")
print("<html>")
print("<head>")
print("<title>Account Management</title>")
print("</head>")
print("<h1 align=center> Account Management")
print("</h1")
print("<body>")
import os
from datetime import date, datetime
from math import floor
import cgi

print("<nav>")
print("<ul>")
print("<li><a href='snmpTrap.cgi'>Fault Management</a></li>")
print("<li><a href='config-man.html'>Configuration Management</a></li>")
print("<li><a href='hw04script-opt.cgi'>Accounting Management</a></li>")
print("<li><a href='performance.html'>Performance Management</a></li>")
print("<li><a href='../hw05/hw03Security.cgi'>Security Management</a></li>")
print("</ul>")
print("</nav>")
def get_secure_logs(log_directory):
    """
    Returns a list of all secure logs in the given directory.

    Args:
        log_directory (str): Directory path to look for secure logs.

    Returns:
        list: List of secure logs.
    """
    file_list = []
    for file in os.listdir(log_directory):
        if file.startswith("secure") and not file.endswith("gz"):
            file_list.append(os.path.join(log_directory, file))
    return file_list


def parse_secure_logs(file_list):
    """
    Parses secure logs and returns session information.

    Args:
        file_list (list): List of secure logs.

    Returns:
        tuple: A tuple containing two dictionaries with session information for each account.
    """
    year_add = str(date.today().year)
    time_format = '%Y/%b/%d %H:%M:%S'
    open_time = {}
    session_count = {}
    session_time = {}

    for log_file in file_list:
        with open(log_file, 'r') as fd:
            syslog = fd.readlines()

            for line in syslog:
                data = line.split()
                n = len(data)
                if n < 10:
                    continue

                if (data[6] == "session") and (data[7] == "opened"):
                    try:
                        n1 = data[4].index('[')
                        n2 = data[4].index(']')
                        pid = data[4][n1 + 1: n2]
                    except ValueError:
                        continue

                    user_id = data[10]
                    parsed_time = year_add + "/" + data[0] + "/" + data[1] + " " + data[2]
                    open_time[pid] = datetime.strptime(parsed_time, time_format)

                elif (data[6] == "session") and (data[7] == "closed"):
                    try:
                        n1 = data[4].index('[')
                        n2 = data[4].index(']')
                        pid = data[4][n1 + 1:n2]
                    except ValueError:
                        continue

                    user_id = data[10]
                    parsed_time = year_add + "/" + data[0] + "/" + data[1] + " " + data[2]
                    close_time = datetime.strptime(parsed_time, time_format)

                    if pid in open_time:
                        duration = (close_time - open_time[pid]).seconds
                        if user_id in session_time:
                            session_count[user_id] += 1
                            session_time[user_id] += duration
                        else:
                            session_count[user_id] = 1
                            session_time[user_id] = duration

    return session_count, session_time


def print_summary_report(session_count, session_time):
    """
    Prints a summary report of the session information.

    Args:
        session_count (dict): A dictionary containing the session count for each account.
        session_time (dict): A dictionary containing the session time for each account.
    """
    print("<h1 style='font-family: Arial, sans-serif; font-size: 36px; text-align: center;'>Account Usage Report</h1>\n")
    print("<table align='center' style='border-collapse: collapse; font-family: Arial, sans-serif; font-size: 24px; width: 80%; margin: 0 auto;'>")
    print("<caption style='font-size: 24px; margin-bottom: 20px;'>Session Information</caption>")
    print("<thead>")
    print("<tr>")
    print("<th scope='col' style='background-color: #0072c6; color: #fff; padding: 10px;'>Account</th>")
    print("<th scope='col' style='background-color: #0072c6; color: #fff; padding: 10px;'>Count</th>")
    print("<th scope='col' style='background-color: #0072c6; color: #fff; padding: 10px;'>Total Time</th>")
    print("<th scope='col' style='background-color: #0072c6; color: #fff; padding: 10px;'>Average</th>")
    print("</tr>")
    print("</thead>")
    print("<tbody>")

    for x in sorted(session_count.keys()):
        print("<tr>")
        print("<th scope='row' style='background-color: #f2f2f2; border: 1px solid #ddd; padding: 10px;'>%s</th>" % x)
        print("<td align='center' style='background-color: #fff; border: 1px solid #ddd; padding: 10px;'>%d</td>" % session_count.get(x))
        print("<td align='center' style='background-color: #fff; border: 1px solid #ddd; padding: 10px;'>%.2f seconds</td>" % session_time.get(x))
        print("<td align='center' style='background-color: #fff; border: 1px solid #ddd; padding: 10px;'>%.2f seconds</td>" % float(floor(session_time.get(x) / session_count.get(x))))
        print("</tr>")

    print("</tbody>")
    print("</table>")



log_files = get_secure_logs("/var/log/")
session_count, session_time = parse_secure_logs(log_files)
print_summary_report(session_count, session_time)

print("</body>")
print("</html>")
