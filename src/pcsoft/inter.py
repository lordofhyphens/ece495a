# inter.py - graphical front-end

from Tkinter import *
import os, sys, glob, socket
from pcsoft_cfg import *

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

		# "Type" label
		Label(self.acqfrm, text="Type: ").grid(row=0, column=0, sticky=E)

		# Data type drop-down menu
		typeOpts = [
			" ",
			"Oscilloscope Waveform",
			"DC Voltage",
			"DC Current",
			"AC Voltage",
			"AC Current"
			]

		acqtype = StringVar()
		acqtype.set(typeOpts[0])

		typeMenu = OptionMenu(self.acqfrm, acqtype, *typeOpts)
		typeMenu.grid(row=0, column=1, in_=self.acqfrm, sticky=E+W)


		# "Label" label
		Label(self.acqfrm, text="Label (optional): ").grid(row=1, column=0, sticky=E)
		
		# "Label" entry
		self.acqlabel = StringVar()
		Entry(self.acqfrm, textvariable=self.acqlabel).grid(row=1, column=1, sticky=E+W)



		# Begin/End Acquisition buttons
		self.beginAcq = Button(self.acqfrm, text="Begin Acquisition", width=15, command=self.beginAcqClick)
		self.endAcq = Button(self.acqfrm, text="End Acquisition", width=15, command=self.endAcqClick)
		self.beginAcq.grid(row=3, column=0, columnspan=2, in_=self.acqfrm, sticky=S)

		# Do some resizing
		self.acqfrm.columnconfigure(0, minsize=40)
		self.acqfrm.columnconfigure(1, minsize=160)
		self.acqfrm.rowconfigure(2, minsize=15)




	def makeDispWidgets(self):
		# Data Display LabelFrame
		self.dispfrm = LabelFrame(self, text="Data Display", padx=5, pady=5)
		self.dispfrm.grid(row=0, column=1, in_=self)

		## Make acq listbox, bind select event
		self.acqlist = Listbox(self.dispfrm, selectmode=EXTENDED)
		self.acqlist.grid(row=0, column=0, in_=self.dispfrm, columnspan=4, rowspan=3, sticky=E+W)
		self.acqlist.bind('<<ListboxSelect>>', self.checkSel)


		# Make acq listbox scrollbar
		listscroll = Scrollbar(self.dispfrm, orient=VERTICAL)
		listscroll.config(command=self.acqlist.yview)
		listscroll.grid(row=0, column=4, in_=self.dispfrm, columnspan=1, rowspan=3, sticky=N+S)
		self.fillListBox()

		# Refresh/Clear/Delete/Display buttons
		refreshList = Button(self.dispfrm, text="Refresh", width=7, command=self.fillListBox)
		clearList = Button(self.dispfrm, text="Clear", width=7, command=self.clearAcqs)
		self.deleteB = Button(self.dispfrm, text="Delete", width=7, command=self.deleteAcq)
		self.displayB = Button(self.dispfrm, text="Display", width=7, command=self.displayAcq)

		# Add all four buttons to grid
		refreshList.grid(row=4, column=0, in_=self.dispfrm)
		clearList.grid(row=4, column=1, in_=self.dispfrm)
		self.deleteB.grid(row=4, column=2, in_=self.dispfrm)
		self.displayB.grid(row=4, column=3, in_=self.dispfrm)

		# Disable display&delete buttons to begin
		self.displayB.configure(state=DISABLED)
		self.deleteB.configure(state=DISABLED)



	def makeCtrlWidgets(self):
		# Control Interface LabelFrame
		self.ctrlfrm = LabelFrame(self, text="Control Interface")
		self.ctrlfrm.grid(row=1, column=0, in_=self, columnspan=2, sticky=E+W)

		# "CONFIG 1-6" label
		config16Lbl = Label(self.ctrlfrm, text="Config. 1-6:")
		config16Lbl.grid(row=0, column=0, columnspan=6, sticky=W)

		# Generate and draw checkboxes, do some column resizing while we're at it
		c = []
		cnfgChck = []

		for i in range(0, 6):
			c.append(IntVar())
			cnfgChck.append(Checkbutton(self.ctrlfrm, text="", variable=c[i]))
			cnfgChck[i].grid(row=1, column=i, in_=self.ctrlfrm)
			self.ctrlfrm.columnconfigure(i, weight=0, minsize=15)


		# Active Input radio label
		activeinLbl = Label(self.ctrlfrm, text="Active Input Type:")
		activeinLbl.grid(row=0, column=7, in_=self.ctrlfrm, columnspan=2, sticky=W)

		# Active Input analog/digital buttons
		r = IntVar()
		self.rad1 = Radiobutton(self.ctrlfrm, text="Analog", variable=r, value=1)
		self.rad2 = Radiobutton(self.ctrlfrm, text="Digital", variable=r, value=2)
		self.rad1.grid(row=1, column=7, in_=self.ctrlfrm, columnspan=1)
		self.rad2.grid(row=1, column=8, in_=self.ctrlfrm, columnspan=1)


		# Output enable label
		outen = IntVar()
		outenChck = Checkbutton(self.ctrlfrm, text="Output Enable", variable=outen)
		outenChck.grid(row=1, column=10, in_=self.ctrlfrm, sticky=W)


		# Resize columns 6 & 9 for spacing
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

		infofile = open("acqinfo.txt", "r")
		rln = infofile.readline()

		self.acqlist.delete(0, END)

		while rln != "":
			# Strip trailing newline and return characters
			rln = rln.strip("\r\n")
			rlnsplit = rln.split('|')

			# Prettify the acqlist entry
			acqlistline = rln[2:5]+' '+rln[0:2]+', '+rln[5:9]+': '+rln[10:len(rlnsplit[0])-1]

			# Add label if it exists
			if rlnsplit[1] != '':
				acqlistline += '  -  '+rlnsplit[1].replace('(>$%pipe%$<)', '|')

			self.acqlist.insert(END, acqlistline)
			rln = infofile.readline()

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
			for acqfile in glob.glob(pathtodata+acqnames[i]+'*'+fsuffix):
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
			for acqfile in glob.glob(pathtodata+acq+'*'+fsuffix):
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


		

	def beginAcqClick(self):
		"""Replace beginAcq button with endAcq, send begin message to acqdata"""

		self.beginAcq.grid_remove()
		self.endAcq.grid(row=3, column=0, columnspan=2, in_=self.acqfrm, sticky=S)

		# If old behavior, call acqbin. Otherwise launch acqdata in a subprocess
		# and send "begin" message over socket
		if self.old == True:
			# get acqlabel
			theacqlabel = self.acqlabel.get()
			# pipes used to delimit label so replace all instances
			theacqlabel = theacqlabel.replace('|', '(>$%pipe%$<)')
			acqdata.acqbin(acqfile, theacqlabel)
		else:
			self.openSocket()
			self.proc = subprocess.Popen('acqdata.py',shell=True)
			self.conn, self.addr = self.sckt.accept()

			data = self.conn.recv(1024)

			if data == "init":
				self.conn.send('begin')




	def endAcqClick(self):
		"""Replace endAcq button with beginAcq, send end message to acqdata"""
		if self.old == False:
			self.conn.sendto("end", self.addr)
			self.proc.wait()
			self.closeSocket()

		self.endAcq.grid_remove()
		self.beginAcq.grid(row=3, column=0, columnspan=2, in_=self.acqfrm, sticky=S)
		self.fillListBox()
		self.setListToEnd()



	
	def getAcqFromSel(self, sel):
		""" Given the selection number, return the acquisition name as
		used in the file name (i.e. DDMonYYYY_N)"""

		acqval = self.acqlist.get(sel)
		return acqval[4:6]+acqval[0:3]+acqval[8:12]+'_'+acqval[14:len(acqval)+1]




	def setListToEnd(self):
		"""Sets listbox to display the end of the list. Used after endAcq."""
		
		# Get size of acqlist
		listlen = self.acqlist.size()
		
		# Set acqlist yview to bottom
		self.acqlist.yview(listlen - 10)

		


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

