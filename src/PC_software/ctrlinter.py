from Tkinter import *


class App(Frame):
	def __init__(self, master = None):
		frm = Frame(master, padx=3, pady=3)
		frm.grid(row=0, column=0)
		

		# Make OptionMenu label
		self.typesLabel = Label(frm, text="Data: ")
		self.typesLabel.grid(row=0, column=0, sticky = W)


		# Make OptionMenu
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

		self.typesMenu = OptionMenu(frm, var, *typeOpts)
		self.typesMenu.grid(row=0, column=1, sticky = E + W)

		
		# Make Begin/End Acquisition buttons
		self.beginAcq = Button(frm, text="Begin Acquisition", width=20, command=self.beginAcqClick)
		self.endAcq = Button(frm, text="End Acquisition", width=20, command=self.endAcqClick)
		self.beginAcq.grid(row=2, column=0, columnspan=2, sticky=S)


		# Do some resizing
		frm.columnconfigure(0, minsize=40)
		frm.columnconfigure(1, minsize=160)
		frm.rowconfigure(1, minsize=10)


	def beginAcqClick(self):
			 self.beginAcq.grid_remove();
			 self.endAcq.grid(row=2, column=0, columnspan=2, sticky=S)


	def endAcqClick(self):
			 self.endAcq.grid_remove();
			 self.beginAcq.grid(row=2, column=0, columnspan=2, sticky=S)
		



root = Tk()
app = App(root)
root.mainloop() 
