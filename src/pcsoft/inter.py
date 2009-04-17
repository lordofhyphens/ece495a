# inter.py - graphical front-end

from Tkinter import *
from socket import *
import os, sys, glob 


class App(Toplevel):
	def __init__(self):
		Toplevel.__init__(self)
		self.protocol("WM_DELETE_WINDOW", self.newClose)
		self.makeAcqWidgets()
		self.makeDispWidgets()
		self.makeCtrlWidgets()
		self.pathto = "data\\"
		self.fsuff = ".dat"
		self.initSocket()


	def newClose(self):
		self.sock.close()
		root.destroy()


	def initSocket(self):
		# Socket params
		host = "localhost"
		port = 19367
		self.addr = (host,port)

		# Create socket
		self.sock = socket(AF_INET, SOCK_DGRAM)


	def makeAcqWidgets(self):
		# Data Acquisition LabelFrame
		self.acqfrm = LabelFrame(self, text="Data Acquisition", padx=5, pady=5)
		self.acqfrm.grid(row=0, column=0, in_=self, sticky=N+E+S+W)

		# OptionMenu label
		typeLabel = Label(self.acqfrm, text="Type: ")
		typeLabel.grid(row=0, column=0, sticky = W)

		# Data type drop-down menu
		typeOpts = [
			" ",
			"Oscilloscope Waveform",
			"DC Voltage",
			"DC Current",
			"AC Voltage",
			"AC Current"
			]

		var = StringVar()
		var.set(typeOpts[0])

		typeMenu = OptionMenu(self.acqfrm, var, *typeOpts)
		typeMenu.grid(row=0, column=1, in_=self.acqfrm, sticky = E + W)

		# Begin/End Acquisition buttons
		self.beginAcq = Button(self.acqfrm, text="Begin Acquisition", width=15, command=self.beginAcqClick)
		self.endAcq = Button(self.acqfrm, text="End Acquisition", width=15, command=self.endAcqClick)
		self.beginAcq.grid(row=2, column=0, columnspan=2, in_=self.acqfrm, sticky=S)

		# Do some resizing
		self.acqfrm.columnconfigure(0, minsize=40)
		self.acqfrm.columnconfigure(1, minsize=160)
		self.acqfrm.rowconfigure(1, minsize=15)


	def makeDispWidgets(self):
		# Data Display LabelFrame
		self.dispfrm = LabelFrame(self, text="Data Display", padx=5, pady=5)
		self.dispfrm.grid(row=0, column=1, in_=self)

		self.acqlist = Listbox(self.dispfrm)
		self.acqlist.grid(row=0, column=0, in_=self.dispfrm, columnspan=4, rowspan=3, sticky=E+W)
		self.refreshListBox()

		# Refresh/Clear/Delete/Display buttons
		refreshList = Button(self.dispfrm, text="Rfrsh", width=5, command=self.refreshListBox)
		clearList = Button(self.dispfrm, text="Clr", width=5, command=self.clearAcqs)
		deleteItem = Button(self.dispfrm, text="Del", width=5, command=self.deleteAcq)
		displayData = Button(self.dispfrm, text="Disp", width=5, command=self.displayAcq)

		refreshList.grid(row=4, column=0, in_=self.dispfrm, sticky=W)
		clearList.grid(row=4, column=1, in_=self.dispfrm)
		deleteItem.grid(row=4, column=2, in_=self.dispfrm)
		displayData.grid(row=4, column=3, in_=self.dispfrm)



	def makeCtrlWidgets(self):
		# Control Interface LabelFrame
		self.ctrlfrm = LabelFrame(self, text="Control Interface")
		self.ctrlfrm.grid(row=1, column=0, in_=self, columnspan=2, sticky=E+W)


		# Generate and draw checkboxes, do some column resizing while we're at it
		c = [0, 0, 0, 0, 0, 0]
		chcks = []

		for i in range(0, 6):
			chcks.append(Checkbutton(self.ctrlfrm, text="", variable=c[i]))
			chcks[i].grid(row=0, column=i, in_=self.ctrlfrm)
			self.ctrlfrm.columnconfigure(0, weight=0, minsize=20)
	
	

		# Radio buttons
		r = IntVar()
		self.rad1 = Radiobutton(self.ctrlfrm, text="One", variable=r, value=1)
		self.rad2 = Radiobutton(self.ctrlfrm, text="Two", variable=r, value=2)

		self.rad1.grid(row=1, column=0, columnspan=6)
		self.rad2.grid(row=2, column=0, columnspan=6)


		# Resize that mug


			


	def refreshListBox(self):
		infofile = open("acqinfo.txt", "r")
		nextLine = infofile.readline()

		self.acqlist.delete(0, END)

		while nextLine != "":
			self.acqlist.insert(END, nextLine.rstrip(":\r\n"))
			nextLine = infofile.readline()

		infofile.close()


	def clearAcqs(self):
		acqnames = self.acqlist.get(0, END)
		
		# Delete acq files
		for i in range(len(acqnames)):
			for acqfile in glob.glob(self.pathto+acqnames[i]+'*.dat'):
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
			for acqfile in glob.glob(self.pathto+self.acqlist.get(acqsToDel[i])+'*.dat'):
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
		self.refreshListBox()



	def displayAcq(self):
		sel = self.acqlist.curselection()

		if len(sel) == 1:
			infofile = open("acqinfo.txt", "r")

			nextLine = infofile.readline()

			# Get acqdisp contents
			while nextLine != "":
				nextLine = nextLine.rstrip("\r\n")

				if nextLine.split(":")[0] == self.acqlist.get(int(sel[0])):
					toWrite = nextLine

				nextLine = infofile.readline()

			infofile.close()

			# Write 'em.
			dispfile = open("acqdisp.txt", "w")
			dispfile.write(toWrite)
			dispfile.close()


		
	def beginAcqClick(self):
		self.beginAcq.grid_remove()
		self.endAcq.grid(row=2, column=0, columnspan=2, in_=self.acqfrm, sticky=S)
		self.sock.sendto("begin", self.addr)


	def endAcqClick(self):
		self.sock.sendto("end", self.addr)
		self.endAcq.grid_remove()
		self.beginAcq.grid(row=2, column=0, columnspan=2, in_=self.acqfrm, sticky=S)
		self.refreshListBox()
		

# Launch acqdata
# import subprocess
# proc = subprocess.Popen('acqdata.py',shell=True)


# Create main window and hide
root = Tk()
root.withdraw()

# Create a top level, add a title
app = App()
app.title("PCDiag Control/Display Interface")
root.mainloop() 

