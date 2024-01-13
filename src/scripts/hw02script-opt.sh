#!/usr/bin/bash
# Author: Areeb Abubaker (for an hw02)
# Date: 01/18/23
# Description: Computing the RTT (Round Trip Time) with various Packet Sizes for a list of given IP Addresses
# Usage: hw02script.sh <no command line arguments>

# Set the content type for CGI script
echo "content-type: text/plain"
echo

# Calculate the number of columns in the terminal window
COLS=$(tput cols)

# Print header line for all columns
printf "%-15s %11s \t %13s \t %13s \n" "IP Address" "Packet Size" "RTT" "SD"

# Loop over all the given IP addresses
for h in 140.192.40.4 172.26.1.101 100.1.1.17 100.1.1.18 100.1.1.19 192.168.1.16 192.168.2.8; do

  # Print separator line between hosts
  printf "%*s\n" "$COLS" "" | tr " " "-"

  # Loop over all packet sizes from 64 to 2048 in steps of 64
  for ((size = 64; size <= 2048; size *= 2)); do

    # Test if the host is alive using a simple two-ping test
    RESULT_TEMP=$(/usr/local/bin/supercmd -f -c 2 -s "$size" "$h" | grep -F transmitted)

    # Extract packet loss percentage from the output
    LOSS=$(echo "$RESULT_TEMP" | cut -d" " -f6)

    # If packet loss is 0%, the host is alive, so calculate RTT and SD
    if [[ "$LOSS" = "0%" ]]; then

      # Perform 100-ping test to calculate RTT and SD
      RESULT_FINAL=$(/usr/local/bin/supercmd ping -f -c 100 -s "$size" "$h" | grep -F rtt | cut -d" " -f4)

      # Extract RTT and SD from the output
      RTT=$(echo "$RESULT_FINAL" | cut -d"/" -f2)
      SD=$(echo "$RESULT_FINAL" | cut -d"/" -f4)

      # Print the relevant information for the given host and packet size
      printf "%-15s \t %7s \t  %9.3f \t %9.3f \n" "$h" "$size" "$RTT" "$SD"

    # If packet loss is non-zero, the host is not reachable, so print a message and skip to the next host
    else
      printf "Message: fail to reach the target host: %11s\n" "$h"
      continue 5
    fi
  done
done
