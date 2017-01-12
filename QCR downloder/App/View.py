from tkinter import *
from App.Module import ModulePART
import  os

class Application(Frame):

    def __init__(self,csvPath, master=None):
        Frame.__init__(self,master)
        self.grid()
        self.Module = ModulePART(csvPath)

        self.createWidgets()
        print(self.Module)

    def createWidgets(self):
        self.label = Label(self, text='CSV Path:', width=10)
        self.label.grid(row=0)
        self.csvPath = Entry(self, width=30)
        self.csvPath.grid(row=0,column=1, sticky=W)
        #add buttons
        self.alertButton = Button(self, text="Download Only", command=self.DownloadOnly)
        self.alertButton.grid(row=1, column=0, sticky=E)
        self.alertButton1 = Button(self, text="Analysis", command=self.DownloadOnly)
        self.alertButton1.grid(row=1, column=1, sticky=W)
        self.alertButton2 = Button(self, text="Clear", command=self.ClearText)
        self.alertButton2.grid(row=1, column=1, sticky=E)
        #add SN choose Button
        self.ChooseSNButton = Menubutton(self, text='Choose SN to check fail info', relief=RAISED)
        self.ChooseSNButton.menu = Menu(self.ChooseSNButton, tearoff=0)
        self.ChooseSNButton['menu'] = self.ChooseSNButton.menu

        def add_ChooseButonLabel(*SNs):
            print(self.ChooseSNButton)
            for x in SNs:
                self.ChooseSNButton.menu.add_checkbutton(label=x,
                                                         command=self.ShowFailResult)
        self.Module.parseCsv()

        SNs = self.Module.SNs
        print(SNs)
        if len(SNs) > 0:
            add_ChooseButonLabel(*SNs)

        self.ChooseSNButton.grid(row=2, column=1, sticky=E)

        # add text to show result

        self.textFiled = Text(self, bg='black',fg='white', width=55)
        self.textFiled.insert('0.0', 'this is the analysis result\n-------------------------\n')
        self.textFiled.grid(row=3, columnspan=2, sticky=W)
        self.sb= Scrollbar(self)
        self.sb.grid(row=3,column=2, sticky='ns')
        self.textFiled.configure(yscrollcommand=self.sb.set)
        self.sb.configure(command=self.textFiled.yview)

    def DownloadOnly(self):
        pass

    def ClearText(self):
        self.textFiled.delete('3.0', END)

    def ShowFailResult(self):
        pass


if __name__ == '__main__':
    csv_Path = os.path.abspath(os.path.join(os.getcwd(), 'example.csv'))
    app = Application(csv_Path)
    app.master.title('QCR Downloader')

    app.mainloop()


