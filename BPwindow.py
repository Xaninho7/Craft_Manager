from tkinter import *
from tkinter import ttk
import tkinter
import threading
import time


class New_Blueprint:
    def __init__(self, conn, listMaterials):
        self.statusLabel = None
        self.var = None
        self.matItemCombo = None
        self.muEntry = None
        self.muLabel = None
        self.succItemLabel = None
        self.save_bpn = None
        self.costEntry = None
        self.costLabel = None
        self.bpNameEntry = None
        self.bpNameLabel = None
        self.succItemCombo = None
        self.bp_window = Toplevel()
        self.conn = conn
        self.listMaterials = listMaterials
        self.idBlueprint = 0
        self.succ = threading.Thread(target=self.succSave, args=(), daemon=True)

    def save_BP(self):
        sql = f'INSERT INTO Blueprint (Name, CostClick, MU, idMaterialSuccess) VALUES ' \
              f'(\'{self.bpNameEntry.get()}\', {self.costEntry.get()}, {self.muEntry.get()},' \
              f'{self.listMaterials.itemsList[self.succItemCombo.current()].id}); '
        cur = self.conn.cursor()
        cur.execute(sql)
        self.conn.commit()
        sql = f'SELECT id FROM Blueprint WHERE Name = \'{self.bpNameEntry.get()}\';'
        cur.execute(sql)
        results = cur.fetchone()
        self.idBlueprint = results[0]
        self.succ.start()

    def succSave(self):
        self.statusLabel.configure(text='Blueprint Saved!')
        time.sleep(3)
        self.statusLabel.configure(text='')

    def openWindow(self):
        self.bp_window.title('Add a new Blueprint')
        self.bp_window.geometry('410x200')
        self.bp_window.config(bg='#222629')
        self.bp_window.resizable(False, False)
        icon = PhotoImage(file='icon.png')
        self.bp_window.iconphoto(True, icon)
        self.listMaterials.refresh()

        # BP name
        self.bpNameLabel = Label(self.bp_window, text='Name of the blueprint:', font=('Montserrat', 9), bg='#222629',
                                 fg='#86c232',
                                 padx=5, pady=5, width=35, anchor='w')
        self.bpNameLabel.place(x=10, y=4)
        self.bpNameEntry = Entry(self.bp_window, font=('Arial', 11), width=40)
        self.bpNameEntry.place(x=15, y=27)

        self.succItemLabel = Label(self.bp_window, text='Name of the item:', font=('Montserrat', 9), bg='#222629',
                                   fg='#86c232',
                                   padx=5, pady=5, width=35, anchor='w')
        self.succItemLabel.place(x=10, y=54)

        # combobox item
        self.var = tkinter.StringVar()
        self.succItemCombo = ttk.Combobox(self.bp_window, width=27, textvariable=self.var, state='readonly')
        self.succItemCombo['values'] = [x.name for x in self.listMaterials.itemsList]
        self.succItemCombo.current(0)
        self.succItemCombo.place(x=15, y=77)

        # Cost per attempt
        self.costLabel = Label(self.bp_window, text='Attempt cost:', font=('Montserrat', 9), bg='#222629', fg='#86c232',
                               padx=5, pady=5, anchor='w')
        self.costLabel.place(x=10, y=124, anchor='w')
        self.costEntry = Entry(self.bp_window, font=('Arial', 11), width=10)
        self.costEntry.place(x=15, y=147, anchor='w')
        self.costEntry.insert(END, '1')

        # click cost
        self.muLabel = Label(self.bp_window, text='BP Markup[%]:', font=('Montserrat', 9), bg='#222629', fg='#86c232',
                             padx=5, pady=5)
        self.muLabel.place(x=125, y=124, anchor='w')
        self.muEntry = Entry(self.bp_window, font=('Arial', 11), width=10)
        self.muEntry.place(x=130, y=147, anchor='w')
        self.muEntry.insert(END, '100')

        # save button
        self.save_bpn = Button(self.bp_window, text='Add BP', width=10, font=('Montserrat', 10, 'bold'),
                               command=self.save_BP,
                               bg='#6f2232', fg='White', activebackground='#6f2232', activeforeground='white', padx=3,
                               pady=3)
        self.save_bpn.place(x=320, y=145, anchor=CENTER)

        # Status Label
        self.statusLabel = Label(self.bp_window, text='', font=('Montserrat', 11, 'bold'), bg='#222629', fg='#86c232',
                                 padx=5, pady=5, anchor='w')
        self.statusLabel.place(x=320, y=95, anchor=CENTER)
