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

# def topology:
# Switches fields:
#     inetAddress
#     connectedSince
#     switchDPID
# To get individual values, here is the command:
# inetAddress: print switches[0].get('inetAddress') 

# Get the list of switches with their dpid
# command = "curl -s http://%s/wm/core/controller/switches/json" % (controllerRestIP)
# result = os.popen(command).read()
# switches = json.loads(result)
# print the datapath id of switches
# print "Number of switches: %d" % len(switches)
# for i in range(len(switches)):
#   print switches[i]['switchDPID']

# Get number of hosts connected to the switch
# for i in range(len(switches)):
#   command = "curl -s http://%s/wm/device/?dpid=%s" % (controllerRestIP, switches[i]['switchDPID'])
#   result = os.popen(command).read()
#   deviceInfo = json.loads(result)
#   print deviceInfo
  # print "Number of hosts: %d" % (len(deviceInfo))

# Get all the static flows for the switch:
# for i in range(len(switches)):
#   command = "curl -s http://%s/wm/staticflowpusher/list/%s/json" % (controllerRestIP, switches[i]['switchDPID']) 
#   flows = os.popen(command).read()
#   print flows

# switch_dpid = "04:55:2c:23:3a:3f:37:60"
# # Add a static flow
# command = "curl -X POST -d '{\"switch\": \"04:55:2c:23:3a:3f:37:60\", \"name\":\"flow-mod-8\", \"table\":\"200\"," + \
#           "\"cookie\":\"0\", \"priority\":\"2\", \"in_port\":\"10\",\"active\":\"true\", \"actions\":\"output=56\"}'" + \
#           " http://128.104.222.57:8080/wm/staticflowpusher/json"
# result = os.popen(command).read()
# print result

# eth_dst = "90:e2:ba:b3:ba:44"
# command = "curl -X POST -d '{\"switch\":\"04:55:2c:23:3a:3f:37:60\", \"name\":\"flow-mod-1\", \"table\":\"100\"," + \
#           "\"cookie\":\"0\", \"priority\":\"32768\", \"eth_dst\":\"90:e2:ba:b3:ba:44\", \"eth_type\":\"0x0800\","+ \
#           "\"ipv4_dst\":\"10.10.1.2\", \"active\":\"true\", \"actions\":\"output=13\"}'" + \
#           " http://128.104.223.10:8080/wm/staticflowpusher/json"
# result = os.popen(command).read()
# print result

# command = "curl -X POST -d '{\"switch\": \"04:69:2c:23:3a:3f:42:69\", \"name\":\"flow-mod-9\", \"table\":\"200\"," + \
#           "\"cookie\":\"0\", \"priority\":\"3\", \"ipv4_dst\":\"10.10.1.1\", \"ipv4_src\":\"10.10.1.2\", \"eth_type\":\"0x0800\"," + \
#           "\"tcp_src\":\"5010\", \"tcp_dst\":\"5009\", \"active\":\"true\", \"actions\":\"output=56\"}'" + \
#           " http://128.104.222.34:8080/wm/staticflowpusher/json"
# result = os.popen(command).read()
# print result


# Get all the flows for the switch:
while True:
  # for i in range(len(switches)):
  command = "curl -s http://%s/wm/core/switch/all/flow/json" % (controllerRestIP) 
# command = "curl -s http://%s/wm/staticflowpusher/list/%s/json" % (controllerRestIP, switches[i]['switchDPID']) 
  flows = os.popen(command).read()
  print flows

# Get tables present in storage
# command = "curl -s http://%s/wm/core/storage/tables/json" % (controllerRestIP) 
# flows = os.popen(command).read()
# print flows

