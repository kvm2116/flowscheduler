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
print switches
print "Number of switches connected = %d" % len(switches) 

def addflow(dpid, ipv4_src, ipv4_dst, tcp_src, tcp_dst, outport):
	command = "curl -X POST -d '{\"switch\": \"%s\", \"name\":\"flow-mod-9\", \"table\":\"200\"," + \
          "\"cookie\":\"0\", \"priority\":\"3\", \"ipv4_src\":\"%s\", \"ipv4_dst\":\"%s\", \"eth_type\":\"0x0800\"," + \
          "\"tcp_src\":\"%s\", \"tcp_dst\":\"%s\", \"ip_proto\":\"0x06\", \"active\":\"true\", \"actions\":\"output=%s\"}'" + \
          " http://128.104.222.74:8080/wm/staticflowpusher/json" % (dpid, ipv4_src, ipv4_dst, tcp_src, tcp_dst, outport)
	result = os.popen(command).read()
	print result


# command = "curl -X POST -d '{\"switch\": \"04:4d:2c:23:3a:3f:2a:93\", \"name\":\"flow-mod-9\", \"table\":\"200\"," + \
#           "\"cookie\":\"0\", \"priority\":\"3\", \"ipv4_src\":\"10.10.1.1\", \"ipv4_dst\":\"10.10.1.2\", \"eth_type\":\"0x0800\"," + \
#           "\"tcp_src\":\"5001\", \"tcp_dst\":\"5002\", \"ip_proto\":\"0x06\", \"active\":\"true\", \"actions\":\"output=47\"}'" + \
#           " http://128.104.222.94:8080/wm/staticflowpusher/json"
# result = os.popen(command).read()
# print result
# addflow("04:4d:2c:23:3a:3f:2a:93", "10.10.1.1", "10.10.1.2", "5001", "5002", "47")


# Get all the static flows for the switch:
# for i in range(len(switches)):
#   command = "curl -s http://%s/wm/staticflowpusher/list/%s/json" % (controllerRestIP, switches[i]['switchDPID']) 
#   flows = os.popen(command).read()
#   print flows

switch_dpid = "04:55:2c:23:3a:3f:0e:c4"
def getflows():
	allflows_command = "curl -s http://%s/wm/core/switch/all/flow/json" % (controllerRestIP)
	result = os.popen(allflows_command).read()
	printflows(result, True)

"""
isAll: true, print all the results 
		false, flows in table 200
"""
def printflows(result,isAll):
	parsedResult = json.loads(result)
	flow_results = parsedResult[switch_dpid]['flows']
	if isAll:
		for item in flow_results:
			print item
	else:
		for item in flow_results:
			if item['table_id'] == "0xc8" :	
				print item
	print("--- --- --- --- --- --- --- --- ---")

# def deleteFlow():
# 	delete_command = "curl -X DELETE -d '{"name":"flow-mod-1"}' http://<controller_ip>:8080/wm/core/switch/json"

# Add output to controller flow in table 200
command = "curl -X POST -d '{\"switch\": \"04:55:2c:23:3a:3f:0e:c4\", \"name\":\"flow-mod-8\", \"table\":\"200\"," + \
          "\"cookie\":\"0\", \"priority\":\"0\", \"active\":\"true\", \"actions\":\"output=controller\"}'" + \
          " http://128.104.222.74:8080/wm/staticflowpusher/json"
result = os.popen(command).read()
print result
while(True):
	getflows()


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