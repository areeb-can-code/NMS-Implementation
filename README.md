# Network Management System (NMS) Project

## Overview

This project encompasses a Web-based Network Management System (NMS) designed for comprehensive network administration. The system is implemented using various scripting technologies and CGI (Common Gateway Interface) to interact with HTML pages dynamically.

## Structure

### Script Files

- **snmpTrap-cgi.py**: Handles SNMP trap functionality.
- **hw04script-opt-cgi.py**: Manages system log analysis.
- **hw02script-opt.py**: Performs traceroute functionality with Round Trip Time (RTT) functionality.
- **snmpwalk.py**: Conducts SNMP walk.
- **setSysInfo-cgi.py**: Sets system information.
- **getMACTable-cgi.py**: Retrieves the MAC address table.
- **getARPTable-cgi.py**: Fetches the ARP address table.
- **performance_metrics.py**: Captures performance metrics using a cron job.

### HTML Files

- **index.html**: Main homepage of the NMS.
- **fault_management.html**: Displays fault management information.
- **config_management.html**: Shows device configuration and system information.
- **account_management.html**: Provides user usage reports.
- **performance_management.html**: Includes throughput, system load reports, and RTT reports.
- **security_management.html**: Exhibits intrusion detection reports.

## Running the Project Locally

1. Clone this repository to your local machine.

   ```bash
   git clone https://github.com/areeb-can-code/NMS-Project.git

Certainly! Here's the content in Markdown format:

markdown

# Network Management System (NMS) Project

## Overview

This project encompasses a Web-based Network Management System (NMS) designed for comprehensive network administration. The system is implemented using various scripting technologies and CGI (Common Gateway Interface) to interact with HTML pages dynamically.

## Structure

### Script Files

- **snmpTrap-cgi.py**: Handles SNMP trap functionality.
- **hw04script-opt-cgi.py**: Manages system log analysis.
- **hw02script-opt.py**: Performs traceroute functionality with Round Trip Time (RTT) functionality.
- **snmpwalk.py**: Conducts SNMP walk.
- **setSysInfo-cgi.py**: Sets system information.
- **getMACTable-cgi.py**: Retrieves the MAC address table.
- **getARPTable-cgi.py**: Fetches the ARP address table.
- **performance_metrics.py**: Captures performance metrics using a cron job.

### HTML Files

- **index.html**: Main homepage of the NMS.
- **fault_management.html**: Displays fault management information.
- **config_management.html**: Shows device configuration and system information.
- **account_management.html**: Provides user usage reports.
- **performance_management.html**: Includes throughput, system load reports, and RTT reports.
- **security_management.html**: Exhibits intrusion detection reports.

## Running the Project Locally

1. Clone this repository to your local machine.

   ```bash
   git clone https://github.com/areeb-can-code/NMS-Project.git
```

2.  Navigate to the project directory
    Open index.html in a web browser.

3. Click on the links to various functionalities, and observe how the corresponding Python scripts are executed via CGI to populate the HTML pages dynamically.

Screenshots

Refer to the accompanying report document for screenshots and detailed explanations of each functionality.
