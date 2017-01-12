import scipy.io
import csv
import sys
import operator
from random import randrange


if len(sys.argv) < 3:
	print "wrong inputs"
	exit(-1)

def getNumToIpMapping(filename):
	mapping = {}
	with open(filename, 'rb') as f:
		reader = csv.reader(f, delimiter= ',')
		for row in reader:
			mapping[row[0]] = row[1]
		f.close()
	return mapping


def getFileList(fileList):
	return  fileList

mapping = getNumToIpMapping(sys.argv[1])
files = getFileList([sys.argv[i] for i in range(2, len(sys.argv))])
try:
	fopens = [open("server%d.csv" % i, "w") for i in range(1,17)]
	header = ['start_time', 'src_ip', 'src_port', 'dest_ip', 'dest_port', 'size']
	writers = [csv.DictWriter(fopens[i],header) for i in range(16)]

	for file in files:
		mat = scipy.io.loadmat(file)
		sizes = mat["JOBSIZE"]
		srcServers = None
		destServers = None
		# assign two lists in SERVERS to src and des
		for item in mat["SERVERS"]:
			srcServers = destServers
			destServers = item
		startTimes = mat["JOB_ARR_TIME"]
		
		for i in range(sizes.size):
			sz = sizes.item(i)
			srcServer = srcServers.item(i) # !! when finished mapping, only use srcIP&desIP
			srcIP = mapping[str(srcServer)]
			destServer = destServers.item(i)
			destIP = mapping[str(destServer)]
			startTime = startTimes.item(i)
			srcPort = randrange(10000,10199)
			destPort = randrange(11000,11199) 
			writer = writers[srcServer-1]
			#header = ['start_time', 'src_ip', 'src_port', 'dest_ip', 'dest_port', 'size']
			writer.writerow({'start_time':startTime,'src_ip':srcIP, 'src_port':srcPort, 'dest_ip':destIP, 'dest_port':destPort, 'size':sz})		

finally:
	for f in fopens:
		f.close()

# sorting
for i in range(1,17):
	data = None
	with open("server%d.csv" % i, "r") as f:
		reader = csv.reader(f)
		data = list(reader)
		data.sort(key = lambda x: float(x[0]))
	with open("server%d.csv" % i, "w") as f:
		writer = csv.writer(f)
		writer.writerow(header)
		for line in data:
			writer.writerow(line)




