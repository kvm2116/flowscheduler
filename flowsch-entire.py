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

import httplib
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
controllerIP, port = controllerRestIP.split(":")
num_groups = int(args.num_groups)


class Forwarding(object):
  
    def __init__(self, server):
        self.server = server
  
    def get(self, data):
        ret = self.rest_call({}, 'GET')
        return json.loads(ret[2])
  
    def set(self, data):
        ret = self.rest_call(data, 'POST')
        return ret[0] == 204
  
    def rest_call(self, data, action):
        path = '/wm/forwarding/json'
        headers = {
            'Content-type': 'application/json',
            'Accept': 'application/json',
            }
        body = json.dumps(data)
        conn = httplib.HTTPConnection(self.server, 8080)
        conn.request(action, path, body, headers)
        response = conn.getresponse()
        ret = (response.status, response.reason, response.read())
        # print ret
        conn.close()
        return ret


# Get the list of switches with their dpid
command = "curl -s http://%s/wm/core/controller/switches/json" % (controllerRestIP)
result = os.popen(command).read()
switches = json.loads(result)
dpid = switches[0]['switchDPID']

# create stats and group variables
switch_port_stats = {}
switch_flow_stats = {}
switch_flow_groups = {}
path_assignment = {}
leaf_switches = ['00:65:5c:8a:38:3e:cd:28', '00:65:2c:23:3a:3e:ed:a9']
switch_ports = {'00:65:5c:8a:38:3e:cd:28':						# LEAF 0
					[1,5,33,37,65,69],
				'00:65:2c:23:3a:3e:ed:a9':						# LEAF 1
					[1,5,33,37,65,69],
				'00:65:bc:ea:fa:b3:5e:32':						# SPINE 0
					[],
				'00:65:bc:ea:fa:6c:69:1d':						# SPINE 1
					[]
				} # dpid, ports to spine/leaf

rack_attachments = {0: 
						[
							('10.10.1.1', 9),
							('10.10.1.2', 10),
							('10.10.1.3', 11),
							('10.10.1.4', 12),
							('10.10.1.5', 13),
							('10.10.1.6', 14),
							('10.10.1.7', 15),
							('10.10.1.8', 16),
							('10.10.1.9', 17),
							('10.10.1.10', 18),
							('10.10.1.11', 19),
							('10.10.1.12', 20),
							('10.10.1.13', 21),
							('10.10.1.14', 22),
							('10.10.1.15', 23),
							('10.10.1.16', 24),
						], 
					1:
						[
							('10.10.2.1', 9),
							('10.10.2.2', 10),
							('10.10.2.3', 11),
							('10.10.2.4', 12),
							('10.10.2.5', 13),
							('10.10.2.6', 14),
							('10.10.2.7', 15),
							('10.10.2.8', 16),
							('10.10.2.9', 17),
							('10.10.2.10', 18),
							('10.10.2.11', 19),
							('10.10.2.12', 20),
							('10.10.2.13', 21),
							('10.10.2.14', 22),
							('10.10.2.15', 23),
							('10.10.2.16', 24),
						]
					}


def initializeGroups(leaf_switches):
	for dpid in leaf_switches:
		groups = {}
		for i in range(0,num_groups):
			groups[i] = 0
		switch_flow_groups[dpid] = groups

def IP2Int(ip):
    o = map(int, ip.split('.'))
    res = (16777216 * o[0]) + (65536 * o[1]) + (256 * o[2]) + o[3]
    return res

"""
Get the group bandwidth usage
key is ipv4_src and ipv4_dst
value is dictionary of groups
for dictionary of groups: key is group number, value is bandwidth usage
"""
def get_group_bw_usage():
	initializeGroups(leaf_switches)
	for dpid in switch_flow_stats:
		flow_stats = switch_flow_stats[dpid]
		# print dpid 
		# print flow_stats
		groups = switch_flow_groups[dpid]
		for flow in flow_stats:
			flow_group_id = (IP2Int(flow[0]) ^ IP2Int(flow[1]) ^ int(flow[2]) ^ int(flow[3])) % num_groups
			counts = switch_flow_stats[flow]
			groups[flow_group_id] += counts['byte_diff']
		switch_flow_groups[dpid] = groups

def get_path_cost(dpid):
	port_congestion = {}
	for port in switch_ports[dpid]:
		port_congestion[port] = switch_port_stats[dpid][port]['tx_bytes_diff']
	return port_congestion

"""
For each src-dst ip tuple, there is a set of paths.
Scheduler has to assign paths to each of the groups based on path utilization
"""
def scheduler():
	for dpid in switch_flow_groups:
		groups = switch_flow_groups[dpid]
		sorted_groups = sorted(groups.items(), key=lambda x: x[1], reverse=True)

		groups_path = {}
		port_congestion = get_path_cost(dpid)
		for group_id, byte_count in sorted_groups:
			min_value = 99999999999999999999 
			min_port = -1
			for port in switch_ports[dpid]:
				if port not in port_congestion:
					port_congestion[port] = 0
				if port_congestion[port] < min_value:
					min_value = port_congestion[port]
					min_port = port
			groups_path[group_id] = min_port
			port_congestion[min_port] += byte_count
		path_assignment[dpid] = groups_path
	return path_assignment

