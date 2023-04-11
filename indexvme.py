from tkinter import ttk
from tkinter import *
import sqlite3

class product:
    db_name = "database.db"

    def __init__(self, window):
        self.wind = window
        self.wind.title('Products App')

        frame = LabelFrame (self.wind, text='Register a New Product')
        frame.grid(row=0, column=0, columnspan=3, pady=20)

        Label(frame, text)



if __name__ == '__main__':
    window = Tk()
    