# Delete "password_db.db" for a new master password
# Master password is actually "hacked"
import sqlite3, hashlib
import tkinter as tk

# Database
with sqlite3.connect("password_db.db") as db:
    cursor = db.cursor()

cursor.execute("""
CREATE TABLE IF NOT EXISTS masterpassword(
id INTEGER PRIMARY KEY,
password TEXT NOT NULL);
""")

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
    window.geometry("700x300")

    correct_lbl = tk.Label(window,text="Passwort Manager",anchor=tk.CENTER)
    correct_lbl.pack()

check = cursor.execute("SELECT * FROM masterpassword") # if u have a master password it goes to the login screen
if cursor.fetchall():
    login_screen()
else:
    first_screen()

window.mainloop()