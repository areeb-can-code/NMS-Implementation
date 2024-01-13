#!/usr/bin/python
# ****************************************************
#     getRoutingTable.py
# this is a CGI adjusted script
# usage: python getRoutingTable.py <host> <vlan>
#
#     Description: get the IP Routing table from remote host/router
#     Date: 02/23/2023
#     Author: Areeb Abubaker
#     Location: /home/net484/student/net484s08/public_html/hw07/getRoutingTable.cgi
#     CGI - Form parameters : host = <IP Address>
# ***************************************************
print("Content-type:text/html\n")
print("<html>")
print("<head>")
print("<title>NET-384 IP Routing Table</title>")
print("</head>")
print("<body>")

import sys
import snmpwalk
import cgi

RouteTypeList = ('unknown', 'other', 'valid', 'direct', 'indirect', 'undefined')  # use tuple
RouteProtoList = ( # all routing names or routing protocols
    'unknown', 'other', 'local', 'netmgmt', 'icmp', 'egp', 'ggp', 'hello', 'rip', 'is-is', 'es-is', 'igrp', 'bbn',
    'ospf',
    'bgp', 'undefined')

# *********************************************************
#  main program
# *********************************************************
form = cgi.FieldStorage()  # processing the submit form
if form.getvalue('host'):
    host = str(form.getvalue('host'))
else:
    host = "172.26.1.4"  # Linux04 Default Device
# if (len(sys.argv) == 1):
#   print("syntax: python %s <host>" % sys.argv[0])
#   sys.exit()
print("<h1 align=center> IP Routing Table (host = %s)" % host)
print("</h1>")
# host = sys.argv[1]
community = 'public'

# **************************************
#    interface index
# **************************************
oidx = "1.3.6.1.2.1.2.2.1.1"
ifTable = {}
snmpResult = snmpwalk.snmpwalk(host, community, oidx, 0, ifTable)

# **************************************
#    interface description (ifDescr)
# **************************************
oidy = "1.3.6.1.2.1.2.2.1.2"  # ifDescr
tmpTbl = {}
ifDescrTable = {}
snmpResult = snmpwalk.snmpwalk(host, community, oidy, 0, tmpTbl)
for x in tmpTbl:
    if x in ifTable:
        ifDescrTable[ifTable[x]] = tmpTbl[x]  # key: ifIndex   val: ifDescr

# **************************************
#    ipRouteDest 
# **************************************
oid1 = "1.3.6.1.2.1.4.21.1.1"
ipRouteDest = {}
snmpwalk.snmpwalk(host, community, oid1, 1, ipRouteDest)

# **************************************
#    ipRouteIf 
# **************************************
oid2 = "1.3.6.1.2.1.4.21.1.2"
tmpTbl = {}
ipRouteIfTbl = {}
snmpwalk.snmpwalk(host, community, oid2, 0, tmpTbl)
for x in tmpTbl:
    y = tmpTbl[x]

    if y == 0:
        ipRouteIfTbl[x] = 'default'  ### modified ipRouteTbl to ipRouteIfTbl
    elif y in ifDescrTable:
        ipRouteIfTbl[x] = ifDescrTable[y]
    else:
        print("Program Assert: unknown routeIfIndex=", y)

# **************************************
#    ipRouteNextHop 
# **************************************
oid7 = "1.3.6.1.2.1.4.21.1.7"
ipRouteNextHop = {}
snmpwalk.snmpwalk(host, community, oid7, 1, ipRouteNextHop)

# **************************************
#    ipRouteType 
# **************************************
oid8 = "1.3.6.1.2.1.4.21.1.8"
ipRouteType = {}
snmpwalk.snmpwalk(host, community, oid8, 0, ipRouteType)

oid9 = "1.3.6.1.2.1.4.21.1.9"
ipRouteProto = {}
snmpwalk.snmpwalk(host, community, oid9, 0, ipRouteProto)

oid11 = "1.3.6.1.2.1.4.21.1.11"
ipRouteMask = {}
snmpwalk.snmpwalk(host, community, oid11, 1, ipRouteMask)

# **********************************************
#   complete reading SNMP data
#   print the routing table
# *********************************************
print("<table align=center border=3>")
print("<th> MIB OID</th>")
print("<th>  Route Destination</th>")
print("<th> Next Hope (Gateway)</th>")
print("<th> Interface</th>")
print("<th>Route Type </th>")
print("<th>Route Protocol</th>")
print("<th>Network Mask</th>")
# print("%16s %16s %16s %16s %12s %16s %18s\n" % (
# 'OID', 'ipRouteDest', 'ipRouteNextHop', 'ipRouteifDescr',
# 'ipRouteType', 'ipRouteProto', 'ipRouteMask'))
for i in ipRouteDest:
    rtype = RouteTypeList[ipRouteType[i]]
    rproto = RouteProtoList[ipRouteProto[i]]
    # print("%16s %16s %16s %16s %9s(%d) %12s(%2d) %18s" % (
    #    i,
    #       ipRouteDest[i],
    #           ipRouteNextHop[i],
    #               ipRouteIfTbl[i],
    #                   rtype,
    #                       ipRouteType[i],
    #                               rproto,
    #                                   ipRouteProto[i],
    #                                           ipRouteMask[i]))
    print("<tr>")
    print("<td> %s</td>" % i)
    print("<td align=center> %s</td>" % ipRouteDest[i])
    print("<td align=center> %s</td>" % ipRouteNextHop[i])
    print("<td align=center> %s</td>" % ipRouteIfTbl[i])
    print("<td align=center> %s (%d)</td>" % (rtype, ipRouteType[i]))
    print("<td align=center> %s (%d) </td>" % (rproto, ipRouteProto[i]))
    print("<td align=center> %s</td>" % ipRouteMask[i])
    print("</tr>")

# End table
print("</table>")
print("</body>")
print("</html>")
