import tkinter as tk
import random
import string
# Main Gui
window = tk.Tk()
window.geometry("800x450")
window.title("Passwort Generator")
window.resizable(0,0)
window.configure(bg="#424242")


#Generator

digit = string.digits
lower = string.ascii_lowercase
upper = string.ascii_uppercase
symbol = string.punctuation
# All of the above together
all = digit + lower + upper + symbol

length = int(input("Geben Sie die Länge des generierten Passwords ein: "))

if length > 60:
    print("60 ist die maximale Angabe")
    length = 60

generator = random.sample(all,length)
password = "".join(generator)

print(password)


window.mainloop()