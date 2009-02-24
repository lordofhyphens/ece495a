# acqdata.py
# Performs data acquisition over serial port
# Well, acquires data from a file at the moment.
import sys, struct


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
	


def openNewOut(filenum):
	return open(r'data\d'+str(filenum)+'.dat', "wb")



def parseHexTextData(chunk):
	parsed = ""
	parseNums = []

	for i in range(0, len(chunk)):
		parsed += hex2bin(chunk[i])

	
	for j in range(0, len(parsed) / 8):
		range1 = j*8
		range2 = (j+1)*8
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

dfilenum = 0;
dfileinc = 0;
writeF = openNewOut(dfilenum)


# Read 4096-byte chunks from file and convert each char to integer
while 1:
	thisChunk = f.read(4096).rstrip('\n')

	# Open a new binary file if the old file is 100 kb in size
	if dfileinc > 24:
		dfilenum += 1
		writeF.close()
		writeF = openNewOut(dfilenum)

	# If read data is empty, break loop
	# Otherwise keep processing data
	if len(thisChunk) == 0: 
		break
	else:
		parseNums = parseHexTextData(thisChunk)

		for i in range(0, len(parseNums)):
			writeF.write(struct.pack('B', parseNums[i]))


