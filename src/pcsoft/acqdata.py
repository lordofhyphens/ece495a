# acqdata.py - acquires data over serial port or binary input file (for debugging)


import os, sys, struct, socket, serial
from time import localtime, strftime, sleep
from pcsoft_cfg import *


# Setup global variables
global filepart, fileinc
filepart = 'a'
fileinc = 0


def getPre():
	"""Returns date-based file prefix as well as the acquisition number for this day"""
	# Get prefix, in ddMonYYYY format
	pref = strftime("%d%b%Y", localtime());

	# Using pathtodata, find list of all files with above prefix
	# and get the last acqnum with split()
	max = 0;
	undsplit = []
	for root, dirs, files in os.walk(pathtodata):
		for name in files:
			name = name.split('.')[0]
			undsplit = name.split('_')

			if undsplit[0] == pref:
				if int(undsplit[1][0:len(undsplit[1])-1]) > max:
					max = int(undsplit[1][0:len(undsplit[1])-1])

	# Increment acqnum, return acqnum & prefix
	acqnum = max + 1
	return acqnum, pref




def openNewOut(filepart, pref, acqnum):
	"""Opens a data acquisition file, returns a) the file handle 
	and b) the name of acquisition file (excluding extension)"""

	filename = pref+'_'+str(acqnum)+filepart+fext
	acqname = pref+'_'+str(acqnum)
	return open(pathtodata+filename, "wb"), acqname




class acqFileConfig:
	"""configures the write to acqinfo.txt"""

	def __init__(self, pref, label):
		self.prefix = pref
		self.lastCh = ""
		self.acqlabel = label

	def setLast(self, ch):
		self.lastCh = ch

	def updateInfo(self):
		self.writetext = self.prefix+':'+self.lastCh+'|'+self.acqlabel+'\n'
		self.infoF = open("acqinfo.txt", "a")
		self.infoF.write(self.writetext)



def parseSerial(chunk):
	"""Parse a chunk from the serial port"""
	pass



def parseBin(chunk):
	"""Parse a chunk of binary data into a string"""

	parsed = []
	for i in range(0, len(chunk)):
		parsed.append(struct.unpack('b', chunk[i]))

	return parsed




def acqbin(acqfile, acqlabel):
	"""Acquire data from binary input file. Used to test interface
	in the event that real serial input tests are never performed."""

	# Setup global variables
	global filepart, fileinc;
	filepart = 'a'
	fileinc = 0

	# Get date-based file prefix
	acqnum, pref = getPre()

	# Open acqfile, first output file & initialize acqFileConfig class
	f = open(acqfile, "rb")
	writeF, acqName = openNewOut(filepart, pref, acqnum)
	conf = acqFileConfig(acqName, acqlabel)

	# Read 4096-byte chunks from file and convert each char to integer
	while 1:
		rdchunk = f.read(4096).rstrip('\n')

		# Open a new binary file if current file exceeds partsize global
		if fileinc > (partsize/4) - 1:
			filepart = chr(ord(filepart) + 1)
			fileinc = 0;
			writeF.close()
			writeF, writeFileName = openNewOut(filepart, pref, acqnum)
			conf.setLast(filepart)
	
		# If read data is empty, break loop
		# Otherwise keep processing data
		if len(rdchunk) == 0: 
			break
		else:
			parsed = parseBin(rdchunk)

			for i in range(0, len(parsed)):
				writeF.write(struct.pack('b', parsed[i][0]))
	
		fileinc += 1
	

	# write to acqinfo
	conf.updateInfo()
		



def main():
	# Get date-based file prefix
	acqnum, pref = getPre()
	
	# Establish socket
	sckt = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
	sckt.connect((sckhost, sckport))
	sckt.send('init')

	termseq = ''
	
	drecv = sckt.recv(1024).split(':')
	if drecv[0] == 'begin':
		print "Beginning acquisition"

	"""
	# Open acqfile, first output file & initialize acqFileConfig class
	writeF, acqName = openNewOut(filepart, pref, acqnum)
	conf = acqFileConfig(acqName, acqlabel)
	
	# Open serial port
	ser = serial.Serial(serialport, baudrate=serialbaud)

	while 1:
		rdchunk = ser.read(5000)

		# Open a new binary file if current file exceeds partsize global
		if fileinc > (partsize/4) - 1:
			filepart = chr(ord(filepart) + 1)
			fileinc = 0;
			writeF.close()
			writeF, writeFileName = openNewOut(filepart, pref, acqnum)
			conf.setLast(filepart)
	
		# If read data is empty, break loop
		# Otherwise keep processing data
		if len(rdchunk) == 0: 
			break
		else:
			parsed = parseSerial(rdchunk)

			for i in range(0, len(parsed)):
				writeF.write(struct.pack('b', parsed[i][0]))
	
		fileinc += 1
	

	# close serial port, write to acqinfo
	ser.close()
	conf.updateInfo()
	"""

	# Sleep 3 seconds to simulate data acq over serial
	print "Ending acquisition"


	# Close socket
	sckt.shutdown(socket.SHUT_RDWR)
	sckt.close()

	
if __name__ == "__main__":
	sys.exit(main())
