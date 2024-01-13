# ***************************************************
#   module - snmpwalk 
#
#	functions: tripOID, snmpwalk
# ************************************************************
print("Content-type:text/html\n")
print("<html>")
print("<head>")
print("<title>POST SNMPWALK</title>")
print("</head>")
print("<body>")
from pysnmp.entity.rfc3413.oneliner import cmdgen


# *****************************************
#   trimOID - remove the prefix of OID
#   Example:
#        input: 1.3.6.1.2.1.4.21.1.1.192.168.1.0
#	 output: 192.168.1.0
# ******************************************
def trimOID(prefix, oid):
    x = "%s" % (oid)
    n1 = len(prefix)
    n2 = len(x)
    if (n1 >= n2):
        print("Program Assert:", n1, prefix, n2, oid)
    else:
        # print "TRACE:", n1, prefix, n2, x, "==>", x[(n1+1):n2]
        return x[(n1 + 1):n2]


# ***************************************************
#   function: snmpwalk
#   input: host, community, oid
#   port is hard coded = 161
#
#   flag: 0: integer or string    1:IPv4 Address   2:MAC Address
#   return: 
# ***************************************************
def snmpwalk(host, community, prefixOID, flag, snmpTbl):
    cmdGen = cmdgen.CommandGenerator()  # create the object for SNMP API
    errorIndication, retResult, errorIndex, snmpResult = cmdGen.nextCmd(
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
                x = list(map(ord, str(val)))  # need to convert val to str
                ipv4 = "%d.%d.%d.%d" % (x[0], x[1], x[2], x[3])
                snmpTbl[idx] = ipv4
            elif flag == 2:  # MAC Address
                x = list(map(ord, str(val)))
                if len(x) == 6:
                    mac = "%02x-%02x-%02x-%02x-%02x-%02x" % (x[0], x[1], x[2], x[3], x[4], x[5])
                else:
                    mac = 'none'
                snmpTbl[idx] = mac
            else:
                print("Program Assert:", entry, oid, val)

    return 0
print("</body>")
print("</html>")