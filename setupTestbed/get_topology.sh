#!/bin/bash
# Get topology for the two racks

# From the setupTestbed/
#./get_topology.sh

# run this file, get list of all flows and find output ports for each ip address from there

ssh mkunal@128.104.222.247 "sudo screen -d -m iperf -c 10.10.1.1 -n 1k"
ssh mkunal@128.104.222.248 "sudo screen -d -m iperf -c 10.10.1.1 -n 1k"
ssh mkunal@128.104.222.249 "sudo screen -d -m iperf -c  10.10.1.1 -n 1k"
ssh mkunal@128.104.222.250 "sudo screen -d -m iperf -c 10.10.1.1 -n 1k"
ssh mkunal@128.104.222.251 "sudo screen -d -m iperf -c 10.10.1.1 -n 1k"
ssh mkunal@128.104.222.252 "sudo screen -d -m iperf -c 10.10.1.1 -n 1k"
ssh mkunal@128.104.222.253 "sudo screen -d -m iperf -c 10.10.1.1 -n 1k"
ssh mkunal@128.104.222.254 "sudo screen -d -m iperf -c 10.10.1.1 -n 1k"
ssh mkunal@128.104.222.255 "sudo screen -d -m iperf -c 10.10.1.1 -n 1k"
ssh mkunal@128.104.223.0 "sudo screen -d -m iperf -c 10.10.1.1 -n 1k"
ssh mkunal@128.104.223.1 "sudo screen -d -m iperf -c 10.10.1.1 -n 1k"
ssh mkunal@128.104.223.2 "sudo screen -d -m iperf -c 10.10.1.1 -n 1k"
ssh mkunal@128.104.223.3 "sudo screen -d -m iperf -c 10.10.1.1 -n 1k"
ssh mkunal@128.104.223.4 "sudo screen -d -m iperf -c 10.10.1.1 -n 1k"
ssh mkunal@128.104.223.5 "sudo screen -d -m iperf -c 10.10.1.1 -n 1k"

ssh mkunal@128.104.223.7 "sudo screen -d -m iperf -c 10.10.2.1 -n 1k"
ssh mkunal@128.104.223.8 "sudo screen -d -m iperf -c 10.10.2.1 -n 1k"
ssh mkunal@128.104.223.9 "sudo screen -d -m iperf -c 10.10.2.1 -n 1k"
ssh mkunal@128.104.223.10 "sudo screen -d -m iperf -c 10.10.2.1 -n 1k"
ssh mkunal@128.104.223.11 "sudo screen -d -m iperf -c 10.10.2.1 -n 1k"
ssh mkunal@128.104.223.12 "sudo screen -d -m iperf -c 10.10.2.1 -n 1k"	
ssh mkunal@128.104.223.13 "sudo screen -d -m iperf -c 10.10.2.1 -n 1k"
ssh mkunal@128.104.223.14 "sudo screen -d -m iperf -c 10.10.2.1 -n 1k"
ssh mkunal@128.104.223.15 "sudo screen -d -m iperf -c 10.10.2.1 -n 1k"
ssh mkunal@128.104.223.16 "sudo screen -d -m iperf -c 10.10.2.1 -n 1k"
ssh mkunal@128.104.223.17 "sudo screen -d -m iperf -c 10.10.2.1 -n 1k"
ssh mkunal@128.104.223.18 "sudo screen -d -m iperf -c 10.10.2.1 -n 1k"
ssh mkunal@128.104.223.19 "sudo screen -d -m iperf -c 10.10.2.1 -n 1k"
ssh mkunal@128.104.223.20 "sudo screen -d -m iperf -c 10.10.2.1 -n 1k"
ssh mkunal@128.104.223.21 "sudo screen -d -m iperf -c 10.10.2.1 -n 1k"