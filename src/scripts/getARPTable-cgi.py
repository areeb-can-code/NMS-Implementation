#!/usr/bin/python
print("Content-type:text/html\n")
print("<html>")
print("<head>")
print("<title>NET-384 ARP Table</title>")
print("</head>")
print("<body>")

# ****************************************************
#     getARPTable.py
# 	usage: python getARPTable.py <host>
#
#     Description: Get the ARP table from remote host specifying host IP as the first command line argument
#     Date: 02/22/2023
#     Author: Areeb Abubaker
#     Location: /home/net484/student/net484s08/public_html/hw07/getARPTable.py
#     Form Parameters: host = <IP Address>
#
#

#     local Python module: snmpwalk
# ***************************************************
# ***************************************************
#   module - snmpwalk
#
# 	functions: tripOID, snmpwalk
# ************************************************************


# *****************************************
#   trimOID - remove the prefix of OID
#   Example:
#        input: 1.3.6.1.2.1.4.21.1.1.192.168.1.0
#	 output: 192.168.1.0
# ******************************************
from pysnmp.entity.rfc3413.oneliner import cmdgen
import cgi


def trimOID(prefix, oid):
    oid_x = "%s" % oid
    num1_prefix = len(prefix)
    n2 = len(oid_x)
    if num1_prefix >= n2:
        print("Program Assert:", num1_prefix, prefix, n2, oid)
    else:
        # print "TRACE:", n1, prefix, n2, x, "==>", x[(n1+1):n2]
        return oid_x[(num1_prefix + 1):n2]


# ***************************************************
#   function: snmpwalk
#   input: host, community, oid
#   port is hard coded = 161
#
#   flag: 0: integer or string    1:IPv4 Address   2:MAC Address
#   return:
# ***************************************************
def snmpwalk(host, community, prefixOID, flag, snmpTbl):
    cmdGen_snmp = cmdgen.CommandGenerator()  # create the object for SNMP API
    errorIndication, retResult, errorIndex, snmpResult = cmdGen_snmp.nextCmd(
        cmdgen.CommunityData(community),
        cmdgen.UdpTransportTarget((host, 161)),
        prefixOID
    )
    # future work: adding the error checking code here
    # print ("snmpResult Type: ", type(snmpResult), "\n snmpResult: ", snmpResult) ### debug
    for entry in snmpResult:
        # print ("\n entry in snmpResult", entry) ### debug
        for oid, val in entry:
            idx = trimOID(prefixOID, oid)
            if flag == 0:
                snmpTbl[idx] = val
                # print "OID=%s  idx=%s  value=%s" % (oid, idx, val)
            elif flag == 1:  # IP address
                x_list = list(map(ord, str(val)))  # need to convert val to str
                ipv4 = "%d.%d.%d.%d" % (x_list[0], x_list[1], x_list[2], x_list[3])
                snmpTbl[idx] = ipv4
            elif flag == 2:  # MAC Address
                x_list = list(map(ord, str(val)))
                if len(x_list) == 6:
                    mac = "%02x-%02x-%02x-%02x-%02x-%02x" % (
                        x_list[0], x_list[1], x_list[2], x_list[3], x_list[4], x_list[5])
                else:
                    mac = 'none'
                snmpTbl[idx] = mac
            else:
                print("Program Assert:", entry, oid, val)

    return 0


# *********************************************************
#  main program
# *********************************************************
# if (len(sys.argv) == 1):
#    print("syntax: python %s <host>" % sys.argv[0])
#    sys.exit()


community = 'public'

form = cgi.FieldStorage()  # processing the submit form
if form.getvalue('host'):
    host = str(form.getvalue('host'))
else:
    host = "172.26.1.4"  # Linux04 Default Device
cmdGen = cmdgen.CommandGenerator()  # create the object for SNMP API

print("<h1 align=center> ARP Table (host = %s)" % host)
print("</h1>")
# **************************************
#    interface index
# **************************************
oid1 = "1.3.6.1.2.1.2.2.1.1"
n1 = len(oid1)
ifTable = {}
snmpResult = snmpwalk(host, community, oid1, 0, ifTable)

# **************************************
#    interface description (ifDescr)
# **************************************
oid2 = "1.3.6.1.2.1.2.2.1.2"  # ifDescr
tmpTbl = {}
ifDescrTable = {}
snmpResult = snmpwalk(host, community, oid2, 0, tmpTbl)
for x in tmpTbl:
    if x in ifTable:
        ifDescrTable[ifTable[x]] = tmpTbl[x]  # key: ifIndex   val: ifDescr

# **************************************
#    ARP interface index 
# **************************************
oid3 = "1.3.6.1.2.1.4.22.1.1"  # ifIndex
arpIfTable = {}
snmpResult = snmpwalk(host, community, oid3, 0, arpIfTable)

# **************************************
#    ARP IP address
# **************************************
oid4 = "1.3.6.1.2.1.4.22.1.3"  # IP address
arpIPTable = {}
snmpResult = snmpwalk(host, community, oid4, 1, arpIPTable)

# **************************************
#    ARP MAC address
# **************************************
oid5 = "1.3.6.1.2.1.4.22.1.2"  # MAC address
arpMACTable = {}
snmpResult = snmpwalk(host, community, oid5, 2, arpMACTable)

# **********************************************
#   complete reading SNMP data
#   print the ARP table (in HTML FORMAT)
# *********************************************
print("<table align=center border=3>")
print("<th> MIB OID</th>")
print("<th> Interface</th>")
print("<th> IP Address</th>")
print("<th> MAC Address</th>")
for i in arpIfTable:
    if arpIfTable[i] in ifDescrTable:
        ifName = ifDescrTable[arpIfTable[i]]
    else:
        ifName = "N/A(%d)" % arpIfTable[i]
    # print("%20s %12s  %15s  %20s" % (i, ifName, arpIPTable[i], arpMACTable[i]))
    print("<tr>")
    print("<td> %s</td>" % i)
    print("<td align=center> %s</td>" % ifName)
    print("<td align=center> %s</td>" % arpIfTable[i])
    print("<td align=center> %s</td>" % arpMACTable[i])
    print("</tr>")

# End table
print("</table>")
print("</body>")
print("</html>")
