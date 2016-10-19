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
   python flowsch.py {IP:REST_PORT} {num_groups}

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
parser.add_argument("num_groups", action='store', default='2', help='number of groups, e.g., 2 or 10')
args = parser.parse_args()

controllerRestIP = args.controllerRestIP # the ip address along with the port number
num_groups = int(args.num_groups)

# Get the list of switches with their dpid
command = "curl -s http://%s/wm/core/controller/switches/json" % (controllerRestIP)
result = os.popen(command).read()
switches = json.loads(result)
dpid = switches[0]['switchDPID']

# create stats and group variables
port_stats = {}
flow_stats = {}
flow_groups = {}
output_ports = [47,49]		# TODO update the list of output ports for each switch
path_assignment = {}

"""
Get the group bandwidth usage
key is ipv4_src and ipv4_dst
value is dictionary of groups
for dictionary of groups: key is group number, value is bandwidth usage
"""
def get_group_bw_usage():
	for flow in flow_stats:
		# initialize the groups for this src-dst ip tuple if it does not exist
		if (flow[0], flow[1]) not in flow_groups:
			groups = {}
			for i in range(0,num_groups):
				groups[i] = 0
			flow_groups[(flow[0], flow[1])] = groups
		groups = flow_groups[(flow[0], flow[1])]
		# compute group_id for this flow
		group_id = (int(flow[2]) ^ int(flow[3])) % num_groups
		# add byte_count to this group_id usage
		counts = flow_stats[flow]
		groups[group_id] += counts['byte_diff']
		flow_groups[(flow[0], flow[1])] = groups

def get_port_usages():
	port_congestion = {}
	for port in output_ports:
		port_congestion[port] = port_stats[dpid][port]['tx_bytes_diff']
	return port_congestion

"""
For each src-dst ip tuple, there is a set of paths.
Scheduler has to assign paths to each of the groups based on path utilization
"""
def scheduler():
	for ip_tuple in flow_groups:
		groups = flow_groups[ip_tuple]
		sorted_groups = sorted(groups.items(), key=lambda x: x[1], reverse=True)
		groups_path = {}
		port_congestion = get_port_usages()
		for group_id, byte_count in sorted_groups:
			min_value = 99999999999999999999 
			min_port = -1
			for port in output_ports:
				if port_congestion[port] < min_value:
					min_value = port_congestion[port]
					min_port = port
			groups_path[group_id] = min_port
			port_congestion[min_port] += byte_count
		path_assignment[ip_tuple] = groups_path
	return path_assignment

"""
flow_stats data structure:
key: tuple of (ipv4_src, ipv4_dst, tcp_src, tcp_dst)
value: dictionary, where key is (pkt_count, pkt_diff, byte_count, byte_diff)
"""
def parse_flows(flows, dpid):
	parsedResult = json.loads(flows)
	flow_results = parsedResult['flows']
	for item in flow_results:
		match = item['match']
		if item['table_id'] == "0xc8" :				# table id = 200
			if (match['ipv4_src'], match['ipv4_dst'], match['tcp_src'], match['tcp_dst']) in flow_stats:
				stat = flow_stats[(match['ipv4_src'], match['ipv4_dst'], match['tcp_src'], match['tcp_dst'])]
				flow_stats[(match['ipv4_src'], match['ipv4_dst'], match['tcp_src'], match['tcp_dst'])] = {'pkt_count' : long(item['packet_count']),
															'pkt_diff' : long(item['packet_count']) - stat['pkt_count'], 
															'byte_count' : long(item['byte_count']), 
															'byte_diff': long(item['byte_count']) - stat['byte_count']}
			else:
				flow_stats[(match['ipv4_src'], match['ipv4_dst'], match['tcp_src'], match['tcp_dst'])] = {'pkt_count' : long(item['packet_count']),
															'pkt_diff' : 0, 'byte_count' : long(item['byte_count']), 
															'byte_diff': 0}
			# match = item['match']
			# actions = item['instructions']['instruction_apply_actions']['actions']
			# actions = actions.split("=")
			# port_num = actions[1]
	# print flow_stats

def add_port_stat(dpid, port_number, rx_packets, rx_bytes, tx_packets, tx_bytes, rx_packets_diff, rx_bytes_diff, tx_packets_diff, tx_bytes_diff):
	port_stats[dpid][port_number] = {'rx_packets' : rx_packets, 'rx_bytes' : rx_bytes, 
										'tx_packets' : tx_packets, 'tx_bytes' : tx_bytes,
										'rx_packets_diff': rx_packets_diff, 'rx_bytes_diff' : rx_bytes_diff,
										'tx_packets_diff': tx_packets_diff, 'tx_bytes_diff' : tx_bytes_diff}

# Calculation does not account for overflows
def parse_ports(ports, dpid):
	parsedResult = json.loads(ports)
	stats = parsedResult['port_reply'][0]['port']
	for item in stats:
		if dpid in port_stats:
			port_number = long(item['port_number'])
			if port_number in port_stats[dpid]:
				rx_packets_diff = long(item['receive_packets']) - port_stats[dpid][port_number]['rx_packets']
				rx_bytes_diff = long(item['receive_bytes']) - port_stats[dpid][port_number]['rx_bytes']
				tx_packets_diff = long(item['transmit_packets']) - port_stats[dpid][port_number]['tx_packets']
				tx_bytes_diff = long(item['transmit_bytes']) - port_stats[dpid][port_number]['tx_bytes']

				add_port_stat(dpid, port_number, long(item['receive_packets']), long(item['receive_bytes']), 		# update entry
								long(item['transmit_packets']), long(item['transmit_bytes']), 
								rx_packets_diff, rx_bytes_diff, tx_packets_diff, tx_bytes_diff)
			else:
				add_port_stat(dpid, port_number, long(item['receive_packets']), long(item['receive_bytes']), 		# add entry for new port number
								long(item['transmit_packets']), long(item['transmit_bytes']), 
								0, 0, 0, 0)
		else:																										# add entry for new switch
			port_stats[dpid] = {}
			port_number = long(item['port_number'])
			add_port_stat(dpid, port_number, long(item['receive_packets']), long(item['receive_bytes']), 
								long(item['transmit_packets']), long(item['transmit_bytes']), 
								0, 0, 0, 0)
	# print port_stats

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
		parse_flows(flows, switches[i]['switchDPID'])
		get_group_bw_usage()
		parse_ports(ports, switches[i]['switchDPID'])
		path_assignment = scheduler()
		print path_assignment
	print("--- %s seconds ---" % (time.time() - start_time))