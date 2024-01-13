#!/usr/bin/python
#
#	Program Description: detect link failure - up/down status from SNMP Trap
#
#	Author: Anthony Chung (after a script by James Yu)
#
#       Last updated: Feb 22, 2022
#

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
                lines.append("%s %s %s %-15s %s %s %s" % (trapDate, trapTime, ip, trap, ifIndex, ifDescr, ifType))
                flag = 'none'

    # print lines in reverse order and only print the first 30 items
    lines = lines[::-1][:30]
    for line in lines:
        print(line)

    fd.close()


process_snmp_trap_log("/home/net484/share/snmpTrap.log")
