from tkinter import ttk
from tkinter import *

class Cliente:
    def __init__(self, root):
        self.wind = root
        self.wind.title('Cliente')
        self.wind.geometry('850x600')
        self.wind.config(bg='teal')






if __name__ == '__main__':
    root = Tk()
    Cliente = Cliente(root)
    root.mainloop
