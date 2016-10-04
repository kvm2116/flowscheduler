#! /usr/bin/python
"""

The Flow Scheduler project utilizes floodlight OpenFlow controller rest APIs to dynamically update flow entries on all switches
based on network traffic.
This code gets the topology information connected to the Floodlight Controller
This information can be verified by visiting the website:
  http://<controller IP address>:8080/ui/index.html
  Example: http://128.110.152.148:8080/ui/index.html where the controller's IP address is 128.110.152.148
The code also gives example of how to add the forwarding rules in the switches

Syntax:
   python flowsch.py {IP:REST_PORT}

@author Kunal Mahajan, mkunal@cs.columbia.edu
PhD Candidate in CS
Columbia University
"""

import os
import sys
import subprocess
import json
import argparse
import io
import time

parser = argparse.ArgumentParser(description='Flow Scheduler')
parser.add_argument("controllerRestIP", action='store', default='localhost:8080', help='controller IP:RESTport, e.g., localhost:8080 or A.B.C.D:8080')
args = parser.parse_args()

controllerRestIP = args.controllerRestIP # the ip address along with the port number
print "Controller IP: %s" % controllerRestIP

# Get the list of switches with their dpid
command = "curl -s http://%s/wm/core/controller/switches/json" % (controllerRestIP)
result = os.popen(command).read()
switches = json.loads(result)
print "Number of switches connected = %d" % len(switches) 

def addflow(dpid, ipv4_src, ipv4_dst, tcp_src, tcp_dst, outport):
	command = "curl -X POST -d '{\"switch\": \"%s\", \"name\":\"flow-mod-9\", \"table\":\"200\"," + \
          "\"cookie\":\"0\", \"priority\":\"3\", \"ipv4_src\":\"%s\", \"ipv4_dst\":\"%s\", \"eth_type\":\"0x0800\"," + \
          "\"tcp_src\":\"%d\", \"tcp_dst\":\"%d\", \"ip_proto\":\"0x06\", \"active\":\"true\", \"actions\":\"output=%d\"}'" + \
          " http://128.104.222.34:8080/wm/staticflowpusher/json" % (dpid, ipv4_src, ipv4_dst, tcp_src, tcp_dst, outport)
	result = os.popen(command).read()
	print result

addflow("04:4d:2c:23:3a:3f:10:88", "10.10.1.1", "10.10.1.2", 5001, 5002, 5)