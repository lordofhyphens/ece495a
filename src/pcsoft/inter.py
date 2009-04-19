# inter.py - graphical front-end

import os, sys, glob, socket
from Tkinter import *
from pcsoft_cfg import *
from math import ceil
from time import sleep

global acqfile
acqfile = ''


class App(Toplevel):
	def __init__(self):
		# Init window, setup window close handler
		Toplevel.__init__(self)
		self.protocol("WM_DELETE_WINDOW", self.newClose)

		# Set old behavior flag & init socketOpened
		self.socketOpened = False
		if acqfile != "":
			self.old = True
		else:
			self.old = False

		# Draw interface widgets
		self.makeAcqWidgets()
		self.makeDispWidgets()
		self.makeCtrlWidgets()




	def newClose(self):
		"""Close socket connection and destroy the root window"""

		# If socket is open, close it
		if self.socketOpened == True:
			self.closeSocket()
		
		print "\nTerminating PCDiag Interface"
		root.destroy()




	def openSocket(self):
		"""Create socket connection"""

		# Establish socket
		self.sckt = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
		self.sckt.bind((sckhost, sckport))
		self.sckt.listen(1)
		self.socketOpened = True


	

	def closeSocket(self):
		"""Close socket connection"""

		self.conn.shutdown(socket.SHUT_RDWR)
		self.sckt.close()
		self.socketOpened = False




	def makeAcqWidgets(self):
		# Data Acquisition LabelFrame
		self.acqfrm = LabelFrame(self, text="Data Acquisition", padx=5, pady=5)
		self.acqfrm.grid(row=0, column=0, in_=self, sticky=N+E+S+W)


		# "Label" label
		Label(self.acqfrm, text="Label (optional): ").grid(row=1, column=0, sticky=E)
		
		# "Label" entry box
		self.acqlabel = StringVar()
		self.labelentry = Entry(self.acqfrm, textvariable=self.acqlabel)
		self.labelentry.grid(row=1, column=1, sticky=E+W)



		# Begin/End Acquisition buttons
		self.beginAcq = Button(self.acqfrm, text="Begin Acquisition", width=15, command=self.performAcq)
		self.beginAcq.grid(row=4, column=0, columnspan=2, in_=self.acqfrm, sticky=S)

		# Do some resizing
		self.acqfrm.columnconfigure(0, minsize=40)
		self.acqfrm.columnconfigure(1, minsize=160)
		self.acqfrm.rowconfigure(0, minsize=20)
		self.acqfrm.rowconfigure(2, minsize=20)




	def makeDispWidgets(self):
		# Data Display LabelFrame
		self.dispfrm = LabelFrame(self, text="Data Display", padx=5, pady=5)
		self.dispfrm.grid(row=0, column=1, in_=self)

		
		# Make arrow buttons
		self.llarr = Button(self.dispfrm, text="<<", width=1, command=self.firstPage)
		self.llarr.grid(row=0, column=2, in_=self.dispfrm, sticky=E+W)
		self.larr = Button(self.dispfrm, text="<", width=1, command=self.backPage)
		self.larr.grid(row=0, column=3, in_=self.dispfrm, sticky=E+W)

		self.rarr = Button(self.dispfrm, text=">", width=1, command=self.forwardPage)
		self.rarr.grid(row=0, column=4, in_=self.dispfrm, sticky=E+W)
		self.rrarr = Button(self.dispfrm, text=">>", width=1, command=self.lastPage)
		self.rrarr.grid(row=0, column=5, in_=self.dispfrm, sticky=E+W)


		# Make acq listbox, bind select event
		self.acqlist = Listbox(self.dispfrm, selectmode=EXTENDED)
		self.acqlist.grid(row=1, column=0, in_=self.dispfrm, columnspan=6, rowspan=3, sticky=E+W)
		self.acqlist.bind('<<ListboxSelect>>', self.checkSel)

		# Make acq list scrollbar
		listscroll = Scrollbar(self.dispfrm, orient=VERTICAL, relief=SUNKEN)
		listscroll.config(command=self.acqlist.yview)
		self.acqlist.config(yscrollcommand=listscroll.set)
		listscroll.grid(row=1, column=6, in_=self.dispfrm, columnspan=1, rowspan=3, sticky=N+S)

		# Init acqlpg
		self.acqlpg = 0 # Current page

		# Configure larr & llarr to be disabled by default
		self.larr.configure(state=DISABLED)
		self.llarr.configure(state=DISABLED)

		# Get acqlnum
		self.acqlnum = 0 # Number of acqs
		f = open("acqinfo.txt", "r")
		for line in f:
			self.acqlnum = self.acqlnum + 1
		f.close()

		# Set lastpg
		self.lastpg = ceil(1.0*self.acqlnum/acqpgsize) - 1
		
		# If page is last page, disable rarr & rrarr
		if self.acqlpg == self.lastpg:
			self.rarr.configure(state=DISABLED)
			self.rrarr.configure(state=DISABLED)

		# Put acqs in list
		self.fillListBox()


		# Refresh/Clear/Delete/Display buttons
		refreshList = Button(self.dispfrm, text="Refresh", width=7, command=self.fillListBox)
		clearList = Button(self.dispfrm, text="Clear", width=7, command=self.clearAcqs)
		self.deleteB = Button(self.dispfrm, text="Delete", width=7, command=self.deleteAcq)
		self.displayB = Button(self.dispfrm, text="Display", width=7, command=self.displayAcq)

		# Add all four buttons to grid
		refreshList.grid(row=4, column=0, in_=self.dispfrm, columnspan=1)
		clearList.grid(row=4, column=1, in_=self.dispfrm, columnspan=1)
		self.deleteB.grid(row=4, column=2, in_=self.dispfrm, columnspan=2)
		self.displayB.grid(row=4, column=4, in_=self.dispfrm, columnspan=2)

		# Disable display&delete buttons to begin
		self.displayB.configure(state=DISABLED)
		self.deleteB.configure(state=DISABLED)




	def makeCtrlWidgets(self):
		# Control Interface LabelFrame
		self.ctrlfrm = LabelFrame(self, text="Control Interface")
		self.ctrlfrm.grid(row=1, column=0, in_=self, columnspan=2, sticky=E+W)

		# "CONFIG 1-6" label
		config16Lbl = Label(self.ctrlfrm, text="Config. 1-6:")
		config16Lbl.grid(row=1, column=0, columnspan=6, sticky=W)

		# Generate and draw checkboxes, do some column resizing while we're at it
		c = []
		cnfgChck = []

		for i in range(0, 6):
			c.append(IntVar())
			cnfgChck.append(Checkbutton(self.ctrlfrm, text="", variable=c[i]))
			cnfgChck[i].grid(row=2, column=i, in_=self.ctrlfrm)
			self.ctrlfrm.columnconfigure(i, weight=0, minsize=15)


		# Active Input radio label
		activeinLbl = Label(self.ctrlfrm, text="Active Input Type:")
		activeinLbl.grid(row=1, column=7, in_=self.ctrlfrm, columnspan=2, sticky=W)

		# Active Input analog/digital buttons
		r = IntVar()
		self.rad1 = Radiobutton(self.ctrlfrm, text="Analog", variable=r, value=1)
		self.rad2 = Radiobutton(self.ctrlfrm, text="Digital", variable=r, value=2)
		self.rad1.grid(row=2, column=7, in_=self.ctrlfrm, columnspan=1)
		self.rad2.grid(row=2, column=8, in_=self.ctrlfrm, columnspan=1)


		# Output enable label
		outen = IntVar()
		outenChck = Checkbutton(self.ctrlfrm, text="Output Enable", variable=outen)
		outenChck.grid(row=2, column=10, in_=self.ctrlfrm, sticky=W)


		# Resize for prettiness
		self.ctrlfrm.rowconfigure(3, weight=0, minsize=10)
		self.ctrlfrm.columnconfigure(6, weight=0, minsize=20)
		self.ctrlfrm.columnconfigure(9, weight=0, minsize=20)




	def checkSel(self, evt):
		"""Handles Listbox Select events"""

		# Get number of selections
		sellen = len(self.acqlist.curselection())

		if sellen > 1:
			self.displayB.configure(state=DISABLED)
			self.deleteB.configure(state=NORMAL)	
		elif sellen == 0:
			self.displayB.configure(state=DISABLED)
			self.deleteB.configure(state=DISABLED)	
		else:
			self.displayB.configure(state=NORMAL)
			self.deleteB.configure(state=NORMAL)	



	def fillListBox(self):
		"""Reads acquisition list from acqinfo.txt, clears old contents of acquisition
		list and re-adds them."""

		# Open acqinfo, read first line
		infofile = open("acqinfo.txt", "r")
		rln = infofile.readline()

		# Clear acqlist
		self.acqlist.delete(0, END)
		
		i = 0
		lcount = 0
		while (rln != "") and (lcount < acqpgsize):
			# Strip trailing newline and return characters, then split label from line
			rln = rln.strip("\r\n")
			rlnsplit = rln.split('|')

			if i >= self.acqlpg*acqpgsize and i < (self.acqlpg+1)*acqpgsize:
				# Prettify the acqlist entry
				acqlistline = rln[2:5]+' '+rln[0:2]+', '+rln[5:9]+': '+rln[10:len(rlnsplit[0])-1]

				# Add label if it exists
				if rlnsplit[1] != '':
					acqlistline += '  -  '+rlnsplit[1].replace('(>$%pipe%$<)', '|')

				# Add entry to acqlist, increment lcount
				self.acqlist.insert(END, acqlistline)
				lcount = lcount+1

			# Read next line, increment i
			rln = infofile.readline()
			i = i+1

		# Close acqinfo
		infofile.close()




	def clearAcqs(self):
		"""Deletes all acquisition files in pathtodata, clears contents of acqinfo.txt and
		acqdisp.txt, clears acquisition list."""

		# Get acquisition names
		acqnames = []
		infofile = open("acqinfo.txt", "r")
		rln = infofile.readline()
		while rln != "":
			acqnames.append(rln.split(':')[0])
			rln = infofile.readline()

		
		# Delete acq files
		for i in range(len(acqnames)):
			# reconstruct acq filename
			for acqfile in glob.glob(pathtodata+acqnames[i]+'*'+fext):
				os.remove(acqfile)

		# Clear listbox entries
		self.acqlist.delete(0, END)

		
		# Clear acqinfo & acqdisp
		infofile = open("acqinfo.txt", "w")
		infofile.write("")
		infofile.close()

		dispfile = open("acqdisp.txt", "w")
		dispfile.write("")
		dispfile.close()

		# Reset paging vars
		self.acqlnum = 0
		self.acqlpg = 0
		self.lastpg = 0




	def deleteAcq(self):
		"""Deletes currently selected acquisitions, including their related
		files in pathtodata and any pertinent entries in acqinfo and acqdisp. Clears
		the acquisition(s) from the acquisition list as well."""

		# Get currently selected acquisitions
		sel = self.acqlist.curselection()
		acqsToDel = []
		infoLines = []

		# Build and sort acqsToDel
		for i in range(len(sel)):
			acqsToDel.append(int(sel[i]))

		acqsToDel = sorted(acqsToDel)

		# Open acqinfo and read first line
		infofile = open("acqinfo.txt", "r")
		nextLine = infofile.readline()

		# Filter out all to-be-deleted acqs from acqinfo and store in infoLines
		i = 0;
		delInd = 0;
		while nextLine != "":
			nextLine = nextLine.rstrip("\r\n")

			if delInd < len(acqsToDel):
				if i != acqsToDel[delInd]:
					infoLines.append(nextLine);
				else:
					delInd += 1
			else:
				infoLines.append(nextLine);

			nextLine = infofile.readline()
			i = i + 1

		infofile.close()


		# Delete acq files
		for i in range(len(acqsToDel)):
			acq = self.getAcqFromSel(acqsToDel[i])
			for acqfile in glob.glob(pathtodata+acq+'*'+fext):
				os.remove(acqfile)


		# Update acqinfo
		infofile = open("acqinfo.txt", "w")

		for i in range(len(infoLines)):
			infofile.write(infoLines[i]+"\n")
		infofile.close()


		# Clear acqdisp if necessary
		dispfile = open("acqdisp.txt", "r")
		acqdisp = dispfile.readline()
		dispfile.close()

		for i in range(len(acqsToDel)):
			if acqdisp.split(":")[0] == self.acqlist.get(acqsToDel[i]):
				dipsfile = open("acqdisp.txt", "w")
				dispfile.write("")
				dipsfile.close()
				break

		# Refresh listbox
		self.fillListBox()




	def displayAcq(self):
		"""Writes currently selected acquisition to acqdisp.txt"""

		# Get current selection
		sel = self.acqlist.curselection()

		# Open acqinfo and read first line
		infofile = open("acqinfo.txt", "r")
		nextLine = infofile.readline()

		# While last read line is not empty (i.e. no EOF)
		while nextLine != "":
			# Strip off newline
			nextLine = nextLine.rstrip("\r\n")

			# acqinfo stores acquisitions one per line in the following format:
			#
			# DDMonYYYY_P:c
			#
			# "DD"   - two-digit date of acquisition 
			# "Mon"  - 3-letter abbreviation of the month of the acquisition
			# "YYYY" - four digit year of the acquisition
			# "P"    - denotes the Pth acquisition on said day
			# "c"    - character of the last part of the acquisition
			#
			# The acquisition itself is fully described by everything before the colon,
			# so split string at the colon and compare with the name of the selected
			# acquisition, which does not include the last part. The only purpose
			# of this loop is to determine the last part of the acquisition, which we
			# cannot determine from the list selection alone.
			if nextLine.split(":")[0] == getAcqFromSel(int(sel[0])):
				toWrite = nextLine
				break

			# Read next line
			nextLine = infofile.readline()


		# Close acqinfo, write to acqdisp
		infofile.close()
		dispfile = open("acqdisp.txt", "w")
		dispfile.write(toWrite)
		dispfile.close()


		

	def performAcq(self):
		"""Begin performing data acquisition"""

		# Disable beginAcq, disable labelentry 
		self.beginAcq.configure(state=DISABLED)
		self.labelentry.configure(state=DISABLED)

		# Force a re-draw
		self.beginAcq.update_idletasks()
		self.labelentry.update_idletasks()

		# If old behavior, call acqbin. Otherwise launch acqdata in a subprocess
		# and send "begin" message over socket
		if self.old == True:
			# get acqlabel
			theacqlabel = self.acqlabel.get()

			# pipes used to delimit label so replace all instances
			theacqlabel = theacqlabel.replace('|', '(>$%pipe%$<)')

			# Acquire data
			acqdata.acqbin(acqfile, theacqlabel)
		else:
			# Open socket, launch subprocess & accept sock connection
			self.openSocket()
			self.proc = subprocess.Popen('acqdata.py',shell=True)
			self.conn, self.addr = self.sckt.accept()

			data = self.conn.recv(1024)

			if data == "init":
				self.conn.send('begin')

				# If no old behavior, send a terminate message, wait for child and close socket
				if self.old == False:
					self.conn.sendto("end", self.addr)
					self.proc.wait()
					self.closeSocket()
				
		
		# Pause for 1 second, give acquisition time to do its thang
		sleep(1)

		# Enable labelentry and beginAcq
		self.beginAcq.configure(state=NORMAL)
		self.labelentry.configure(state=NORMAL)

		# Update acqlnum
		self.acqlnum = self.acqlnum + 1
		self.lastpg = ceil(1.0*self.acqlnum/acqpgsize) - 1


		if self.acqlpg != self.lastpg:
			# If page is not last and keeponacq is false, change to last.
			if viewnewacq == True:
				self.lastPage()
				self.fillListBox()
			else:
				# This is in case we were on what was previously the last page
				# i.e. If page size = 10 and we're at 10 acqs, this acq causes
				# page 2 to become available
				self.rarr.configure(state=NORMAL)
				self.rrarr.configure(state=NORMAL)
		else:
			self.fillListBox()


		# Set display to end of page if past visible threshhold
		if self.acqlpg == self.lastpg:
			pglen = self.acqlnum % acqpgsize
			if pglen > 10:
				self.acqlist.yview(pglen - 10)


			

	def getAcqFromSel(self, sel):
		""" Given the selection number, return the acquisition name as
		used in the file name (i.e. DDMonYYYY_N)"""

		acqval = self.acqlist.get(sel)
		return acqval[4:6]+acqval[0:3]+acqval[8:12]+'_'+acqval[14:len(acqval)+1]




	def backPage(self):
		"""Sends acqlist back one page"""
		
		# If current page is last page, re-enable rarr & rrarr
		if self.acqlpg == self.lastpg:
			self.rarr.configure(state=NORMAL)
			self.rrarr.configure(state=NORMAL)

		# Decrement acqlpg and re-fill listbox
		self.acqlpg = self.acqlpg - 1
		self.fillListBox()

		# If page is now first, disable larr & llarr
		if self.acqlpg == 0:
			self.larr.configure(state=DISABLED)
			self.llarr.configure(state=DISABLED)




	def firstPage(self):
		"""Sends acqlist to last page"""
		
		# If current page is last page, re-enable rarr & rrarr
		if self.acqlpg == self.lastpg:
			self.rarr.configure(state=NORMAL)
			self.rrarr.configure(state=NORMAL)

		# Set acqlpg to 0 and re-fill listbox
		self.acqlpg = 0
		self.fillListBox()

		# If page is now first, disable larr & llarr
		if self.acqlpg == 0:
			self.larr.configure(state=DISABLED)
			self.llarr.configure(state=DISABLED)


		

	def forwardPage(self):
		"""Sends acqlist forward one page"""

		# If current page is first, re-enable larr & llarr
		if self.acqlpg == 0:
			self.larr.configure(state=NORMAL)
			self.llarr.configure(state=NORMAL)

		# Increment acqlpg and re-fill listbox
		self.acqlpg = self.acqlpg + 1
		self.fillListBox()
			
		# If page is now last, disable rarr & rrarr
		if self.acqlpg == self.lastpg:
			self.rarr.configure(state=DISABLED)
			self.rrarr.configure(state=DISABLED)



	
	def lastPage(self):
		"""Sends acqlist to last page"""

		# If current page is first, re-enable larr & llarr
		if self.acqlpg == 0:
			self.larr.configure(state=NORMAL)
			self.llarr.configure(state=NORMAL)

		# Set acqlpg to last and re-fill listbox
		self.acqlpg = self.lastpg
		self.fillListBox()
			
		# If page is now last, disable rarr & rrarr
		if self.acqlpg == self.lastpg:
			self.rarr.configure(state=DISABLED)
			self.rrarr.configure(state=DISABLED)




# If command line arg present, invoke binary input file behavior
if len(sys.argv) == 2:
	acqfile = sys.argv[1]

# If old behavior, import old acqdata. Else import subprocess
if acqfile != '':
	import acqdata
else:
	import subprocess



# Create main window and hide
root = Tk()
root.withdraw()

# Create a top level, add a title
app = App()
app.title("PCDiag Control/Display Interface")
root.mainloop() 

