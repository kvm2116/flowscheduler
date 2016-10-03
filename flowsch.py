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
port_stat = {}

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

def parse_flows(flows):
	print flows
	parsedResult = json.loads(flows)
	flow_stat = parsedResult['flows']
	for item in flow_stat:
		match = item['match']
		actions = item['instructions']['instruction_apply_actions']['actions']
		print type(actions)
	
def parse_ports(ports):
	parsedResult = json.loads(ports)
	port_stat = parsedResult['port_reply'][0]['port']
	for item in port_stat:
		port_number = item['port_number']
		rx_packets = item['receive_packets']
		rx_bytes = item['receive_bytes']
		tx_packets = item['transmit_packets']
		tx_bytes = item['transmit_bytes']
		print port_number

def rest_call(command):
	return os.popen(command).read()

# Get all the flows for the switches:
while True:
	start_time = time.time()
	for i in range(len(switches)):
		flow_command = "curl -s http://%s/wm/core/switch/%s/flow/json" % (controllerRestIP, switches[i]['switchDPID']) 
		flows = rest_call(flow_command)
		port_command = "curl -s http://%s/wm/core/switch/%s/port/json" % (controllerRestIP, switches[i]['switchDPID']) 
		ports = rest_call(port_command)
		# print "Switch %s" % switches[i]['switchDPID']
		parse_flows(flows)
		parse_ports(ports)
	print("--- %s seconds ---" % (time.time() - start_time))