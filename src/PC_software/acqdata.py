##################################################
#                   acqdata.py                   #
##################################################
# Performs data acquisition over serial port     #
# Well, acquires data from a file at the moment. #
##################################################

import os, sys, struct
from time import gmtime, strftime


############################
#   Function definitions   #
############################

def getPre():
	pref = strftime("%d%b%Y", gmtime());

	max = 0;
	undsplit = []
	for root, dirs, files in os.walk('data\\'):
		for name in files:
			name = name.split('.')[0]
			undsplit = name.split('_')
			if undsplit[0] == pref:
				if int(undsplit[1][0]) > max:
					max = int(undsplit[1][0])

	acqnum = max + 1
	return acqnum, pref



def openNewOut(filepart, pref, acqnum):
	filename = 'data\\'+pref+'_'+str(acqnum)+filepart+'.dat'
	return open(filename, "wb"), filename


class acqConfig:
	"configures acqconfig.txt"
	def __init__(self, file):
		self.beginFile = file
		self.endFile = ""

	def update(self, file):
		self.endFile = file

	def write(self):
		self.writetext = self.beginFile+';'+self.endFile+';'
		self.confFile = open("acqconfig.txt", "w")
		self.confFile.write(self.writetext)


def hex2bin(c):
	c = c.upper()
	
	if c == "0":
		return "0000"
	elif c == "1":
		return "0001"
	elif c == "2":
		return "0010"
	elif c == "3":
		return "0011"
	elif c == "4":
		return "0100"
	elif c == "5":
		return "0101"
	elif c == "6":
		return "0110"
	elif c == "7":
		return "0111"
	elif c == "8":
		return "1000"
	elif c == "9":
		return "1001"
	elif c == "A":
		return "1010"
	elif c == "B":
		return "1011"
	elif c == "C":
		return "1100"
	elif c == "D":
		return "1101"
	elif c == "E":
		return "1110"
	elif c == "F":
		return "1111"
	else:
		return "0000"



def parseHexTextData(chunk):
	parsed = ""
	parseNums = []

	for i in range(0, len(chunk)):
		parsed += hex2bin(chunk[i])

	
	for j in range(0, len(parsed), 8):
		if (j+8) > len(parsed):
			range2 = len(parsed)
		else:
			range2 = j + 8

		parseNums.append(int(parsed[j:range2], 2))


	return parseNums



def parseBin(chunk):
	parsed = []
	for i in range(0, len(chunk)):
		parsed.append(struct.unpack('b', chunk[i]))

	return parsed

		


def acq(acqfile=""):
	acqnum, pref = getPre()

	if(acqfile == ""):
		prompt = "Please enter the name of the file to acquire data from: "
		acqfile = raw_input(prompt)

	print "\nAcquiring data from", acqfile

	# Determine if input file is binary
	if acqfile.find('.bin') == -1:
		f = open(acqfile, "r")
		inIsBin = 0
	else:
		f = open(acqfile, "rb")
		inIsBin = 1

	dfilepart = 'a';
	dfileinc = 0;
	writeF, writeFileName = openNewOut(dfilepart, pref, acqnum)
	conf = acqConfig(writeFileName)

	# Read 4096-byte chunks from file and convert each char to integer
	while 1:
		thisChunk = f.read(4096).rstrip('\n')

		# Open a new binary file if the old file is 100 kb in size
		if dfileinc > 24:
			dfilepart = chr(ord(dfilepart) + 1)
			dfileinc = 0;
			writeF.close()
			writeF, writeFileName = openNewOut(dfilepart, pref, acqnum)
			conf.update(writeFileName)
	
		# If read data is empty, break loop
		# Otherwise keep processing data
		if len(thisChunk) == 0: 
			break
		else:
			if(inIsBin):
				parseNums = parseBin(thisChunk)
			else:
				parseNums = parseHexTextData(thisChunk)


			for i in range(0, len(parseNums)):
				writeF.write(struct.pack('b', parseNums[i][0]))
	
		dfileinc += 1
	

	conf.write()

