#!/usr/bin/python
print("Content-type:text/html\n")
#
#       Location:  /home/achung/net484/lec05/hw05script.py
#       Author: Anthony Chung (after a script by James Yu)
#       Date: January 26, 2022
#       Description: computer the hourly system load average
#       Usage: python hw05script.py {-daily | -hourly | - raw} <date1> <data2>
#       Output
#               1. Hour
#               2. Number of top sessions
#               3. Active users
#               4. Average system Load (based on 15-min load average)
#               5. Peak Load (max of 1-min, 5-min, and 15-min load)

#
#	note: two different data formats
#	(1) top - 00:02:02 up 38 days,  6:35,  0 users,  load average: 0.00, 0.00, 0.00   (n=14)
#	(2) top - 17:31:01 up 36 days, 4 min,  0 users,  load average: 0.00, 0.00, 0.00  (n=15)
#
#	For hw05, your task is to modify the code to become a cgi script so that the inputs are taken from the html form
#       (instead of command line arguments) and the outputs are printed as formatted html code.
# -------------------------------------------------------------------------------------
print("<html>")
print("<head>")
print("<title>NET-384 Load Report</title>")
print("</head>")
print("<h1 align=center> NET384/484: System Load Report")
print("</h1")
print("<body>")

import cgi
import sys
import datetime as dt
from datetime import datetime

# For hw05 cgi script, you should import cgi module, and modify the following lines (up to the next note about hw05
# cgi script) to use cgi to retrieve arguments from you html form, and store them in the corresponding variables.
# There is no need to give SYNTAX information since it will not be called from a command line.
# ************************************************** Get data from fields, use cgi.FieldStorage to create the form
# object ************************************************** Create instance of FieldStorage


form = cgi.FieldStorage()
# take in variable names
user = form.getvalue('user')
password = form.getvalue('password')
userData = open("/home/net484/student/net484s08/public_html/hw05/UserData.data")
syslog = userData.readlines()  # this is literally splitting all the lines
lenFile = len(syslog)
x = 0
print("<p> %d </p>" % lenFile)
for line in syslog:
    data = line.split(";")  # so you can access each element
    if (data[0] == str(user)) and (data[1] == str(password)):
        break
    x += 1
    if x == lenFile:
        print("</body>")
        print("</html>")
        print("<p> User %s password did not match </p" % str(user))
        quit()
if form.getvalue('sdate'):
    sdate = form.getvalue('sdate')
else:
    sdate = "no start date"  # probably stop parsing
if form.getvalue('edate'):
    edate = form.getvalue('edate')
else:
    edate = "no end date"
if form.getvalue('rtype'):
    rtype = form.getvalue('rtype')
else:
    rtype = "No Report Type Selected"

# ask which data it is and set op the same
print("<p> This is rtype %s  </p>" % rtype)
(op) = int(rtype)
if op == 1:
    opcode = 1
    dtype = "daily"
elif op == 2:
    opcode = 2
    dtype = "hourly"
elif op == 3:
    opcode = 3
    dtype = "raw"
else:
    opcode = 1
    dtype = "daily"

print("<center> User= %s Report Type= %s </center>" % (str(user), dtype))

# ************************************************
#  change date format from mm-dd to yyyy-mm-dd
#
# ************************************************
fmt = "%Y-%m-%d"
d1 = datetime.strptime(sdate, fmt).date()  # start date
d2 = datetime.strptime(edate, fmt).date()  # end date

# For hw05 cgi script, once you are able to get the arguments correctly, you
# can use the follow section of code as is, up to and before the printing of data (i.e.
# up to the next note about hw05 cgi script).

# initialization of Dictionary

session = {}  # number of top sessions based on daily, hourly, or raw
user = {}  # number of active users in the session
uptime = {}  # uptime since last reboot (not used)
sysLoad = {}  # system load
peak = {}  # peak load

delta = d2 - d1

prefix = "/home/achung/cron/top/"
for i in range(delta.days + 1):
    x = (d1 + dt.timedelta(days=i))
    mmdd = x.strftime('%m-%d')  # change the format from yyyy-mm-dd to mm-dd
    topFile = prefix + "top." + mmdd
    try:  # if file does not exist, skip and continue with the next date
        with open(topFile) as fd:
            topData = fd.readlines()
    except IOError:
        continue

    lineNo = 0  # not used, for debugging only
    for line in topData:
        if line.startswith('top'):
            inline = line.rstrip('\n')  # remove '\n' at the end of line
            data = inline.split()
            n = len(data)
            (hour, min, sec) = data[2].split(':')

            # ******* set the key for Dictionary tables
            if opcode == 1:  # daily data
                key = mmdd
            elif opcode == 2:
                key = mmdd + ":" + hour  # hourly data
            elif opcode == 3:
                key = mmdd + ":" + hour + ":" + min  # raw data
            else:
                print("Program Assert: unknown opcode=", opcode)
                sys.exit(1)

            if key in session:
                session[key] += 1
            else:  # initialize all Dictionary tables
                session[key] = 1
                user[key] = 0
                uptime[key] = ''
                sysLoad[key] = 0.0
                peak[key] = 0.0

            if n == 14:
                uptime[key] = data[4] + data[5] + data[6]
                user[key] += int(data[7])
                pt = 11
            elif n == 15:  # event occur between 00:00 and 00:59
                uptime[key] = data[4] + data[5] + data[6] + data[7]
                user[key] += int(data[8])
                pt = 12
            else:
                print("data abnormalities")  # there are additional cases not implemented yet
                continue

            # print lineNo, n, load1, load2, load3
            load01 = float(data[pt].rstrip(','))  # not used, keept it for debugging
            load05 = float(data[pt + 1].rstrip(','))
            load15 = float(data[pt + 2])
            sysLoad[key] += load15  # average is based on 15-min load average
            if key in peak:
                # data is collected at 15-min interval, so it is possible that load15>load05
                if peak[key] < load01: peak[key] = load01
                if peak[key] < load05: peak[key] = load05
                if peak[key] < load05: peak[key] = load15

            # print "DEBUF", lineNo, key, load01, load05, load15
            lineNo += 1
    # end one top file
# end  all top files

# For hw05 cgi script, adapt the following lines to output html. Remember to begin with printing out
# content type followed by a blank line.

# Used table structure in HTML and printed out table headers
print("<table align=center border=3>")
print("<th> Time</th>")
print("<th> Session</th>")
print("<th> User</th>")
print("<th> Load Average</th>")
print("<th> Peak Load</th>")

for key in sorted(session.keys()):
    n = session[key]
    if n < 1:
        print("<p>Program Assert: %s =</p>", n)
        sys.exit(1)
    avgUser = user[key] / n
    avgOccupancy = sysLoad[key] / n
    # Used table structure in HTML and printed out table items
    print("<tr>")
    print("<td> %s</td>" % key)
    print("<td align=center> %d</td>" % session[key])
    print("<td align=center> %.2f</td>" % avgUser)
    print("<td align=center> %.2f</td>" % avgOccupancy)
    print("<td align=center> %.2f</td>" % peak[key])
    print("</tr>")
# End table
print("</table>")
print("</body>")
print("</html>")
