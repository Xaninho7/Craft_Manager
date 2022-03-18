from tkinter import *
from tkinter import ttk
import tkinter


class EditeBP:
    def __init__(self, conn, listBPs, listMats):
        self.bVar = None
        self.mVar = None
        self.addMatButton = None
        self.addMat = None
        self.style = None
        self.table = None
        self.tableFrame = None
        self.choseMat = None
        self.amountEntry = None
        self.amountLabel = None
        self.choseBP = None
        self.conn = conn
        self.listBPs = listBPs
        self.listMats = listMats
        self.editeBpWindow = Toplevel()

    def addMattoBP(self,):
        sql = f'INSERT INTO  BlueprintMaterials(idBlueprint, idMaterial, Qtd) VALUES(' \
              f'{self.listBPs.bplist[self.choseBP.current()].id},' \
              f'{self.listMats.itemsList[self.choseMat.current()].id},{self.amountEntry.get()});'
        cur = self.conn.cursor()
        cur.execute(sql)
        self.conn.commit()
        self.refreshDBdata()

    def refreshDBdata(self, event=None):
        sql = f'SELECT Material.Name, Qtd FROM BlueprintMaterials INNER JOIN Material ON idMaterial = Material.id ' \
              f'WHERE idBlueprint = {self.listBPs.bplist[self.choseBP.current()].id};'
        cur = self.conn.cursor()
        cur.execute(sql)
        results = cur.fetchall()
        self.table.delete(*self.table.get_children())
        for x, y in enumerate(results):
            self.table.insert("", 'end', iid=x, values=(y[0], y[1]))

    def openWindow(self):
        self.editeBpWindow.title('Edit Blueprint')
        self.editeBpWindow.geometry('410x400')
        self.editeBpWindow.config(bg='#222629')
        self.editeBpWindow.resizable(False, False)
        icon = PhotoImage(file='icon.png')
        self.editeBpWindow.iconphoto(True, icon)
        self.listBPs.refresh()
        self.listMats.refresh()

        # ComboBox Blueprints
        self.bVar = tkinter.StringVar()
        self.choseBP = ttk.Combobox(self.editeBpWindow, width=35, textvariable=self.bVar, state='readonly')
        self.choseBP['values'] = [x.name for x in self.listBPs.bplist]
        self.choseBP.place(x=205, y=27, anchor=CENTER)
        self.choseBP.current()
        self.choseBP.bind('<<ComboboxSelected>>', self.refreshDBdata)

        # Amount of items
        self.amountLabel = Label(self.editeBpWindow, text='Amount:', font=('Montserrat', 9), bg='#222629',
                                 fg='#86c232', pady=5, width=35, anchor='w')
        self.amountLabel.place(x=250, y=54)
        self.amountEntry = Entry(self.editeBpWindow, font=('Arial', 11), width=10)
        self.amountEntry.place(x=250, y=77)
        self.amountEntry.insert(END, '1')

        # Combobox materiais
        self.mVar = tkinter.StringVar()
        self.choseMat = ttk.Combobox(self.editeBpWindow, width=27, textvariable=self.mVar, state='readonly')
        self.choseMat['values'] = [x.name for x in self.listMats.itemsList]
        self.choseMat.place(x=15, y=77)
        self.choseMat.current(0)

        # add material to the bp button
        self.addMatButton = Button(self.editeBpWindow, text='Add Material', font=('Montserrat', 10),
                                   command=self.addMattoBP, bg='#86c232', fg='White', activebackground='#86c232',
                                   activeforeground='white', padx=3, pady=2, width=15)
        self.addMatButton.place(x=205, y=150, anchor=CENTER)

        # Table of material
        self.tableFrame = Frame(self.editeBpWindow, width=350)
        self.tableFrame.place(x=205, y=270, anchor=CENTER)
        self.style = ttk.Style()
        self.style.theme_use('clam')
        self.style.configure('Treeview', background='silver', foreground='black', fieldbackground='silver')

        self.table = ttk.Treeview(self.tableFrame, columns=('1', '2'), show='headings', height=8)
        self.table.pack()
        self.table.heading('1', text='Material Name')
        self.table.heading('2', text='Amount')
        self.table.column('1', anchor='w', width=250, stretch=NO)
        self.table.column('2', anchor='center', width=60, stretch=NO)

        self.refreshDBdata()
