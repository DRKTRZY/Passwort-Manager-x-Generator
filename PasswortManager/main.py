# Delete "password_db.db" for a new master password it also delete the entry's
# Master password is currently "hacked"
# Recovery Key is currently "a7fd28da94654a07ad31f3c1ed243a58" <- if you get a new key please change it here too
import sqlite3, hashlib
import tkinter as tk
from tkinter import simpledialog
from functools import partial
import uuid
import pyperclip
import base64
import os
from cryptography.hazmat.primitives import hashes
from cryptography.hazmat.primitives.kdf.pbkdf2 import PBKDF2HMAC
from cryptography.hazmat.backends import default_backend
from cryptography.fernet import Fernet

# Database
with sqlite3.connect("password_db.db") as db:
    cursor = db.cursor()

cursor.execute("""
CREATE TABLE IF NOT EXISTS masterpassword(
id INTEGER PRIMARY KEY,
password TEXT NOT NULL,
recovery_key TEXT NOT NULL);
""")

cursor.execute("""
CREATE TABLE IF NOT EXISTS vault(
id INTEGER PRIMARY KEY,
website TEXT NOT NULL,
username TEXT NOT NULL,
password TEXT NOT NULL);
""")


# Popup
def popup(text):
    answer = simpledialog.askstring("input string", text)
    return answer

# Window
window = tk.Tk()

window.title("Password Manager")
window.geometry("500x400")

# Functions etc
def hash_password(input):
    hash = hashlib.sha256(input)
    hash = hash.hexdigest()
    return hash

def first_screen():
    for widget in window.winfo_children():
        widget.destroy()

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
            sql = "DELETE FROM masterpassword WHERE id = 1"
            cursor.execute(sql)

            hashed_password = hash_password(entry.get().encode('utf-8'))
            key = str(uuid.uuid4().hex) # Create a random Recovery Key
            recovery_key = hash_password(key.encode('utf-8'))

            insert_password = """INSERT INTO masterpassword(password, recovery_key)
            VALUES(?, ?) """
            cursor.execute(insert_password, ((hashed_password),(recovery_key)))
            db.commit()
            error_lbl.config(text="")
            recovery_screen(key)
        else:
            error_lbl.config(text="Passwörter stimmen nicht mit einander ein")

    btn = tk.Button(window,width=10,text="Save",command=save_password) # Button for First Screen
    btn.pack(pady=10)

# Login Screen & Recovery Screen
def recovery_screen(key):
    for widget in window.winfo_children():
        widget.destroy()

    window.geometry("350x300")

    mstr_pswrd = tk.Label(window, pady=10, text="Speichere diesen Recovery Key")
    mstr_pswrd.config(anchor=tk.CENTER)
    mstr_pswrd.pack()

    key_lbl = tk.Label(window, pady=10, text=key)
    key_lbl.pack()

    def copy_key():
        pyperclip.copy(key_lbl.cget("text"))

    copy_btn = tk.Button(window, width=10, text="Copy", command=copy_key)  # Button for First Screen
    copy_btn.pack(pady=10)

    def done():
        password_vault()

    done_btn = tk.Button(window, width=10, text="Done", command=done)  # Button for First Screen
    done_btn.pack(pady=10)

def reset_screen():
    for widget in window.winfo_children():
        widget.destroy()

    window.geometry("350x300")

    mstr_pswrd = tk.Label(window, pady=10, text="Gib den Recovery Key ein")
    mstr_pswrd.config(anchor=tk.CENTER)
    mstr_pswrd.pack()

    recovery_entry = tk.Entry(window, width=20, show="*")
    recovery_entry.pack()
    recovery_entry.focus()

    key_lbl = tk.Label(window)
    key_lbl.pack()

    def get_recovery_key():
        recovery_key_check = hash_password(str(recovery_entry.get()).encode('utf-8'))
        cursor.execute('SELECT * FROM masterpassword WHERE id = 1 AND recovery_key = ?',[(recovery_key_check)])
        return cursor.fetchall()

    def check_recovery_key():
        checked = get_recovery_key()
        if checked:
            first_screen()
        else:
            recovery_entry.delete(0, 'end')
            key_lbl.config(text="Falscher Key")

    check_btn = tk.Button(window, width=10, text="Check Key", command=check_recovery_key)  # Button for First Screen
    check_btn.pack(pady=10)

