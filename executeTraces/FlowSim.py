import os
import sys
import traceback
import time
import threading
from threading import Timer
import subprocess
import re
import csv
import math

""" Simulate flows given in input file using iperf, and write results to output file
	
	E.g.:

	python FlowSim.py flows.csv sim_stats.csv

	Will read flow information from flows.txt and write results to sim_stats-<datetime>.csv 

	This script expects that the format of the input flows file is:

	time,src_ip,src_port,dst_ip,dst_port,size
	t_1,sip_1,sp_1,dip_1,dp_2,s1
	t_2,sip_2,sp_2,dip_2,dp_2,s_2
	...
	t_n,sip_n,sp_n,dip_n,dp_n,s_n

	Where time is given in seconds, and size is given in bytes.  To attempt to synchronize across machines, 
	outgoing flows will not begin until after 90 seconds have passed.  The input file will be read 
	and iPerf servers will be started on ports 11000-11199 during this interval.  After all outgoing flows
	have completed, the program will wait for 3 minutes before terminating the iPerf servers. 

	Note: to support large number of concurrent flows, the maximum number of open files descriptors
	will likely need to be increased. 

	To see the maximum number of open file descriptors on a linux machine, try:

	cat /proc/sys/fs/file-max

	To increase maximum number of file descriptors to 10000, try:

	su -
	sysctl -w fs.file-max=100000

	To have limit remain at 10000 after reboot, edit /etc/sysctl.conf and append the line:
	fs.file-max = 100000
"""

write_lock = threading.Lock() # lock for writing to output file
all_finished = threading.Event() # event for signalling when all flows have completed

class flow:
	"""Object for storing flow information"""

	def __init__(self):
		start_time = 0
		src_ip = ""
		src_port = 0
		dst_ip = ""
		dst_port = 0 
		flow_size = 0 

def parseFlow(row): 
	"""Parse flow information from a row of the input file, return flow object"""
	new_flow = flow()
	try: 
		new_flow.start_time = float(row[0])
		new_flow.src_ip = row[1]
		new_flow.src_port = int(row[2])
		new_flow.dst_ip = row[3]
		new_flow.dst_port = int(row[4])
		new_flow.flow_size = int(math.ceil(float(row[5])))
		return new_flow
	except:
		traceback.print_exc()

def scheduleFlows(flows, output_filepath):
	""" schedule execution of iperf tasks to simulate flows, set all_finished event when all iperf clients have finished"""
	flow_id = 0
	iperf_client_threads = list()
	for flow in flows:
		p = Timer(flow.start_time, simulateFlow, (flow_id, flow, output_filepath))
		p.start()
		flow_id += 1
		iperf_client_threads.append(p)
	for p in iperf_client_threads:
		p.join()
	all_finished.set()

