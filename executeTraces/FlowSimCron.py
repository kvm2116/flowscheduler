import os
import sys
import time
import subprocess
import traceback

""" Create a job in cron to execute FlowSim.py at the specified hour and minute of the current day
	The time, path to FlowSim.py, input filepath, and output filepath must be provided as arguments
	In addition, a cron file must exist for the current user.

	Optional arguments can be provided to execute FlowSim.py multiple times at a specified interval. 

	E.g.:

	python FlowSimCron.py 14:00 /home/FlowSim.py /home/input_flows /home/output.csv 4 10 

	Will schedule execution of FlowSim.py 4 times beginning at 2:00pm, at 10 minute intervals between each execution, 
	with FlowSim.py located at /home/FlowSim.py, the flows input file located at /home/input_flows, 
	and the output file written to /home/output-<execution-datetime>.csv
	"""

def main(argv):
	hour, minute, simfile, infile, outfile, trials, interval = parseArgs(argv)

	daymonth = time.strftime("%d,%m")
	daymonth_tokens = daymonth.split(",")
	day = int(daymonth_tokens[0])
	month = int(daymonth_tokens[1])

	cmd_line = ["crontab", "-l"]
	try:
		with open("mycron", "w") as mycron:
			subprocess.call(cmd_line, stdout=mycron)
	except:
		traceback.print_exc()
		sys.exit(-1)

	try:
		with open("mycron", "a") as mycron:
			for i in range(0, trials):
				# enter a cron job for each trial 
				flow_sim_cmd = "{} {} {} {} 0-7 python {} {} {}".format(minute, hour, day, month, simfile, infile, outfile)
				cmd_line = ["echo", flow_sim_cmd]
				subprocess.call(cmd_line, stdout=mycron)
				# increment time parameters for subsequent trial 
				minute = minute + interval
				if minute > 59:
					minute = minute % 60 
					hour += 1 
				if hour > 23:
					# limited support here for running overnight - shouldn't have intervals greater than 24 hours
					hour = hour % 24
					day = day + 1 
				if day > 30 and (month == 4 or month == 9 or month == 6 or month == 11):
					day = 1
					month += 1
				elif day > 28 and month == 2:
					# check for leap years, accurate through year 2100...
					if year % 4 == 0 and day > 29:
						day = 1
						month += 1
					elif year % 4 != 0:
						day = 1
						month += 1
				elif day > 31:
					day = 1
					month += 1
					if month > 12:
						month = 1
	except:
			traceback.print_exc()
			sys.exit(-1)

	cmd_line = ["crontab", "mycron"]
	try:
		subprocess.call(cmd_line)
	except:
		traceback.print_exc()

	cmd_line = ["rm", "mycron"]
	try:
		subprocess.call(cmd_line)
	except:
		traceback.print_exc()

def parseArgs(argv):
	"""Parse command line arguments and return values; exit and print error message if invalid"""
	if (len(argv) < 4):
		print "Error: Insufficient command line arguments"
		usage()
		sys.exit(-1)
	elif (len(argv) > 6):
		print "Error: Too many arguments, extra arguments ignored"

	tokens = argv[0].split(':')
	if (len(tokens) != 2):
		print "Error: time formatted incorrectly, enter as HH:MM (e.g. 14:10)"
		usage()
		sys.exit(-1)
	try: 
		hour = int(tokens[0])
		minute = int(tokens[1])
		if hour < 0 or hour > 23:
			print "Error: hour in time must be between 0 and 23 (e.g., 14:10)"
			usage()
			sys.exit(-1)
		if minute < 0 or minute > 59:
			print "Error: minute in time must be between 0 and 59 (e.g., 14:10)"
			usage()
			sys.exit(-1)
	except:
		print "Error: must provide time as HH:MM (e.g., 14:10)"
		usage()
		sys.exit(-1)

	if len(argv) > 4:
		if len(argv) < 6:
			print "Error: when running experiment multiple times, must provide an interval for repetitions"
			usage()
			sys.exit(-1)
		try: 
			trials = int(argv[4])
			if (trials < 1):
				print "Error: must provide number of trials as an integer greater than 0"
				usage()
				sys.exit(-1)
		except:
			print "Error: must provide number of trials as an integer"
			usage()
			sys.exit(-1)
		try:
			interval = int(argv[5])
			if (interval < 5):
				print "Error: interval between trials must be at least 5 minutes"
				usage()
				sys.exit(-1)
		except:
			print "Error; must provide interval between trials as an integer (minutes)"
			usage()
			sys.exit(-1)
	else:
		trials = 1
		interval = 0
	return hour, minute, argv[1], argv[2], argv[3], trials, interval

def usage():
	print "Usage: python FlowSimCron <time> <path_to_FlowSim.py> <input_file> <output_File> [<number_of_trials> <interval>]"

if __name__ == '__main__':
	main(sys.argv[1:])