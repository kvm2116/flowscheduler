"""
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

# def addflow(dpid, ipv4_src, ipv4_dst, tcp_src, tcp_dst, outport):
# 	command = "curl -X POST -d '{\"switch\": \"%s\", \"name\":\"flow-mod-9\", \"table\":\"200\"," + \
#           "\"cookie\":\"0\", \"priority\":\"3\", \"ipv4_src\":\"%s\", \"ipv4_dst\":\"%s\", \"eth_type\":\"0x0800\"," + \
#           "\"tcp_src\":\"%s\", \"tcp_dst\":\"%s\", \"ip_proto\":\"0x06\", \"active\":\"true\", \"actions\":\"output=%s\"}'" + \
#           " http://128.104.223.6:8080/wm/staticflowpusher/json" % (dpid, ipv4_src, ipv4_dst, tcp_src, tcp_dst, outport)
# 	result = os.popen(command).read() # TODO: ip address
# 	print result


switch_dpid = "00:65:5c:8a:38:3e:cd:28"			# TODO: switch dpid 
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

# # Add output to controller flow in table 200
command = "curl -X POST -d '{\"switch\": \"00:65:5c:8a:38:3e:cd:28\", \"name\":\"flow-mod-9\", \"table\":\"200\"," + \
          "\"cookie\":\"0\", \"priority\":\"5\", \"ipv4_src\":\"10.10.1.1\", \"ipv4_dst\":\"10.10.2.1\"," + \
          "\"active\":\"true\", \"actions\":\"output=1\"}'" + \
          " http://128.104.222.246:8080/wm/staticflowpusher/json" 

result = os.popen(command).read()
print result
while(True):
	getflows()


