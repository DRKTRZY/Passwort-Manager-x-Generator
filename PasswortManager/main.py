import sqlite3, hashlib
import tkinter as tk

window = tk.Tk()

window.title("Password Manager")
window.geometry("500x400")

def loginscreen():
    window.geometry("350x200")

lbl = tk.Label(window,pady=10,text="Geben Sie das Master Passwort ein")
lbl.config(anchor=tk.CENTER)
lbl.pack()

error_lbl = tk.Label(window)
error_lbl.pack()

entry = tk.Entry(window,width=20,show="*")
entry.pack()
entry.focus()

def check_password():
    password = "hay"
    if password == entry.get():
        password_vault()
    else:
        entry.delete(0, 'end')
        error_lbl.config(text="Falsches Passwort")
btn = tk.Button(window,width=10,text="Enter",command=check_password)
btn.pack(pady=10)

def password_vault():
    for widget in window.winfo_children():
        widget.destroy()
    window.geometry("700x300")

    correct_lbl = tk.Label(window,text="Passwort ist korrekt",anchor=tk.CENTER)
    correct_lbl.pack()
loginscreen()
window.mainloop()