def login_screen():
    for widget in window.winfo_children():
        widget.destroy()

    window.geometry("350x300")

    lbl = tk.Label(window,pady=10,text="Geben sie das Master password ein")
    lbl.config(anchor=tk.CENTER)
    lbl.pack()

    error_lbl = tk.Label(window)
    error_lbl.pack()

    entry = tk.Entry(window,width=20,show="*")
    entry.pack()
    entry.focus()

    def get_master_password():
        check_hashed_password = hash_password(entry.get().encode('utf-8'))
        cursor.execute("SELECT * FROM masterpassword WHERE id = 1 AND password = ?", [(check_hashed_password)])
        return cursor.fetchall()

    def check_password():
        match = get_master_password()

        if match:
            password_vault()
        else:
            entry.delete(0, 'end')
            error_lbl.config(text="Falsches Passwort")

    def reset_password():
        reset_screen()

    btn = tk.Button(window,width=10,text="Enter",command=check_password)
    btn.pack(pady=10)

    reset_btn = tk.Button(window,width=24,text="Masterpasswort zurücksetzen",command=reset_password)
    reset_btn.pack(pady=10)


def password_vault():
    for widget in window.winfo_children():
        widget.destroy()

# Entry Functions
    def add_entry():
        txt_website = "Website"
        txt_username = "Username"
        txt_password = "Password"

        website = popup(txt_website)
        username = popup(txt_username)
        password = popup(txt_password)

        insert_fields = """INSERT INTO vault(website,username,password)
        VALUES(?, ?, ?)"""

        cursor.execute(insert_fields,(website,username,password))
        db.commit()

        password_vault()

    def remove_entry(input):
        cursor.execute("DELETE FROM vault WHERE id = ?", (input,))
        db.commit()
        password_vault()

    window.geometry("850x450")

    correct_lbl = tk.Label(window,text="Passwort Manager",anchor=tk.CENTER)
    correct_lbl.grid(column=1)

    # Label for the Entry's
    create_entry_btn = tk.Button(window, text="+",command=add_entry)
    create_entry_btn.grid(column=1,pady=10)

    lbl_website = tk.Button(window, text="Website")
    lbl_website.grid(row=2,column=0,padx=80)
    lbl_username = tk.Button(window, text="Username")
    lbl_username.grid(row=2, column=1, padx=80)
    lbl_password= tk.Button(window, text="Password")
    lbl_password.grid(row=2, column=2, padx=80)

    cursor.execute("SELECT * FROM vault")
    if (cursor.fetchall() != None):
        i = 0
        while True:
            cursor.execute("SELECT * FROM vault")
            array = cursor.fetchall()
            array_lbl = tk.Label(window, text=(array[i][1]), font=("Bahnschrift, 12"))
            array_lbl.grid(column=0, row=i+3)
            array_lbl = tk.Label(window, text=(array[i][2]), font=("Bahnschrift, 12"))
            array_lbl.grid(column=1, row=i + 3)
            array_lbl = tk.Label(window, text=(array[i][3]), font=("Bahnschrift, 12"))
            array_lbl.grid(column=2, row=i + 3)

            delete_btn = tk.Button(window,text="Löschen",command= partial(remove_entry,array[i][0]))
            delete_btn.grid(column=3,row=i+3,pady=10)

            i = i+1
            cursor.execute("SELECT * FROM vault")
            if (len(cursor.fetchall()) <= i):
                break

check = cursor.execute("SELECT * FROM masterpassword") # if u have a master password it goes to the login screen
if cursor.fetchall():
    login_screen()
else:
    first_screen()

window.mainloop()