import sqlite3, hashlib
from tkinter import *

window = Tk()

window.title("Password Manager")
window.geometry("500x400")

def loginscreen():
    window.geometry("350x200")

lbl = Label(window,pady=10,text="Geben Sie das Master Passwort ein")
lbl.config(anchor=CENTER)
lbl.pack()

entry = Entry(window,width=20)
entry.pack()

btn = Button(window,width=10,text="Enter")
btn.pack(pady=10)

loginscreen()
window.mainloop()

