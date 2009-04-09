##################################################
#                   acqdata.py                   #
##################################################
# Performs data acquisition over serial port     #
# Well, acquires data from a file at the moment. #
##################################################

import os, sys, struct
from time import localtime, strftime
from socket import *

global pathTo;
pathTo = 'data\\'


############################
#   Function definitions   #
############################

def getPre():
	"""Returns date-based file prefix as well as the acquisition number for this day"""
	# Get prefix, in ddMonYYYY format
	pref = strftime("%d%b%Y", localtime());

	# Using pathTo, find list of all files with above prefix
	# and get the last acqnum with split()
	max = 0;
	undsplit = []
	for root, dirs, files in os.walk(pathTo):
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
	filename = pref+'_'+str(acqnum)+filepart+'.dat'
	acqname = pref+'_'+str(acqnum)
	return open(pathTo+filename, "wb"), acqname


class acqConfig:
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
		


def main():
	# Get date-based file prefix
	acqnum, pref = getPre()

	# Socket params
	host = "localhost"
	port = 19367
	buf = 4096
	addr = (host,port)

	sock = socket(AF_INET, SOCK_DGRAM)

	dfilepart = 'a';
	dfileinc = 0;
	writeF, acqName = openNewOut(dfilepart, pref, acqnum)
	conf = acqConfig(acqName)




if __name__ == "__main__":
	sys.exit(main())



