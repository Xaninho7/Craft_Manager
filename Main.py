from tkinter import *
from MaterialsWindow import Material_window
from Run import Run
import sqlite3
from sqlite3 import Error
from BPwindow import New_Blueprint
from MaterialsList import *
from BlueprintList import *
from EditeBP import EditeBP
from PIL import Image, ImageTk


def create_connection():
    try:
        conn2 = sqlite3.connect(r"db_CM.db")
        print(sqlite3.version)
        return conn2
    except Error as e:
        print(e)


settings = {}
with open('windowSettings.txt', 'r') as file:
    for var in file:
        values = var.strip()
        values = values.split(' ')
        settings[values[0]] = values[1]


main_window = Tk()
main_window.geometry('500x300')
main_window.title('Craft Manager')
main_window.config(bg='#222629')
main_window.resizable(False, False)
icon = PhotoImage(file='icon.png')
main_window.iconphoto(True, icon)

conn = create_connection()

listMaterials = ListMaterial(conn)
listBPs = ListBP(conn)


def newMaterialFunction():
    newMaterial = Material_window(conn)
    newMaterial.openWindow()


def new_bp():
    newBP = New_Blueprint(conn, listMaterials)
    newBP.openWindow()


def editBP():
    editeBP = EditeBP(conn, listBPs, listMaterials)
    editeBP.openWindow()


def runWindow():
    runProg = Run(conn, listBPs, settings)
    runProg.openWindow()


runPhoto = Image.open('run.png')
addMatPhoto = Image.open('addMaterial.png')
addBPhoto = Image.open('addBP.png')
editBPPhoto = Image.open('editBP.png')

runPhoto = runPhoto.resize((int(runPhoto.width * 0.3), int(runPhoto.height * 0.3)), Image.ANTIALIAS)
runPhoto = ImageTk.PhotoImage(runPhoto)

addMatPhoto = addMatPhoto.resize((int(addMatPhoto.width * 0.2), int(addMatPhoto.height * 0.2)), Image.ANTIALIAS)
addMatPhoto = ImageTk.PhotoImage(addMatPhoto)

addBPhoto = addBPhoto.resize((int(addBPhoto.width * 0.23), int(addBPhoto.height * 0.21)), Image.ANTIALIAS)
addBPhoto = ImageTk.PhotoImage(addBPhoto)

editBPPhoto = editBPPhoto.resize((int(editBPPhoto.width * 0.22), int(editBPPhoto.height * 0.2)), Image.ANTIALIAS)
editBPPhoto = ImageTk.PhotoImage(editBPPhoto)


# running
run_button = Button(image=runPhoto, borderwidth=3, command=runWindow)
run_button.place(x=350, y=150, anchor='center')

# new bp window
newBP_button = Button(image=addBPhoto, borderwidth=3, command=new_bp)
newBP_button.place(x=20, y=115)

# new material
newMatButton = Button(image=addMatPhoto, borderwidth=3, command=newMaterialFunction)
newMatButton.place(x=23, y=20)

# edit bp window
editBPButton = Button(image=editBPPhoto, borderwidth=3, command=editBP)
editBPButton.place(x=23, y=210)

main_window.mainloop()

conn.close()
