# inter.py - graphical front-end

from Tkinter import *
from socket import *
import os, sys, glob 


class App(Frame):
	def __init__(self, master = None):
		self.makeAcqWidgets(master)
		self.makeDispWidgets(master)
		self.makeCtrlWidgets(master)
		self.pathto = "data\\"
		self.fsuff = ".dat"
		self.initSocket()


	def initSocket(self):
		# Socket params
		host = "localhost"
		port = 19368
		self.addr = (host,port)

		# Create socket
		self.sock = socket(AF_INET, SOCK_DGRAM)


	def makeAcqWidgets(self, master):
		# Data Acquisition LabelFrame
		acqfrm = LabelFrame(master, text="Data Acquisition", padx=5, pady=5)
		acqfrm.grid(row=0, column=0, sticky=N+E+S+W)

		# OptionMenu label
		self.typesLabel = Label(acqfrm, text="Data: ")
		self.typesLabel.grid(row=0, column=0, sticky = W)


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

		self.typesMenu = OptionMenu(acqfrm, var, *typeOpts)
		self.typesMenu.grid(row=0, column=1, sticky = E + W)

		# Begin/End Acquisition buttons
		self.beginAcq = Button(acqfrm, text="Begin Acquisition", width=20, command=self.beginAcqClick)
		self.endAcq = Button(acqfrm, text="End Acquisition", width=20, command=self.endAcqClick)
		self.beginAcq.grid(row=2, column=0, columnspan=2, sticky=S)

		# Do some resizing
		acqfrm.columnconfigure(0, minsize=40)
		acqfrm.columnconfigure(1, minsize=160)
		acqfrm.rowconfigure(1, minsize=10)


	def makeDispWidgets(self, master):
		# Data Display LabelFrame
		dispfrm = LabelFrame(master, text="Data Display", padx=5, pady=5)
		dispfrm.grid(row=0, column=4)

		self.acqlist = Listbox(dispfrm)
		self.acqlist.grid(row=0, column=0, columnspan=4, rowspan=3, sticky=E+W)
		self.refreshListBox()

		# Refresh/Clear/Delete/Display buttons
		self.refreshList = Button(dispfrm, text="Rfrsh", width=5, command=self.refreshListBox)
		self.clearList = Button(dispfrm, text="Clr", width=5, command=self.clearAcqs)
		self.deleteItem = Button(dispfrm, text="Del", width=5, command=self.deleteAcq)
		self.displayData = Button(dispfrm, text="Disp", width=5, command=self.displayAcq)

		self.refreshList.grid(row=4, column=0, columnspan=1, sticky=W)
		self.clearList.grid(row=4, column=1, columnspan=1)
		self.deleteItem.grid(row=4, column=2, columnspan=1)
		self.displayData.grid(row=4, column=3, columnspan=1)



	def makeCtrlWidgets(self, master):
		# Control Interface LabelFrame
		ctrlfrm = LabelFrame(master, text="Control Interface", padx=5, pady=5)
		ctrlfrm.grid(row=5, column=0, sticky=W)

		# Checkboxes
		c = [0, 0, 0, 0, 0, 0, 0]
		self.chck1 = Checkbutton(ctrlfrm, text="", variable=c[0])
		self.chck2 = Checkbutton(ctrlfrm, text="", variable=c[1])
		self.chck3 = Checkbutton(ctrlfrm, text="", variable=c[2])
		self.chck4 = Checkbutton(ctrlfrm, text="", variable=c[3])
		self.chck5 = Checkbutton(ctrlfrm, text="", variable=c[4])
		self.chck6 = Checkbutton(ctrlfrm, text="", variable=c[5])
		self.chck7 = Checkbutton(ctrlfrm, text="Check7", variable=c[6])

		self.chck1.grid(row=1, column=1)
		self.chck2.grid(row=1, column=2)
		self.chck3.grid(row=1, column=3)
		self.chck4.grid(row=1, column=4)
		self.chck5.grid(row=1, column=5)
		self.chck6.grid(row=1, column=6)
		self.chck7.grid(row=1, column=7)
	

		# Radio buttons
		r = IntVar()
		self.rad1 = Radiobutton(ctrlfrm, text="One", variable=r, value=1)
		self.rad2 = Radiobutton(ctrlfrm, text="Two", variable=r, value=2)

		self.rad1.grid(row=11, column=1, columnspan=1)
		self.rad2.grid(row=11, column=2, columnspan=1)

			


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
		self.endAcq.grid(row=2, column=0, columnspan=2, sticky=S)
		self.sock.sendto("begin", self.addr)


	def endAcqClick(self):
		self.sock.sendto("end", self.addr)
		self.endAcq.grid_remove()
		self.beginAcq.grid(row=2, column=0, columnspan=2, sticky=S)
		self.refreshListBox()
		

# Launch acqdata
import subprocess
proc = subprocess.Popen('acqdata.py',shell=True)


# Run interface
root = Tk()
app = App(root)
root.title("PCDiag Control/Display Interface")
root.mainloop() 
