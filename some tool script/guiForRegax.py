from tkinter import *
import os
import re


class Application(Frame):
	def __init__(self, master=None):
		Frame.__init__(self, master=master)

		self.displayresult = Label(self)
		self.outputFiled = Entry(self)
		self.outputText = Label(self)
		self.inputField = Entry(self)
		self.inputText = Label(self)
		self.search = Button(self)
		self.match = Button(self)
		self.findall = Button(self)
		self.regax = Label(self)
		self.regaxInput =Entry(self)

		self.grid()
		self.createWidget()

	def createWidget(self):
		self.inputText['text'] = "input:"
		self.inputText.grid(row=0, column=0)
		self.inputField["width"] = 50
		self.inputField.grid(row=0, column=1, columnspan=6)

		self.regax["text"] = "Regax input"
		self.regaxInput["width"] = 50
		self.regax.grid(row= 1, column=0)
		self.regaxInput.grid(row=1, column=1, columnspan=6)
		self.outputText['text'] = "output:"
		self.outputText.grid(row=2, column=0)
		self.outputFiled["width"] = 50
		self.outputFiled.grid(row=2, column=1, columnspan=6)
		self.search['text'] = 'search'
		self.search['command'] = self.searching
		self.search.grid(row=3, column=0)

		self.match['text'] = 'match'
		self.match.grid(row=3, column=1)
		self.findall["text"] = "findall"
		self.findall.grid(row=3, column=2)

		self.displayresult["text"] = "the regax result"
		self.displayresult.grid(row=4, column=0, columnspan=7)

	def searching(self):
		theContent= self.inputField.get()
		theregax = self.regaxInput.get()
		regax= re.compile(theregax)
		theSearchingresult = regax.search(theContent)
		if theSearchingresult is None:
			self.outputFiled.delete(0, END)
			self.outputFiled.insert(0, 'No matching')
		else:
			print(theSearchingresult.groups())
			self.outputFiled.delete(0, END)
			results = theSearchingresult.group(1)
			self.outputFiled.insert(0, results)
	def match(self):
		theContent= self.inputField.get()
		theregax = self.regaxInput.get()
		regax= re.compile(theregax)
		theSearchingresult = regax.search(theContent)
		if theSearchingresult is None:
			self.outputFiled.delete(0, END)
			self.outputFiled.insert(0, 'No matching')
		else:
			print(theSearchingresult.groups())
			self.outputFiled.delete(0, END)
			results = theSearchingresult.group(1)
			self.outputFiled.insert(0, results)


if __name__ == '__main__':
	app = Application()
	app.master.title = 'Regax'
	app.mainloop()
