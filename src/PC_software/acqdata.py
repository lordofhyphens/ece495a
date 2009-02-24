# acqdata.py
# Performs data acquisition over serial port
# Well, acquires data from a file at the moment.
import os, sys, struct


# Get file prefix
from time import gmtime, strftime
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

	

###***** Function definitions *****##

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



def bin2int(bin):
	conv = 0;

	for i in range(0, len(bin)):
		conv = conv + int(bin[i]) * 2**(7-i)
	
	return conv
	


def openNewOut(filepart):
	filename = 'data\\'+pref+'_'+str(acqnum)+filepart+'.dat'
	return open(filename, "wb")



def parseHexTextData(chunk):
	parsed = ""
	parseNums = []

	for i in range(0, len(chunk)):
		parsed += hex2bin(chunk[i])

	
	for j in range(0, len(parsed) / 8):
		range1 = j*8
		range2 = (j+1)*8
		parseNums.append(bin2int(parsed[range1:range2]))


	# If data doesn't evenly match 8 bit chunks, pad last 4
	if range2 != len(parsed):
		range1 = range2
		range2 = len(parsed)
		parseNums.append(bin2int(parsed[range1:range2]))


	return parseNums

		





###***** Begin program *****###

if len(sys.argv) == 2:
	acqfile = sys.argv[1]
else:
	if len(sys.argv) == 1:
		prompt = "Please enter the name of the file to acquire data from: "
	elif len(sys.argv) > 2:
		prompt = "Too many arguments, please enter the name of the file to acquire data from: "
	
	acqfile = raw_input(prompt)


print "\nAcquiring data from", acqfile
f = open(acqfile, "r")

dfilepart = 'a';
dfileinc = 0;
writeF = openNewOut(dfilepart)


# Read 4096-byte chunks from file and convert each char to integer
while 1:
	thisChunk = f.read(4096).rstrip('\n')

	# Open a new binary file if the old file is 100 kb in size
	if dfileinc > 24:
		dfilepart = chr(ord(dfilepart) + 1)
		dfileinc = 0;
		writeF.close()
		writeF = openNewOut(dfilepart)

	# If read data is empty, break loop
	# Otherwise keep processing data
	if len(thisChunk) == 0: 
		break
	else:
		parseNums = parseHexTextData(thisChunk)

		for i in range(0, len(parseNums)):
			writeF.write(struct.pack('B', parseNums[i]))
	
	dfileinc += 1


