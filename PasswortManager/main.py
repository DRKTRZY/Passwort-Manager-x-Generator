import sqlite3, hashlib
import tkinter as tk

window = tk.Tk()

window.title("Password Manager")
window.geometry("500x400")

def first_screen():
    window.geometry("350x300")

    mstr_pswrd = tk.Label(window, pady=10, text="Erstelle ein Master Passwort")
    mstr_pswrd.config(anchor=tk.CENTER)
    mstr_pswrd.pack()

    re_enter_lbl = tk.Label(window, pady=10, text="Geben sie das Passwort erneut ein")
    re_enter_lbl.pack()

    error_lbl = tk.Label(window)
    error_lbl.pack()

    entry = tk.Entry(window, width=20, show="*")
    entry.pack()
    entry.focus()

    re_enter = tk.Entry(window,width=20)
    re_enter.pack()
    re_enter.focus()

    def save_password():
        if entry.get() == re_enter.get():
            error_lbl.config(text="")
            pass
        else:
            error_lbl.config(text="Passwörter stimmen nicht mit einander ein")

    btn = tk.Button(window,width=10,text="Save",command=save_password)
    btn.pack(pady=10)

def login_screen():
    window.geometry("350x300")

    lbl = tk.Label(window,pady=10,text="Geben sie das Master password ein")
    lbl.config(anchor=tk.CENTER)
    lbl.pack()

    error_lbl = tk.Label(window)
    error_lbl.pack()

    entry = tk.Entry(window,width=20,show="*")
    entry.pack()
    entry.focus()

    def check_password():
        password = "hey"
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
first_screen()
window.mainloop()