#!/usr/bin/python
#
#	Program Description: detect link failure - up/down status from SNMP Trap
#
#	Author: Anthony Chung (after a script by James Yu)
#
#       Last updated: Feb 22, 2022
#
print("Content-type:text/html\n")
print("<html>")
print("<head>")
print("<title>SNMP Trap - Interface Information</title>")
print("<link rel='stylesheet' type='text/css' href='style.css'>")
print("</head>")
print("<h1 align=center> Fault Management using SNMP Traps")
print("</h1")
print("<body>")
print("<nav>")
print("<ul>")
print("<li><a href='../project/snmpTrap.cgi'>Fault Management</a></li>")
print("<li><a href='../project/config-man.html'>Configuration Management</a></li>")
print("<li><a href='../project/hw04script-opt.cgi'>Accounting Management</a></li>")
print("<li><a href='../project/performance.html'>Performance Management</a></li>")
print("<li><a href='../hw05/hw03Security.cgi'>Security Management</a></li>")
print("</ul>")
print("</nav>")

from datetime import date


def process_snmp_trap_log(log_path):
    """
    Processes SNMP trap log file and prints information about traps related to interface information

    Args:
    log_path (str): The path to the SNMP trap log file to process

    Returns:
    None
    """
    year = str(date.today().year)  # current year
    with open(log_path, "r") as fd:
        trapData = fd.readlines()

    flag = 'none'
    lines = []  # store lines in a list
    for line in trapData:
        inline = line.rstrip('\n')
        items = inline.split()

        if not items:
            continue  # skip empty lines

        if items[0].find(year) == 0:  # check SNMP trap of the current year
            trapDate = items[0]
            trapTime = items[1]
            ip = items[2].split('(')[0]  # get only the ip address
            if len(items) > 9 and items[7] == 'v1,':
                flag = 'dateline'
            else:
                flag = 'none'
        elif flag == 'dateline' and items[0] == 'SNMPv2-SMI::enterprises.9.1.359':
            trap = " %s_%s_%s" % (items[1], items[2], items[3])
            flag = 'trap359'
        elif flag == 'trap359' and inline.find('IF-MIB') > 0:
            n = len(items)
            i = 0
            while i < n:
                if items[i].find('IF-MIB::ifIndex') == 0:
                    i += 3
                    ifIndex = items[i]
                    flag = 'if_info_found'
                elif items[i].find('IF-MIB::ifDescr') == 0:
                    i += 3
                    ifDescr = items[i].replace('"', '')
                elif items[i].find('IF-MIB::ifType') == 0:
                    i += 3
                    ifType = items[i][-2]
                i += 1
            # end (while)
            if flag == 'if_info_found':
                status_class = 'status-up' if 'Up' in trap else 'status-down'
                status_icon = 'fa-check-circle' if 'Up' in trap else 'fa-exclamation-circle'
                status_text = 'Link Up' if 'Up' in trap else 'Link Down'
                line = "<tr>"
                line += "<td> %s </td>" % (trapDate)
                line += "<td> %s </td>" % (trapTime)
                line += "<td> %s </td>" % (ip)
                line += "<td> %s </td>" % (ifDescr)
                line += "<td class='%s'>" % status_class
                line += "  <span class='status-icon'>"
                line += "    <i class='fas %s'></i>" % status_icon
                line += "  </span>"
                line += "  %s" % status_text
                line += "</td>"
                line += "</tr>"
                lines.append(line)
            print("</tbody>")
    fd.close()
    return reversed(lines)


print("<table class='table' align='center'>")
print("<thead>")
print("<tr>")
print("<th scope='col'>Date</th>")
print("<th scope='col'>Time</th>")
print("<th scope='col'>Device</th>")
print("<th scope='col'>Interface</th>")
print("<th scope='col'>Status</th>")
print("</tr>")
print("</thead>")
count = 0
for line in process_snmp_trap_log("/home/net484/share/snmpTrap.log"):
    print(line)
    count += 1
    if count == 30:
        break
print("</table>")
print("</body>")
print("</html>")
