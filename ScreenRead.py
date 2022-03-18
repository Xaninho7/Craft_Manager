from tkinter import *
from PIL import Image, ImageTk, ImageGrab
import pytesseract


class ScreenRead:
    def __init__(self, defaultWindow='', isDigit=False):
        self.readButton = None
        self.grab = None
        self.width = 0
        self.height = 0
        self.y = 0
        self.x = 0
        self.newWindow = None
        self.button2 = None
        self.button = None
        self.custom_config = None
        self.posWin = False
        # self.defaultWindow = '250x100+1372+375'
        self.defaultWindow = defaultWindow
        self.xCorrct = 8
        self.yCorrct = 31
        self.setted = False
        self.isDigit = isDigit

    def readWindow(self):
        if not self.posWin:
            self.newWindow = Toplevel()
            self.newWindow.geometry(self.defaultWindow)
            self.newWindow.attributes('-alpha', 0.5)
            self.newWindow.config(background='red')
            self.newWindow.attributes('-toolwindow', True)
            self.newWindow.attributes('-topmost', True)
        else:
            self.getPos()
            self.defaultWindow = f'{self.width}x{self.height}+{self.x-self.xCorrct}+{self.y-self.yCorrct}'
            self.newWindow.destroy()
            self.setted = True

        self.posWin = not self.posWin

    def getPos(self):
        self.x = self.newWindow.winfo_rootx()
        self.y = self.newWindow.winfo_rooty()
        self.height = self.newWindow.winfo_height()
        self.width = self.newWindow.winfo_width()

    def read(self):
        if not self.setted:
            return ''

        pytesseract.pytesseract.tesseract_cmd = r'C:\Program Files\Tesseract5\tesseract.exe'
        grab = ImageGrab.grab(bbox=(self.x, self.y, self.x + self.width, self.y + self.height))
        # grab.show()
        # print(grab)
        readConfig = r'--tessdata-dir "C:\Program Files\Tesseract5\tessdata" --oem 3 --psm 6'
        if self.isDigit:
            readConfig += ' -c tessedit_char_whitelist=0123456789'
        # print(readConfig)
        return pytesseract.image_to_string(grab, lang='eng', config=readConfig)
