from Tkinter import *
import os, sys, acqdata

def getAcqFile(argv):
	global acqfile
	if(len(argv) == 2):
		acqfile = argv[1]
	else:
		if(len(argv) > 2):
			prompt = "Too many arguments. Please enter file to acquire data from: "
		else:
			prompt = "No acq file supplied. Please enter file to acquire data from: "

		acqfile = raw_input(prompt)


class App(Frame):
	def __init__(self, master = None):
		self.makeAcqWidgets(master)
		self.makeDispWidgets(master)
		self.pathto = "data\\"
		self.fsuff = ".dat"


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
		# Acquisition Display LabelFrame
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
			


	def refreshListBox(self):
		self.infofile = open("acqinfo.txt", "r")
		self.nextLine = self.infofile.readline()

		self.acqlist.delete(0, END)

		while self.nextLine != "":
			self.acqlist.insert(END, self.nextLine.rstrip(":\r\n"))
			self.nextLine = self.infofile.readline()

		self.infofile.close()


	def clearAcqs(self):
		acqs = []
		thisacq = []

		self.infofile = open("acqinfo.txt", "r")
		self.nextLine = self.infofile.readline()

		while self.nextLine != "":
			acqs.append(self.nextLine.rstrip("\r\n"))
			self.nextLine = self.infofile.readline()

		self.infofile.close()
		self.acqlist.delete(0, END)

		for i in range(len(acqs)):
			thisacq = acqs[i].split(":")
			self.delAcqFiles(thisacq[0], thisacq[1])

			self.infofile = open("acqinfo.txt", "w")
			self.infofile.write("")
			self.infofile.close()

			self.cfgfile = open("acqconfig.txt", "w")
			self.cfgfile.write("")
			self.cfgfile.close()


	
	def delAcqFiles(self, acqpref, acqend):
		if acqend == '':
			os.remove(self.pathto+acqpref+'a'+self.fsuff)
		else:
			for i in range(ord('a'), ord(acqend)):
				os.remove(self.pathto+acqpref+chr(i)+self.fsuff)
		



	def deleteAcq(self):
		sel = self.acqlist.curselection()
		self.acqsToDel = []
		self.infoLines = []
		self.delLines = []

		for i in range(len(sel)):
			self.acqsToDel.append(int(sel[i]))

		self.acqsToDel = sorted(self.acqsToDel)

		self.infofile = open("acqinfo.txt", "r")
		self.nextLine = self.infofile.readline()

		i = 0;
		delInd = 0;
		while self.nextLine != "":
			self.nextLine = self.nextLine.rstrip("\r\n")

			if delInd < len(self.acqsToDel):
				if i != self.acqsToDel[delInd]:
					self.infoLines.append(self.nextLine);
				else:
					self.delLines.append(self.nextLine);
					delInd += 1
			else:
				self.infoLines.append(self.nextLine);

			self.nextLine = self.infofile.readline()
			i = i + 1


		# Delete the files in pathto
		for i in range(len(self.delLines)):
			delSplit = self.delLines[i].split(":")
			self.delAcqFiles(delSplit[0], delSplit[1]);

		self.infofile.close()


		self.infofile = open("acqinfo.txt", "w")

		for i in range(len(self.infoLines)):
			self.infofile.write(self.infoLines[i]+"\n")
		self.infofile.close()


		self.refreshListBox()


	def displayAcq(self):
		pass


	def beginAcqClick(self):
		self.beginAcq.grid_remove();
		self.endAcq.grid(row=2, column=0, columnspan=2, sticky=S)
		acqdata.acq(acqfile)


	def endAcqClick(self):
		self.endAcq.grid_remove();
		self.beginAcq.grid(row=2, column=0, columnspan=2, sticky=S)
		self.refreshListBox()
		



getAcqFile(sys.argv)
root = Tk()
app = App(root)
root.title("PCDiag Control/Display Interface")
root.mainloop() 
