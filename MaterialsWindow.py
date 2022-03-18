from tkinter import *
from labeled_Entry import Labeled_Entry
from tkinter import messagebox


class Material_window:

    def __init__(self, conn):
        self.markup_label = None
        self.material_markup = None
        self.value_label = None
        self.material_value = None
        self.conn = conn
        self.new_material = Toplevel()
        self.material_name = None
        self.frame = Frame(self.new_material, width=40, bg='#222629')
        self.name_label = Label(self.material_name)

    def openWindow(self):
        self.new_material.title('Add a New Material')
        self.new_material.geometry('460x180')
        self.new_material.config(bg='#222629')
        self.new_material.resizable(False, False)
        icon = PhotoImage(file='icon.png')
        self.new_material.iconphoto(True, icon)

        # material name
        self.name_label = Label(self.new_material, text='Name of the material:', font=('Montserrat', 9), bg='#222629',
                                fg='#86c232', width=35, anchor='w')
        self.name_label.place(x=13, y=4)
        self.material_name = Labeled_Entry(self.new_material, font=('Arial', 11), width=50, label='Ex: Basic Screws')
        self.material_name.place(x=15, y=27)

        #  frame MU + value
        self.frame.place(x=15, y=55)

        # material value
        self.value_label = Label(self.frame, text='Value [un]:', font=('Montserrat', 9), bg='#222629', fg='#86c232',
                                 padx=5, width=10, anchor='center')
        self.value_label.pack()
        self.material_value = Labeled_Entry(self.frame, font=('Montserrat', 10), label='Ex: 0.35', width=10,
                                            textg='black')
        self.material_value.pack()

        # material MU
        self.markup_label = Label(self.frame, text='Markup [%]:', font=('Montserrat', 9), bg='#222629', fg='#86c232',
                                  padx=5, width=10, anchor='center')
        self.markup_label.pack()
        self.material_markup = Labeled_Entry(self.frame, font=('Montserrat', 10), label='Ex: 103.5', width=10)
        self.material_markup.pack()

        # save button
        save_mat = Button(self.new_material, text='Save Material', font=('Montserrat', 10, 'bold'),
                          command=self.save_material,
                          bg='#6f2232', fg='White', activebackground='#6f2232',
                          activeforeground='white', padx=3, pady=3)
        save_mat.place(x=250, y=110, anchor='w')

    def window_lift(self):
        self.new_material.lift()
        self.new_material.attributes('-topmost', True)
        self.new_material.attributes('-topmost', False)

    def save_material(self):
        name = self.material_name.get()
        value = self.material_value.get()
        mu = self.material_markup.get()
        try:
            value = float(value)
            mu = float(mu)
        except ValueError:
            messagebox.showerror(title='Invalid Value', message='Item value or markup must be a number!')
            return self.window_lift()
        if name == '' or name == self.material_name.label:
            messagebox.showerror(title='Empty Name', message='The name of an item can not be empty!\n'
                                                             'It is recommended to copy/paste from the original.')
            return self.window_lift()

        sql = f'INSERT INTO Material (Name, Value, MU) VALUES (\'{name}\', {value}, {mu});'
        cur = self.conn.cursor()
        self.window_lift()
        cur.execute(sql)
        self.conn.commit()

        messagebox.showinfo(title='Material Saved!', message='The material was successfully added to the DataBase!')
        self.window_lift()
