# inter.py - graphical front-end

import os, sys, glob, socket, subprocess
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
		self.octaveOpened = False
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

		# If octave is opened, close it
		if self.octaveOpened == True:
			self.dispproc.terminate()
		
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
		
		# "Label" entry box, init searchlbl
		self.acqlabel = StringVar()
		self.labelentry = Entry(self.acqfrm, textvariable=self.acqlabel)
		self.labelentry.grid(row=1, column=1, columnspan=8, sticky=E+W)
		self.searchlbl = ''


		# "Stop trigger" label
		Label(self.acqfrm, text="Stop Trigger: ").grid(row=3, column=0, sticky=E)

		# Generate trigger checkbuttons
		self.t = []
		trigChck = []

		for i in range(0, 8):
			self.t.append(IntVar())
			trigChck.append(Checkbutton(self.acqfrm, padx=0, pady=0, variable=self.t[i]))
			trigChck[i].grid(row=3, column=(i+1), rowspan=2, sticky=N+S)
			self.acqfrm.columnconfigure((i+1), weight=0, minsize=0)

		# "MSB first" label
		Label(self.acqfrm, text="(MSB first)").grid(row=4, column=0, sticky=E)

		# Begin/End Acquisition buttons
		self.beginAcq = Button(self.acqfrm, text="Begin Acquisition", width=15, command=self.performAcq)
		self.beginAcq.grid(row=6, column=0, columnspan=9, in_=self.acqfrm, sticky=S)

		# Do some resizing
		self.acqfrm.columnconfigure(0, minsize=40)
		self.acqfrm.rowconfigure(0, minsize=20)
		self.acqfrm.rowconfigure(2, minsize=20)
		self.acqfrm.rowconfigure(5, minsize=20)




	def makeDispWidgets(self):
		# Data Display LabelFrame
		self.dispfrm = LabelFrame(self, text="Data Display", padx=5, pady=5)
		self.dispfrm.grid(row=0, column=1, in_=self)


		# Search entry box
		self.searchentry = Entry(self.dispfrm, width=7)
		self.searchentry.grid(row=0, column=0, in_=self.dispfrm, sticky=E+W)
		self.searchentry.insert(0, "Search...")
		self.searchentry.bind("<Button-1>", self.searchClick)
		self.searchentry.bind("<Double-Button-1>", self.searchDClick)
		self.searchentry.bind("<Return>", self.refreshListBox)
		self.searchentry.bind("<Key>", self.searchChanged)

		
		# Make arrow buttons
		self.llarr = Button(self.dispfrm, text="<<", width=1, command=self.firstPage)
		self.llarr.grid(row=0, column=3, in_=self.dispfrm, sticky=E+W)
		self.larr = Button(self.dispfrm, text="<", width=1, command=self.backPage)
		self.larr.grid(row=0, column=4, in_=self.dispfrm, sticky=E+W)

		self.rarr = Button(self.dispfrm, text=">", width=1, command=self.forwardPage)
		self.rarr.grid(row=0, column=5, in_=self.dispfrm, sticky=E+W)
		self.rrarr = Button(self.dispfrm, text=">>", width=1, command=self.lastPage)
		self.rrarr.grid(row=0, column=6, in_=self.dispfrm, sticky=E+W)


		# Make acq listbox, bind select event
		self.acqlist = Listbox(self.dispfrm, selectmode=EXTENDED)
		self.acqlist.grid(row=1, column=0, in_=self.dispfrm, columnspan=7, rowspan=3, sticky=E+W)
		self.acqlist.bind('<<ListboxSelect>>', self.checkSel)

		# Make acq list scrollbar
		listscroll = Scrollbar(self.dispfrm, orient=VERTICAL, relief=SUNKEN)
		listscroll.config(command=self.acqlist.yview)
		self.acqlist.config(yscrollcommand=listscroll.set)
		listscroll.grid(row=1, column=7, in_=self.dispfrm, columnspan=1, rowspan=3, sticky=N+S)

		# Init acqlpg, slbl
		self.acqlpg = 0 # Current page
		self.slbl = ''

		# Get acqtotalnum & acqlnum
		self.acqtotalnum = 0 # Number of acqs
		f = open("acqinfo.txt", "r")
		for line in f:
			self.acqtotalnum = self.acqtotalnum + 1
		f.close()

		# Set acqlnum & lastpg
		self.acqlnum = self.acqtotalnum
		self.lastpg = ceil(1.0*self.acqlnum/acqpgsize) - 1
		
		# Put acqs in list and update arrows
		self.fillListBox()
		self.updateArrows()


		# Refresh/Clear/Delete/Display buttons
		refreshList = Button(self.dispfrm, text="Refresh", width=8, command=self.refreshListBox)
		clearList = Button(self.dispfrm, text="Clear", width=8, command=self.clearAcqs)
		self.deleteB = Button(self.dispfrm, text="Delete", width=8, command=self.deleteAcq)
		self.displayB = Button(self.dispfrm, text="Display", width=8, command=self.displayAcq)

		# Add all four buttons to grid
		refreshList.grid(row=4, column=0, in_=self.dispfrm, columnspan=1)
		clearList.grid(row=4, column=1, in_=self.dispfrm, columnspan=1)
		self.deleteB.grid(row=4, column=3, in_=self.dispfrm, columnspan=2)
		self.displayB.grid(row=4, column=5, in_=self.dispfrm, columnspan=2)

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




	def searchClick(self, event):
		"""If search entry box is clicked on with default value, clear it"""

		if self.searchentry.get() == "Search...":
			self.searchentry.delete(0, END)
			self.searchentry.insert(0, '')




	def searchDClick(self, event):
		"""If search entry box is double clicked, clear value"""

		# If double click occurs when search box has content, disable arrow buttons
		if self.searchentry.get() != '' or self.searchentry.get() != "Search...":
			self.searchChanged()

		# Clear it
		self.searchentry.delete(0, END)
		self.searchentry.insert(0, '')



	
	def searchChanged(self, event=None):
		"""If search term has been changed, disable arrow buttons until
		search term is submitted"""

		self.larr.configure(state=DISABLED)
		self.llarr.configure(state=DISABLED)
		self.rarr.configure(state=DISABLED)
		self.rrarr.configure(state=DISABLED)



	
	def updatePageParams(self):
		"""Update acqlnum, lastpg"""

		# Get current label search entry
		searchterm = self.searchentry.get()

		# If search term is new, set page to first
		if searchterm != self.slbl:
			self.acqlpg = 0

		self.slbl = searchterm
		if self.slbl == "Search...":
			self.slbl = ''

		# First acqinfo open, get number of search matches
		self.acqsrchnum = 0

		if self.slbl != '':
			infofile = open("acqinfo.txt", "r")
			for line in infofile:
				if line.split('|')[1].find(self.slbl) != -1:
					self.acqsrchnum += 1
			infofile.close()

		# Update acqlnum & lastpg
		if self.acqsrchnum == 0:
			self.acqlnum = self.acqtotalnum
		else:
			self.acqlnum = self.acqsrchnum

		self.lastpg = ceil(1.0*self.acqlnum/acqpgsize) - 1
		

	

	def fillListBox(self):
		"""Reads acquisition list from acqinfo.txt, clears old contents of acquisition
		list and re-adds them."""
		
		# Re-open acqinfo, read first line
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

			if self.slbl == '' or rlnsplit[1].find(self.slbl) != -1:
				if i >= self.acqlpg*acqpgsize and i < (self.acqlpg+1)*acqpgsize:
					# Prettify the acqlist entry
					acqlistline = rln[2:5]+' '+rln[0:2]+', '+rln[5:9]+': '+rln[10:len(rlnsplit[0])-1]

					# Add label if it exists
					if rlnsplit[1] != '':
						acqlistline += '  -  '+rlnsplit[1].replace('(>$%pipe%$<)', '|')

					# Add entry to acqlist, increment lcount
					self.acqlist.insert(END, acqlistline)
					lcount = lcount+1

				i = i+1

			# Read next line
			rln = infofile.readline()

		# Close acqinfo, update arrows
		infofile.close()
		self.updateArrows()




	def refreshListBox(self, event=None):
		"""Refresh acqisition list"""

		self.updatePageParams()
		self.fillListBox()




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
		self.acqtotalnum = 0
		self.acqsrchnum = 0
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
		self.updatePageParams()
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
			if nextLine.split(":")[0] == self.getAcqFromSel(int(sel[0])):
				toWrite = nextLine
				break

			# Read next line
			nextLine = infofile.readline()


		# Close acqinfo, write to acqdisp
		infofile.close()
		dispfile = open("acqdisp.txt", "w")
		dispfile.write(toWrite)
		dispfile.close()


		# if Octave was previously launched, kill it
		if self.octaveOpened == True:
			self.dispproc.terminate()
			self.dispproc.wait()
			self.octaveOpened == False

		# Launch octave to display data
		self.dispproc = subprocess.Popen(['octave', '--persist', '--silent', 'dispd.m'], shell=True)
		self.octaveOpened = True

		


		

	def performAcq(self):
		"""Perform data acquisition"""

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
			self.proc = subprocess.Popen(['python', 'acqdata.py'],shell=True)
			self.conn, self.addr = self.sckt.accept()

			data = self.conn.recv(1024)

			if data == "init":
				termtrig = ""
				for i in range(0, 8):
					termtrig += str(self.t[i].get())

				self.conn.send('begin:'+termtrig)

				# If no old behavior, send a terminate message, wait for child and close socket
				if self.old == False:
					self.conn.sendto("end", self.addr)
					self.proc.wait()
					self.closeSocket()
				
		
		# Pause for half a second, give acquisition time to do its thang
		sleep(0.5)

		# Enable labelentry and beginAcq
		self.beginAcq.configure(state=NORMAL)
		self.labelentry.configure(state=NORMAL)

		# Update acqtotalnum, update page params
		self.acqtotalnum = self.acqtotalnum + 1
		self.updatePageParams()
	
		# If viewnewacq is true and page isn't last, change to last
		if viewnewacq == True and self.acqlpg != self.lastpg:
			self.acqlpg = self.lastpg

		self.fillListBox()

		# Set display to end of page if past visible threshhold
		if self.acqlpg == self.lastpg:
			pglen = (self.acqlnum - 1) % acqpgsize
			if pglen >= 10:
				self.acqlist.yview(pglen - 10 + 1)


			

	def getAcqFromSel(self, sel):
		""" Given the selection number, return the acquisition name as
		used in the file name (i.e. DDMonYYYY_N)"""

		acqval = self.acqlist.get(sel)
		acqvalsplit = acqval.split('  -  ')

		if len(acqvalsplit) == 1:
			return acqval[4:6]+acqval[0:3]+acqval[8:12]+'_'+acqval[14:len(acqval)+1]
		else:
			return acqval[4:6]+acqval[0:3]+acqval[8:12]+'_'+acqval[14:len(acqvalsplit[0])]




	def backPage(self):
		"""Sends acqlist back one page"""
		
		# Decrement acqlpg, re-fill listbox & update arrows
		self.acqlpg = self.acqlpg - 1
		self.fillListBox()




	def firstPage(self):
		"""Sends acqlist to last page"""
		
		# Set acqlpg to 0, re-fill listbox & update arrows
		self.acqlpg = 0
		self.fillListBox()


		

	def forwardPage(self):
		"""Sends acqlist forward one page"""

		# Increment acqlpg, re-fill listbox & update arrows
		self.acqlpg = self.acqlpg + 1
		self.fillListBox()
			



	
	def lastPage(self):
		"""Sends acqlist to last page"""

		# Set acqlpg to last. re-fill listbox and update arrows
		self.acqlpg = self.lastpg
		self.fillListBox()


	
	def updateArrows(self):
		"""Enable/disable arrows based on current page"""

		self.larr.configure(state=NORMAL)
		self.llarr.configure(state=NORMAL)
		self.rarr.configure(state=NORMAL)
		self.rrarr.configure(state=NORMAL)

		if self.acqlpg == 0:
			self.larr.configure(state=DISABLED)
			self.llarr.configure(state=DISABLED)
		
		if self.acqlpg == self.lastpg:
			self.rarr.configure(state=DISABLED)
			self.rrarr.configure(state=DISABLED)






# If command line arg present, invoke binary input file behavior
if len(sys.argv) == 2:
	acqfile = sys.argv[1]

# If command line arg is present, import acqdata for binary acquisition
if acqfile != '':
	import acqdata




# Create main window and hide
root = Tk()
root.withdraw()

# Create a top level, add a title
app = App()
app.title("PCDiag Control/Display Interface")
root.mainloop() 

