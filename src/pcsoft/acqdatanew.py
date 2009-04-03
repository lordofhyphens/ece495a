##################################################
#                   acqdata.py                   #
##################################################
# Performs data acquisition over serial port     #
# Well, acquires data from a file at the moment. #
##################################################

import os, sys, struct
from time import localtime, strftime

global pathTo;
pathTo = 'data\\'


############################
#   Function definitions   #
############################

def getPre():
	pref = strftime("%d%b%Y", localtime());

	max = 0;
	undsplit = []
	for root, dirs, files in os.walk(pathTo):
		for name in files:
			name = name.split('.')[0]
			undsplit = name.split('_')
			if undsplit[0] == pref:
				if int(undsplit[1][0]) > max:
					max = int(undsplit[1][0])

	acqnum = max + 1
	return acqnum, pref



def openNewOut(filepart, pref, acqnum):
	filename = pref+'_'+str(acqnum)+filepart+'.dat'
	acqname = pref+'_'+str(acqnum)
	return open(pathTo+filename, "wb"), acqname


class acqConfig:
	"configures acqdisp.txt"
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
	acqnum, pref = getPre()

	dfilepart = 'a';
	dfileinc = 0;
	writeF, acqName = openNewOut(dfilepart, pref, acqnum)
	conf = acqConfig(acqName)




if __name__ == "__main__":
	sys.exit(main())