def simulateFlow(flow_id, flow, output_filepath):
	""" execute an iperf client for a given flow, and write flow id, duration, and bandwidth to output file"""
	try:
		print "flow {} starting".format(flow_id)
		#iperf3 version commented below
		#cmd_line = ["/usr/bin/iperf3", "-c", str(flow.dst_ip), "-p", str(flow.dst_port), "-i", "0", "-n", str(flow.flow_size)]
		cmd_line = ["/usr/bin/iperf", "-c", str(flow.dst_ip), "-p", str(flow.dst_port), "-n", str(flow.flow_size)]
		p = subprocess.Popen(cmd_line, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
		out, err = p.communicate()
		p.wait()
	except:
		traceback.print_exc()

	print "flow {} finished".format(flow_id)

	""" Lines below parse output from iperf; example output is shown below for iperf:

	------------------------------------------------------------
	Client connecting to 127.0.0.1, TCP port 10000
	TCP window size: 2.50 MByte (default)
	------------------------------------------------------------
	[  3] local 127.0.0.1 port 49322 connected with 127.0.0.1 port 10000
	[ ID] Interval       Transfer     Bandwidth
	[  3]  0.0- 0.0 sec   128 KBytes  27.6 Gbits/sec


	Example ouput is shown below for iperf3, with '-i 0' option:

	Connecting to host 127.0.0.1, port 10000
	[  4] local 127.0.0.1 port 47338 connected to 127.0.0.1 port 10000
	[ ID] Interval           Transfer     Bandwidth       Retr  Cwnd
	[  4]   0.00-5.90   sec  9.31 GBytes  13.6 Gbits/sec    0   2.00 MBytes       
	- - - - - - - - - - - - - - - - - - - - - - - - -
	[ ID] Interval           Transfer     Bandwidth       Retr
	[  4]   0.00-5.90   sec  9.31 GBytes  13.6 Gbits/sec    0             sender
	[  4]   0.00-5.90   sec  9.30 GBytes  13.6 Gbits/sec                  receiver

	iperf Done.
	"""

	#print out
	#print err

	interval_string = re.findall("[0-9]+\.?[0-9]+-[\s]*[0-9]+\.?[0-9]+[\s]+sec", out)[0]
	bandwidth_string = re.findall("[0-9]+\.?[0-9]+ [a-zA-Z]+/sec", out)[0]

	interval = re.findall("[0-9]+\.?[0-9]+", interval_string)
	duration = float(interval[1]) - float(interval[0])

	bandwidth_val = float(re.findall("[0-9]+\.?[0-9]+", bandwidth_string)[0])
	bandwidth_unit = re.findall("[a-zA-Z]+", bandwidth_string)[0]

	if bandwidth_unit == 'G':
		bandwidth = bandwidth_val * 1000000
	elif bandwidth_unit == 'M':
		bandwidth = bandwidth_val * 1000
	else:
		bandwidth = bandwidth_val

	with(write_lock):
		try: 
			with open(output_filepath, 'ab') as output:
				writer = csv.writer(output)
				output_row = [flow_id, flow.flow_size, duration, bandwidth]
				writer.writerow(output_row)
		except:
			print("Error writing output")
			traceback.print_exc()


def startServers():
	""" Start an iperf server listening to each of ports 11000-11199"""
	server_processes = list()
	FNULL = open(os.devnull, 'w')
	for i in range(11000, 11200):
		#iperf3 version commented below
		#cmd_line = ["/usr/bin/iperf3", "-s", "-p", str(i)]
		cmd_line = ["/usr/bin/iperf", "-s", "-p", str(i)]
		p = subprocess.Popen(cmd_line, stdout=FNULL, close_fds=True)
		server_processes.append(p)
	return server_processes

def killServers(server_processes):
	""" Terminate the iperf servers""" 
	for p in server_processes:
		p.terminate()

def main(argv): 

	validate_args(argv)

	init_time = time.time()
	path_time = time.strftime("%Y-%m-%d-h%H-m%M-s%S", time.localtime(init_time))

	flow_filepath = argv[0]
	output_template = argv[1]
	template_tokens = output_template.split(os.path.sep)
	output_filepath = ""
	if len(template_tokens) > 1:
		if output_template[0] == os.path.sep:
			output_filepath = os.path.sep
		for i in range(0, len(template_tokens)-1):
			output_filepath = os.path.join(output_filepath, template_tokens[i])
		output_template = template_tokens[-1]
	name_tokens = output_template.split(".")
	filename = ""
	if len(name_tokens) > 1:
		for i in range(0, len(name_tokens)-2):
			filename = filename + name_tokens[i] + '.'
		filename = filename + name_tokens[-2] + "-{}".format(path_time)
		filename = filename + "." + name_tokens[-1]
	else:
		filename = output_filepath + "-{}".format(path_time)

	output_filepath = os.path.join(output_filepath, filename)
	flows = list()

	# write header line to output file
	try: 
		with open(output_filepath, 'wb') as output:
			writer = csv.writer(output)
			header_row = ["flow_id", "flow_size(bytes)", "duration(s)","bandwidth(Kbps)"]
			writer.writerow(header_row)
	except:
		print("Error writing to output file")
		traceback.print_exc()
		sys.exit(-1)

	# read input file and parse flow information
	try:
		with open(flow_filepath, 'r') as input:
			input.readline() # discard header row
			reader = csv.reader(input)

			for row in reader:
				flow = parseFlow(row)
				flows.append(flow)
	except:
		print("Error reading input file")
		traceback.print_exc()
		sys.exit(-1)
	print "Input file read..."

	all_finished.clear()
	# start iperf servers
	server_processes = startServers()
	print "iPerf servers started..."

	# begin sending flows 10 seconds after start time, to synchronize across machines
	wait_time = 10 - (time.time() - init_time)
	print "Flow transmissions beginning in {} seconds".format(wait_time)
	time.sleep(wait_time)

	# schedule and execute outgoing flows
	scheduleFlows(flows, output_filepath)

	# after all outgoing flows have completed, wait three minutes, then terminate servers
	# this is pretty arbitrary; preferable to manually terminate after simulation is finished?
	# or specify time to wait before terminating servers as a command line argument?
	# otherwise, need machines to somehow signal each other when they have completed outgoing flows
	all_finished.wait()
	print ("All outgoing flows completed, iPerf servers terminating in three minutes...")
	time.sleep(180)
	killServers(server_processes)
	# note: when using iperf3, terminating servers will cause "iperf3: interrupt - the server has terminated" messages to stderr
	print "Output written to {}".format(output_filepath)

def validate_args(argv):
	"""Basic validation of command line arguments"""
	if len(argv) < 2:
		print "Insufficient command line arguments"
		usage()
		sys.exit(-1)
	if len(argv) > 2:
		print "Too many command line arguments, extra arguments ignored"

def usage():
	"""Print usage message"""
	print "Usage: python FlowSim.py <input_file> <output_file>"

if __name__ == '__main__':
	main(sys.argv[1:])