#!/usr/bin/python
print("Content-type:text/html\n")
print("<html>")
print("<head>")
print("<title>NET-384 MAC Address Table - NET 384 </title>")
print("</head>")
print("<body>")

# Imports
import snmpwalk
import cgi

# main program
# if len(sys.argv) != 3:
#    print("syntax: python %s <host> <vlan>" % (sys.argv[0]))
#    sys.exit()

# host = sys.argv[1]
# vlan = sys.argv[2]


form = cgi.FieldStorage()  # processing the submit form
if form.getvalue('host'):
    host = str(form.getvalue('host'))  # assigning host to the first form submit form
else:
    host = "192.168.1.1"  # Default Switch 01
if form.getvalue('vlan'):
    vlan = str(form.getvalue('vlan'))  # assigning vlan to the second form submit form
else:  # Default VLAN 1
    vlan = 1

print("<h1 align=center> MAC Address Table for <br> Switch = %s and VLAN = %s" % (host, vlan))
print("</h1>")  # Printing out the header for the page
community = 'public' + '@' + vlan

oid1 = '1.3.6.1.2.1.17.4.3.1.1'  # MAC address in the MAC forwarding table
oid2 = '1.3.6.1.2.1.17.4.3.1.2'  # Interface (ifIndex) in the MAC forwarding table
oid3 = '1.3.6.1.2.1.2.2.1.2'  # Interface description

tbl1 = {}  # Empty Dict to contain the MAC Addr
snmpwalk.snmpwalk(host, community, oid1, 2, tbl1)
tbl2 = {}  # Empty Dict to contain the ifIndex of all devices' MAC Address
snmpwalk.snmpwalk(host, community, oid2, 0, tbl2)
tbl3 = {}  # Empty Dict to contain the Interface description or IfDescr
snmpwalk.snmpwalk(host, community, oid3, 0, tbl3)

# Headers for the tables
print("<table align=center border=3>")
print("<th> MIB OID</th>")
print("<th> Interface</th>")
print("<th> MAC Address</th>")

# print("{:<25} {:<35} {:<25}".format("MIB OID", "Interface", "MAC Address"))  # , "IfDescr"))
# print("-" * 60)

for x in tbl1:  # traversing through the keys of the dictionary and trying to match the MAC Addresses,
    # with their descriptions, and OIDs
    mac_address = tbl1[x] #  grabbing the relevant MAC Addr from the OID
    if_index = tbl2[x] # grabbing the relvevant index from the OID
    if_descr = tbl3[str(if_index)] if str(if_index) in tbl3 else '' # I have to convert the index to a string and check
    # if it's in table 3 meaning a description exists.
    if if_descr:  # if there's a relevant description or interface name, then assign it accordingly
        if_descr = ''.join(map(chr, if_descr)).strip()
    else:  # otherwise, label it as unknown and just provide the ifIndex
        if_descr = "unknown ({})".format((str(if_index)))
    # mac_parts = list(map(ord, str(mac_address))) # The MAC STRING in OCTETs
    # mac_str = ':'.join(['{:02x}'.format(x) for x in mac_parts]) # This added ":" as delimiter
    # print("{:<25} {:<35} {:<25}".format(x, if_descr, mac_address))  # ,str(if_index)))

    # Printing out output
    print("<tr>")
    print("<td align=center> %s</td>" % x)
    print("<td align=center> %s</td>" % if_descr)
    print("<td align=center> %s</td>" % mac_address)
    print("</tr>")

# End table
print("</table>")
print("</body>")
print("</html>")
