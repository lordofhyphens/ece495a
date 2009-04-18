# acqdata.py - acquires data over serial port

import os, sys, struct
from time import localtime, strftime
from socket import *


# Setup global variables
global pathto, fsuffix, filepart, fileinc;
pathto = 'data\\'
fsuffix = '.dat'
filepart = 'a'
fileinc = 0


def getPre():
	"""Returns date-based file prefix as well as the acquisition number for this day"""
	# Get prefix, in ddMonYYYY format
	pref = strftime("%d%b%Y", localtime());

	# Using pathto, find list of all files with above prefix
	# and get the last acqnum with split()
	max = 0;
	undsplit = []
	for root, dirs, files in os.walk(pathto):
		for name in files:
			name = name.split('.')[0]
			undsplit = name.split('_')
			if undsplit[0] == pref:
				if int(undsplit[1][0]) > max:
					max = int(undsplit[1][0])

	# Increment acqnum, return acqnum & prefix
	acqnum = max + 1
	return acqnum, pref




def openNewOut(filepart, pref, acqnum):
	"""Opens a data acquisition file, returns a) the file handle 
	and b) the name of acquisition file (excluding extension)"""

	filename = pref+'_'+str(acqnum)+filepart+fsuffix
	acqname = pref+'_'+str(acqnum)
	return open(pathto+filename, "wb"), acqname




class acqFileConfig:
	"""configures acqinfo.txt"""

	def __init__(self, pref):
		self.prefix = pref
		self.lastCh = ""

	def setLast(self, ch):
		self.lastCh = ch

	def updateInfo(self):
		self.writetext = self.prefix+':'+self.lastCh+'\n'
		self.infoF = open("acqinfo.txt", "a")
		self.infoF.write(self.writetext)




def parseBin(chunk):
	"""Parse a chunk of binary data into a string"""

	parsed = []
	for i in range(0, len(chunk)):
		parsed.append(struct.unpack('b', chunk[i]))

	return parsed




def acqbin(acqfile):
	"""Acquire data from binary input file. Used to test interface
	in the event that real serial input tests are never performed."""

	# Setup global variables
	global pathto, fsuffix, filepart, fileinc;
	pathto = 'data\\'
	fsuffix = '.dat'
	filepart = 'a'
	fileinc = 0

	# Get date-based file prefix
	acqnum, pref = getPre()

	# Open acqfile, first output file & initialize acqFileConfig class
	f = open(acqfile, "rb")
	writeF, acqName = openNewOut(filepart, pref, acqnum)
	conf = acqFileConfig(acqName)

	# Read 4096-byte chunks from file and convert each char to integer
	while 1:
		thisChunk = f.read(4096).rstrip('\n')

		# Open a new binary file if the old file is 100 kb in size
		if fileinc > 24:
			filepart = chr(ord(filepart) + 1)
			fileinc = 0;
			writeF.close()
			writeF, writeFileName = openNewOut(filepart, pref, acqnum)
			conf.setLast(filepart)
	
		# If read data is empty, break loop
		# Otherwise keep processing data
		if len(thisChunk) == 0: 
			break
		else:
			parseNums = parseBin(thisChunk)

			for i in range(0, len(parseNums)):
				writeF.write(struct.pack('b', parseNums[i][0]))
	
		fileinc += 1
	

	conf.updateInfo()
		



def main():
	# Get date-based file prefix
	acqnum, pref = getPre()

	# Socket params
	host = "localhost"
	port = 19367
	addr = (host,port)
	buff = 4096

	# Create socket and bind
	sock = socket(AF_INET, SOCK_DGRAM)
	sock.bind(addr)


	while(1):
		data = sock.recv(buff)
		
		if data == "begin":
			print "Beginning acquisition"

			#
			writeF, acqName = openNewOut(filepart, pref, acqnum)
			conf = acqFileConfig(acqName)

		elif data == "end":
			print "Ending acquisition (word is bond)"

	
if __name__ == "__main__":
	sys.exit(main())
