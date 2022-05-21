# Delete "password_db.db" for a new master password it also delete the entry's
# Master password is currently "hacked"
import sqlite3, hashlib
import tkinter as tk
from tkinter import simpledialog
from functools import partial

# Database
with sqlite3.connect("password_db.db") as db:
    cursor = db.cursor()

cursor.execute("""
CREATE TABLE IF NOT EXISTS masterpassword(
id INTEGER PRIMARY KEY,
password TEXT NOT NULL);
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
    hash = hashlib.md5(input)
    hash = hash.hexdigest()
    return hash

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
            hashed_password = hash_password(entry.get().encode('utf-8'))
            error_lbl.config(text="")
            insert_password = """INSERT INTO masterpassword(password)
            VALUES(?) """
            cursor.execute(insert_password, [(hashed_password)])
            db.commit()
            password_vault()
        else:
            error_lbl.config(text="Passwörter stimmen nicht mit einander ein")

    btn = tk.Button(window,width=10,text="Save",command=save_password) # Button for First Screen
    btn.pack(pady=10)

# Login Screen
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

    btn = tk.Button(window,width=10,text="Enter",command=check_password)
    btn.pack(pady=10)

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