"""
flow_stats data structure:
key: tuple of (ipv4_src, ipv4_dst, tcp_src, tcp_dst)
value: dictionary, where key is (pkt_count, pkt_diff, byte_count, byte_diff)
"""
def parse_flows(flows):
	flow_stats = {}
	parsedResult = json.loads(flows)
	# print parsedResult
	# print "\n\n"
	for dpid in parsedResult:
		# print dpid
		flow_results = parsedResult[dpid]['flows']
		for item in flow_results:
			match = item['match']
			# print match
			if 'ipv4_src' not in match or 'ipv4_dst' not in match or 'tcp_src' not in match or 'tcp_dst' not in match:
				continue
			if item['table_id'] == "0xc8":				# table id = 200
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
		switch_flow_stats[dpid] = flow_stats
		# print "\n\n"
			# match = item['match']
			# actions = item['instructions']['instruction_apply_actions']['actions']
			# actions = actions.split("=")
			# port_num = actions[1]
	# print switch_flow_stats

def add_port_stat(dpid, port_number, rx_packets, rx_bytes, tx_packets, tx_bytes, rx_packets_diff, rx_bytes_diff, tx_packets_diff, tx_bytes_diff):
	switch_port_stats[dpid][port_number] = {'rx_packets' : rx_packets, 'rx_bytes' : rx_bytes, 
										'tx_packets' : tx_packets, 'tx_bytes' : tx_bytes,
										'rx_packets_diff': rx_packets_diff, 'rx_bytes_diff' : rx_bytes_diff,
										'tx_packets_diff': tx_packets_diff, 'tx_bytes_diff' : tx_bytes_diff}

# Calculation does not account for overflows
def parse_ports(ports):
	parsedResult = json.loads(ports)
	# print parsedResult
	# print "\n\n"
	for dpid in parsedResult:
		# print dpid
		stats = parsedResult[dpid]['port_reply'][0]['port']

		for item in stats:
			if dpid in switch_port_stats:
				port_number = long(item['port_number'])
				if port_number in switch_port_stats[dpid]:
					rx_packets_diff = long(item['receive_packets']) - switch_port_stats[dpid][port_number]['rx_packets']
					rx_bytes_diff = long(item['receive_bytes']) - switch_port_stats[dpid][port_number]['rx_bytes']
					tx_packets_diff = long(item['transmit_packets']) - switch_port_stats[dpid][port_number]['tx_packets']
					tx_bytes_diff = long(item['transmit_bytes']) - switch_port_stats[dpid][port_number]['tx_bytes']

					add_port_stat(dpid, port_number, long(item['receive_packets']), long(item['receive_bytes']), 		# update entry
									long(item['transmit_packets']), long(item['transmit_bytes']), 
									rx_packets_diff, rx_bytes_diff, tx_packets_diff, tx_bytes_diff)
				else:
					add_port_stat(dpid, port_number, long(item['receive_packets']), long(item['receive_bytes']), 		# add entry for new port number
									long(item['transmit_packets']), long(item['transmit_bytes']), 
									0, 0, 0, 0)
			else:																										# add entry for new switch
				switch_port_stats[dpid] = {}
				port_number = long(item['port_number'])
				add_port_stat(dpid, port_number, long(item['receive_packets']), long(item['receive_bytes']), 
									long(item['transmit_packets']), long(item['transmit_bytes']), 
									0, 0, 0, 0)
	# print switch_port_stats

def rest_call(command):
	return os.popen(command).read()

def convert_to_json(path_assignment):
	# convert keys in path_assignment to strings
	str_path_assignment = {}
	for item in path_assignment:
		str_path_assignment[str(item)] = path_assignment[item]
	return json.dumps(str_path_assignment)


pusher = Forwarding(controllerIP)
# Get all the flows for the switches:
while True:
	start_time = time.time()
	flow_command = "curl -s http://%s/wm/core/switch/all/flow/json" % (controllerRestIP) 
	flows = rest_call(flow_command)
	port_command = "curl -s http://%s/wm/core/switch/all/port/json" % (controllerRestIP) 
	ports = rest_call(port_command)
	parse_flows(flows)
	get_group_bw_usage()
	parse_ports(ports)
	path_assignment = scheduler()
	if len(path_assignment.keys()) != 0:
		# print iptuple_port_dict
		json_path_assignment = convert_to_json(path_assignment)
		print json_path_assignment
		pusher.set(json_path_assignment)
	print("--- %s seconds ---" % (time.time() - start_time))