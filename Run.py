import time
from datetime import datetime
import tkinter
from tkinter import *
from tkinter import ttk
from RTread import ReadLines
import threading
from ScreenRead import ScreenRead


class Run:
    def __init__(self, conn, listBPs, settings):
        self.total = None
        self.totalResd = 0.0
        self.clickUpdThr = None
        self.loadBut = None
        self.clicksWinBut = None
        self.bpWinBut = None
        self.resWinBut = None
        self.trackClick = None
        self.checkVar = None
        self.resValuesCheck = None
        self.clickCounting = True
        self.checkValues = ''
        self.settings = settings
        self.limitedItem = False
        self.statusLabel = None
        self.idRun = None
        self.runDate = None
        self.readChat = None
        self.saveButton = None
        self.total_clicks = None
        self.click_label = None
        self.frame3 = None
        self.startStopButton = None
        self.fin_metal = None
        self.fin_metal_label = None
        self.final_label = None
        self.frame2 = None
        self.ini_metal = None
        self.ini_metal_label = None
        self.initial_label = None
        self.frame1 = None
        self.choseBPs = None
        self.var = None
        self.options = None
        self.window = None
        self.conn = conn
        self.listBPs = listBPs
        self.readChat = ReadLines()
        self.getRes = ScreenRead(settings['residue'], False)
        self.getClicks = ScreenRead(settings['clicks'], True)
        self.getBP = ScreenRead(settings['blueprint'], False)
        self.reading = True
        self.read = None

    def clickUpdate(self):
        oldClick = 0
        while self.clickCounting:
            time.sleep(.5)
            strClick = self.getClicks.read().strip()
            if not strClick.isnumeric():
                continue
            intClick = int(strClick)
            if intClick > oldClick:
                self.total_clicks.delete(0, END)
                self.total_clicks.insert(END, strClick)
                oldClick = intClick
                self.readChat.runClicks = intClick

    def startStop(self):
        if self.reading:
            # creating the runs DB
            self.runDate = datetime.now()
            day = self.runDate.strftime("%d/%m/%Y")
            hour = self.runDate.strftime("%H:%M:%S")
            sql = f'INSERT INTO Runs (idBlueprint, Data, Hora) VALUES ' \
                  f'(\'{self.listBPs.bplist[self.choseBPs.current()].id}\',\'{day}\',\'{hour}\');'
            cur = self.conn.cursor()
            cur.execute(sql)
            self.conn.commit()

            # get run's ID
            sql = f'SELECT id FROM Runs WHERE idBlueprint={self.listBPs.bplist[self.choseBPs.current()].id}' \
                  f' AND Data=\'{day}\' AND Hora=\'{hour}\';'
            cur.execute(sql)
            results = cur.fetchone()
            self.idRun = results[0]
            # print('Run ID: ', self.idRun, 'Blueprint ID: ', self.listBPs.bplist[self.choseBPs.current()].name)

            # Start thread and change settings
            self.readChat.running = True
            self.read = threading.Thread(target=self.readChat.startRead,
                                         args=(self.idRun, self.limitedItem, self.getClicks,
                                               self.getRes,), daemon=True)
            
            self.read.start()

            # clickUpdate = threading.Thread(target=self.clickUpdate, args=())
            if '(L) Blueprint' in self.listBPs.bplist[self.choseBPs.current()].name:
                self.limitedItem = True
            else:
                self.trackClickRT()

            self.startStopButton.configure(text='Stop', bg='#E0A96D', fg='Black')
            self.reading = False
            self.statusLabel.configure(text='Reading the file...!')
            self.loadBut.configure(state='disabled')
            self.choseBPs.configure(state='disabled')
        else:
            self.readChat.running = False

            if self.clickCounting:
                self.clickCounting = False

            self.startStopButton.configure(state='disabled')
            self.total_clicks.delete(0, END)
            self.total_clicks.insert(END, self.getClicks.read().strip())
            self.startStopButton.configure(text='Start', bg='#86c232', fg='white')
            self.saveButton.configure(state='normal', bg='#6f2232')
            self.statusLabel.configure(text='Read has stopped')
            self.reading = True
            if self.limitedItem:
                residue = self.getRes.read()
                if residue.strip() != '':
                    self.resValuesCheck.configure(text=residue)
                    resValues = residue.split('\n')
                    totalResidue = 0
                    for value in resValues:
                        word = value.split(' ')
                        if len(word) > 0:
                            word[0] = word[0].strip()
                            if word[0].isnumeric():
                                totalResidue += int(word[0])
                    self.fin_metal.delete(0, END)
                    self.fin_metal.insert(END, totalResidue)
            else:
                self.fin_metal.delete(0, END)
                self.fin_metal.insert(END, '0')
            self.shallowSave()

    def shallowSave(self):
        metalIni = int(self.ini_metal.get())
        finMet = int(self.fin_metal.get())
        self.totalResd = (metalIni + self.readChat.gainedResidue - finMet) / 100
        if not self.limitedItem:
            self.total = 0
        clk = str(self.total_clicks.get())
        if not clk.isdigit():
            clk = 0
        else:
            clk = int(self.total_clicks.get())
        sql = f'UPDATE Runs SET Clicks = {clk}, ResidueSpent = {self.totalResd} WHERE id = {self.idRun};'
        cur = self.conn.cursor()
        cur.execute(sql)
        self.conn.commit()

    def save(self):
        self.shallowSave()
        self.saveButton.configure(state='disabled', bg='gray')
        self.statusLabel.configure(text='Successfully saved!!')
        self.loadBut.configure(state='normal')
        self.total_clicks.delete(0, END)
        self.total_clicks.insert(END, '0')
        self.readChat.gainedResidue = 0

    def updateSettings(self):
        text = f'residue {self.getRes.defaultWindow}\nclicks {self.getClicks.defaultWindow}\n' \
               f'blueprint {self.getBP.defaultWindow}\n \n{self.totalResd}'
        with open('windowSettings.txt', 'w') as file:
            file.write(text)

    def iniLoad(self):
        residue = self.getRes.read()
        self.updateSettings()
        if residue != '':
            self.resValuesCheck.configure(text=residue)
            resValues = residue.split('\n')
            totalResidue = 0
            for value in resValues:
                word = value.split(' ')
                if len(word) > 0:
                    if word[0].isnumeric():
                        totalResidue += int(word[0])
            self.ini_metal.delete(0, END)
            self.ini_metal.insert(END, totalResidue)
        else:
            self.ini_metal.delete(0, END)
            self.ini_metal.insert(END, '0')

        blueprint = self.getBP.read().strip()
        if blueprint != '':
            self.choseBPs.set('')
            for x in range(0, len(self.listBPs.bplist)):
                if blueprint == self.listBPs.bplist[x].name:
                    self.choseBPs.current(x)
                    break

        if self.var.get().strip() != '':
            self.startStopButton.configure(state='normal')

        self.choseBPs.config(state='readonly')

    def comboSelected(self, index, value, op):
        if self.var.get().strip() != '':
            self.startStopButton.configure(state='normal')
        else:
            self.startStopButton.configure(state='disabled')

    def trackClickRT(self):
        if self.readChat.running:
            if self.checkVar.get() == 1:
                self.clickCounting = True
                self.clickUpdThr = threading.Thread(target=self.clickUpdate, args=(), daemon=True)
                self.clickUpdThr.start()
            else:
                if self.clickCounting:
                    self.clickCounting = False

    def openWindow(self):
        self.window = Toplevel()
        self.window.title('Craft Run')
        self.window.geometry('390x400')
        self.window.config(bg='#222629')
        self.window.resizable(False, False)
        icon = PhotoImage(file='icon.png')
        self.window.iconphoto(True, icon)
        self.window.attributes('-topmost', True)

        # Combobox creation
        self.var = tkinter.StringVar()
        self.choseBPs = ttk.Combobox(self.window, width=40, textvariable=self.var)
        self.choseBPs['values'] = [x.name for x in self.listBPs.bplist]
        self.choseBPs.config(font=('Montserrat', 11), state='disabled')
        self.choseBPs.set('')
        self.var.trace('w', self.comboSelected)
        # self.choseBPs.bind('<<ComboboxSelected>>', self.comboSelected())
        self.choseBPs.place(x=195, y=75, anchor=CENTER)

        # checkbox to keep tracking clicks
        self.checkVar = IntVar()
        self.checkVar.set(1) # isto
        self.trackClick = Checkbutton(self.window, text='Track attempts in real time', variable=self.checkVar,
                                      onvalue=1, offvalue=0, activeforeground='#222629', activebackground='#86c232',
                                      command=self.trackClickRT, font=('Montserrat', 11), bg='#222629', fg='#86c232')
        self.trackClick.place(x=195, y=117, anchor=CENTER)

        # initial residue
        self.frame1 = Frame(self.window, width=50, bg='#222629')
        self.frame1.place(x=110, y=165, anchor='center')
        self.initial_label = Label(self.frame1, text=' Initial Value:', font=('Montserrat', 11), bg='#222629',
                                   fg='#86c232', width=10)
        self.initial_label.pack()
        self.ini_metal = Entry(self.frame1, font=('Arial', 11), width=10)
        self.ini_metal.insert(END, '0')
        self.ini_metal.pack()

        # final residue
        self.frame2 = Frame(self.window, width=50, bg='#222629')
        self.frame2.place(x=280, y=165, anchor='center')
        self.final_label = Label(self.frame2, text=' Final Value:', font=('Montserrat', 11), bg='#222629', fg='#86c232',
                                 width=10)
        self.final_label.pack()
        self.fin_metal = Entry(self.frame2, font=('Arial', 11), width=10)
        self.fin_metal.insert(END, '0')
        self.fin_metal.pack()

        # start/stop
        self.startStopButton = Button(self.window, text='Start', font=('Montserrat', 11, 'bold'),
                                      command=self.startStop,
                                      width=10, state='disabled',
                                      bg='#86c232', fg='White', activebackground='#86c232', activeforeground='white')
        self.startStopButton.place(x=110, y=230, anchor='center')

        # total clicks
        self.frame3 = Frame(self.window, width=50, bg='#222629')
        self.frame3.place(x=280, y=225, anchor='center')
        self.click_label = Label(self.frame3, text='Total clicks:', font=('Montserrat', 11), bg='#222629', fg='#86c232',
                                 width=10)
        self.click_label.pack()
        self.total_clicks = Entry(self.frame3, font=('Arial', 11), width=10)
        self.total_clicks.insert(END, '0')
        self.total_clicks.pack()
        # newBP_window.mainloop()

        # save
        self.saveButton = Button(self.window, text='Save', font=('Montserrat', 12, 'bold'), command=self.save, width=10,
                                 bg='gray', fg='White', activebackground='#6f2232', activeforeground='white', padx=3,
                                 pady=3, state='disabled')
        self.saveButton.place(x=100, y=310, anchor='center')

        # checking values from OCD
        self.resValuesCheck = Label(self.window, text='', justify='left',
                                    font=('Montserrat', 10), bg='#222629', fg='#F79862', width=25)
        self.resValuesCheck.place(x=210, y=290, anchor=NW)
        # status Label
        self.statusLabel = Label(self.window, text="Insert Parameters",
                                 font=('Montserrat', 12), bg='#222629', fg='#F79862', width=25)
        self.statusLabel.place(x=100, y=350, anchor='center')

        self.resWinBut = Button(self.window, text='Residue', command=self.getRes.readWindow, width=8, fg='white',
                                activebackground='#276880', bg='#276880', activeforeground='white',
                                font=('Montserrat', 10))
        self.resWinBut.place(x=60, y=30, anchor='center')

        self.bpWinBut = Button(self.window, text='BP', command=self.getBP.readWindow, width=8, fg='white',
                               activebackground='#276880', bg='#276880', activeforeground='white',
                               font=('Montserrat', 10))
        self.bpWinBut.place(x=140, y=30, anchor='center')

        self.clicksWinBut = Button(self.window, text='Attempts', command=self.getClicks.readWindow, width=8, fg='white',
                                   activebackground='#276880', bg='#276880', activeforeground='white',
                                   font=('Montserrat', 10))
        self.clicksWinBut.place(x=220, y=30, anchor='center')

        self.loadBut = Button(self.window, text='Load', command=self.iniLoad, width=8, fg='white',
                              activebackground='#572780', bg='#572780', activeforeground='white',
                              font=('Montserrat', 10))
        self.loadBut.place(x=320, y=30, anchor='center')
