import tkinter as tk
import random
from tkinter import ttk
from tkinter import messagebox
import alt_strings as strings
import pyperclip

# Main Gui
window = tk.Tk()
window.geometry("800x450")
window.title("Passwort Generator")
window.resizable(0,0)
window.configure(bg="#424242")

empty_entry = tk.StringVar()
length = tk.IntVar()
symbol_characters = tk.IntVar()
digit_characters = tk.IntVar()
upper_characters = tk.IntVar()
lower_characters = tk.IntVar()
digit = strings.digit
lower = strings.lower
upper = strings.upper
symbol = strings.symbols
all = digit + lower + upper + symbol

# Functions
def randomPassword():
    signs = all
    if symbol_characters.get() and digit_characters.get() and lower_characters.get() == 1:
        signs = digit + symbol + lower
    elif symbol_characters.get() and digit_characters.get() and upper_characters.get() == 1:
        signs = digit + symbol + upper
    elif symbol_characters.get() and upper_characters.get() and lower_characters.get() == 1:
        signs = symbol + upper + lower
    elif lower_characters.get() and digit_characters.get() and upper_characters.get() == 1:
        signs = digit + lower + upper
    elif symbol_characters.get() and upper_characters.get() == 1 and lower_characters.get() == 0:
        signs = symbol + upper
    elif symbol_characters.get() and digit_characters.get() == 1 and lower_characters.get() == 0:
        signs = symbol + digit
    elif symbol_characters.get() and lower_characters.get() == 1 and upper_characters.get() == 0:
        signs = symbol + lower
    elif lower_characters.get() and upper_characters.get() == 1 and symbol_characters.get() == 0:
        signs = lower + upper
    elif lower_characters.get() and digit_characters.get() == 1 and upper_characters.get() == 0:
        signs = lower + digit
    elif lower_characters.get() and symbol_characters.get() == 1 and upper_characters.get() == 0:
        signs = lower + symbol
    elif upper_characters.get() and digit_characters.get() == 1 and symbol_characters.get() == 0:
        signs = digit + upper
    elif lower_characters.get() == 1 and symbol_characters.get() == 0:
        signs = lower
    elif digit_characters.get() == 1 and upper_characters.get() == 0:
        signs = digit
    elif symbol_characters.get() == 1 and upper_characters.get() == 0:
        signs = symbol
    elif upper_characters.get() == 1 and symbol_characters.get() == 0:
        signs = upper
    elif symbol_characters.get() and digit_characters.get() and upper_characters.get() and lower_characters == 1:
        signs = all
    else:
        messagebox.showerror("Error", "Sie müssen mindestens eine Option auswählen")
    generator = random.sample(signs,length.get())
    password = "".join(generator)
    empty_entry.set(password)

def copy_entry():
    copy_title = empty_entry.get()
    pyperclip.copy(copy_title)

# Buttons etc
password_entry = tk.Entry(window,textvariable=empty_entry,width=30)
password_entry.place(relx=.5,rely=.5,anchor=tk.CENTER)

generate_button = tk.Button(window,text="Generate",command=randomPassword)
generate_button.place(x=210,y=100,width=300,height=30)
slider = tk.Scale(window, from_=12, to=60,variable=length)
slider.place(x=600,y=100)
symbol_box = ttk.Checkbutton(window,text="Sonderzeichen",variable=symbol_characters,onvalue=1,offvalue=0).pack()
digit_box = ttk.Checkbutton(window,text="Ziffern",variable=digit_characters,onvalue=1,offvalue=0).pack()
upper_box = ttk.Checkbutton(window,text="Grossbuchstaben",variable=upper_characters,onvalue=1,offvalue=0).pack()
lower_box = ttk.Checkbutton(window,text="Kleinbuchstaben",variable=lower_characters,onvalue=1,offvalue=0).pack()
copy_button = tk.Button(window,text="Kopieren",command=copy_entry)
copy_button.place(x=300,y=200)

lbl = tk.Label(window, text ="Tipp:  Je mehr Sie auswählen, desto sicherer ist das Passwort",bg="#424242")
lbl.pack()

window.mainloop()